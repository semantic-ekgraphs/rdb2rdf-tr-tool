const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000" || "http://localhost:3001" ;

async function readResponse(response) {
  const data = await response.json().catch(() => ({}));
  if (!response.ok || data.success === false) {
    throw new Error(data.message || `Erro HTTP ${response.status}`);
  }
  return data;
}

export async function executeTask1(file1, file2) {
  console.log('call task 1')
  const form = new FormData();
  form.append("file1", file1);
  form.append("file2", file2);
  
  const response = await fetch(`${API_BASE}/r2rml-to-tr/metadata-extraction/`, {
  // const response = await fetch(`${API_BASE}/api/workflow/task-1`, {
    method: "POST",
    body: form,
  });
  return readResponse(response);
}

export async function reviewTask1(task1Result, feedback, action = "revise") {
  const response = await fetch(`${API_BASE}/api/workflow/review`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task1Result, feedback, action }),
  });
  return readResponse(response);
}

export async function executeTask2(task1Result) {
  const response = await fetch(`${API_BASE}/api/workflow/task-2`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    // Apenas a saída da Task 1 é enviada à Task 2.
    body: JSON.stringify({ task1Result }),
  });
  return readResponse(response);
}

export async function executeTask3(task2Result) {
  const response = await fetch(`${API_BASE}/api/workflow/task-3`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    // A Task 3 recebe exclusivamente a saída aprovada da Task 2.
    body: JSON.stringify({ task2Result }),
  });
  return readResponse(response);
}
// teste tela 1 do stage 2
export async function executeTask1_2(task3Result) {
  const response = await fetch(`${API_BASE}/api/workflow/task-1_2`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    // A Task 1_2 recebe exclusivamente a saída aprovada da Task 3. ve ainda a regra no doc
    body: JSON.stringify({ task3Result }),
  });
  return readResponse(response);
}

export async function getHealth() {
  const response = await fetch(`${API_BASE}/api/health`);
  return readResponse(response);
}


// Obtém a definição dos agentes/tasks. A sidebar consome esta estrutura sem
// precisar conhecer individualmente cada agente; o fallback fica no App.jsx.
export async function getWorkflowDefinition() {
  const response = await fetch(`${API_BASE}/api/workflow/definition`);
  return readResponse(response);
}
