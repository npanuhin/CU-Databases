import datetime
import struct
import os

from constants import TYPE_FORMATS, SCHEMA_TYPE, RECORD_TYPE


def mkpath(*paths: str) -> str:
    return os.path.normpath(os.path.join(*paths))


def get_struct_format(schema: SCHEMA_TYPE) -> str:
    fmt = '='
    for column in schema:
        if column['type'] == 'string':
            fmt += str(column['length'])
        fmt += TYPE_FORMATS[column['type']][0]
    return fmt


def get_record_size(schema: SCHEMA_TYPE) -> int:
    size = 0
    for column in schema:
        if column['type'] == 'string':
            size += column['length']
        else:
            size += TYPE_FORMATS[column['type']][1]
    return size


def serialize(schema: SCHEMA_TYPE, values: RECORD_TYPE) -> bytes:
    fmt = get_struct_format(schema)
    encoded = []
    for column, value in zip(schema, values):
        # print(f'Serializing: {column["name"]} = "{value}" (type: {column["type"]})')
        if column['type'] == 'string':
            encoded.append(value.encode('utf-8').ljust(column['length'], b'\x00'))
        elif column['type'] == 'char':
            encoded.append(value.encode('utf-8'))
        elif column['type'] == 'datetime':
            if isinstance(value, datetime.date):
                value = datetime.datetime.combine(value, datetime.time.min)
            encoded.append(int(value.timestamp()))
        else:
            encoded.append(value)
    # print(f'Packing {fmt}')
    return struct.pack(fmt, *encoded)


def deserialize(schema: SCHEMA_TYPE, raw_bytes: bytes) -> RECORD_TYPE:
    fmt = get_struct_format(schema)
    # print(f'Unpacking {fmt}')
    unpacked = struct.unpack(fmt, raw_bytes)
    result = []
    for column, value in zip(schema, unpacked):
        if column['type'] == 'string':
            result.append(value.decode('utf-8').rstrip('\x00'))
        elif column['type'] == 'char':
            result.append(value.decode('utf-8'))
        elif column['type'] == 'datetime':
            result.append(datetime.datetime.fromtimestamp(value))
        else:
            result.append(value)
    return result
