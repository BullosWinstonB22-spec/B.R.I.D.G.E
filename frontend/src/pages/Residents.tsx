import { useEffect, useState } from "react";
import { residentsApi, Resident } from "../api";

export default function Residents() {
  const [rows, setRows] = useState<Resident[]>([]);
  const [q, setQ] = useState("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    residentsApi.list().then((d) => setRows(d.results ?? [])).catch((e) => setError(e.message));
  }, []);

  const filtered = rows.filter((r) =>
    `${r.resident_id} ${r.first_name} ${r.last_name} ${r.household_no} ${r.classification}`.toLowerCase().includes(q.toLowerCase())
  );

  return (
    <div className="card">
      <h2>Resident Directory ({filtered.length})</h2>
      <input placeholder="Search ID / name / household / classification…" value={q}
        onChange={(e) => setQ(e.target.value)} style={{ marginBottom: 12, width: "100%", maxWidth: 420 }} />
      {error && <p style={{ color: "#b00020" }}>{error}</p>}
      {!error && filtered.length === 0 && <p style={{ color: "var(--muted)" }}>No residents match.</p>}
      {filtered.length > 0 && (
        <div style={{ overflowX: "auto" }}>
          <table>
            <thead><tr><th>Resident ID</th><th>Name</th><th>Household</th><th>Gender</th><th>Classification</th><th>Voter</th><th>Status</th></tr></thead>
            <tbody>
              {filtered.map((r) => (
                <tr key={r.id}>
                  <td>{r.resident_id}</td>
                  <td>{r.first_name} {r.middle_name} {r.last_name}</td>
                  <td>{r.household_no}</td>
                  <td>{r.gender}</td>
                  <td><span className="badge">{r.classification}</span></td>
                  <td>{r.voter}</td>
                  <td><span className="badge">{r.resident_status}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
