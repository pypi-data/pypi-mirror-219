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

    def find(self, key: str, value: str) -> list:
        """Returns a list of dicts that contain the given key/value pair."""
        matching_entries = []
        for entry in self.__data[self.__coll]:
            if key in entry and entry[key] == value:
                matching_entries.append(entry)
        return matching_entries

    def get(self, id: int) -> dict:
        """Returns the entry with the given id in the current collection, or None if no entry is found."""
        for entry in self.__data[self.__coll]:
            if entry.get('id') == id:
                return entry
        print(f'No entry found with id: {id} in collection: {self.__coll}')
        return None

    def add(self, entry: dict) -> None:
        """Add an entry to the current collection."""
        if not isinstance(entry, dict):
            raise TypeError('Entry must be of type dict.')
        else:
            ids = [item['id'] for item in self.__data[self.__coll]]
            add_data = {'id': ids[-1] + 1 if ids else 0}
            add_data.update(entry)
            self.__data[self.__coll].append(add_data)

    def edit(self, id: int, key: str, value) -> None:
        """Edit an entry with the given id in the current collection."""
        if key == 'id':
            raise ValueError('Cannot edit the id of an entry.')
        for entry in self.__data[self.__coll]:
            if entry.get('id') == id:
                entry[key] = value
                return
        print(f'No entry found with id: {id} in collection: {self.__coll}')

    def rm_item(self, id: int):
        """Delete an entry at the given index from the current collection."""
        try:
            to_delete = self.find('id', id)[0]
            to_delete_index = self.__data[self.__coll].index(to_delete)
            del self.__data[self.__coll][to_delete_index]
            self.__deleted = True
        except IndexError:
            print(f'No entry found for id: {id} in collection: {self.__coll}')

    def rm_key(self, key: str, id) -> None:
        """Delete a key from an entry with the given id in the current collection."""
        if key == 'id':
            raise ValueError('Cannot delete the id of an entry.')
        try:
            to_delete = self.find('id', id)[0]
            if key in to_delete:
                del to_delete[key]
            else:
                print(f'Key: {key} not found in entry with id: {id} in collection: {self.__coll}')
        except IndexError:
            print(f'No entry found for id: {id} in collection: {self.__coll}')


    def rm_coll(self, collection: str) -> None:
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

    def rm_key_for_all(self, key: str) -> None:
        """Delete a key from all entries in the current collection."""
        if key == 'id':
            raise ValueError('Cannot delete the id of an entry.')
        for entry in self.__data[self.__coll]:
            if key in entry:
                del entry[key]

    def add_key_for_all(self, key: str, value='') -> None:
        """Add a key to all entries in the current collection."""
        if key == 'id':
            raise ValueError('Cannot add the id of an entry.')
        for entry in self.__data[self.__coll]:
            entry[key] = value

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
            self.create_coll(collection)
            self.__coll = collection
            print(f'Created and switched to collection: {collection}')

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

    def to_json(self, path: str='./') -> None:
        """Write the collection to a JSON file."""
        with open(f'{path}{self.__coll}.json', 'w') as f:
            json.dump(self.__data[self.__coll], f)

    def to_yaml(self, path: str='./') -> None:
        """Write the collection to a YAML file."""
        with open(f'{path}{self.__coll}.yaml', 'w') as f:
            yaml.dump(self.__data[self.__coll], f)

    def reindex(self) -> None:
        """Reindex the current collection."""
        for i, entry in enumerate(self.__data[self.__coll]):
            entry['id'] = i

    def coll_list(self) -> list:
        """List all collections in the database."""
        return [key for key in self.__data]

    def get_coll(self) -> None:
        """Return the current collection."""
        return self.__data[self.__coll]
    
    def set_coll(self, coll: list) -> None:
        """Overwrite the current collection."""
        if not isinstance(coll, list):
            raise TypeError('Collection must be of type list.')
        self.__data[self.__coll] = coll
        print(f'Colelction {self.__coll} overwritten.')
    
    def get_full_db(self) -> None:
        """Return the full database."""
        return self.__data
    