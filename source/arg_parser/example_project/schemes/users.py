from pydantic import BaseModel, Json

'''
You have to use pydantic models for your handlers to get data from HTTP body.
Right now you can use only basic types and pydantic Json type for your annotations in pydantic models.

(!) In this version, the use of nested models for handler arguments is not supported.
'''


class UserModel(BaseModel):
    id: int
    name: str
    age: int
    data: Json
