from pydantic import BaseModel


class TextInput(BaseModel):
    query: str
