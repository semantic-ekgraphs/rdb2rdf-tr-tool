// src/services/workflowApi.js
const FASTAPI_URL = import.meta.env.VITE_FASTAPI_URL || "http://127.0.0.1:8000";

export async function executeTask1(file1, file2) {
  const formData = new FormData();
  formData.append("file1", file1);
  formData.append("file2", file2);

  const response = await fetch(`${FASTAPI_URL}/r2rml-to-tr/metadata-extraction/`, {
    method: "POST",
    body: formData, // Sem Content-Type manual (o navegador define com boundary)
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Erro ao processar Task 1");
  }

  return response.json();
}

export async function executeTask2(task1Result) {
  const response = await fetch(`${FASTAPI_URL}/r2rml-to-tr/entitiy-preservation-analysis/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task1Result }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Erro ao processar Task 2");
  }

  return response.json();
}

export async function executeTask3(task2Result) {
  const response = await fetch(`${FASTAPI_URL}/r2rml-to-tr/tr-gen/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task2Result }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Erro ao processar Task 3");
  }

  return response.json();
}

export async function executeTask1_2(task3Result) {
  const response = await fetch(`${FASTAPI_URL}/tr-to-after-trigger/trigger-planning/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task3Result }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Erro ao processar Task 1_2");
  }

  return response.json();
}

export async function reviewTask1(task1Result, feedback, action) {
  // Caso queira tratar a revisão localmente ou criar uma rota no FastAPI
  return {
    status: action === "approve" ? "approved" : "feedback_received",
    task1Result,
    message: action === "approve" ? "Aprovado com sucesso" : "Feedback recebido",
  };
}

export async function getWorkflowDefinition() {
  // Pode retornar a constante DEFAULT_WORKFLOW diretamente sem passar por requisição
  return null;
}