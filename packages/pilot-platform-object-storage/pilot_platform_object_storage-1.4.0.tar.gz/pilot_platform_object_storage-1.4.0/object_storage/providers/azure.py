# Copyright (C) 2023 Indoc Research
#
# Contact Indoc Research for any questions regarding the use of this source code.

import logging
from pathlib import Path
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from uuid import uuid4

import aiofiles
import aiofiles.os
from aiofiles.os import makedirs
from aiofiles.threadpool.binary import AsyncBufferedReader
from azure.core.exceptions import ClientAuthenticationError
from azure.core.exceptions import HttpResponseError
from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobBlock
from azure.storage.blob.aio import BlobClient

logger = logging.getLogger('pilot.object-storage')


class AzureClient:
    """Base base class for object storage clients."""

    def _handle_exception(self, exc: Exception) -> Exception:
        """Handles exceptions raised during Azure Blob Storage operations."""
        if isinstance(exc, ClientAuthenticationError):
            logger.exception(
                'Failed to authenticate with Azure. Check the correctness of tenant_id, client_id, or client_secret.'
            )
        elif isinstance(exc, ResourceNotFoundError):
            logger.info('The requested resource was not found.')
        elif isinstance(exc, HttpResponseError):
            logger.exception(f'Error in HTTP response: {exc.status_code} - {exc.reason}')
        else:
            logger.exception('Unexpected error occurred')
        return exc

    async def _create_parent_dir(self, file_path: str) -> None:
        """The funtion will create the parent folder by the file path."""

        dirname = str(Path(file_path).parent)
        await makedirs(dirname, exist_ok=True)

    async def _upload(
        self,
        client: BlobClient,
        file_path: str,
        key: str,
        progress_callback: Optional[Callable[[str, int, int], Awaitable[Any]]] = None,
        chunk_size: int = 4 * 1024 * 1024,
    ) -> Dict[str, Any]:
        """Upload a file to sas URL."""

        async with aiofiles.open(file_path, mode='rb') as f:
            uploaded_blocks = await self._upload_chunks(client, file_path, key, f, chunk_size, progress_callback)
            return await self._commit_blob(client, uploaded_blocks)

    async def _upload_chunks(
        self,
        client: BlobClient,
        file_path: str,
        key: str,
        file_obj: AsyncBufferedReader,  # has to be checked the correct type
        chunk_size: int = 4 * 1024 * 1024,
        progress_callback: Optional[Callable[[str, int, int], Awaitable[Any]]] = None,
        current: int = 0,
    ) -> List[BlobBlock]:
        """Upload the file by cutting into chunks.

        If there is progress callback, will upload the chunk from the current point.
        """
        uploaded_blocks = []
        file_length = (await aiofiles.os.stat(file_path)).st_size

        while True:
            chunk = await file_obj.read(chunk_size)
            if not chunk:
                break
            block_id = str(uuid4())
            await client.stage_block(block_id=block_id, data=chunk)
            if progress_callback:
                current = min(current + chunk_size, file_length)
                await progress_callback(key, current, file_length)
            uploaded_blocks.append(BlobBlock(block_id=block_id))
        return uploaded_blocks

    async def _commit_blob(self, client: BlobClient, block_list: Optional[List[BlobBlock]] = None) -> Dict[str, Any]:
        """Commits the uncommitted blocks of a blob, making them a part of the blob's content."""
        if block_list:
            return await client.commit_block_list(block_list)
        _, block_list = await client.get_block_list('uncommitted')
        return await client.commit_block_list(block_list)

    async def _download_bytes(
        self,
        client: BlobClient,
        key: str,
        progress_callback: Optional[Callable[[str, int, int], Awaitable[Any]]] = None,
    ) -> bytes:
        """Download a file bytes from the specified container."""

        stream = await client.download_blob(max_concurrency=4)
        chunk_list = []
        current = 0
        async for chunk in stream.chunks():
            current += len(chunk)
            if progress_callback:
                await progress_callback(key, current, stream.size)
            chunk_list.append(chunk)
        return b''.join(chunk_list)

    async def _download(
        self,
        client: BlobClient,
        key: str,
        file_path: str,
        chunk_size: Optional[int] = 4 * 1024 * 1024,
        progress_callback: Optional[Callable[[str, int, int], Awaitable[Any]]] = None,
    ) -> None:
        """Download a file from the specified container."""

        async def progress_hook(current: int, total: int) -> None:
            if progress_callback:
                await progress_callback(key, current, total)

        async with aiofiles.open(file_path, 'wb') as file:
            stream = await client.download_blob(max_concurrency=4, progress_hook=progress_hook)
            await file.write(await stream.read(chunk_size))

    async def _copy_from_url(
        self,
        client: BlobClient,
        source_url: str,
    ) -> str:
        """Copies a file from a URL to a blob in the specified container."""

        resp = await client.start_copy_from_url(source_url=source_url)
        return resp['copy_status']

    async def _delete(self, client: BlobClient) -> None:
        """Delete the blob and all its snapshots."""

        return await client.delete_blob(delete_snapshots='include')

    async def _resume_upload(
        self,
        client: BlobClient,
        key: str,
        file_path: str,
        chunk_size: int = 4 * 1024 * 1024,
        progress_callback: Optional[Callable[[str, int, int], Awaitable[Any]]] = None,
    ) -> None:
        """Uploads a file to an Azure Blob Storage container, resuming an interrupted upload if there is an uncommitted
        block list."""

        uploaded_blocks = []
        offset = 0

        _, block_list = await client.get_block_list('uncommitted')
        for block in block_list:
            offset += block.size
            uploaded_blocks.append(block.id)

        current = offset
        file_length = (await aiofiles.os.stat(file_path)).st_size
        file_renaming_length = file_length - offset

        if file_renaming_length:
            async with aiofiles.open(file_path, mode='rb') as f:
                await f.seek(offset)
                uploaded_blocks += await self._upload_chunks(
                    client, file_path, key, f, chunk_size, progress_callback, current
                )

        await self._commit_blob(client, uploaded_blocks)

    async def _get_blob_chunks(
        self,
        client: BlobClient,
    ) -> Tuple[list[BlobBlock], list[BlobBlock]]:
        """Returns a list of committeed and uncommitted the info of blob chunks."""

        commited_block_list, uncommited_block_list = await client.get_block_list('all')

        return commited_block_list, uncommited_block_list
