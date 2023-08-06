#!/usr/bin/env python3

import argparse
import asyncio
from datetime import datetime
import copy
import json
import logging
import os
import sys
import uuid
from multiprocessing.pool import ThreadPool as Pool

import pkg_resources
from c8connector import C8Connector, Sample, ConfigAttributeType, Schema
from c8connector import ConfigProperty, ensure_datetime
from datetime import datetime, timezone
from tempfile import mkstemp
from fastavro import writer, parse_schema
from jsonschema import Draft7Validator, FormatChecker
from pathlib import Path
from prometheus_client import CollectorRegistry, Counter, Gauge, start_http_server
from singer import get_logger
from threading import Lock
from typing import AsyncIterable, Dict

from macrometa_target_bigquery import stream_utils
from macrometa_target_bigquery.db_sync import DbSync
from macrometa_target_bigquery.exceptions import (
    RecordValidationException,
    InvalidValidationOperationException
)

LOGGER = get_logger('macrometa_target_bigquery')
logging.getLogger('bigquery.connector').setLevel(logging.WARNING)

DEFAULT_BATCH_SIZE_ROWS = 10000
DEFAULT_PARALLELISM = 0  # 0 The number of threads used to flush tables
DEFAULT_MAX_PARALLELISM = 16  # Don't use more than this number of threads by default when flushing streams in parallel
DEFAULT_HARD_DELETE = False
DEFAULT_BATCH_AWAIT_TIME = 60

# Create a custom CollectorRegistry
registry_package = CollectorRegistry()
export_lag = Gauge("export_lag", "The average time from when the data changes in GDN collections are reflected in external data sources",
                   ['region', 'tenant', 'fabric', 'workflow'], registry=registry_package)
export_errors = Counter("export_errors", "Total count of errors while exporting data from GDN collections",
                        ['region', 'tenant', 'fabric', 'workflow'], registry=registry_package)

region_label = os.getenv("GDN_FEDERATION", "NA")
tenant_label = os.getenv("GDN_TENANT", "NA")
fabric_label = os.getenv("GDN_FABRIC", "NA")
workflow_label = os.getenv("WORKFLOW_UUID", "NA")


class BigQueryTargetConnector(C8Connector):
    """BigQueryTargetConnector's C8Connector impl."""

    def name(self) -> str:
        """Returns the name of the connector."""
        return "BigQuery"

    def package_name(self) -> str:
        """Returns the package name of the connector (i.e. PyPi package name)."""
        return "macrometa-target-bigquery"

    def version(self) -> str:
        """Returns the version of the connector."""
        return pkg_resources.get_distribution('macrometa_target_bigquery').version

    def type(self) -> str:
        """Returns the type of the connector."""
        return "target"

    def description(self) -> str:
        """Returns the description of the connector."""
        return "Send data into Google's BigQuery table."

    def logo(self) -> str:
        """Returns the logo image for the connector."""
        return ""

    def validate(self, integration: dict) -> None:
        """Validate given configurations against the connector.
        If invalid, throw an exception with the cause.
        """
        pass

    def samples(self, integration: dict) -> list[Sample]:
        """Fetch sample data using the given configurations."""
        return []

    def schemas(self, integration: dict) -> list[Schema]:
        """Get supported schemas using the given configurations."""
        return []

    def reserved_keys(self) -> list[str]:
        """List of reserved keys for the connector."""
        return []

    def config(self) -> list[ConfigProperty]:
        """Get configuration parameters for the connector."""
        return [
            ConfigProperty('project_id', 'Project ID', ConfigAttributeType.STRING, True, False,
                           description='BigQuery project ID.',
                           placeholder_value='my_project_id'),
            ConfigProperty('credentials_file', 'Credentials JSON File', ConfigAttributeType.FILE, True, False,
                           description='Content of the credentials.json file for your service account. See the '
                                       '"Activate the Google BigQuery API" section of the repository\'s README and '
                                       'https://cloud.google.com/docs/authentication/production.',
                           placeholder_value='credentials.json contents'),
            ConfigProperty('target_schema', 'Target Schema/Dataset', ConfigAttributeType.STRING, True, True,
                           description='Name of the schema/dataset where the tables will be created. '
                                       'The schema will be created if it does not exist (Case-sensitive).',
                           placeholder_value='my_schema'),
            ConfigProperty('target_table', 'Target Table', ConfigAttributeType.STRING, True, True,
                           description='Name of the bigquery table. The table will be created if it does not exist (Case-sensitive).',
                           placeholder_value='my_table'),
            ConfigProperty('location', 'Location', ConfigAttributeType.STRING, False, True,
                           description='If the dataset does not exist, the region where BigQuery creates it will be determined by'
                                       ' the provided location (default: US). However, if the dataset already exists, the location of the dataset'
                                       ' will be used eventually.',
                           placeholder_value='US'),
            ConfigProperty('batch_size_rows', 'Batch Size', ConfigAttributeType.INT, False, False,
                           description='Maximum number of rows in each batch. At the end of each batch, '
                                       'the rows in the batch are loaded into BigQuery.',
                           default_value='10000'),
            ConfigProperty('batch_wait_limit_seconds', 'Batch Wait Limit (Seconds)',
                           ConfigAttributeType.INT, False, False,
                           description='Maximum time to wait for batch to reach batch size rows.',
                           placeholder_value='60'),
            ConfigProperty('add_metadata_columns', 'Add Metadata Columns', ConfigAttributeType.BOOLEAN, False, False,
                           description='Metadata columns add extra row level information about data ingestions, '
                                       '(i.e. when was the row read in source, when was inserted or deleted in bigquery, '
                                       'etc.) Metadata columns are created automatically by adding extra columns to '
                                       'the tables with a column prefix _sdc_.',
                           default_value='false'),
            ConfigProperty('hard_delete', 'Hard Delete', ConfigAttributeType.BOOLEAN, False, False,
                           description='When hard_delete option is true then DELETE SQL commands will be performed in'
                                       ' BigQuery to delete rows in tables. It\'s achieved by continuously checking the'
                                       ' _sdc_deleted_at metadata column sent by the data source. As deleting rows '
                                       'requires metadata columns, hard_delete option automatically enables the '
                                       'add metadata columns option as well.',
                           default_value='false'),
        ]

    def capabilities(self) -> list[str]:
        """Return the capabilities[1] of the connector.
        [1] https://docs.meltano.com/contribute/plugins#how-to-test-a-tap
        """
        return []


def add_metadata_columns_to_schema(schema_message):
    """Metadata _sdc columns according to the stitch documentation at
    https://www.stitchdata.com/docs/data-structure/integration-schemas#sdc-columns

    Metadata columns gives information about data injections
    """
    extended_schema_message = schema_message
    extended_schema_message['schema']['properties']['_sdc_extracted_at'] = {'type': ['null', 'string'],
                                                                            'format': 'date-time'}
    extended_schema_message['schema']['properties']['_sdc_batched_at'] = {'type': ['null', 'string'],
                                                                          'format': 'date-time'}
    extended_schema_message['schema']['properties']['_sdc_deleted_at'] = {'type': ['null', 'string'],
                                                                          'format': 'date-time'}

    return extended_schema_message


def emit_state(state):
    if state is not None:
        line = json.dumps(state)
        LOGGER.info('Emitting state {}'.format(line))
        sys.stdout.write("{}\n".format(line))
        sys.stdout.flush()


async def read_stdin() -> AsyncIterable[str]:
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    reader_protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: reader_protocol, sys.stdin)
    while True:
        line = await reader.readline()
        if not line:
            break
        yield line.decode('utf-8').rstrip('\r\n')


# pylint: disable=too-many-locals,too-many-branches,too-many-statements
async def persist_lines(state, flushed_state, schemas, key_properties, validators, records_to_load, row_count,
                        stream_to_sync, total_row_count, batch_size_rows, default_hard_delete, hard_delete_mapping,
                        time_schedule, config, flush_lock, time_extracted_list) -> None:

    # Loop over lines from stdin
    lines = read_stdin()
    async for line in lines:
        try:
            o = json.loads(line)
        except json.decoder.JSONDecodeError:
            LOGGER.error("Unable to parse:\n{}".format(line))
            raise

        if 'type' not in o:
            raise Exception("Line is missing required key 'type': {}".format(line))

        t = o['type']

        if t == 'RECORD':
            if 'stream' not in o:
                raise Exception("Line is missing required key 'stream': {}".format(line))
            if o['stream'] not in schemas:
                raise Exception(
                    "A record for stream {} was encountered before a corresponding schema".format(o['stream']))

            # Get schema for this record's stream
            stream = o['stream']

            stream_utils.adjust_timestamps_in_record(o['record'], schemas[stream])

            # Validate record
            if config.get('validate_records'):
                try:
                    validators[stream].validate(stream_utils.float_to_decimal(o['record']))
                except Exception as ex:
                    if type(ex).__name__ == "InvalidOperation":
                        raise InvalidValidationOperationException(
                            f"Data validation failed and cannot load to destination. RECORD: {o['record']}\n"
                            "multipleOf validations that allows long precisions are not supported (i.e. with 15 digits"
                            "or more) Try removing 'multipleOf' methods from JSON schema.")
                    raise RecordValidationException(f"Record does not pass schema validation. RECORD: {o['record']}")

            with flush_lock:
                primary_key_string = stream_to_sync[stream].record_primary_key_string(o['record'])
                if not primary_key_string:
                    primary_key_string = 'RID-{}'.format(total_row_count[stream])

                # increment row count only when a new PK is encountered in the current batch
                if primary_key_string not in records_to_load[stream]:
                    row_count[stream] += 1
                    total_row_count[stream] += 1

                # append record
                if config.get('add_metadata_columns') or hard_delete_mapping.get(stream, default_hard_delete):
                    records_to_load[stream][primary_key_string] = stream_utils.add_metadata_values_to_record(o)
                else:
                    records_to_load[stream][primary_key_string] = o['record']

                if 'time_extracted' in o:
                    time_extracted_list.append(ensure_datetime(o["time_extracted"]))
                else:
                    time_extracted_list.append(datetime.now(timezone.utc))

                if row_count[stream] >= batch_size_rows and row_count[stream] > 0:
                    LOGGER.info("Flush triggered by batch_size_rows (%s) reached in %s",
                                 batch_size_rows, stream)

                    # flush all streams, delete records if needed, reset counts and then emit current state
                    if config.get('flush_all_streams'):
                        filter_streams = None
                    else:
                        filter_streams = [stream]

                    # Flush and return a new state dict with new positions only for the flushed streams
                    flushed_state = flush_streams(
                        records_to_load,
                        row_count,
                        stream_to_sync,
                        config,
                        state,
                        flushed_state,
                        time_extracted_list,
                        filter_streams=filter_streams)

                    # emit last encountered state
                    emit_state(copy.deepcopy(flushed_state))
                    time_schedule['last_executed_time'] = datetime.now()

        elif t == 'SCHEMA':
            if 'stream' not in o:
                raise Exception("Line is missing required key 'stream': {}".format(line))

            stream = o['stream']

            schemas[stream] = stream_utils.float_to_decimal(o['schema'])
            validators[stream] = Draft7Validator(schemas[stream], format_checker=FormatChecker())

            with flush_lock:
                # flush records from previous stream SCHEMA
                # if same stream has been encountered again, it means the schema might have been altered
                # so previous records need to be flushed
                if row_count.get(stream, 0) > 0:
                    if config.get('flush_all_streams'):
                        filter_streams = None
                    else:
                        filter_streams = [stream]

                    flushed_state = flush_streams(
                        records_to_load, row_count, stream_to_sync, config, state, flushed_state, time_extracted_list, filter_streams=filter_streams
                    )

                    # emit latest encountered state
                    emit_state(flushed_state)

                # key_properties key must be available in the SCHEMA message.
                if 'key_properties' not in o:
                    raise Exception("key_properties field is required")

                # Log based and Incremental replications on tables with no Primary Key
                # cause duplicates when merging UPDATE events.
                # Stop loading data by default if no Primary Key.
                #
                # If you want to load tables with no Primary Key:
                #  1) Set ` 'primary_key_required': false ` in the target-bigquery config.json
                #  or
                #  2) Use fastsync [postgres-to-bigquery, mysql-to-bigquery, etc.]
                if config.get('primary_key_required', True) and len(o['key_properties']) == 0:
                    LOGGER.critical("Primary key is set to mandatory but not defined in the [{}] stream".format(stream))
                    raise Exception("key_properties field is required")

                key_properties[stream] = o['key_properties']

                if config.get('add_metadata_columns') or hard_delete_mapping.get(stream, default_hard_delete):
                    stream_to_sync[stream] = DbSync(config, add_metadata_columns_to_schema(o))
                else:
                    stream_to_sync[stream] = DbSync(config, o)

                try:
                    stream_to_sync[stream].create_schema_if_not_exists()
                    stream_to_sync[stream].sync_table()
                except Exception as e:
                    LOGGER.error("""
                        Cannot sync table structure in BigQuery schema: {} .
                    """.format(
                        stream_to_sync[stream].schema_name))
                    raise e

                records_to_load[stream] = {}
                row_count[stream] = 0
                total_row_count[stream] = 0

        elif t == 'ACTIVATE_VERSION':
            with flush_lock:
                stream = o['stream']
                LOGGER.debug('ACTIVATE_VERSION message - ignoring')

        elif t == 'STATE':
            with flush_lock:
                LOGGER.debug('Setting state to {}'.format(o['value']))
                state = o['value']

                # Initially set flushed state
                if not flushed_state:
                    flushed_state = copy.deepcopy(state)

        else:
            raise Exception("Unknown message type {} in message {}"
                            .format(o['type'], o))

    # if some bucket has records that need to be flushed but haven't reached batch size
    # then flush all buckets.
    if sum(row_count.values()) > 0:
        with flush_lock:
            # flush all streams one last time, delete records if needed, reset counts and then emit current state
            flushed_state = flush_streams(records_to_load, row_count, stream_to_sync, config, state, flushed_state, time_extracted_list)
            time_schedule['last_executed_time'] = datetime.now()

    with flush_lock:
        # emit latest state
        emit_state(copy.deepcopy(flushed_state))


# pylint: disable=too-many-arguments
def flush_streams(
        streams,
        row_count,
        stream_to_sync,
        config,
        state,
        flushed_state,
        time_extracted_list,
        filter_streams=None):
    """
    Flushes all buckets and resets records count to 0 as well as empties records to load list
    :param streams: dictionary with records to load per stream
    :param row_count: dictionary with row count per stream
    :param stream_to_sync: BigQuery db sync instance per stream
    :param config: dictionary containing the configuration
    :param state: dictionary containing the original state from tap
    :param flushed_state: dictionary containing updated states only when streams got flushed
    :param filter_streams: Keys of streams to flush from the streams' dict. Default is every stream
    :return: State dict with flushed positions
    :return: Dictionary with flush timestamps for each stream flushed
    """
    parallelism = config.get("parallelism", DEFAULT_PARALLELISM)
    max_parallelism = config.get("max_parallelism", DEFAULT_MAX_PARALLELISM)
    default_hard_delete = config.get("hard_delete", DEFAULT_HARD_DELETE)
    hard_delete_mapping = config.get("hard_delete_mapping", {})

    # Parallelism 0 means auto parallelism:
    #
    # Auto parallelism trying to flush streams efficiently with auto defined number
    # of threads where the number of threads is the number of streams that need to
    # be loaded, but it's not greater than the value of max_parallelism
    if parallelism == 0:
        n_streams_to_flush = len(streams.keys())
        if n_streams_to_flush > max_parallelism:
            parallelism = max_parallelism
        else:
            parallelism = n_streams_to_flush

    # Select the required streams to flush
    if filter_streams:
        streams_to_flush = filter_streams
    else:
        streams_to_flush = list(streams.keys())

    if len(streams_to_flush) > 1:
        # Single-host, process-based parallelism to avoid the dreaded GIL.
        with Pool(parallelism) as pool:
            jobs = []
            for stream in streams_to_flush:
                jobs.append(
                    pool.apply_async(
                        load_stream_batch,
                        kwds={
                            'stream': stream,
                            'records_to_load': streams[stream],
                            'row_count': row_count,
                            'db_sync': stream_to_sync[stream],
                            'time_extracted_list': time_extracted_list,
                            'delete_rows': hard_delete_mapping.get(
                                stream, default_hard_delete
                            ),
                        },
                    )
                )
            for future in jobs:
                future.get()
    else:
        # If we only have one stream to sync let's not introduce overhead.
        # for stream in streams_to_flush:
        load_stream_batch(
            stream=streams_to_flush[0],
            records_to_load=streams[streams_to_flush[0]],
            row_count=row_count,
            db_sync=stream_to_sync[streams_to_flush[0]],
            time_extracted_list=time_extracted_list,
            delete_rows=hard_delete_mapping.get(streams_to_flush[0], default_hard_delete)
        )

    # reset flushed stream records to empty to avoid flushing same records
    # reset row count for flushed streams
    for stream in streams_to_flush:
        streams[stream] = {}
        row_count[stream] = 0
        time_extracted_list = []

        # Update flushed streams
        if filter_streams:
            # update flushed_state position if we have state information for the stream
            if state is not None and stream in state.get('bookmarks', {}):
                # Create bookmark key if not exists
                if 'bookmarks' not in flushed_state:
                    flushed_state['bookmarks'] = {}
                # Copy the stream bookmark from the latest state
                flushed_state['bookmarks'][stream] = copy.deepcopy(state['bookmarks'][stream])

        # If we flush every bucket use the latest state
        else:
            flushed_state = copy.deepcopy(state)

    # Return with state message with flushed positions
    return flushed_state


def load_stream_batch(stream, records_to_load, row_count, db_sync, time_extracted_list, delete_rows=False):
    # Load into bigquery
    if row_count[stream] > 0:
        flush_records(stream, records_to_load, row_count[stream], db_sync, time_extracted_list)

        # Delete soft-deleted, flagged rows - where _sdc_deleted at is not null
        if delete_rows:
            db_sync.delete_rows(stream)


def flush_records(stream, records_to_load, row_count, db_sync, time_extracted_list):
    parsed_schema = parse_schema(db_sync.avro_schema())
    csv_fd, csv_file = mkstemp()
    with open(csv_file, 'wb') as out:
        writer(out, parsed_schema, db_sync.records_to_avro(records_to_load.values()))

    # Seek to the beginning of the file and load
    with open(csv_file, 'r+b') as f:
        db_sync.load_avro(f, row_count)

    event_time = datetime.now(timezone.utc)
    for time_extracted in time_extracted_list:
        diff = event_time - time_extracted
        export_lag.labels(region_label, tenant_label, fabric_label, workflow_label).set(diff.total_seconds())

    # Delete temp file
    os.remove(csv_file)


async def setup_flush_task(config, filter_streams=None):
    state = None
    flushed_state = None
    schemas = {}
    key_properties = {}
    validators = {}
    records_to_load = {}
    row_count = {}
    stream_to_sync = {}
    total_row_count = {}
    time_extracted_list = []
    batch_size_rows = config.get('batch_size_rows', DEFAULT_BATCH_SIZE_ROWS)
    default_hard_delete = config.get('hard_delete', DEFAULT_HARD_DELETE)
    hard_delete_mapping = config.get('hard_delete_mapping', {})
    time_schedule = {
        'batch_wait_limit_seconds': config.get('batch_wait_limit_seconds', DEFAULT_BATCH_AWAIT_TIME),
        'last_executed_time': datetime.now(),
    }
    flush_lock = Lock()
    event_loop = asyncio.get_event_loop()
    persist_lines_coro = persist_lines(state, flushed_state, schemas, key_properties, validators, records_to_load, row_count,
                        stream_to_sync, total_row_count, batch_size_rows, default_hard_delete, hard_delete_mapping,
                        time_schedule, config, flush_lock, time_extracted_list)
    asyncio.run_coroutine_threadsafe(persist_lines_coro, event_loop)
    flush_task_coro = flush_task(time_schedule, records_to_load, row_count, stream_to_sync, config, state, flushed_state,
                                 flush_lock, time_extracted_list, filter_streams)
    asyncio.run_coroutine_threadsafe(flush_task_coro, event_loop)

    # Wait for all Futures to complete and propagate any exceptions raised
    await asyncio.gather(
        persist_lines_coro,
        flush_task_coro,
    )


async def flush_task(time_schedule, streams, row_count, stream_to_sync, config, state, flushed_state,
                     flush_lock, time_extracted_list, filter_streams=None) -> None:
    while True:
        timedelta = datetime.now() - time_schedule['last_executed_time']
        if (
            timedelta.total_seconds() >= time_schedule['batch_wait_limit_seconds']
            and sum(row_count.values()) > 0
        ):
            with flush_lock:
                # flush all streams one last time, delete records if needed, reset counts and then emit current state.
                flushed_state = flush_streams(streams, row_count, stream_to_sync, config, state, flushed_state,
                                              time_extracted_list, filter_streams)
                # emit latest state
                emit_state(copy.deepcopy(flushed_state))
                time_schedule['last_executed_time'] = datetime.now()
        # Add sleep statement to ensure periodic execution
        await asyncio.sleep(time_schedule['batch_wait_limit_seconds'])


def create_credentials_file(config: Dict) -> Dict:
    path_uuid = uuid.uuid4().hex
    try:
        if config.get('credentials_file'):
            path = f"/opt/bigquery/{path_uuid}/client_secrets.json"
            client_secrets = Path(path)
            client_secrets.parent.mkdir(exist_ok=True, parents=True)
            client_secrets.write_text(config['credentials_file'])
            config['credentials_file'] = client_secrets
            LOGGER.info(f"Client credentials file created at: {path}")
    except Exception as e:
        LOGGER.warn(f"Failed to client credentials file: /opt/bigquery/{path_uuid}/. {e}")
    return config


def delete_credentials_file(config: Dict) -> None:
    try:
        if config.get('credentials_file'):
            path = config['credentials_file']
            client_secrets = Path(path)
            config['credentials_file'] = client_secrets.read_text()
            client_secrets.unlink()
            LOGGER.info(f"Client credentials file deleted from: {path}")
            client_secrets.parent.rmdir()
    except Exception as e:
        LOGGER.warn(f"Failed to delete client credentials file: {e}")


def validate_config(config):
    def validate_integer(value, error_message, key=None):
        try:
            if int(value) < 0 or (key == 'batch_size_rows' and int(value) == 0):
                raise ValueError
        except Exception:
            raise Exception(error_message)

    batch_size_rows = config.get('batch_size_rows', DEFAULT_BATCH_SIZE_ROWS)
    validate_integer(batch_size_rows, 'The batch size provided is not valid. '
                                       'Only integer values greater than 0 '
                                       'are supported as batch size.',
                                       key='batch_size_rows')

    batch_wait_limit = config.get('batch_wait_limit_seconds', DEFAULT_BATCH_AWAIT_TIME)
    validate_integer(batch_wait_limit, 'The batch wait limit provided is not valid. '
                                        'Only integer values greater than or equal to 0 '
                                        'are supported as batch wait limit.')

    data_flattening_max_level = config.get('data_flattening_max_level', 0)
    validate_integer(data_flattening_max_level, 'The data flattening max level provided is not valid. '
                                                 'Only integer values greater than or equal to 0 '
                                                 'are supported as data flattening max level.')


async def main_impl():
    # Start the Prometheus HTTP server for exposing metrics
    LOGGER.info("Bigquery target is starting the metrics server.")
    start_http_server(8001, registry=registry_package)
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    args = parser.parse_args()

    if args.config:
        with open(args.config) as config_input:
            config = json.load(config_input)
    else:
        config = {}

    try:
        # Field validations
        validate_config(config)
        config = create_credentials_file(config)
        # Consume singer messages
        await setup_flush_task(config)

        LOGGER.debug("Exiting normally")
    except Exception as e:
        LOGGER.info("Exception raised: %s", e)
        # Increment export_errors metric
        export_errors.labels(region_label, tenant_label, fabric_label, workflow_label).inc()
        delete_credentials_file(config)
        raise e
    delete_credentials_file(config)


def main():
    """Main entry point"""
    try:
        asyncio.run(main_impl())
    except Exception as exc:
        LOGGER.critical(exc)
        raise exc


if __name__ == '__main__':
    main()
