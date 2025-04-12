from datetime import date, timedelta
from random import randint

from DB import DB


db = DB('data/database')
N = 200

if 'people' in db.tables:
    db.drop_table('people')

db.create_table('people', (
    {'name': 'id', 'type': 'int'},
    {'name': 'age', 'type': 'int'},
    {'name': 'active', 'type': 'bool'},
    {'name': 'birthday', 'type': 'datetime'},
    {'name': 'name', 'type': 'string', 'length': 100},
))

for i in range(N):
    db.insert('people', (
        i,
        20 + (i % 10),
        i % 2 == 0,
        date(2000, 1, 1) + timedelta(days=i),
        f'Some Name {i}',
    ))
print(f'Inserted {N} rows')

rows = db.select('people')
print(f'Selected {len(list(rows))} rows')

print()

db.delete('people', {'id': 1})
print('Deleted 1 row')

rows = db.select('people')
print(f'Selected {len(list(rows))} rows')

print()

random_id = randint(2, N - 1)
selected_people = tuple(db.select('people', where={'id': random_id}))
assert len(selected_people) == 1
print('Selected random person:', selected_people[0])

print('Updating name of this person...')
db.update('people', {'name': 'New Name'}, where={'id': random_id})

selected_people = tuple(db.select('people', ['name'], where={'id': random_id}))
print('Selected only name of this person again:', selected_people[0])
