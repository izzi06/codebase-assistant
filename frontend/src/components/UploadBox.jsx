function UploadBox({
  selectedFile,
  projectId,
  message,
  isUploading,
  onFileChange,
  onUpload,
}) {
  return (
    <section className="mx-auto max-w-2xl rounded-2xl border border-slate-800 bg-slate-900/70 p-6 shadow-xl">
      <div className="flex flex-col items-center gap-4 text-center">
        <label className="w-full cursor-pointer rounded-xl border-2 border-dashed border-slate-700 bg-slate-950 p-6 hover:border-blue-500">
          <input
            type="file"
            accept=".zip"
            onChange={onFileChange}
            className="hidden"
          />

          <div className="space-y-2">
            <p className="font-medium">
              {selectedFile ? selectedFile.name : "Choose a ZIP file"}
            </p>
            <p className="text-sm text-slate-500">
              Click here to select a codebase ZIP.
            </p>
          </div>
        </label>

        <button
          onClick={onUpload}
          disabled={isUploading}
          className="rounded-xl bg-blue-600 px-6 py-3 font-semibold text-white shadow-lg shadow-blue-950/40 hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isUploading ? "Uploading..." : "Upload ZIP"}
        </button>

        {message && <p className="text-sm text-slate-300">{message}</p>}

        {projectId && (
          <div className="w-full rounded-xl bg-slate-950 px-4 py-3 text-left text-sm text-slate-400">
            <span className="text-slate-500">Project ID:</span>{" "}
            <span className="text-slate-200">{projectId}</span>
          </div>
        )}
      </div>
    </section>
  );
}

export default UploadBox;