from typing import Dict
import weakref
from TypeValidators.ValidatorFactory import ValidatorFactory


class ArrayType:
    def __init__(self, schema: Dict, required: bool = False):
        self.data = weakref.WeakKeyDictionary()
        self.required = required
        self._schema = schema
        self.name = None

        self._min_items = self._schema.get("minItems", 0)
        self._max_items = self._schema.get("maxItems")
        self._unique_items = self._schema.get("uniqueItems", False)

        self._items = self._schema.get("items")
        self._contains = self._schema.get("contains")
        self._additional_items = self._schema.get("additionalItems")

    def __set__(self, instance, values):
        if self.required and values is None:
            raise ValueError(f"ArrayField '{self.name}' value is required but got None.")
        elif values is not None:
            if not isinstance(values, list):
                raise ValueError(f"{self.name} expects list but got {type(values).__name__}.")

            if len(values) < self._min_items:
                raise ValueError(f"{self.name} expects minimum number of items {self._min_items}, got {len(values)}")

            if self._max_items is not None and self._max_items < len(values):
                raise ValueError(f"{self.name} expects maximum number of items {self._max_items}, got {len(values)}")
            
            if self._unique_items:
                if len(set(values)) != len(values):
                    raise ValueError(f"{self.name} array field expects unique items.")
            
            if self._items is not None:
                if isinstance(self._items, dict):
                    validator = ValidatorFactory.get_validator(self._items, self.required)
                    for value in values:
                        validator.validate(value)
                elif isinstance(self._items, list):
                    if self._additional_items is not None:
                        validators = [ValidatorFactory.get_validator(item) for item in self._items]
                        additional_validators = [ValidatorFactory.get_validator(self._additional_items) for _ in range(len(values)-len(self._items))]
                        validators.extend(additional_validators)
                    else:
                        if len(self._items) != len(values):
                            raise ValueError(f"ArrayType {self.name} does not expect any additional items.")
                        validators = [ValidatorFactory.get_validator(item) for item in self._items]

                    for value, validator in zip(values, validators):
                        validator.validate(value)

            if self._contains is not None:
                validator = ValidatorFactory.get_validator(self._contains)
                if not any(lambda x: self._check_if_exception(validator, x) == 0 for x in values):
                    raise ValueError(f"ArrayType {self.name} expects at least one {self._contains} but got none.")
        self.data[instance] = values 
    
    def __set_name__(self, owner_class, name):
        self.name = name 
    
    def __get__(self, instance, owner_class):
        if instance is None:
            return self 
        value = self.data.get(instance)
        if self.required and value is None:
            raise ValueError(f"Value of the required field '{self.name}' is not defined yet.")
        return value 

    def __delete__(self, instance):
        self.data.pop(instance, None)
    
    @classmethod
    def _check_if_exception(cls, validator, value):
        try:
            validator.validate(value)
        except ValueError:
            return 1
        else:
            return 0

    
