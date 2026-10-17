import ResultViewer from "../components/ResultViewer";

export default function Task3Page({ result, busy, error, notice, onRun, onBack, task2Approved }) {
  return (
    <div className="page-stack">
      <div className="page-intro">
        <div>
          
          <h1>TR generation</h1>
          <p>The third task uses the approved output from Task 2 as its input..</p>
        </div>
        <span className={`status-pill ${result ? "status-success" : "status-pending"}`}>{result ? "Concluída" : "Pronta para executar"}</span>
      </div>

      <div className="info-strip">
        <span className="info-mark">i</span>
        <span>Input for Task 3: confirmed output from Task 2. The two original files are not sent again..</span>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {notice && <div className="alert alert-info">{notice}</div>}

      {!result && (
        <section className="surface-card task-launch-card">
          <div className="task-launch-icon">Ⅱ</div>
          <div>
            <h2>Execute the next task</h2>
            <p>When you start, the Node will forward only the approved result from Task 2 to the route configured for Task 3.</p>
            <button type="button" className="button button-primary" onClick={onRun} disabled={busy || !task2Approved}>
              {busy ? <><span className="spinner" /> Executing Task 3...</> : <>Execute Task 3 <span>→</span></>}
            </button>
          </div>
        </section>
      )}

      {result && <ResultViewer result={result} title="Output of the third task" />}

      <div className="bottom-navigation">
        <button type="button" className="button button-light" onClick={onBack} disabled={busy}>← Return to Task 1</button>
        {result && <span className="status-pill status-success">Workflow completed up to Task 3</span>}
      </div>
    </div>
  );
}
