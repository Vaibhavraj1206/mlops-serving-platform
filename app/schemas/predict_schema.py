from pydantic import BaseModel

class MLInput(BaseModel):
    user_id: int
    # Pehle data_text: str tha, ab numbers ki list hai
    features: list[float]