from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from core.database import get_db
from models.project import Project

from services.repo_storage import (
    save_uploaded_zip,
    create_project_folder,
    extract_zip,
    list_project_files,
)

from pathlib import Path
from models.repository_file import RepositoryFile

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("")
def upload_zip(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):

    zip_path = save_uploaded_zip(file)
    project_id, project_dir = create_project_folder()

    extract_zip(zip_path, project_dir)

    files = list_project_files(project_dir)

    repository_files = []

    for file_path in files:
        absolute_path = project_dir / file_path

        repository_files.append(
            RepositoryFile(
                project_id=project_id,
                path=file_path,
                extension=Path(file_path).suffix,
                size_bytes=absolute_path.stat().st_size,
            )
        )

    project = Project(
        id=project_id, filename=file.filename, file_count=len(files), status="uploaded"
    )

    try:
        db.add(project)
        db.add_all(repository_files)
        db.commit()
        db.refresh(project)
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="failed to save project metadata"
        ) from error

    return {
        "message": "file uploaded and extracted successfully",
        "project_id": project_id,
        "filename": file.filename,
        "file_count": len(files),
        "files": files,
        "created_at": project.created_at,
    }
