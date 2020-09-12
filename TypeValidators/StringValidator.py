from typing import Dict  
import re


class ValidString:
    def __init__(self, schema: Dict, required : bool = False):
        self.name = None 
        self.required = required
        self._schema = schema

        self._min_length = self._schema.get("minLength")
        self._max_lenght = self._schema.get("maxLength")
        self._pattern = self._schema.get("pattern")
        self._pattern = re.compile(self._pattern) if self._pattern is not None else None
        self._enum = self._schema.get("enum")

    def validate(self, value):
        if self.required and value is None:
            raise ValueError(f"StringField '{self.name}' value is required but got None.")
        elif value is not None:
            if not isinstance(value, str):
                raise ValueError(f"{self.name} expects string but got {type(value).__name__}.")

            if self._min_length is not None and len(value) < self._min_length:
                raise ValueError(f"{self.name} leangth should be at least {self._min_length}")

            if self._max_lenght is not None and self._max_lenght < len(value):
                raise ValueError(f"{self.name} lenght should be smaller than {self._max_lenght}")

            if self._pattern is not None and not self._pattern.match(value):
                raise ValueError(f"{self.name} pattern should match '{self._pattern}'.")

            if self._enum is not None and value not in self._enum:
                raise ValueError(f"{self.name} StringType value must be in the enum list, enum={self._enum}")
            
    