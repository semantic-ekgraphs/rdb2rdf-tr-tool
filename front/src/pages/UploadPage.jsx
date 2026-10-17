import { useState } from "react";

function FileInput({ label, description, file, onChange, accept }) {
  return (
    <label className="upload-box">
      <input type="file" accept={accept} onChange={(e) => onChange(e.target.files?.[0] || null)} />
      <span className="upload-icon">↑</span>
      <strong>{file ? file.name : label}</strong>
      <span className="muted">{file ? `${(file.size / 1024).toFixed(1)} KB` : description}</span>
      <span className="upload-link">{file ? "Replace file" : "Select file"}</span>
    </label>
  );
}

export default function UploadPage({ busy, onRunTask1 }) {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);

  async function submit(event) {
    event.preventDefault();
    if (!file1 || !file2) return;
    await onRunTask1(file1, file2);
  }

  return (
    <div className="page-stack">
      <div className="page-intro">
        <div>
          <h1>Stage 1 – Transformation Rule Generation</h1>
          <p>The objective of this stage is to transform an R2RML specification into a set of formally
defined Transformation Rules (TRs) that conform to the conceptual framework.</p>
          
          
          <h1>Metadata Extraction and Normalization</h1>
          <p>Select the two files required to start the first task of the workflow.</p>
        </div>
        <span className="step-pill">1 de 3</span>
      </div>

      <form onSubmit={submit} className="surface-card">
        <div className="section-heading">
          <div>
            <h2>Input files</h2>
            <p>The two files are used only during the execution of Task 1.</p>
          </div>
          <span className="required-label">2 Required files</span>
        </div>

        <div className="upload-grid">
          <FileInput
            label="Relational schema"
            description="Select the scheme source"
            file={file1}
            onChange={setFile1}
            accept=".sql,.csv,.json,.txt,.ttl,.rml,.yaml,.yml,.md"
          />
          <FileInput
            label="R2RML mappings"
            description="Select the R2RML rules source"
            file={file2}
            onChange={setFile2}
            accept=".ttl,.rml,.sql,.csv,.json,.txt,.yaml,.yml,.md"
          />
        </div>

        <div className="info-strip">
          <span className="info-mark">i</span>
          <span>Following Task 1, the next stage will receive exclusively the confirmed output from the first task.</span>
        </div>

        <div className="form-footer">
          <span className="muted">Accepted formats depend on the processing configured in the backend.</span>
          <button className="button button-primary" type="submit" disabled={busy || !file1 || !file2}>
            {busy ? <><span className="spinner" /> Executing Task 1...</> : <>Send files and Execute <span>→</span></>}
          </button>
        </div>
      </form>
    </div>
  );
}
