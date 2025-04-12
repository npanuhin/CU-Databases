from typing import Any, Iterable

from dataclasses import dataclass, field
import os

from utils import mkpath, get_record_size, serialize, deserialize
from constants import PAGE_SIZE, SCHEMA_TYPE, RECORD_TYPE


@dataclass
class Table:
    name: str
    schema: SCHEMA_TYPE
    db_path: str
    pages_total: int = 0

    column_indices: dict[str, int] = field(init=False)
    record_size: int = field(init=False)

    def __post_init__(self):
        self.record_size = get_record_size(self.schema)
        self.column_indices = {column['name']: i for i, column in enumerate(self.schema)}

    def _get_page_path(self, page_num: int) -> str:
        return mkpath(self.db_path, f'{self.name}_page_{page_num}.bin')

    def _load_page(self, page_num: int) -> list[RECORD_TYPE]:
        assert os.path.isfile(self._get_page_path(page_num))

        records = []

        with open(self._get_page_path(page_num), 'rb') as file:
            while len(record := file.read(self.record_size)) == self.record_size:
                records.append(deserialize(self.schema, record))

        return records

    def _dump_page(self, page_num: int, records: list[RECORD_TYPE]):
        with open(self._get_page_path(page_num), 'wb') as file:
            for record in records:
                file.write(serialize(self.schema, record))

    def select(self, columns: list[str] | None = None, where: dict[str, Any] | None = None) -> Iterable[RECORD_TYPE]:
        if columns is None:
            columns = [column['name'] for column in self.schema]
        if where is None:
            where = {}

        # print(f'SELECT {columns} FROM `{self.name}` WHERE {where}')

        for page_num in range(1, self.pages_total + 1):
            records = self._load_page(page_num)
            for record in records:
                if all(
                    record[self.column_indices[column]] == value
                    for column, value in where.items()
                ):
                    yield [record[self.column_indices[column]] for column in columns]

    def insert(self, values: RECORD_TYPE):
        # print(f'INSERT INTO `{self.name}` VALUES {values}')

        if self.pages_total:
            records = self._load_page(self.pages_total)
        else:
            self.pages_total = 1
            records = []

        if len(records) + 1 > PAGE_SIZE // self.record_size:
            self.pages_total += 1
            records = []

        records.append(values)
        self._dump_page(self.pages_total, records)

    def update(self, values: dict[str, Any], where: dict[str, Any]):
        # print(f'UPDATE `{self.name}` SET {values} WHERE {where}')

        for page_num in range(1, self.pages_total + 1):
            records = self._load_page(page_num)
            for i, record in enumerate(records):
                if all(
                    record[self.column_indices[column]] == value
                    for column, value in where.items()
                ):
                    for column, value in values.items():
                        records[i][self.column_indices[column]] = value
            self._dump_page(page_num, records)

    def delete(self, where: dict[str, Any]):
        # print(f'DELETE FROM `{self.name}` WHERE {where}')

        for page_num in range(1, self.pages_total + 1):
            records = self._load_page(page_num)
            records = [
                record
                for record in records
                if not all(
                    record[self.column_indices[column]] == value
                    for column, value in where.items()
                )
            ]
            self._dump_page(page_num, records)

    def drop(self):
        for page_num in range(1, self.pages_total + 1):
            os.remove(self._get_page_path(page_num))

    def to_json(self) -> dict[str, Any]:
        return {
            'schema': self.schema,
            'pages_total': self.pages_total,
        }
