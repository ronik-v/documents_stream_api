from logging import getLogger


class DocumentStorageService:
    """Service for file streaming"""

    def __init__(self, storage_path: str, chunk_size: int | None = None):
        self.storage_path = storage_path
        self.chunk_size = chunk_size

        self.logger = getLogger(__name__)

    async def read_file_by_file_id(self, file_id: str) -> bytes: ...

    async def write_by_file_id(self, file_id: str) -> None: ...

    async def get_file_ids(self) -> list[str]: ...
