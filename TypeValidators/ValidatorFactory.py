from typing import Dict  
from TypeValidators.StringValidator import ValidString
from TypeValidators.IntegerValidator import ValidInteger
from TypeValidators.NumberValidator import ValidNumber
from TypeValidators.BooleanValidator import ValidBoolean
from TypeValidators.NullValidator import ValidNull


class ValidatorFactory:

    @classmethod
    def get_validator(cls, schema: Dict, required: bool = False):
        type_ = schema.get("type")

        if type_ == "string":
            return ValidString(schema, required)
        elif type_ == "integer":
            return ValidInteger(schema, required)
        elif type_ == "number":
            return ValidNumber(schema, required)
        elif type_ == "boolean":
            return ValidBoolean(schema, required)
        elif type_ == "null":
            return ValidNull(schema, required)

        