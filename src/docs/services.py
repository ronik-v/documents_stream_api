import asyncio
import aiofiles
import os

from typing import Final
from logging import getLogger

from src.docs.contracts import StorageFiles
from src.config import settings
from src.docs.schemas import StorageFileOUT


class DocumentStorageService:
    """Service for file streaming"""

    def __init__(self, storage_path: str = settings.STATIC_PATH, chunk_size: int = 1024):
        self.storage_path = storage_path
        self.chunk_size = chunk_size

        self._split: Final[int] = 1024 * 1024
        self.logger = getLogger(__name__)

    async def read_file_by_file_id(self, file_id: str) -> bytes:
        if "." not in file_id:
            raise ValueError(f"Invalid file_id: '{file_id}'. Expected a file name with an extension.")

        file_path: str = os.path.join(self.storage_path, file_id)

        if self.chunk_size:
            chunks: list[bytes] = []

            async with aiofiles.open(file_path, mode="rb") as f:
                while True:
                    chunk = await f.read(self.chunk_size)
                    if not chunk:
                        break
                    chunks.append(chunk)
            return b"".join(chunks)
        else:
            async with aiofiles.open(file_path, mode="rb") as f:
                return await f.read()

    async def write_by_file_id(
            self,
            file_id: str,
            data: str,
            offset: int | None = None,
            line: int | None = None,
            column: int | None = None,
    ) -> None:
        file_path: str = os.path.join(self.storage_path, file_id)

        if offset is not None:
            async with aiofiles.open(file_path, mode="r+b") as f:
                await f.seek(offset)
                await f.write(data.encode("utf-8"))
            return

        if line is not None:
            if os.path.exists(file_path):
                async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
                    lines = await f.readlines()
            else:
                lines: list[str] = []

            while len(lines) <= line:
                lines.append("\n")

            if column is not None:
                original_line = lines[line].rstrip("\n")
                if len(original_line) < column:
                    original_line = original_line.ljust(column)
                new_line = original_line[:column] + data + original_line[column:]
            else:
                new_line = data
            lines[line] = new_line + "\n"

            async with aiofiles.open(file_path, mode="w", encoding="utf-8") as f:
                await f.writelines(lines)

            return

        async with aiofiles.open(file_path, mode="ab") as f:
            await f.write(data.encode("utf-8"))

    async def get_file_ids(self) -> StorageFiles:
        def _get_files() -> StorageFiles:
            if not os.path.exists(self.storage_path):
                self.logger.warning("Storage path %s does not exist", self.storage_path)
                return []
            files = os.listdir(self.storage_path)
            result: StorageFiles = []
            for file_name in files:
                file_path = os.path.join(self.storage_path, file_name)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    size_mb = stat.st_size / self._split
                    _, ext = os.path.splitext(file_name)
                    file_type = ext.lstrip(".")
                    result.append(StorageFileOUT(file_id=file_name, file_type=file_type, file_size_mb=round(size_mb, 2)))
            return result

        return await asyncio.to_thread(_get_files)
