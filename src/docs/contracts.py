from typing import Protocol


class StreamFileProtocol(Protocol):
    """Interface for file service"""

    async def read_file_by_file_id(self, file_id: str) -> bytes: ...

    async def write_by_file_id(self, file_id: str) -> None: ...

    async def get_file_ids(self) -> list[str]: ...
