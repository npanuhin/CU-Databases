import re

regex = re.compile(r"""
    \"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\.\d{6}\"
""", re.IGNORECASE | re.VERBOSE | re.DOTALL | re.UNICODE)

with open('yellow-tripdata-2025-01.csv', 'r', encoding='utf-8') as file:
    lines = file.readlines()


for i, line in enumerate(lines):
    lines[i] = result = re.sub(regex, r'"\1"', line)

with open('yellow-tripdata-2025-01.clickhouse.csv', 'w', encoding='utf-8') as file:
    file.writelines(lines)

with open('C:/yellow-tripdata-2025-01.clickhouse.csv', 'w', encoding='utf-8') as file:
    file.writelines(lines)
