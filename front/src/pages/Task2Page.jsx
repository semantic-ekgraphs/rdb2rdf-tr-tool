import ResultViewer from "../components/ResultViewer";

export default function Task2Page({ result, busy, error, notice, onRun, onBack, task1Approved }) {
  return (
    <div className="page-stack">
      <div className="page-intro">
        <div>
          
          <h1>Entity-Preservation Analysis</h1>
          <p>The second task uses the approved output from Task 1 as its only input.</p>
        </div>
        <span className={`status-pill ${result ? "status-success" : "status-pending"}`}>{result ? "Completed" : "Ready to execute"}</span>
      </div>

      <div className="info-strip">
        <span className="info-mark">i</span>
        <span>Input for Task 2: confirmed output from Task 1. The two original files are not sent again.</span>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {notice && <div className="alert alert-info">{notice}</div>}

      {!result && (
        <section className="surface-card task-launch-card">
          <div className="task-launch-icon">Ⅱ</div>
          <div>
            <h2>Execute the next task</h2>
            <p>When you start, the Node will forward only the approved result from Task 1 to the route configured for Task 2.</p>
            <button type="button" className="button button-primary" onClick={onRun} disabled={busy || !task1Approved}>
              {busy ? <><span className="spinner" /> Executing Task 2...</> : <>Execute Task 2 <span>→</span></>}
            </button>
          </div>
        </section>
      )}

      {result && <ResultViewer result={result} title="Output of the second task" />}

      <div className="bottom-navigation">
        <button type="button" className="button button-light" onClick={onBack} disabled={busy}>← Return to Task 1</button>
        {result && <span className="status-pill status-success">Workflow completed up to Task 2</span>}
      </div>
    </div>
  );
}
