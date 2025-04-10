from typing import Any

import os


class KeyValueStore:
    def __init__(self, filepath: str = 'data/store.log'):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self.filepath = filepath
        self.reload()

    def reload(self):
        self.kv: dict[str, Any] = {}

        if not os.path.exists(self.filepath):
            return

        with open(self.filepath, 'r', encoding='utf-8') as file:
            for line in map(str.strip, file):
                parts = line.split(' ', 2)
                if not parts:
                    continue
                cmd, key = parts[0], parts[1]
                if cmd == 'SET':
                    self.kv[key] = parts[2]
                elif cmd == 'DELETE':
                    self.kv.pop(key, None)

    def __setitem__(self, key: str, value: Any):
        with open(self.filepath, 'a', encoding='utf-8') as file:
            print(f'SET {key} {value}', file=file)
        self.kv[key] = value

    def __getitem__(self, key: str):
        return self.kv[key]

    def __delitem__(self, key: str):
        with open(self.filepath, 'a', encoding='utf-8') as file:
            print(f'DELETE {key}', file=file)
        del self.kv[key]
