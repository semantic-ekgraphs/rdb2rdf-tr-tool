import ResultViewer from "../components/ResultViewer";

export default function Task1_2Page({ result, busy, error, notice, onRun, onBack, task2Approved }) {
  return (
    <div className="page-stack">
      <div className="page-intro">
        <div>
          <h1>Stage 2 – AFTER Trigger Generation</h1>
          <p>This stage automatically synthesizes PostgreSQL AFTER triggers from the Transformation Rules defined in Stage 1.</p>

          <h1>TR generation</h1>
          <p>TASK 1_2 uses the approved output of Task 3 as its input.</p>
        </div>
        <span className={`status-pill ${result ? "status-success" : "status-pending"}`}>{result ? "Completed" : "Ready to execute"}</span>
      </div>

      <div className="info-strip">
        <span className="info-mark">i</span>
        <span>Input for Task 1_2: confirmed output from Task 3. The two original files are not sent again.</span>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {notice && <div className="alert alert-info">{notice}</div>}

      {!result && (
        <section className="surface-card task-launch-card">
          <div className="task-launch-icon">Ⅱ</div>
          <div>
            <h2>Execute the next task</h2>
            <p>When you start, the Node will forward only the approved result from Task 3 to the route configured for Task 1_2..</p>
            <button type="button" className="button button-primary" onClick={onRun} disabled={busy || !task2Approved}>
              {busy ? <><span className="spinner" /> Executing Task 1_2...</> : <>Execute Task 1_2 <span>→</span></>}
            </button>
          </div>
        </section>
      )}

      {result && <ResultViewer result={result} title="Completion of the first task by the second agent" />}

      <div className="bottom-navigation">
        <button type="button" className="button button-light" onClick={onBack} disabled={busy}>← Return to Task 1</button>
        {result && <span className="status-pill status-success">Workflow completed up to Task 1_2</span>}
      </div>
    </div>
  );
}
