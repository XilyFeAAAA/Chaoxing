#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import aiofiles
from pathlib import Path
from http import HTTPStatus
from natsort import natsorted
from dataclasses import dataclass
from typing import Annotated, Callable
from fastapi import Form, UploadFile, File, BackgroundTasks, HTTPException
# local
from app.common import constants
from app.common.enums import StatusEnum
from app.utils.number_helper import generate_random_num


@dataclass
class UploadInfo:
    file_id: str
    status: int


async def merge_file(self, file_name: str, file_id: str):
    """merge files of slice into an integrity"""
    temp_folder = constants.TEMPFILE_FOLDER_PATH / file_id
    file_path = constants.TEMPFILE_FOLDER_PATH / file_name
    if not temp_folder.exists():
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="invaild temp files")
    async with aiofiles.open(file_path, "wb") as output:
        for temp_path in natsorted(temp_folder.iterdir(), key=lambda x: x.name):
            async with aiofiles.open(temp_path, "rb") as chunk:
                await output.write(await chunk.read())


class upload_chunks:
    """Dependency to receive an uploaded file with small size"""

    def __init__(self, *,
                 uploading_callback: Annotated[Callable | None, None],
                 uploaded_callback: Annotated[Callable | None, None]):
        """if output_path exists, the file or files should be saved and return pathlib.Path object"""
        self.uploading_callback = uploading_callback
        self.uploaded_callback = uploaded_callback

    async def __call__(self,
                       background_tasks: BackgroundTasks,
                       chunk_index: Annotated[int, Form(description="index of chunks")],
                       chunks: Annotated[int, Form(description="number of total chunks")],
                       file: Annotated[UploadFile, File(description="upload file")],
                       file_id: Annotated[str, Form()] = None,
                       file_name: Annotated[str, Form(...)] = None) -> UploadInfo:
        if file_id is None:
            file_id = generate_random_num(constants.TEMPFILE_ID_LENGTH)
        # 秒传功能（判断md5）
        base_folder: Path = constants.TEMPFILE_FOLDER_PATH
        temp_folder = base_folder / file_id
        if not temp_folder.exists():
            temp_folder.mkdir(parents=True)
        file_path = temp_folder / str(chunk_index)
        if not file_path.exists():
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(await file.read())
        if chunk_index < chunks - 1:
            result = UploadInfo(file_id, StatusEnum.uploading.value)
            return await self.uploading_callback(result) if self.uploading_callback is not None else result
        else:
            # async merge tempfiles after last file
            suffix = Path(file.filename).suffix
            final_filename = file_name + suffix
            background_tasks.add_task(merge_file, final_filename, file_id)
            result = UploadInfo(file_id, StatusEnum.uploaded.value)
            return await self.uploaded_callback(result) if self.uploaded_callback is not None else result
