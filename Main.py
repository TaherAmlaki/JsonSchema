import json 
from Models.CreateObjectModel import CreateObjectClass


with open("./schema_example.json", "r") as jf:
    schema = json.load(jf)

model_creator = CreateObjectClass(class_name="Test", schema=schema)
model_cls = model_creator.model
model = model_cls()

good_data = {"number": [1600], "street_name": "Pennsylvania", 
             "street_type": "Avenue"}
model.validate(good_data)

print("model.to_dict()=>", model.to_dict())
# print(model.to_json())

# validation_result, message = model.validate(bad_data)
# print(validation_result, message)
# print(model.to_json())

