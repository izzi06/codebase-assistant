from fastapi import APIRouter, HTTPException
from services.repo_storage import list_files_for_project, read_file_contents, get_project_dir
from pathlib import Path

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/{project_id}/files")
async def get_project_files(project_id: str):
    files = list_files_for_project(project_id)

    return {
        "project_id": project_id,
        "file_count": len(files),
        "files": files  
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

