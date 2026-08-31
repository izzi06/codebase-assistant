from fastapi import APIRouter, HTTPException, Depends
from services.repo_storage import (
    list_files_for_project,
    read_file_contents,
    get_project_dir,
)
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.database import get_db
from models.project import Project

router = APIRouter(prefix="/projects", tags=["Projects"])


"""@router.get("/{project_id}/files")
async def get_project_files(project_id: str):
    files = list_files_for_project(project_id)

    return {"project_id": project_id, "file_count": len(files), "files": files}



@router.get("/{project_id}/files/content")
def get_file_content(project_id: str, path: str):
    project_dir = get_project_dir(project_id)
    requested_path = project_dir / path
    if not str(requested_path.resolve()).startswith(str(project_dir.resolve())):
        raise HTTPException(status_code=400, detail="unsafe file path")

    file_content = read_file_contents(requested_path)

    return {
        "project_id": project_id,
        "path": path,
        "filename": Path(path).name,
        "extension": Path(path).suffix,
        "line_count": len(file_content.splitlines()),
        "content": file_content,
    }

"""


# helper
def project_to_dict(project: Project) -> dict:
    return {
        "id": project.id,
        "filename": project.filename,
        "file_count": project.file_count,
        "status": project.status,
        "created_at": project.created_at,
    }


@router.get("")
def get_projects(db: Session = Depends(get_db)):
    statement = select(Project).order_by(Project.created_at.desc())
    projects = db.scalars(statement).all()

    return {
        "project_count": len(projects),
        "projects": [project_to_dict(project) for project in projects],
    }


@router.get("/{project_id}")
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)

    if project is None:
        raise HTTPException(status_code=404, detail="project not found")

    return project_to_dict(project)


@router.get("/{project_id}/files")
def get_project_files(project_id: str):
    files = list_files_for_project(project_id)

    return {
        "project_id": project_id,
        "file_count": len(files),
        "files": files,
    }


@router.get("/{project_id}/files/content")
def get_file_content(project_id: str, path: str):
    project_dir = get_project_dir(project_id)
    requested_path = project_dir / path

    if not str(requested_path.resolve()).startswith(str(project_dir.resolve())):
        raise HTTPException(status_code=400, detail="unsafe file path")

    file_content = read_file_contents(requested_path)

    return {
        "project_id": project_id,
        "path": path,
        "filename": Path(path).name,
        "extension": Path(path).suffix,
        "line_count": len(file_content.splitlines()),
        "content": file_content,
    }
