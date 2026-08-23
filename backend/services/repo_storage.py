import shutil
import uuid
import zipfile
from pathlib import Path
from fastapi import UploadFile, HTTPException

from core.config import UPLOAD_DIR, EXTRACT_DIR, IGNORED_DIRS, IGNORED_FILES


def save_uploaded_zip(file: UploadFile) -> Path:
    if file.filename is None:
        raise HTTPException(status_code=400, detail="no file provided")

    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="only ZIP files are allowed")

    zip_path = UPLOAD_DIR / file.filename

    with zip_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return zip_path


def create_project_folder() -> tuple[str, Path]:
    project_id = str(uuid.uuid4())
    project_dir = EXTRACT_DIR / project_id
    project_dir.mkdir(parents=True, exist_ok=True)

    return project_id, project_dir


def extract_zip(zip_path: Path, project_dir: Path) -> None:
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for member in zip_ref.infolist():
            target_path = project_dir / member.filename

            if not str(target_path.resolve()).startswith(str(project_dir.resolve())):
                raise HTTPException(status_code=400, detail="Unsafe ZIP file")

            zip_ref.extract(member, project_dir)


def list_project_files(project_dir: Path) -> list[str]:
    files = []

    for path in project_dir.rglob("*"):
        relative_path = path.relative_to(project_dir)
        parts = set(relative_path.parts)

        if not path.is_file():
            continue

        if parts.intersection(IGNORED_DIRS):
            continue

        if path.name in IGNORED_FILES:
            continue

        if path.name.startswith("._"):
            continue

        files.append(str(relative_path))

    return files

def get_project_dir(project_id: str) -> Path:
    project_dir = EXTRACT_DIR / project_id

    if not project_dir.exists():
        raise HTTPException(status_code=404, detail="project not found")
    
    return project_dir

def list_files_for_project(project_id: str) -> list[str]:
    project_dir = get_project_dir(project_id)
    return list_project_files(project_dir)

def read_file_contents(path: Path) -> str:
    if not path.exists():
        raise HTTPException(status_code=404, detail="file not found")

    if not path.is_file():
        raise HTTPException(status_code=400, detail="path is not a file")

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="file is not a readable text file")