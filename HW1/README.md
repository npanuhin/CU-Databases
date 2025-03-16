<h1 align="center">HW1</h1>


## Task `A MINUS B`:

[Online Playground](https://sqlplayground.app/sandbox/67b25b4a7244bde43a360873)

```sql
SELECT * FROM people
EXCEPT
SELECT 'Gor', 'Garni Street', 35;
```

Oracle uses `MINUS`, while PostgreSQL allows `EXCEPT`


## Task `A TIMES B`:

[Online Playground](https://sqlplayground.app/sandbox/67b25b6f7244bde43a36088c)

```sql
SELECT people.*, devices.*
FROM people, devices;
```

I couldn’t find a `TIMES` function in SQL, so I used a selection of columns from both tables instead.
