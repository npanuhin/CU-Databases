from KVStore import KeyValueStore


store = KeyValueStore()

store['name'] = 'Zelda'
store['race'] = 'Gerudo'

store['name'] = 'Link'
store['race'] = 'Hylian'

store2 = KeyValueStore()  # New object, reads from file with history

print(store2['name'])  # Link
print(store2['race'])  # Hylian

del store2['race']

store3 = KeyValueStore()  # New object, reads from file with history

try:
    print(store3['race'])  # Should raise KeyError
except KeyError:
    print('Key "race" not found')
