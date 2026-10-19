import { useState } from "react";
import { DEFAULT_WORKFLOW } from "../services/workflowDefinition";

export default function WorkflowLayout({ stage, executionStage = stage, onNavigate, children, status, workflow = DEFAULT_WORKFLOW }) {
  const [collapsedAgents, setCollapsedAgents] = useState({});
  const agents = workflow?.agents?.length ? workflow.agents : DEFAULT_WORKFLOW.agents;

  // O layout não contém nomes fixos de tasks: percorre os agentes e suas tasks
  // recebidos do backend. Assim, novos itens aparecem sem alterar este componente.
  const allTasks = agents.flatMap((agent) => (agent.tasks || []).map((task) => ({ ...task, agentId: agent.id })));

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">RIT</div>
          <div><strong>RDB2RDF IVM Tool</strong><span>LLM Multiagent</span></div>
        </div>

        <div className="sidebar-label">WORKFLOW</div>
        <nav className="steps-nav agent-nav" aria-label="Workflow por agente e task">
          {agents.map((agent) => {
            const tasks = agent.tasks || [];
            const isCollapsed = Boolean(collapsedAgents[agent.id]);
            const agentActive = tasks.some((task) => task.stage === stage);
            return (
              <section className={`agent-group ${agentActive ? "agent-active" : ""}`} key={agent.id}>
                <button
                  type="button"
                  className="agent-heading"
                  aria-expanded={!isCollapsed}
                  onClick={() => setCollapsedAgents((current) => ({ ...current, [agent.id]: !current[agent.id] }))}
                  title="Expandir ou recolher tasks deste agente"
                >
                  <span className="agent-chevron">{isCollapsed ? "▸" : "▾"}</span>
                  <span className="agent-heading-copy"><strong>{agent.name}</strong><small>{agent.description || `${tasks.length} task(s)`}</small></span>
                  <span className="agent-count">{tasks.length}</span>
                </button>
                {!isCollapsed && <div className="agent-tasks">
                  {tasks.map((task) => {
                    const taskStage = Number.isInteger(task.stage) ? task.stage : -1;
                    // `stage` indica somente qual página está selecionada.
                    // `executionStage` indica o progresso real do workflow.
                    // Assim, clicar numa task anterior muda a visualização,
                    // mas não altera o estágio de execução.
                    const active = taskStage === stage;
                    const done = taskStage >= 0 && taskStage < executionStage;
                    // Só ficam navegáveis as etapas que já foram liberadas pelo workflow.
                    const enabled = taskStage >= 0 && taskStage <= executionStage;
                    return <button key={task.id} type="button"
                      className={`nav-step ${active ? "active" : ""} ${done ? "done" : ""}`}
                      onClick={() => enabled && onNavigate(taskStage)} disabled={!enabled}
                      title={task.description || task.name}>
                      <span className="step-number">{done ? "✓" : taskStage >= 0 ? taskStage + 1 : "·"}</span>
                      <span className="step-copy">
                        <strong>{task.name}</strong>
                        {/* <small>{task.description || "Workflow Task"}</small> */}
                      </span>
                    </button>;
                  })}
                </div>}
              </section>
            );
          })}
        </nav>

        <div className="sidebar-footer">
          <span className={`status-dot ${status === "error" ? "error" : ""}`} />
          <span>{status === "running" ? "Executando" : status === "error" ? "Erro na execução" : `${allTasks.length} etapas no workflow`}</span>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div>
            <span className="eyebrow">WORKSPACE </span>
            {/* <div className="topbar-title">{workflow.title || "Stage 1"}</div> */}
            <div className="topbar-title">Stage 1</div>
          </div>
          <span className="environment-tag"><span />Development environment</span>
        </header>
        <div className="page-content">{children}</div>
      </main>
    </div>
  );
}
