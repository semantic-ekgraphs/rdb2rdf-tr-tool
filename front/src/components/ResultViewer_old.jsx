import { useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";


function asText(value) {
  if (typeof value === "string") return value;
  if (value === null || value === undefined) return "";
  return JSON.stringify(value, null, 2);
}

function findRows(value) {
  if (Array.isArray(value)) return value;
  if (value && typeof value === "object") {
    if (Array.isArray(value.rows)) return value.rows;
    if (Array.isArray(value.data)) return value.data;
    if (Array.isArray(value.output)) return value.output;
  }
  return null;
}

function CsvTable({ rows }) {
  const [filter, setFilter] = useState("");
  const columns = useMemo(
    () => [...new Set(rows.flatMap((row) => Object.keys(row || {})))],
    [rows]
  );
  const filtered = rows.filter((row) =>
    JSON.stringify(row).toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <div className="table-tools">
        <span className="muted">{filtered.length} registro(s)</span>
        <input
          className="search-input"
          value={filter}
          onChange={(event) => setFilter(event.target.value)}
          placeholder="Buscar nos resultados..."
          aria-label="Buscar nos resultados"
        />
      </div>
      <div className="table-wrap">
        <table className="data-table">
          <thead><tr>{columns.map((column) => <th key={column}>{column}</th>)}</tr></thead>
          <tbody>
            {filtered.slice(0, 500).map((row, index) => (
              <tr key={index}>
                {columns.map((column) => (
                  <td key={column}>{String(row?.[column] ?? "—")}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {filtered.length > 500 && <p className="muted">Exibindo os primeiros 500 registros. Use a exportação para consultar o arquivo completo.</p>}
    </div>
  );
}
function extractOutput(result) {
  let output = result?.output ?? result?.raw ?? result;

  // Se o backend retornou um JSON como string, tenta interpretá-lo.
  if (typeof output === "string") {
    try {
      const parsed = JSON.parse(output);

      if (parsed && typeof parsed === "object") {
        output = parsed;
      }
    } catch {
      // A string não é JSON: mantém o conteúdo original.
    }
  }

  // Se a saída for um objeto que contém raw, prioriza esse campo.
  if (output && typeof output === "object" && !Array.isArray(output)) {
    if (typeof output.raw === "string") {
      return output.raw;
    }

    if (Array.isArray(output.tasks_output)) {
      return output.tasks_output
        .map((task) => task.raw ?? JSON.stringify(task, null, 2))
        .join("\n\n---\n\n");
    }
  }

  return typeof output === "string"
    ? output
    : JSON.stringify(output, null, 2);
}

function parsePipeTable(text) {
  if (typeof text !== "string") return null;

  const lines = text
    .replace(/\\n/g, "\n")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  if (lines.length < 2 || !lines[0].includes("|")) {
    return null;
  }

  const parseRow = (line) =>
    line
      .replace(/^\|/, "")
      .replace(/\|$/, "")
      .split("|")
      .map((cell) => cell.trim());

  const headers = parseRow(lines[0]);

  // Remove a linha separadora Markdown, se existir.
  const dataLines = lines.slice(1).filter(
    (line) => !/^[\s|:-]+$/.test(line)
  );

  const rows = dataLines.map(parseRow);

  return { headers, rows };
}

function PipeTable({ table }) {
  return (
    <div className="table-output">
      <table>
        <thead>
          <tr>
            {table.headers.map((header, index) => (
              <th key={index}>{header}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {table.rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {table.headers.map((_, colIndex) => (
                <td key={colIndex}>
                  {row[colIndex] ?? ""}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function splitTextAndMarkdownTable(content) {
  if (typeof content !== "string") {
    return { text: "", table: "" };
  }

  const lines = content.split(/\r?\n/);

  const separatorIndex = lines.findIndex((line, index) => {
    const nextLine = lines[index + 1] || "";

    return (
      line.includes("|") &&
      nextLine.includes("|") &&
      /^\s*\|?\s*:?-{3,}/.test(nextLine)
    );
  });

  if (separatorIndex === -1) {
    return { text: content.trim(), table: "" };
  }

  return {
    text: lines.slice(0, separatorIndex).join("\n").trim(),
    table: lines.slice(separatorIndex).join("\n").trim(),
  };
}

export default function ResultViewer({ result, title = "Resultado da task" }) {
  const [expanded, setExpanded] = useState(false);

  if (result === null || result === undefined) {
    return <div className="empty-result">O resultado será exibido aqui após a execução.</div>;
  }

  const output = result.output ?? result.raw ?? result;
  const rows = findRows(output);
  const text = extractOutput(result);
  const lower = `${result.filename || ""} ${result.contentType || ""}`.toLowerCase();
  const looksCsv = lower.includes(".csv") || lower.includes("csv");
  const looksMarkdown =
  lower.includes(".md") ||
  lower.includes("markdown") ||
  lower.includes("text/markdown");
  const pipeTable = parsePipeTable(text);
  
  return (
    <section className="result-panel">
      <div className="result-panel-header">
        <div>
          <span className="eyebrow">SAÍDA</span>
          <h3>{title}</h3>
        </div>
        <div className="result-actions">
          <button type="button" className="button button-light button-small" onClick={() => setExpanded((v) => !v)}>
            {expanded ? "Recolher" : "Expandir"}
          </button>
          <button type="button" className="button button-light button-small" onClick={() => navigator.clipboard?.writeText(text)}>
            Copiar
          </button>
          <button
            type="button"
            className="button button-light button-small"
            onClick={() => {
              const blob = new Blob([text], {
                type: looksMarkdown ? "text/markdown;charset=utf-8" : "text/plain;charset=utf-8"
              });
              const url = URL.createObjectURL(blob);
              const a = document.createElement("a");
              a.href = url;
              a.download = result.filename || "task-result.txt";
              a.click();
              URL.revokeObjectURL(url);
            }}
          >
            Exportar
          </button>
        </div>
      </div>

      {pipeTable ? (
        <PipeTable table={pipeTable} />
      ) : looksMarkdown ? (
        <article className={"markdown-output"}>
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{text}</ReactMarkdown>
        </article>
      ) : (
        <pre className="code-output">{text}</pre>
      )}
      
    </section>
  );
}
