function FileViewer({ selectedPath, fileInfo, fileContent, isReadingFile }) {
  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900/70 shadow-xl">
      <div className="border-b border-slate-800 px-5 py-4">
        {selectedPath ? (
          <div className="space-y-1">
            <h2 className="font-semibold">{selectedPath}</h2>

            {fileInfo && (
              <p className="text-sm text-slate-500">
                {fileInfo.filename} · {fileInfo.extension || "no extension"} ·{" "}
                {fileInfo.lineCount} lines
              </p>
            )}
          </div>
        ) : (
          <div>
            <h2 className="font-semibold">File Viewer</h2>
            <p className="text-sm text-slate-500">
              Click a file to read its contents.
            </p>
          </div>
        )}
      </div>

      <div className="p-5">
        {isReadingFile ? (
          <p className="text-slate-400">Loading file...</p>
        ) : selectedPath ? (
          <pre className="max-h-[620px] overflow-auto rounded-xl bg-slate-950 p-4 text-sm leading-6 text-slate-200">
            <code>{fileContent || "This file is empty."}</code>
          </pre>
        ) : (
          <div className="flex min-h-[300px] items-center justify-center rounded-xl border border-dashed border-slate-800 bg-slate-950 text-slate-500">
            No file selected yet.
          </div>
        )}
      </div>
    </section>
  );
}

export default FileViewer;