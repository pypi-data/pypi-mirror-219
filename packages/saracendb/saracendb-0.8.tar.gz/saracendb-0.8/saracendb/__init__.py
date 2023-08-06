import os
import bson
import json
import yaml
import shutil

class SaracenDB:
    def __init__(self, filename: str, collection: str='default'):
        self.__filename = filename
        self.__data = {}
        self.__coll = collection
        self.__deleted = False
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.__data = bson.decode(f.read())
        if self.__coll not in self.__data:
            self.__data[self.__coll] = []

    @property
    def file(self) -> str:
        """Return the filename of the database."""
        return self.__filename

    @property
    def colls(self) -> list:
        """List all collections in the database."""
        return [key for key in self.__data]

    @property
    def coll(self) -> str:
        """Return the current collection."""
        return self.__coll
    
    @property
    def len(self) -> int:
        """Returm the length of the database."""
        return len(self.__data)

    @property
    def coll_len(self) -> int:
        """Return the length of the current collection."""
        return len(self.__data[self.__coll])

    @property
    def all(self) -> dict:
        """Return the full database."""
        return self.__data

    def find(self, key: str, value: str) -> list:
        """Returns a list of dicts that contain the given key/value pair."""
        matching_entries = []
        for entry in self.__data[self.__coll]:
            if key in entry and entry[key] == value:
                matching_entries.append(entry)
        return matching_entries
    
    def filter(self, keys: list, values: list) -> list:
        """Returns a list of dicts that contain the given key/value pairs."""
        matching_entries = []
        for entry in self.__data[self.__coll]:
            if all(key in entry and entry[key] == value for key, value in zip(keys, values)):
                matching_entries.append(entry)
        return matching_entries

    def get(self, id: int) -> dict:
        """Returns the entry with the given id in the current collection, or None if no entry is found."""
        for entry in self.__data[self.__coll]:
            if entry['#'] == id:
                return entry
        print(f'No entry found with id: {id} in collection: {self.__coll}')
        return None

    def add(self, entry: dict) -> None:
        """Add an entry to the current collection."""
        if not isinstance(entry, dict):
            raise TypeError('Entry must be of type dict.')
        else:
            ids = [item['#'] for item in self.__data[self.__coll]]
            add_data = {'#': ids[-1] + 1 if ids else 0}
            add_data.update(entry)
            self.__data[self.__coll].append(add_data)

    def edit(self, key: str, new_value, id: int,) -> None:
        """Edit an entry with the given id in the current collection. Can also add a new key/value pair."""
        if key == '#':
            raise ValueError('Cannot edit the id of an entry.')
        for entry in self.__data[self.__coll]:
            if entry['#'] == id:
                entry[key] = new_value
                return
        print(f'No entry found with id: {id} in collection: {self.__coll}')

    def edit_many (self, key: str, new_value, ids: list) -> None:
        """Edit multiple entries with the given ids in the current collection. Can also add a new key/value pair."""
        if key == '#':
            raise ValueError('Cannot edit the id of an entry.')
        for entry in self.__data[self.__coll]:
            if entry['#'] in ids:
                entry[key] = new_value

    def edit_all(self, key: str, new_value) -> None:
        """Edit a key in all entries in the current collection. Key/Value pairs will be added if they don't exist."""
        if key == '#':
            raise ValueError('Cannot edit the id of an entry.')
        for entry in self.__data[self.__coll]:
            entry[key] = new_value

    def add_coll(self, collection: str) -> None:
        """Create a new collection and switch to it."""
        if collection in self.__data:
            print(f'Collection already exists for name: {collection}')
        else:
            self.push()
            self.__data[collection] = []
            self.__coll = collection

    def use_coll(self, collection: str) -> None:
        """Switch to a collection."""
        self.push()
        if collection in self.__data:
            self.__coll = collection
            print(f'Switched to collection: {collection}')
        else:
            self.add_coll(collection)
            self.__coll = collection
            print(f'Created and switched to collection: {collection}')

    def del_item(self, id: int):
        """Delete an entry at the given index from the current collection."""
        for i, entry in enumerate(self.__data[self.__coll]):
            if entry['#'] == id:
                del self.__data[self.__coll][i]
                self.__deleted = True
                print(f'Entry with id: {id} deleted from collection: {self.__coll}')
            else:
                print(f'No entry found with id: {id} in collection: {self.__coll}')

    def del_items(self, ids: list):
        """Delete all items from the current collection with the given ids."""
        for id in ids:
            for i, entry in enumerate(self.__data[self.__coll]):
                if entry['#'] == id:
                    del self.__data[self.__coll][i]
                    self.__deleted = True
                    print(f'Entry with id: {id} deleted from collection: {self.__coll}')
                else:
                    print(f'No entry found with id: {id} in collection: {self.__coll}')

    def del_key(self, key: str, id) -> None:
        """Delete a key from an entry with the given id in the current collection."""
        if key == '#':
            raise ValueError('Cannot delete the id of an entry.')
        for entry in self.__data[self.__coll]:
            if entry['#'] == id:
                if key in entry:
                    del entry[key]
                    self.__deleted = True
                    return
        print(f'No entry found with id: {id} in collection: {self.__coll}')

    def del_keys(self, keys: list, id) -> None:
        """Delete multiple keys from an entry with the given id in the current collection."""
        if '#' in keys:
            raise ValueError('Cannot delete the id of an entry.')
        for key in keys:
            for entry in self.__data[self.__coll]:
                if entry['#'] == id:
                    if key in entry:
                        del entry[key]
                        self.__deleted = True
                        return
            print(f'No entry found with id: {id} in collection: {self.__coll}')

    def del_key_for_all(self, key: str) -> None:
        """Delete a key from all entries in the current collection."""
        if key == '#':
            raise ValueError('Cannot delete the id of an entry.')
        for entry in self.__data[self.__coll]:
            if key in entry:
                del entry[key]
                self.__deleted = True

    def del_keys_for_all(self, keys: list) -> None:
        """Delete multiple keys from all entries in the current collection."""
        if '#' in keys:
            raise ValueError('Cannot delete the id of an entry.')
        for key in keys:
            for entry in self.__data[self.__coll]:
                if key in entry:
                    del entry[key]
                    self.__deleted = True

    def del_coll(self, collection: str) -> None:
        """Delete the current collection."""
        if len(self.__data) == 1:
            print('Cannot delete the last collection.')
            return
        if collection == self.__coll:
            print('Cannot delete the collection while using it.')
            return
        try:
            del self.__data[collection]
            self.__deleted = True
        except KeyError:
            pass

    def push(self) -> None:
        """Write changes to the database."""
        with open(self.__filename, 'wb') as f:
            f.write(bson.encode(self.__data))
        if self.__deleted:
            self.compact()
            self.__deleted = False

    def compact(self) -> None:
        """Remove deleted entries from the database / reduce file size."""
        temp_filename = self.__filename + '.tmp'
        with open(temp_filename, 'wb') as f:
            f.write(bson.encode(self.__data))
        shutil.move(temp_filename, self.__filename)

    def to_json(self, coll: str=None, cust_path: str=None) -> None:
        """Write the collection to a JSON file. If no collection is specified the entire db will be written to the file"""
        data, file_path = ''
        if not coll or coll == '':
            coll = 'db'
            data = self.__data
        else:
            data = self.__data[coll]
        if cust_path is None:
            file_path = f'{coll}.json'
        else:
            file_path = cust_path
            with open(file_path, 'w') as f:
                json.dump(data, f)  

    def to_yaml(self, coll: str=None, cust_path: str=None) -> None:
        """Write the collection to a YAML file. If no collection is specified the entire db will be written to the file"""
        data, file_path = ''
        if not coll or coll == '':
            coll = 'db'
            data = self.__data
        else:
            data = self.__data[coll]
        if cust_path is None:
            file_path = f'{coll}.yaml'
        else:
            file_path = cust_path
            with open(file_path, 'w') as f:
                yaml.dump(data, f) 

    def add_json(self, path: str) -> None:
        """add a JSON file to the current collection."""
        with open(path, 'r') as f:
            file = json.load(f)
        if not isinstance(file, list):
            raise TypeError('File must be of type list.')
        for entry in file:
            if not isinstance(entry, dict):
                raise TypeError('File must be of type list of dicts.')
        for entry in file:
            try:
                del entry['#']
            except KeyError: pass
        file = [{'#': i}.update(entry) for i, entry in enumerate(file)]
        self.__data[self.__coll] += file

    def add_yaml(self, path: str) -> None:
        """Import a yaml file to the current collection."""
        with open(path, 'r') as f:
            file = yaml.load(f)
        if not isinstance(file, list):
            raise TypeError('File must be of type list.')
        for entry in file:
            if not isinstance(entry, dict):
                raise TypeError('File must be of type list of dicts.')
        for entry in file:
            try:
                del entry['#']
            except KeyError: pass
        file = [{'#': i}.update(entry) for i, entry in enumerate(file)]
        self.__data[self.__coll] += file

    def reindex(self) -> None:
        """Reindex the current collection."""
        for i, entry in enumerate(self.__data[self.__coll]):
            entry['#'] = i
        self.push()
        self.compact()

    def get_coll(self) -> None:
        """Return the current collection data."""
        return self.__data[self.__coll]
    
    def set_coll(self, coll: list) -> None:
        """Overwrite the current collection."""
        if not isinstance(coll, list):
            raise TypeError('Collection must be of type list.')
        self.__data[self.__coll] = coll
        print(f'Colelction {self.__coll} overwritten.')

    def backup(self, path: str='backup.db') -> None:
        """Backup the database."""
        shutil.copyfile(self.__filename, path)