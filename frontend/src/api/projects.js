const API_BASE_URL = "http://localhost:8000";

export async function uploadProjectZip(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Upload failed");
  }

  return response.json();
}

export async function getProjectFiles(projectId) {
  const response = await fetch(`${API_BASE_URL}/projects/${projectId}/files`);

  if (!response.ok) {
    throw new Error("Could not fetch project files");
  }

  return response.json();
}

export async function readProjectFile(projectId, filePath) {
  const encodedPath = encodeURIComponent(filePath);

  const response = await fetch(
    `${API_BASE_URL}/projects/${projectId}/files/content?path=${encodedPath}`
  );

  if (!response.ok) {
    throw new Error("Could not read file");
  }

  return response.json();
}