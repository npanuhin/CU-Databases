The solution is implemented in [`KVStore.py`](KVStore.py).

> [!NOTE]
> The KVStore class uses an in-memory dictionary for storage, but every time a new instance is initialized, it reads the log file to restore its state, as required by the assignment

The [`run.py`](run.py) file provides a usage demonstration:

```bash
python3 run.py
```


#### Requirements:

- Python 3 (recent version, tested on 3.13) instaled
