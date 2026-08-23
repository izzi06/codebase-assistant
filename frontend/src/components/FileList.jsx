function FileList({ files, selectedPath, onFileClick }) {
  return (
    <aside className="rounded-2xl border border-slate-800 bg-slate-900/70 p-4 shadow-xl">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-lg font-semibold">Files</h2>
        <span className="rounded-full bg-slate-800 px-3 py-1 text-xs text-slate-300">
          {files.length}
        </span>
      </div>

      <div className="max-h-[600px] space-y-2 overflow-y-auto pr-1">
        {files.map((file) => (
          <button
            key={file}
            onClick={() => onFileClick(file)}
            className={`w-full rounded-lg border px-3 py-2 text-left text-sm transition ${
              selectedPath === file
                ? "border-blue-500 bg-blue-950/40 text-blue-100"
                : "border-slate-800 bg-slate-950 text-slate-300 hover:border-slate-600 hover:bg-slate-900"
            }`}
          >
            {file}
          </button>
        ))}
      </div>
    </aside>
  );
}

export default FileList;