import "dotenv/config";
import express from "express";
import cors from "cors";
import multer from "multer";
import axios from "axios";
import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = Number(process.env.PORT || 3001);
const FASTAPI_BASE_URL = (process.env.FASTAPI_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");
// analisar aqui a real parte do envio do processo 
const TASK1_PATH = process.env.FASTAPI_TASK1_PATH || "/r2rml-to-tr/metadata-extraction/";
const TASK2_PATH = process.env.FASTAPI_TASK2_PATH || "/r2rml-to-tr/entitiy-preservation-analysis/";
const TASK3_PATH = process.env.FASTAPI_TASK3_PATH || "/r2rml-to-tr/tr-gen/";
const TASK1_2_PATH = process.env.FASTAPI_TASK1_2_PATH || "/tr-to-after-trigger/trigger-planning/";
const UPLOAD_DIR = path.resolve(__dirname, process.env.UPLOAD_DIR || "../back/temp");
const MAX_FILE_SIZE = Number(process.env.UPLOAD_MAX_MB || 100) * 1024 * 1024;


fs.mkdirSync(UPLOAD_DIR, { recursive: true });

app.use(cors({
  origin: process.env.FRONTEND_ORIGIN
    ? process.env.FRONTEND_ORIGIN.split(",").map((v) => v.trim())
    : true,
}));
app.use(express.json({ limit: "20mb" }));
app.use(express.urlencoded({ extended: true }));

const storage = multer.diskStorage({
  destination: (_req, _file, cb) => cb(null, UPLOAD_DIR),
  filename: (_req, file, cb) => {
    // Mantém uma extensão útil, mas evita caminhos fornecidos pelo cliente.
    const original = path.basename(file.originalname).replace(/[^\w.\-() ]/g, "_");
    const safeName = `${Date.now()}-${Math.random().toString(16).slice(2, 8)}-${original}`;
    cb(null, original);
  },
});

const upload = multer({
  storage,
  limits: { fileSize: MAX_FILE_SIZE, files: 2 },
});

function normalizeTaskResult(data) {
  if (data === null || data === undefined) return { output: null, raw: data };
  if (typeof data === "string") return { output: data, raw: data };
  if (typeof data !== "object") return { output: data, raw: data };

  const output =
    data.result ??
    data.output ??
    data.data ??
    data.content ??
    data.rows ??
    data.filename ??
    data.file ??
    data;

  return {
    output,
    raw: data,
    filename: data.filename || data.file || data.output_file || null,
    contentType: data.content_type || data.contentType || null,
    message: data.message || null,
  };
}

function errorMessage(error) {
  const status = error.response?.status;
  const detail = error.response?.data?.detail || error.response?.data?.message;
  return {
    status: status || 502,
    message: detail || error.message || "Falha ao comunicar com o backend.",
    backendResponse: error.response?.data ?? null,
  };
}

// Definição declarativa consumida pela sidebar React. Para adicionar um agente
// ou task, inclua um objeto nesta estrutura; cada task precisa de id único e stage.
// stage deve corresponder a uma tela/handler que o frontend já implemente.
app.get("/api/workflow/definition", (_req, res) => {
  res.json({
    success: true,
    title: "Workflow Transformation",
    agents: [
      // CONFIGURAÇÃO DA SIDEBAR:
      // Agentes são grupos; cada agente pode declarar quantas tasks precisar.
      // id da task deve ser único. stage conecta a task à tela existente no React.

      {
        id: "Transfomation Rule agent",
        name: "Transformation Rule Generation",
        description: "Preparação e análise das regras de transformação",
        tasks: [
          { 
          id: "upload", 
          name: "Enviar arquivos", 
          description: "Schema e mapeamento", 
          stage: 0, kind: "input", 
          screen: { type: "upload" } 
          },
          {
            id: "task-1",
            name: "Metadata Extraction and Normalization",
            description: "Extração e normalização dos metadados",
            stage: 1,
            execution: { endpoint: "/api/workflow/task-1" },
            screen: { type: "result-review" }
          },
          {
            id: "task-2",
            name: "Entity Preservation Analysis",
            description: "Análise e preservação das entidades",
            stage: 2,
            execution: { endpoint: "/api/workflow/task-2", inputFrom: ["task-1"] },
            screen: { type: "result-review" }
          },
          {
            id: "task-3",
            name: "Transformation Rule Generation",
            description: "Geração das regras a partir do resultado anterior",
            stage: 3,
            execution: { endpoint: "/api/workflow/task-3", inputFrom: ["task-2"] },
            screen: { type: "result-review" }
          }
        ]
      },
      {
        id: "Trigger agent",
        name: "AFTER Trigger Generation",
        description: "Geração de regras de transformação e mapeamento",
        tasks: [
          {
            id: "task-1_2",
            name: "Trigger Planning",
            description: "Geração das regras a partir do resultado anterior",
            stage: 4,
            execution: { endpoint: "/api/workflow/task-4", inputFrom: ["task-3"] },
            screen: { type: "result-review" }
          }
        ]
      }
    ],
  });
});

app.get("/api/health", (_req, res) => {
  res.json({
    ok: true,
    service: "dynamic-workflow-server",
    fastapiBaseUrl: FASTAPI_BASE_URL,
    task1Path: TASK1_PATH,
    task2Configured: Boolean(TASK2_PATH && !TASK2_PATH.includes("replace-with-your-task-2-endpoint")),
    uploadDirectory: UPLOAD_DIR,
  });
});

// TASK 1: os dois uploads são usados exclusivamente nesta primeira execução.
app.post("/api/workflow/task-1", upload.fields([
  { name: "file1", maxCount: 1 },
  { name: "file2", maxCount: 1 },
]), async (req, res) => {
  const file1 = req.files?.file1?.[0];
  const file2 = req.files?.file2?.[0];

  if (!file1 || !file2) {
    return res.status(400).json({
      success: false,
      message: "Envie os dois arquivos: file1 e file2.",
    });
  }

  try {
    // Preserva o contrato conhecido: FastAPI recebe os nomes via query params.
    // Os arquivos ficam no diretório compartilhado configurado em UPLOAD_DIR.
    const response = await axios.post(
      `${FASTAPI_BASE_URL}${TASK1_PATH}`,
      null,
      {
        params: {
          file1: file1.filename,
          file2: file2.filename,
        },
        timeout: 20 * 60 * 1000,
      }
    );

    return res.json({
      success: true,
      taskId: "task-1",
      status: "awaiting_review",
      inputFiles: {
        file1: { originalName: file1.originalname, storedName: file1.filename },
        file2: { originalName: file2.originalname, storedName: file2.filename },
      },
      result: normalizeTaskResult(response.data),
    });
  } catch (error) {
    const e = errorMessage(error);
    return res.status(e.status).json({
      success: false,
      message: e.message,
      backendResponse: e.backendResponse,
    });
  }
});

// HITL: valida o resultado e recebe feedback. A revisão LLM real só deve ser
// conectada quando o endpoint real de revisão do FastAPI estiver definido.
app.post("/api/workflow/review", async (req, res) => {
  const { task1Result, feedback, action } = req.body || {};

  if (!task1Result) {
    return res.status(400).json({
      success: false,
      message: "task1Result é obrigatório.",
    });
  }

  if (action === "approve") {
    return res.json({
      success: true,
      status: "approved",
      task1Result,
      message: "Resultado da Task 1 aprovado para a próxima etapa.",
    });
  }

  if (!String(feedback || "").trim()) {
    return res.status(400).json({
      success: false,
      message: "Informe o feedback antes de solicitar uma revisão.",
    });
  }

  // Sem o endpoint real de revisão, não afirmamos que o LLM modificou o resultado.
  return res.json({
    success: true,
    status: "feedback_received",
    task1Result,
    feedback: String(feedback).trim(),
    requiresBackendReviewIntegration: true,
    message: "Feedback recebido. Conecte esta ação à rota real de revisão do FastAPI para regenerar o resultado.",
  });
});

// TASK 2: envia apenas a saída da Task 1. Nunca reenvia file1/file2.
app.post("/api/workflow/task-2", async (req, res) => {
  const { task1Result } = req.body || {};

  if (!task1Result) {
    return res.status(400).json({
      success: false,
      message: "A saída aprovada da Task 1 é obrigatória.",
    });
  }

  if (!TASK2_PATH || TASK2_PATH.includes("replace-with-your-task-2-endpoint")) {
    return res.status(501).json({
      success: false,
      message: "A rota da Task 2 ainda não foi configurada. Defina FASTAPI_TASK2_PATH no server/.env.",
      receivedOnlyTask1Output: true,
    });
  }

  try {
    // Importante: payload contém exclusivamente task1Result.
    const response = await axios.post(
      `${FASTAPI_BASE_URL}${TASK2_PATH}`,
      { task1Result },
      { timeout: 20 * 60 * 1000 }
    );

    return res.json({
      success: true,
      taskId: "task-2",
      status: "completed",
      result: normalizeTaskResult(response.data),
    });
  } catch (error) {
    const e = errorMessage(error);
    return res.status(e.status).json({
      success: false,
      message: e.message,
      backendResponse: e.backendResponse,
    });
  }
});

// TASK 3: recebe somente a saída aprovada da Task 2.
app.post("/api/workflow/task-3", async (req, res) => {
  const { task2Result } = req.body || {};
  if (!task2Result) return res.status(400).json({ success: false, message: "A saída aprovada da Task 2 é obrigatória." });
  if (!TASK3_PATH) return res.status(501).json({ success: false, message: "A rota da Task 3 não foi configurada." });
  try {
    const response = await axios.post(`${FASTAPI_BASE_URL}${TASK3_PATH}`, { task2Result }, { timeout: 20 * 60 * 1000 });
    return res.json({ success: true, taskId: "task-3", status: "completed", result: normalizeTaskResult(response.data) });
  } catch (error) {
    const e = errorMessage(error);
    return res.status(e.status).json({ success: false, message: e.message, backendResponse: e.backendResponse });
  }
});

//TASK 1_2
app.post("/api/workflow/task-1_2", async (req, res) => {
  const { task3Result } = req.body || {};
  if (!task3Result) return res.status(400).json({ success: false, message: "A saída aprovada da Task 3 é obrigatória." });
  if (!TASK1_2_PATH) return res.status(501).json({ success: false, message: "A rota da Task 1_2 não foi configurada." });
  try {
    const response = await axios.post(`${FASTAPI_BASE_URL}${TASK3_PATH}`, { task2Result }, { timeout: 20 * 60 * 1000 });
    return res.json({ success: true, taskId: "task-1_2", status: "completed", result: normalizeTaskResult(response.data) });
  } catch (error) {
    const e = errorMessage(error);
    return res.status(e.status).json({ success: false, message: e.message, backendResponse: e.backendResponse });
  }
});

// Servir somente arquivos pelo nome armazenado no diretório de upload configurado.
app.get("/api/files/:filename", (req, res) => {
  const filename = path.basename(req.params.filename);
  const target = path.resolve(UPLOAD_DIR, filename);

  if (!target.startsWith(`${UPLOAD_DIR}${path.sep}`) && target !== UPLOAD_DIR) {
    return res.status(400).json({ message: "Nome de arquivo inválido." });
  }

  if (!fs.existsSync(target) || !fs.statSync(target).isFile()) {
    return res.status(404).json({ message: "Arquivo não encontrado." });
  }

  return res.sendFile(target);
});

app.listen(PORT, () => {
  console.log(`Node workflow server: http://localhost:${PORT}`);
  console.log(`Upload directory: ${UPLOAD_DIR}`);
});
