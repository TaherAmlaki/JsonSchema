import json
from typing import Dict, List
from Keywords.SingleType import SingleType
from Keywords.ArrayType import ArrayType 


class ObjectModel:
    """
    Fields will be added to this class at runtime according to the schema
    """
    @classmethod
    def get_fields(cls) -> List[str]:
        return [field_name for field_name, field_value in cls.__dict__.items() if 
                isinstance(field_value, (SingleType, ArrayType))]


    @classmethod
    def get_objects(cls) -> List["ObjectModel"]:
        return [obj_name for obj_name, obj_value in cls.__dict__.items() if isinstance(obj_value, ObjectModel)]
    

    def validate(self, request: Dict):
        fields = type(self).get_fields()
        exceptions = []
        for field in fields:
            attr = getattr(type(self), field, None)
            if isinstance(attr, (SingleType, ArrayType)):
                try:
                    setattr(self, attr.name, request.get(attr.name))
                except ValueError as ex:
                    exceptions.append(ex)

        objects = type(self).get_objects()
        for obj in objects:
            attr = getattr(type(self), obj, None)
            if isinstance(attr, ObjectModel):
                try:
                    attr.validate(request.get(attr.__class__.__name__))
                except ValueError as ex:
                    exceptions.append(ex)
        
        try:
            self._check_min_max_properties()
        except ValueError as ex:
            exceptions.append(ex)

        if len(exceptions) != 0:
            error_msg = "\n".join([f"{ex_ind+1}. {str(ex)}" for ex_ind, ex in enumerate(exceptions)])
            raise ValueError(error_msg)
    

    def to_dict(self) -> Dict:
        res = {}
        fields = type(self).get_fields()
        for field in fields:
            attr = getattr(type(self), field, None)
            res[attr.name] = getattr(self, attr.name, None)
        
        objects = type(self).get_objects()
        for obj in objects:
            attr = getattr(self, obj, None)
            res[attr.name] = attr.to_dict()
        return res


    def _check_min_max_properties(self):
        fields = type(self).get_fields()
        if getattr(self, "_min_propertis", None) is not None and len(fields) < self._min_properties:
            raise ValueError(f"Number of properties should be higher than {self._min_properties}, got {len(fields)}")

        if getattr(self, "_max_properties", None) is not None and self._max_properties < len(fields):
             raise ValueError(f"Number of properties should be lower than {self._max_properties}, got {len(fields)}")
        


        