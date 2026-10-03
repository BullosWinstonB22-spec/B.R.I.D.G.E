import { useEffect, useState } from "react";
import { listEndpoint } from "../api";

interface Column {
  key: string;
  label: string;
  render?: (row: any) => any;
}

export default function CrudPage({
  title,
  endpoint,
  columns,
  emptyMsg,
}: {
  title: string;
  endpoint: string;
  columns: Column[];
  emptyMsg?: string;
}) {
  const [rows, setRows] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listEndpoint(endpoint)
      .then(setRows)
      .catch((e) => setError(e.message));
  }, [endpoint]);

  return (
    <div className="card">
      <h2>{title}</h2>
      {error && <p style={{ color: "#b00020" }}>{error}</p>}
      {!error && rows.length === 0 && <p style={{ color: "var(--muted)" }}>{emptyMsg ?? "No records yet."}</p>}
      {rows.length > 0 && (
        <div style={{ overflowX: "auto" }}>
          <table>
            <thead>
              <tr>{columns.map((c) => <th key={c.key}>{c.label}</th>)}</tr>
            </thead>
            <tbody>
              {rows.map((r, i) => (
                <tr key={r.id ?? i}>
                  {columns.map((c) => <td key={c.key}>{c.render ? c.render(r) : r[c.key] ?? "—"}</td>)}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
