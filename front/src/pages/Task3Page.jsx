import { useMemo, useState } from "react";
import ResultViewer from "../components/ResultViewer";

export default function Task3Page({ result, busy, error, notice, onRun, onBack, task2Approved }) {
  const [activeTab, setActiveTab] = useState(0);

  // Extrai as duas saídas da Crew
  const crewOutputs = useMemo(() => {
    if (!result) return [];

    // Caso o backend retorne o objeto padrão da Crew com tasks_output
    const rawList =
      result.tasks_output ||
      result.output?.tasks_output ||
      (Array.isArray(result) ? result : null);

    if (Array.isArray(rawList) && rawList.length > 0) {
      return rawList.map((taskItem, index) => ({
        // Mantém compatibilidade com string direta ou objeto da tarefa
        raw: typeof taskItem === "string" ? taskItem : (taskItem.raw || taskItem.output || JSON.stringify(taskItem, null, 2)),
        filename: index === 0 ? "termo_de_referencia.md" : "validacao_tr.md",
        title: index === 0 ? "1. Geração do TR" : "2. Validação do TR",
        description: taskItem.description || (index === 0 ? "Documento base gerado" : "Relatório de conformidade e validação")
      }));
    }

    // Fallback: se o backend enviou apenas o resultado agregado em result.raw ou result
    return [{
      raw: result.raw || result.output || result,
      filename: "resultado_crew.md",
      title: "Saída da Crew",
      description: "Resultado da execução"
    }];
  }, [result]);

  return (
    <div className="page-stack">
      <div className="page-intro">
        <div>
          <h1>TR &amp; Validação</h1>
        </div>
        <span className={`status-pill ${result ? "status-success" : "status-pending"}`}>
          {result ? "Concluída" : "Pronta para executar"}
        </span>
      </div>


      {error && <div className="alert alert-error">{error}</div>}
      {notice && <div className="alert alert-info">{notice}</div>}

      {!result && (
        <section className="surface-card task-launch-card">
          <div className="task-launch-icon">Ⅱ</div>
          <div>
            <h2>Executar Crew de TR</h2>
            <button type="button" className="button button-primary" onClick={onRun} disabled={busy || !task2Approved}>
              {busy ? <><span className="spinner" /> Processando TR e Validação...</> : <>Executar Etapa 3 <span>→</span></>}
            </button>
          </div>
        </section>
      )}

      {/* Exibição com Abas (Tabs) para alternar entre TR e Validação */}
      {crewOutputs.length > 1 && (
        <div className="tabs-header" style={{ display: "flex", gap: "8px", margin: "16px 0 8px 0" }}>
          {crewOutputs.map((item, index) => (
            <button
              key={index}
              type="button"
              className={`button ${activeTab === index ? "button-primary" : "button-light"}`}
              onClick={() => setActiveTab(index)}
            >
              {item.title}
            </button>
          ))}
        </div>
      )}

      {/* Renderiza a aba ativa ou ambos empilhados caso prefira */}
      {crewOutputs.length > 0 && (
        <ResultViewer
          result={crewOutputs[activeTab] || crewOutputs[0]}
          title={crewOutputs[activeTab]?.title || "Resultado"}
        />
      )}

      <div className="bottom-navigation">
        <button type="button" className="button button-light" onClick={onBack} disabled={busy}>
          ← Voltar para Task 2
        </button>
        {result && <span className="status-pill status-success">Workflow finalizado com sucesso</span>}
      </div>
    </div>
  );
}
