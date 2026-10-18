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

  // Localiza o cabeçalho da tabela em qualquer ponto da resposta,
  // mesmo que o agente tenha escrito uma explicação antes dela.
  const lines = text.replace(/\\n/g, "\n").split(/\r?\n/);
  const isSeparator = (line) =>
    /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$/.test(line);

  const headerIndex = lines.findIndex((line, index) =>
    line.includes("|") && isSeparator(lines[index + 1] || "")
  );

  if (headerIndex < 0) return null;

  const parseRow = (line) =>
    line.trim()
      .replace(/^\|/, "")
      .replace(/\|$/, "")
      .split("|")
      .map((cell) => cell.trim());

  const headers = parseRow(lines[headerIndex]);
  const rows = [];

  for (let index = headerIndex + 2; index < lines.length; index += 1) {
    const line = lines[index].trim();
    // A tabela termina quando começa outro parágrafo sem pipes.
    if (!line) {
      if (rows.length) break;
      continue;
    }
    if (!line.includes("|")) break;
    if (isSeparator(line)) continue;
    rows.push(parseRow(line));
  }

  if (!headers.length) return null;
  return { headers, rows, startLine: headerIndex, endLine: headerIndex + 1 + rows.length + 1 };
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

function splitTextAndMarkdownTable(content, parsedTable) {
  if (typeof content !== "string" || !parsedTable) {
    return { text: content || "", table: "" };
  }

  const lines = content.replace(/\\n/g, "\n").split(/\r?\n/);
  const before = lines.slice(0, parsedTable.startLine).join("\n").trim();
  const tableLines = lines.slice(parsedTable.startLine, parsedTable.endLine);
  const table = tableLines.join("\n").trim();

  return { text: before, table };
}

export default function ResultViewer({ result, title = "Resultado da task" }) {
  const [expanded, setExpanded] = useState(false);

  if (result === null || result === undefined) {
    return <div className="empty-result">O resultado será exibido aqui após a execução.</div>;
  }

  const output = result.output ?? result.raw ?? result;
  const rows = findRows(output);
  // Alguns modelos concatenam o texto introdutório e a tabela com esse marcador.
  // Na apresentação, tratamos o marcador como uma quebra de linha antes da tabela.
  const text = extractOutput(result).replace(/<channel>\s*\|>/gi, "\n").trim();
  const lower = `${result.filename || ""} ${result.contentType || ""}`.toLowerCase();
  const looksCsv = lower.includes(".csv") || lower.includes("csv");
  const looksMarkdown =
  lower.includes(".md") ||
  lower.includes("markdown") ||
  lower.includes("text/markdown");
  const pipeTable = parsePipeTable(text);
  const { text: introductoryText } = splitTextAndMarkdownTable(text, pipeTable);
  
  return (
    <section className="result-panel">
      <div className="result-panel-header">
        <div>
          {/* <span className="eyebrow">SAÍDA</span> */}
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
        <>
          {introductoryText && (
            <article className="markdown-output result-intro">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{introductoryText}</ReactMarkdown>
            </article>
          )}
          <PipeTable table={pipeTable} />
        </>
      ) : looksMarkdown ? (
        <article className="markdown-output">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{text}</ReactMarkdown>
        </article>
      ) : (
        <pre className="code-output">{text}</pre>
      )}
      
    </section>
  );
}
