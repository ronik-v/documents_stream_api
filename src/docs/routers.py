from litestar import Controller, get
from litestar.response import Stream

from src.docs.schemas import StorageFileOUT


type StorageFiles = list[StorageFileOUT]


class DocumentsController(Controller):
    """Documents api methods"""

    path = "/docs"

    @get(path="/names")
    async def get_file_ids_from_static_storage(self) -> StorageFiles:
        """Get all file objects from storage"""

    @get(path="/{file_id:str}")
    async def get_file_by_id(self, file_id: str) -> Stream:
        """Get file stream"""
