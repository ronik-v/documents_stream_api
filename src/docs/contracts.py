from typing import Protocol

from src.docs.schemas import StorageFileOUT

type StorageFiles = list[StorageFileOUT]


class StreamFileProtocol(Protocol):
    """Interface for file service"""

    async def read_file_by_file_id(self, file_id: str) -> bytes: ...

    async def write_by_file_id(
            self,
            file_id: str,
            data: str,
            offset: int | None = None,
            line: int | None = None,
            column: int | None = None
    ) -> None: ...

    async def get_file_ids(self) -> StorageFiles: ...
