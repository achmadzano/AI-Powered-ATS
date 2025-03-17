from pydantic import BaseModel
from typing import Optional

class Role(BaseModel):
    role: str
    description: str

class CVUpload(BaseModel):
    name: str
    email: Optional[str] = None
    text: str  # Hasil ekstraksi dari CV
