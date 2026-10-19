/**
 * Definição inicial do workflow usada como fallback quando o backend não fornece
 * uma configuração. Para adicionar agentes/tasks sem reescrever a sidebar,
 * retorne o mesmo formato em GET /api/workflow/definition.
 *
 * stage é o identificador da tela/etapa já implementada no App.jsx.
 * Tasks sem stage implementado podem aparecer na sidebar, mas ficam bloqueadas
 * até que o frontend registre um componente/handler para elas.
 */
export const TASK_ORDER = [
  "task1",
  "task2",
  "task3",
  "task1_2",
];

export const DEFAULT_WORKFLOW = {
  title: "Workflow Transformation",
  agents: [
    // Etapa de entrada, mantida no fallback para que a tela de upload continue
    // acessível mesmo quando a definição do servidor não puder ser carregada.
    // Para adicionar outra task a este agente, inclua-a em tasks e use um stage
    // que tenha uma tela/handler implementado em App.jsx.
    {
      id: "Transformation Rule agent",
      name: "Transformation Rule Generation",
      // description: "Preparation and analysis of transformation rules",
      description: "",
      tasks: [
        {
          id: "upload", 
          name: "Send Files",
          // name: "Enviar arquivos", 
          // description: "Schema & mappings....", 
          // description: "Schema e mapeamento", 
          stage: 0, kind: "input", 
          screen: { type: "upload" } 
        },
        {
          id: "task-1",
          name: "Metadata Extraction and Normalization",
          description: "R2RML & schema metadata",
          // description: "Extração e normalização dos metadados",
          stage: 1,
          execution: { endpoint: "/api/workflow/task-1" },
          screen: { type: "result-review" }
        },
        {
          id: "task-2",
          name: "Entity Preservation Analysis",
          description: "Analysis and preservation of entities",
          // description: "Análise e preservação das entidades",
          stage: 2,
          execution: { endpoint: "/api/workflow/task-2", inputFrom: ["task-1"] },
          screen: { type: "result-review" }
        },
        {
          id: "task-3",
          name: "Transformation Rule Generation",
          description: "Generating rules from the previous result",
          // description: "Geração das regras a partir do resultado anterior",
          stage: 3,
          execution: { endpoint: "/api/workflow/task-3", inputFrom: ["task-2"] },
          screen: { type: "result-review" }
        }
      ]
    },
    // AGENTE 2: responsável pela geração/transformação do mapeamento R2RML.
    // É independente do primeiro agente na navegação, mas pode consumir a saída
    // da Task 2 conforme definido no backend.
    {
      id: "Trigger-agent",
      name: "AFTER Trigger Generation",
      description: "Geração de regras de transformação e mapeamento",
      tasks: [
        {
          id: "task-4",
          name: "Trigger Planning",
          description: "Geração das regras a partir do resultado anterior",
          stage: 4,
          execution: { endpoint: "/api/workflow/task-4", inputFrom: ["task-3"] },
          screen: { type: "result-review" }
        }
      ]
    }
  ],
};
