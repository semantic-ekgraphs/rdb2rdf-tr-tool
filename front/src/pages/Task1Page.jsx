import ResultViewer from "../components/ResultViewer";
import FeedbackPanel from "../components/FeedbackPanel";

export default function Task1Page({ result, busy, reviewBusy, notice, error, onFeedback, onApprove, onBack }) {
  return (
    <div className="page-stack">
      <div className="page-intro">
        <div>
          
          <h1>Extracted Metadata</h1>
          <p>Inspect the output. You can request a review or proceed with the current result.</p>
        </div>
        <span className={`status-pill ${result ? "status-success" : "status-pending"}`}>{result ? "Resultado disponível" : "Aguardando execução"}</span>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {notice && <div className="alert alert-info">{notice}</div>}

      <ResultViewer result={result} title="Output of the first task" />

      <FeedbackPanel
        busy={reviewBusy || busy}
        onFeedback={onFeedback}
        onApprove={onApprove}
        disabled={!result}
      />

      <div className="bottom-navigation">
        <button type="button" className="button button-light" onClick={onBack} disabled={busy}>← Voltar aos arquivos</button>
        <span className="muted">Task 2 will not be executed prior to your confirmation.</span>
      </div>
    </div>
  );
}
