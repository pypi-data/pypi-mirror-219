# SaracenDB Documentation

## Introduction

SaracenDB is a Python-based NoSQL database, offering a simple and flexible data storage solution. It uses BSON for data serialization and allows users to create, read, update, and delete data in an easy-to-use manner.

## Class Initialization

```python
db = SaracenDB(filename: str, collection: str='default')
```

- `filename` : Name of the file that will store the database.
- `collection` : Name of the collection to use initially. If not provided, the default collection name will be 'default'.

## Methods

### Add

Add a new entry to the current collection.

```python
db.add(entry: dict) 
```

- `entry` : The data to be added to the collection, in dictionary form.

### Find

Finds entries in the current collection that match a given key-value pair.

```python
db.find(key: str, value: str)
```

- `key` : The key to look for in the entries.
- `value` : The value to look for in the entries.

### Get

Get an entry by its ID in the current collection.

```python
db.get(id: int)
```

- `id` : The ID of the entry.

### Edit

Edit a key-value pair in an entry in the current collection.

```python
db.edit(id: int, key: str, value)
```

- `id` : The ID of the entry.
- `key` : The key to edit.
- `value` : The new value.

### rm_item

Delete an entry from the current collection using its ID.

```python
db.rm_item(id: int)
```

- `id` : The ID of the entry.

### rm_key

Delete a key from an entry in the current collection.

```python
db.rm_key(key: str, id)
```

- `key` : The key to delete.
- `id` : The ID of the entry.

### rm_coll

Delete a collection.

```python
db.rm_coll(collection: str)
```

- `collection` : The name of the collection to delete.

### rm_key_for_all

Delete a key from all entries in the current collection.

```python
db.rm_key_for_all(key: str)
```

- `key` : The key to delete.

### add_key_for_all

Add a key to all entries in the current collection.

```python
db.add_key_for_all(key: str, value='')
```

- `key` : The key to add.
- `value` : The initial value of the new key.

### add_coll

Create a new collection.

```python
db.add_coll(collection: str)
```

- `collection` : The name of the new collection.

### use_coll

Switch to another collection.

```python
db.use_coll(collection: str)
```

- `collection` : The name of the collection to switch to.

### push

Save changes to the database.

```python
db.push()
```

### compact

Remove deleted entries from the database file to reduce file size.

```python
db.compact()
```

### to_json

Write the current collection to a JSON file.

```python
db.to_json(path: str)
```

- `path` : The path of the JSON file.

### to_yaml

Write the current collection to a YAML file.

```python
db.to_yaml(path: str)
```

- `path` : The path of the YAML file.

### db_to_json

Write the entire database to a JSON file.

```python
db.db_to_json(path: str)
```

- `path` : The path of the JSON file.

### db_to_yaml

Write the entire database to a YAML file.

```python
db.db_to_yaml(path: str)
```

- `path` : The path of the YAML file.

### json_to_db

Create a new database from a JSON file.

```python
db.json_to_db(path: str)
```

- `path` : The path of the JSON file.

### yaml_to_db

Create a new database from a YAML file.

```python
db.yaml_to_db(path: str)
```

- `path` : The path of the YAML file.

### import_json_to_coll

Import a JSON file to the current collection.

```python
db.import_json_to_coll(path: str)
```

- `path` : The path of the JSON file.

### import_yaml_to_coll

Import a YAML file to the current collection.

```python
db.import_yaml_to_coll(path: str)
```

- `path` : The path of the YAML file.

### reindex

Reindex the current collection.

```python
db.reindex()
```

### coll_list

List all collections in the database.

```python
db.coll_list()
```

### get_coll

Return the current collection.

```python
db.get_coll()
```

### set_coll

Overwrite the current collection.

```python
db.set_coll(coll: list)
```

- `coll` : The new collection data, in list form.

### get_full_db

Return the full database.

```python
db.get_full_db()
```
