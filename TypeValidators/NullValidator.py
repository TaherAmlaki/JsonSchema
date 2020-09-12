from typing import Dict  


class ValidNull:
    def __init__(self, schema: Dict, required : bool = False):
        self._schema = schema
        self.required = required
        self.name = None 

    def validate(self, value):
        if value is not None:
            raise ValueError(f"NullField '{self.name}' expects None/Null value but got {value}.")
