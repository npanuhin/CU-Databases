<h1 align="center">HW6*</h1>


The [`run.py`](run.py) file provides a usage demonstration:

```bash
python3 run.py
```

This demonstation creates one table within a database, containing 200 entries spanning 6 page files. It then runs different operations on the table. Sample output of the demo:

```
Loaded metadata from stored database
Inserted 200 rows
Selected 200 rows

Deleted 1 row
Selected 199 rows

Selected random person: [36, 26, True, datetime.datetime(2000, 2, 6, 0, 0), 'Some Name 36']
Updating name of this person...
Selected only name of this person again: ['New Name']
```


### Explanation:

Database metadata (JSON)
```jsonc
{
    "{table_name}": {
        "schema": [
            { "name": "{column_name}", "type": "bool" },
            { "name": "{column_name}", "type": "char" },
            { "name": "{column_name}", "type": "int" },
            { "name": "{column_name}", "type": "long" },
            { "name": "{column_name}", "type": "float" },
            { "name": "{column_name}", "type": "string", "length": 100},
            { "name": "{column_name}", "type": "datetime" }
        ],
        "pages_total": 10
    }
}
```

Data type sizes:
```
bool     = 1 byte
char     = 1 byte
int      = 4 bytes
long     = 8 bytes (aka long long in C++)
float    = 8 bytes (aka double in C++)
string   = {number of characters} bytes
datetime = 8 bytes (timestamp: long)
```


#### Requirements:

- Python 3 installed (recent version, tested on 3.13)
