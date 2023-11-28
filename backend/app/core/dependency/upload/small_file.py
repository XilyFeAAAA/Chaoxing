#! /usr/bin/env python
# -*- coding: utf-8 -*-#-
import aiofiles
from pathlib import Path
from typing import Annotated
from dataclasses import dataclass
from fastapi import UploadFile, File, Form
# local
from app.common import constants


@dataclass
class UploadInfo:
    file_name: str
    file: UploadFile


async def async_save(output_path: Path, name: str, file: UploadFile):
    """async save file to self.output_path"""
    file_path = output_path / name
    async with aiofiles.open(file_path, "wb") as f:
        while True:
            data = await file.read(constants.small_chunk_size)
            await f.write(data)
            if len(data) != constants.small_chunk_size:
                break
    return Path(file_path)


class upload_small_multi:
    """Dependency to receive uploaded files with small size"""

    def __init__(self, output_path: Path | None = None):
        """if output_path exists, the file or files should be saved and return pathlib.Path object"""
        self.output_path = output_path

    async def __call__(self,
                       files: Annotated[list[UploadFile], File(description="multiple files upload")],
                       file_names: Annotated[list[str] | None, Form()] = None) -> list[UploadInfo] | list[Path]:
        # Handle cases where names and files do not match
        if len(files) <= len(file_names):
            filenames = file_names[:len(files)]
        else:
            filenames = [file.filename for file in files]
        # output_path exists and return Path objects
        if self.output_path is not None:
            # Handle cases where output_path doesn't exist
            if not self.output_path.exists():
                self.output_path.mkdir()
            return [await async_save(self.output_path, filenames[index], file) for index, file in enumerate(files)]
        else:
            return [UploadInfo(filenames[index], file) for index, file in enumerate(files)]


class upload_small:
    """Dependency to receive a uploaded file with small size"""

    def __init__(self, output_path: Path | None = None):
        """if output_path exists, the file or files should be saved and return pathlib.Path object"""
        self.output_path = output_path

    async def __call__(self,
                       file: Annotated[UploadFile, File(description="single file upload")],
                       file_name: Annotated[str | None, Form()] = None) -> UploadInfo | Path:
        # output_path exists and return Path objects
        if self.output_path is not None:
            # Handle cases where output_path doesn't exist
            if not self.output_path.exists():
                self.output_path.mkdir()
            return await async_save(self.output_path, file_name or file.filename, file)
        else:
            return UploadInfo(file_name or file.filename, file)
