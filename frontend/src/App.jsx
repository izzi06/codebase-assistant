import { useState } from "react";
import {
  uploadProjectZip,
  getProjectFiles,
  readProjectFile,
} from "./api/projects";
import UploadBox from "./components/UploadBox";
import FileList from "./components/FileList";
import FileViewer from "./components/FileViewer";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [projectId, setProjectId] = useState("");
  const [files, setFiles] = useState([]);
  const [selectedPath, setSelectedPath] = useState("");
  const [fileContent, setFileContent] = useState("");
  const [fileInfo, setFileInfo] = useState(null);
  const [message, setMessage] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [isReadingFile, setIsReadingFile] = useState(false);

  function clearProjectState() {
    setProjectId("");
    setFiles([]);
    setSelectedPath("");
    setFileContent("");
    setFileInfo(null);
  }

  function handleFileChange(event) {
    const file = event.target.files[0];

    setSelectedFile(file);
    setMessage("");
    clearProjectState();
  }

  async function handleUpload() {
    if (!selectedFile) {
      setMessage("Please choose a ZIP file first.");
      return;
    }

    try {
      setIsUploading(true);
      setMessage("Uploading and extracting project...");

      const uploadData = await uploadProjectZip(selectedFile);
      const filesData = await getProjectFiles(uploadData.project_id);

      setProjectId(uploadData.project_id);
      setFiles(filesData.files);
      setSelectedPath("");
      setFileContent("");
      setFileInfo(null);
      setMessage(`Uploaded successfully. Found ${filesData.file_count} files.`);
    } catch (error) {
      console.error(error);
      setMessage("Something went wrong while uploading.");
    } finally {
      setIsUploading(false);
    }
  }

  async function handleFileClick(filePath) {
    if (!projectId) {
      setMessage("No project loaded yet.");
      return;
    }

    try {
      setIsReadingFile(true);
      setSelectedPath(filePath);
      setFileContent("");
      setFileInfo(null);

      const data = await readProjectFile(projectId, filePath);

      setFileContent(data.content);
      setFileInfo({
        filename: data.filename,
        extension: data.extension,
        lineCount: data.line_count,
      });
    } catch (error) {
      console.error(error);
      setMessage("Could not read that file.");
    } finally {
      setIsReadingFile(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100 px-6 py-10">
      <div className="mx-auto max-w-6xl space-y-8">
        <header className="text-center space-y-3">
          <p className="text-sm uppercase tracking-[0.3em] text-blue-400">
            AI Codebase Assistant
          </p>

          <h1 className="text-4xl font-bold">
            Upload a repo. Inspect the code.
          </h1>
        </header>

        <UploadBox
          selectedFile={selectedFile}
          projectId={projectId}
          message={message}
          isUploading={isUploading}
          onFileChange={handleFileChange}
          onUpload={handleUpload}
        />

        {files.length > 0 && (
          <section className="grid gap-6 lg:grid-cols-[360px_1fr]">
            <FileList
              files={files}
              selectedPath={selectedPath}
              onFileClick={handleFileClick}
            />

            <FileViewer
              selectedPath={selectedPath}
              fileInfo={fileInfo}
              fileContent={fileContent}
              isReadingFile={isReadingFile}
            />
          </section>
        )}
      </div>
    </main>
  );
}

export default App;