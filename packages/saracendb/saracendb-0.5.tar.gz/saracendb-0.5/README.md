# SaracenDB

`SaracenDB` is a simple key-value store that uses BSON for storage. It provides basic CRUD operations (Create, Read, Update, Delete), as well as a search operation that finds keys starting with a given prefix.

## Installation

```bash
pip install saracendb
```

## Usage

```python
from saracendb import SaracenDB

db = SaracenDB('my_database.sr')

# Put a key-value pair into the database
db.put('key1', 'value1')

# Get a value from the database
value = db.get('key1')  # Returns 'value1'

# Search for keys starting with a prefix
keys = db.search('key')  # Returns ['key1']

# Remove a key-value pair from the database
db.rm('key1')

# Write changes to the database
db.push()
```

## Methods

### `__init__(self, filename: str)`

Creates a new `SaracenDB` instance. If a file with the given filename exists, it is opened and its contents are loaded into the database. If the file does not exist, it is created when `push` is called.

### `get(self, key: str)`

Returns the value associated with the given key. If no entry is found for the key, prints a message and returns `None`.

### `search(self, prefix: str)`

Returns a list of keys that start with the given prefix.

### `put(self, key: str, value)`

Creates or updates an entry with the given key and value. The value can be any type that can be serialized to BSON.

### `rm(self, key: str)`

Deletes an entry with the given key. If no entry is found for the key, prints a message.

### `push(self)`

Writes changes to the database. If any entries have been deleted since the last `push`, compacts the database to remove the deleted entries and reduce the file size.

### `compact(self)`

Removes deleted entries from the database and reduces the file size. This is done by writing the current data to a new file, then replacing the old file with the new one. This method is called automatically by `push` if any entries have been deleted.
