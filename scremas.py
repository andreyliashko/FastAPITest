from pydantic import BaseModel


class UserList(BaseModel):
    id: str
    username: str
    password: str
    first_name: str
    last_name: str
    create_at: str


class StudentModel(BaseModel):
    user_id: int
    name: str
    surname: str
    item_id: str

#
# class AutoId(BaseModel):
#     username: str
#     password: str
#     first_name: str
#     last_name: str
#     create_at: str
