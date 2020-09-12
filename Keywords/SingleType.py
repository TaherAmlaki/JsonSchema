"""
Data descriptors that will be used as class attributes 
"""
from typing import Dict
import weakref
from TypeValidators.ValidatorFactory import ValidatorFactory


class SingleType:
    def __init__(self, schema: Dict, required: bool = False):
        self.data = weakref.WeakKeyDictionary()
        self.required = required
        self._schema = schema
        self.name = None
        self._validator = ValidatorFactory.get_validator(self._schema, self.required)

    def __set_name__(self, owner_class, name) -> None:
        self.name = name 
        if self._validator is not None:
            self._validator.name = name 
    
    def __set__(self, instance, value) -> None:
        if self._validator is not None:
            self._validator.validate(value)
        self.data[instance] = value 
    
    def __get__(self, instance, owner_class=None) -> object:
        if instance is None:
            return self 
        value = self.data.get(instance)
        if self.required and value is None and self._schema.get("type") != "null":
            raise ValueError(f"Value of the required field '{self.name}' is not defined yet.")
        return value 

    def __delete__(self, instance) -> None:
        self.data.pop(instance, None)
