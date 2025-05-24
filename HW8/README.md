# PostreSQL

```bash
sudo su - postgres
psql -U postgres -d hw8
```

```sql
CREATE TABLE nyc_taxi_trips (
    VendorID INTEGER,
    tpep_pickup_datetime TIMESTAMP,
    tpep_dropoff_datetime TIMESTAMP,
    passenger_count INTEGER,
    trip_distance REAL,
    RatecodeID INTEGER,
    store_and_fwd_flag CHAR(1),
    PULocationID INTEGER,
    DOLocationID INTEGER,
    payment_type INTEGER,
    fare_amount REAL,
    extra REAL,
    mta_tax REAL,
    tip_amount REAL,
    tolls_amount REAL,
    improvement_surcharge REAL,
    total_amount REAL,
    congestion_surcharge REAL,
    Airport_fee REAL
);
```

```bash
psql -U postgres -d hw8 -c "\COPY nyc_taxi_trips FROM '/mnt/c/yellow-tripdata-2025-01.csv' CSV HEADER NULL '\N'"
```


# Clickhouse

