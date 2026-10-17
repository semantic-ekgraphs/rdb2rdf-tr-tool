import { useCallback, useEffect, useState } from "react";
import WorkflowLayout from "./components/WorkflowLayout";
import UploadPage from "./pages/UploadPage";
import Task1Page from "./pages/Task1Page";
import Task2Page from "./pages/Task2Page";
import Task3Page from "./pages/Task3Page";
import Task1_2Page from "./pages/Task1_2Page";
import {
  executeTask1,
  executeTask2,
  executeTask3,
  executeTask1_2,
  reviewTask1,
  getWorkflowDefinition,
} from "./services/workflowApi";
import { DEFAULT_WORKFLOW, TASK_ORDER } from "./services/workflowDefinition";

function normalizeResult(response) {
  const result = response?.result ?? response;

  if (
    result &&
    typeof result === "object" &&
    ("output" in result || "raw" in result || "filename" in result)
  ) {
    return result;
  }

  return { output: result, raw: response };
}





export default function App() {
  // 0 = upload, 1 = Task 1, 2 = Task 2, 3 = Task 3, 4 = próxima etapa/agente
  // stage representa o progresso real do workflow (execução/aprovação).
  const [stage, setStage] = useState(0);
  // viewStage representa somente a task/página que o usuário está visualizando.
  // Navegar pela sidebar altera viewStage, nunca stage.
  const [viewStage, setViewStage] = useState(0);
  // A configuração é carregada do backend; o fallback mantém o front utilizável
  // durante desenvolvimento/offline. Agentes/tasks novos são renderizados pela sidebar.
  const [workflow, setWorkflow] = useState(DEFAULT_WORKFLOW);

  useEffect(() => {
    let mounted = true;
    getWorkflowDefinition()
      .then((definition) => { if (mounted && definition?.agents) setWorkflow(definition); })
      .catch(() => { /* API indisponível: usa DEFAULT_WORKFLOW sem bloquear a interface. */ });
    return () => { mounted = false; };
  }, []);
  const [status, setStatus] = useState("idle");
  const [busy, setBusy] = useState(false);
  const [reviewBusy, setReviewBusy] = useState(false);

  const [task1Result, setTask1Result] = useState(null);
  const [approvedTask1Result, setApprovedTask1Result] = useState(null);
  const [task2Result, setTask2Result] = useState(null);
  const [approvedTask2Result, setApprovedTask2Result] = useState(null);
  const [task3Result, setTask3Result] = useState(null);
  //teste stage 2 task 1
  const [approvedTask3Result, setApprovedTask3Result] = useState(null);
  const [task1_2Result, setTask1_2Result] = useState(null);

  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const clearMessages = () => {
    setError("");
    setNotice("");
  };
  //reset status
  const resetAfterTask = useCallback((taskId) => {
    const taskIndex = TASK_ORDER.indexOf(taskId);

    if (taskIndex === -1) {
      console.warn(`Task não encontrada: ${taskId}`);
      return;
    }

    // Cada task declara como limpar seu próprio resultado e aprovação.
    const resetters = {
      task1: () => {
        setTask1Result(null);
        setApprovedTask1Result(null);
      },
      task2: () => {
        setTask2Result(null);
        setApprovedTask2Result(null);
      },
      task3: () => {
        setTask3Result(null);
        setApprovedTask3Result(null);
      },
      task1_2: () => {
        setTask1_2Result(null);
      },
    };

    // Limpa somente as etapas posteriores à task informada.
    TASK_ORDER.slice(taskIndex + 1).forEach((id) => {
      resetters[id]?.();
    });

    setError("");
    setNotice("");
    setStatus("idle");
  }, []);

  const runTask1 = useCallback(async (file1, file2) => {
    setBusy(true);
    setStatus("running");
    clearMessages();
    setTask1Result(null);
    setApprovedTask1Result(null);
    setTask2Result(null);
    setApprovedTask2Result(null);
    setTask3Result(null);
    //teste stage 2 task 1
    setApprovedTask3Result(null);
    setTask1_2Result(null);

    try {
      const response = await executeTask1(file1, file2);
      setTask1Result(normalizeResult(response));
      setStatus("success");
      setStage(1);
      setViewStage(1);
      setNotice("Task 1 completed. Review the output before continuing.");
    } catch (e) {
      setStatus("error");
      setError(e.message || "It was not possible to execute Task 1.");
    } finally {
      setBusy(false);
    }
  }, []);

  const sendFeedback = useCallback(async (feedback) => {
    if (!task1Result) return;

    setReviewBusy(true);
    clearMessages();

    try {
      const response = await reviewTask1(task1Result, feedback, "revise");

      // Só substitui a saída se o backend retornar um resultado revisado.
      if (response?.result) {
        setTask1Result(normalizeResult(response));
      }

      setNotice(
        response?.requiresBackendReviewIntegration
          ? "Feedback received, but the revision still needs to be connected to the actual backend route. The current output has been preserved."
          : response?.message || "Feedback received."
      );
    } catch (e) {
      setError(e.message || "Unable to send feedback.");
    } finally {
      setReviewBusy(false);
    }
  }, [task1Result]);

  const approveTask1 = useCallback(async () => {
    if (!task1Result) return;
    //teste limpeza
    resetAfterTask("task1");
    setReviewBusy(true);
    clearMessages();

    try {
      const response = await reviewTask1(task1Result, "", "approve");
      const approved = response?.task1Result || task1Result;

      setApprovedTask1Result(approved);
      setStage(2);
      setViewStage(2);
      setNotice("Task 1 approved. Begin Task 2 when you are ready.");
    } catch (e) {
      setError(e.message || "It was not possible to confirm the result of Task 1.");
    } finally {
      setReviewBusy(false);
    }
  }, [task1Result,resetAfterTask]);

  const runTask2 = useCallback(async () => {
    if (!approvedTask1Result) {
      setError("First, approve the result of Task 1.");
      return;
    }

    // Invalida as etapas posteriores à Task 2.
    resetAfterTask("task2");

    setBusy(true);
    setStatus("running");
    clearMessages();

    try {
      const response = await executeTask2(approvedTask1Result);
      const result = normalizeResult(response);

      setTask2Result(result);
      setApprovedTask2Result(null);
      //setTask3Result(null);
      setStatus("success");
      setNotice("Task 2 completed. Check the output before releasing Task 3.");
    } catch (e) {
      setStatus("error");
      setError(e.message || "It was not possible to execute Task 2..");
    } finally {
      setBusy(false);
    }
  }, [approvedTask1Result,resetAfterTask]);

  // Aprovação explícita da Task 2 antes de encaminhar seu resultado à Task 3.
  const approveTask2AndContinue = useCallback(() => {
    if (!task2Result) {
      setError("Complete Task 2 before continuing.");
      return;
    }

    setApprovedTask2Result(task2Result);
    clearMessages();
    setStage(3);
    setViewStage(3);
    setNotice("Task 2 confirmed. You may begin Task 3.");
  }, [task2Result]);

  const runTask3 = useCallback(async () => {
    if (!approvedTask2Result) {
      setError("First, confirm the result of Task 2.");
      return;
    }
    //reset status
    resetAfterTask("task3");

    setBusy(true);
    setStatus("running");
    clearMessages();

    try {
      const response = await executeTask3(approvedTask2Result);
      setTask3Result(normalizeResult(response));
      setStatus("success");
      setNotice("Task 3 completed.");
    } catch (e) {
      setStatus("error");
      setError(e.message || "It was not possible to execute Task 3.");
    } finally {
      setBusy(false);
    }
  }, [approvedTask2Result , resetAfterTask]);


  // teste stage 2 task 1
  const approveTask3AndContinue = useCallback(() => {
    if (!task2Result) {
      setError("Complete Task 2 before continuing.");
      return;
    }

    setApprovedTask3Result(task3Result);
    clearMessages();
    setStage(4);
    setViewStage(4);
    setNotice("Task 3 confirmed. You can start Task 1_2.");
  }, [task2Result]);

  
  const runTask1_2 = useCallback(async () => {
    if (!approvedTask2Result) {
      setError("First, confirm the result of Task 3.");
      return;
    }

    setBusy(true);
    setStatus("running");
    clearMessages();

    try {
      const response = await executeTask1_2(approvedTask3Result);
      setTask1_2Result(normalizeResult(response));
      setStatus("success");
      setNotice("Task 1_2 completed.");
    } catch (e) {
      setStatus("error");
      setError(e.message || "It was not possible to execute Task 1_2.");
    } finally {
      setBusy(false);
    }
  }, [approvedTask3Result]);

  const navigate = (next) => {
    // Navegação é apenas visual: não altera o progresso nem reexecuta tasks.
    // A sidebar pode abrir uma task anterior ou posterior sem mudar stage.
    if (!busy && !reviewBusy) {
      setViewStage(next);
      clearMessages();
    }
  };

  return (
    <WorkflowLayout stage={viewStage} executionStage={stage} onNavigate={navigate} status={status} workflow={workflow}>
      {viewStage === 0 && (
        <UploadPage busy={busy} onRunTask1={runTask1} />
      )}

      {viewStage === 1 && (
        <Task1Page
          result={task1Result}
          busy={busy}
          reviewBusy={reviewBusy}
          notice={notice}
          error={error}
          onFeedback={sendFeedback}
          onApprove={approveTask1}
          onBack={() => navigate(0)}
        />
      )}

      {viewStage === 2 && (
        <Task2Page
          result={task2Result}
          busy={busy}
          error={error}
          notice={notice}
          onRun={runTask2}
          onBack={() => navigate(1)}
          task1Approved={Boolean(approvedTask1Result)}
        />
      )}
      {viewStage === 2 && task2Result && !busy && (
        <button type="button" onClick={approveTask2AndContinue}>
          Comfirm task 2 and go task 3
        </button>
      )}

      {viewStage === 3 && (
        <Task3Page
          result={task3Result}
          busy={busy}
          error={error}
          notice={notice}
          onRun={runTask3}
          onBack={() => navigate(2)}
          task2Approved={Boolean(approvedTask2Result)}
        />
      )}
      {viewStage === 3 && task3Result && !busy && (
        <button type="button" onClick={approveTask3AndContinue}>
          Next to After Trigger Generation Agent
        </button>
      )}
      
      {viewStage === 4 && (
        <Task3Page
          result={task1_2Result}
          busy={busy}
          error={error}
          notice={notice}
          onRun={runTask1_2}
          onBack={() => navigate(3)}
          task2Approved={Boolean(approvedTask3Result)}
        />
      )}
      {viewStage === 4 && task1_2Result && !busy && (
        <button type="button" onClick={() => { setStage(5); setViewStage(5); }}>
          Next Agent/Task
        </button>
      )}
      
    </WorkflowLayout>
  );
}
