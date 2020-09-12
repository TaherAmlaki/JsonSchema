from typing import Dict  
import re


class ValidBoolean:
    def __init__(self, schema: Dict, required : bool = False):
        self._schema = schema
        self.required = required
        self.name = None 

    def validate(self, value):
        if self.required and value is None:
            raise ValueError(f"BooleanField '{self.name}' value is required but got None.")
        elif value is not None:
            if not isinstance(value, bool):
                raise ValueError(f"BooleanField '{self.name}' expects boolean but got {type(value).__name__}.")
        