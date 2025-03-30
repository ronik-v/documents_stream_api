import os
from collections.abc import AsyncGenerator
from logging import getLogger
from time import perf_counter
from urllib import parse

from litestar import Controller, get, Router
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from litestar.response import Stream

from src.docs.contracts import StorageFiles
from src.docs.services import DocumentStorageService


class DocumentsController(Controller):
    """Documents API methods"""

    path = "/docs"

    def __init__(self, owner: Router):
        super().__init__(owner)

        self.storage_service = DocumentStorageService()
        self.logger = getLogger(__name__)

    @get(path="/{file_id:str}")
    async def get_file_by_id(
            self,
            file_id: str,
    ) -> Stream:
        """Get file stream"""
        start_time = perf_counter()

        file_path: str = os.path.join(self.storage_service.storage_path, file_id)

        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND, detail="File not found"
            )

        try:
            file_bytes: bytes = await self.storage_service.read_file_by_file_id(file_id)

        except Exception as ex:
            self.logger.error("Ошибка чтения файла %s: %s", file_id, ex)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error reading file",
            )

        decoded_filename: str = parse.unquote(file_id)

        async def file_generator() -> AsyncGenerator[bytes, None]:
            chunk_size = self.storage_service.chunk_size or len(file_bytes)
            for i in range(0, len(file_bytes), chunk_size):
                yield file_bytes[i: i + chunk_size]

        elapsed_time = (perf_counter() - start_time) * 1000

        return Stream(
            file_generator(),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{parse.quote(decoded_filename)}",
                "X-Response-Time": f"{elapsed_time:.2f} ms",
            },
        )

    @get(path="/names")
    async def get_file_ids_from_static_storage(
        self,
    ) -> StorageFiles:
        """Get all file objects from storage"""
        files = await self.storage_service.get_file_ids()
        return files
