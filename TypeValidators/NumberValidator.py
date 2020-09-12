from typing import Dict  
from numbers import Real


class ValidNumber:
    def __init__(self, schema: Dict, required : bool = False):
        self.name = None 
        self.required = required
        self._schema = schema

        self._minimum = self._schema.get("minimum")
        self._maximum = self._schema.get("maximum")
        self._multiple_of = self._schema.get("multipleOf")
        self._exlusive_maximum = self._schema.get("exclusiveMaximum")
        self._exclusive_minimum = self._schema.get("exclusiveMinimum")

        if isinstance(self._exclusive_minimum, bool):
            self._exclusive_minimum = self._minimum if self._exclusive_minimum else None 
        if isinstance(self._exlusive_maximum, bool):
            self._exclusive_maximum = self._maximum if self._exclusive_maximum else None 

    def validate(self, value):
        if self.required and value is None:
            raise ValueError(f"NumericField '{self.name}' value is required but got None.")
        elif value is not None:
            if not isinstance(value, Real):
                raise ValueError(f"NumericField '{self.name}' expects number but got {type(value).__name__}.")
            if self._minimum is not None and value < self._minimum:
                raise ValueError(f"{self.name} value should be at bigger or equal to {self._minimum}")
            if self._maximum is not None and self._maximum < value:
                raise ValueError(f"NumericField '{self.name}' value should be equal or smaller than {self._maximum}")
            if self._exclusive_minimum is not None and value <= self._exclusive_minimum:
                raise ValueError(f"{self.name} value should be bigger than {self._exclusive_minimum}")
            if self._exlusive_maximum is not None and self._exlusive_maximum <= value:
                raise ValueError(f"NumericField '{self.name}' value should be smaller than {self._exlusive_maximum}")
            if self._multiple_of is not None and value % self._multiple_of != 0:
                raise ValueError(f"NumericField '{self.name}' value should be multiple of {self._multiple_of}")
    