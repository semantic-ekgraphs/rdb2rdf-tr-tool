import { useState } from "react";

export default function FeedbackPanel({ busy, onFeedback, onApprove, disabled = false }) {
  const [feedback, setFeedback] = useState("");

  async function submitFeedback() {
    if (!feedback.trim()) return;
    await onFeedback(feedback.trim());
    setFeedback("");
  }

  return (
    <section className="review-card">
      <div className="review-heading">
        <div className="review-icon">↻</div>
        <div>
          <h3>Human-in-the-loop (HITL)</h3>
          <p>You can request adjustments or proceed with the current output.</p>
          {/* <h3>Revisão humana (HITL)</h3>
          <p>Você pode solicitar ajustes ou seguir com a saída atual.</p> */}
        </div>
      </div>
      <label htmlFor="feedback">Review instructions</label>
      {/* <label htmlFor="feedback">Instruções de revisão</label> */}
      <textarea
        id="feedback"
        value={feedback}
        onChange={(event) => setFeedback(event.target.value)}
        // placeholder="Ex.: corrija os nomes das propriedades, preserve estas entidades..."
        placeholder="E.g., correct the property names, preserve these entities..."
        rows={4}
        disabled={busy || disabled}
      />
      <div className="review-actions">
        <button
          type="button"
          className="button button-secondary"
          onClick={submitFeedback}
          disabled={busy || disabled || !feedback.trim()}
        >
          {busy ? "Sending..." : "Send feedback"}
          {/* {busy ? "Enviando..." : "Enviar feedback"} */}
        </button>
        <button
          type="button"
          className="button button-primary"
          onClick={onApprove}
          disabled={busy || disabled}
        >
          Proceed without changes <span aria-hidden="true">→</span>
          {/* Avançar sem alterações <span aria-hidden="true">→</span> */}
        </button>
      </div>
      {/* <p className="helper-text">
        O feedback é registrado separadamente da aprovação. Para que ele regenere a saída automaticamente, conecte o endpoint real de revisão do seu FastAPI.
      </p> */}
    </section>
  );
}
