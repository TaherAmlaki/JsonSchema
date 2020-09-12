from typing import Dict, List
from Models.ObjectModel import ObjectModel 
from Keywords.SingleType import SingleType
from Keywords.ArrayType import ArrayType 
from TypeValidators.ValidatorFactory import ValidatorFactory


class CreateObjectClass:
    # http://json-schema.org/understanding-json-schema/reference/object.html#object
    # TODO: additionalProperties, propertyNames, dependencies
    
    def __init__(self, class_name: str, schema: Dict):
        self._class_name = class_name
        self._schema = schema
        self._properties = self._schema.get("properties", {})
        self._required = self._schema.get("required", [])

        """ These keywords must be transferred to ObjectModel, since they can be validated after object creation in validate() """
        model_dict = {"_min_properties": self._schema.get("minProperties"), 
                      "_max_properties": self._schema.get("maxProperties"), 
                      "_additional_properties": self._schema.get("additionalProperties", True)}

        for field_name, field_schema in self._properties.items():
            field_type = field_schema.get("type")
            if field_type == "object":
                model_creator = CreateObjectClass(class_name=field_name, schema=field_schema)
                field = model_creator.model()
            elif field_type == "array":
                field = ArrayType(field_schema)
            else:
                field = SingleType(field_schema)

            model_dict[field_name] = field
            model_dict[field_name].name = field_name
            if field_name in self._required:
                model_dict[field_name].required = True 
        self._namespace = model_dict


    @property
    def model(self) -> "ObjectModel":
        return type(self._class_name, (ObjectModel, object), self._namespace)
    