from fastapi import APIRouter, UploadFile, File

from services.repo_storage import (
    save_uploaded_zip,
    create_project_folder,
    extract_zip,
    list_project_files,
)

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("")
async def upload_zip(file: UploadFile = File(...)):
    zip_path = save_uploaded_zip(file)

    project_id, project_dir = create_project_folder()

    extract_zip(zip_path, project_dir)

    files = list_project_files(project_dir)

    return {
        "message": "file uploaded and extracted successfully",
        "project_id": project_id,
        "filename": file.filename,
        "file_count": len(files),
        "files": files,
    }