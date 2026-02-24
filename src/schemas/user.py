from pydantic import BaseModel

class UserFormSchema(BaseModel):
    login: str
    password: str