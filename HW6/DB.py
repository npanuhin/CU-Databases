from typing import Any, Iterable

import json
import os

from constants import SCHEMA_TYPE, RECORD_TYPE
from utils import mkpath
from Table import Table


class DB:
    def __init__(self, database_folder_path: str):
        self.path = database_folder_path
        self.load_metadata()

    def load_metadata(self):
        self.tables = {}
        try:
            with open(mkpath(self.path, 'metadata.json'), 'r', encoding='utf-8') as file:
                self.tables = json.load(file)
            for name, table in self.tables.items():
                self.tables[name] = Table(
                    name=name,
                    schema=table['schema'],
                    db_path=self.path,
                    pages_total=table['pages_total']
                )
            print('Loaded metadata from stored database')
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            print('No stored data found')

    def dump_metadata(self):
        if not os.path.isdir(self.path):
            os.makedirs(self.path, exist_ok=True)

        with open(mkpath(self.path, 'metadata.json'), 'w', encoding='utf-8') as file:
            json.dump(self.tables, file, default=lambda x: x.to_json(), indent=4)

    def create_table(self, name: str, schema: SCHEMA_TYPE):
        self.tables[name] = Table(name, schema, self.path)
        self.dump_metadata()

    def drop_table(self, name: str):
        if name in self.tables:
            self.tables[name].drop()
        self.tables.pop(name)
        self.dump_metadata()

    def select(
        self,
        table_name: str,
        columns: list[str] | None = None,
        where: dict[str, Any] | None = None
    ) -> Iterable[RECORD_TYPE]:
        yield from self.tables[table_name].select(columns, where)

    def insert(self, table_name: str, values: RECORD_TYPE):
        self.tables[table_name].insert(values)
        self.dump_metadata()

    def update(self, table_name: str, values: dict[str, Any], where: dict[str, Any]):
        self.tables[table_name].update(values, where)
        self.dump_metadata()

    def delete(self, table_name: str, where: dict[str, Any]):
        self.tables[table_name].delete(where)
        self.dump_metadata()
