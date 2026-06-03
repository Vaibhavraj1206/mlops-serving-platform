from pydantic import BaseModel

class MLInput(BaseModel):
    user_id: int
    data_text: str