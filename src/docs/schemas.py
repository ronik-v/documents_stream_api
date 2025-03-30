from pydantic import BaseModel


class StorageFileOUT(BaseModel):
    """Model response for file in storage"""

    file_id: str
    file_type: str
    file_size_mb: float
