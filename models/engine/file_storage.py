#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Return a dictionary of instantiated objects in __objects.
        If a cls is specified, returns a dictionary of objects of that type.
        Otherwise, returns the __objects dictionary.
        """
        if cls is not None:
            if isinstance(cls, str):
                cls = eval(cls)
            cls_dict = {}
            for k, v in self.__objects.items():
                if isinstance(v , cls):
                    cls_dict[k] = v
            return cls_dict
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({f"{obj.__class__name__}.{obj.id}": obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def get(self, cls, id):
        """A method to retrieve one object
        Returns the object based on the class name and its ID, or
        None if not found
        """
        for item in self.__objects.values():
            if isinstance(item, cls) and item.id == id:
                return item
        return None

    def count(self, cls=None):
        """A method to count the number of objects in storage
        Returns the number of objects in storage matching the given class name
        If no name is passed, returns the count of all objects in storage
        """
        if cls is None:
            return len(self.all())
        return len(self.all(cls))

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete a given object from __objects, if it exists."""
        try:
            del self.__objects[f"{type(obj).__name__}. {obj.id}"]
        except (AttributeError, KeyError):
            pass
        
    def close(self):
            """Call the reload method."""
            self.reload()
