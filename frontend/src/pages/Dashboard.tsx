import { useEffect, useState } from "react";
import { residentsApi } from "../api";

const LABELS: Record<string, string> = {
  residents: "Active Residents",
  households: "Households",
  pending_requests: "Pending Requests",
  open_tasks: "Open Tasks",
  unread_notifications: "Unread Notifications",
  officials: "Barangay Officials",
  programs_ongoing: "Ongoing Programs",
  activity_logs: "Activity Log Entries",
};

export default function Dashboard() {
  const [stats, setStats] = useState<Record<string, number> | null>(null);
  useEffect(() => { residentsApi.dashboard().then(setStats).catch(() => setStats({})); }, []);

  return (
    <>
      <div className="card">
        <h2>Command Center Dashboard</h2>
        <p style={{ color: "var(--muted)", fontSize: 14 }}>Live data migrated from your old BMS database.</p>
      </div>
      <div className="grid">
        {(stats ? Object.entries(stats) : []).map(([k, v]) => (
          <div className="stat" key={k}>
            <div className="num">{v}</div>
            <div className="lbl">{LABELS[k] ?? k}</div>
          </div>
        ))}
      </div>
    </>
  );
}
