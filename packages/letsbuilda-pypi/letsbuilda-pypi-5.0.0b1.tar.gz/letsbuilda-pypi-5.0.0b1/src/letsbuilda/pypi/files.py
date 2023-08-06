"""Interactions with parsing package metadata and contents."""

import tarfile
from io import BytesIO
from zipfile import ZipFile


def read_tarfile(buffer: BytesIO) -> dict[str, str]:
    """Return a dictionary mapping filenames to content."""
    files = {}
    with tarfile.open(fileobj=buffer) as file:
        for tarinfo in file:
            if tarinfo.isreg():
                files[tarinfo.name] = file.extractfile(tarinfo).read().decode(encoding="UTF-8", errors="ignore")
    return files


def read_zipfile(buffer: BytesIO) -> dict[str, str]:
    """Return a dictionary mapping filenames to content."""
    files = {}
    with ZipFile(file=buffer) as zip_file:
        for zip_info in zip_file.infolist():
            if not zip_info.is_dir():
                files[zip_info.filename] = zip_file.read(zip_info).decode(encoding="UTF-8", errors="ignore")
    return files
