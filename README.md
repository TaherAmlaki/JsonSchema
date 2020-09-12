# Data Descriptors in Python, A practice with Json Schema

This small project is a practice on implementing data descriptors in Python to create 
a data model corresponding to a Json Schema. For this purpose each property in json schema 
will be represented as a data descriptor and when json data is used each attribute will validate 
the values. 

## Descriptors 
The implementation of descriptor that I use is to create a local WeakKeyDictionary on the descriptor 
and use instance object as key of that dictionary and after validations save the value into the 
dictionary. Validator is implemented outside the descriptor to keep the descriptor class readable.
Another benefit of having validation logic outside descriptor is the freedom we have when we implement 
a data descriptor for array properties.


## Usage 
CreateObjectClass class will take a name for data model class, and a json schema. An instance of 
this class will have data model namespace prepared. A property "model" on thsi instance will create a 
new class corresponding to json data and return this class which can be itself instantiated with no argument.
This instance inherits from ObjectModel class which implements validate method. Validate method will accept json data 
as argument and validate all the properties. It will collect all exceptions and if any exception exists after 
validations, it will raise a ValueError exception with a message listing all the validation error.
