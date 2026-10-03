import { Routes, Route, Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Residents from "./pages/Residents";
import CrudPage from "./pages/CrudPage";
import { authApi } from "./api";

export default function App() {
  const [authed, setAuthed] = useState(!!localStorage.getItem("bridge_token"));
  const nav = useNavigate();
  const logout = () => { authApi.logout(); setAuthed(false); nav("/"); };

  return (
    <>
      <nav className="nav">
        <Link to="/" style={{ color: "#fff", textDecoration: "none" }}><h1>B.R.I.D.G.E</h1></Link>
        <span className="nav-sub">Baranggay Resident Information & Digital Government Environment</span>
        <span style={{ flex: 1 }} />
        <Link to="/">Public Site</Link>
        {authed ? (
          <>
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/residents">Residents</Link>
            <Link to="/requests">Requests</Link>
            <Link to="/officials">Officials</Link>
            <Link to="/announcements">Announcements</Link>
            <Link to="/programs">Programs</Link>
            <Link to="/gallery">Gallery</Link>
            <Link to="/tasks">Tasks</Link>
            <a href="#" onClick={(e) => { e.preventDefault(); logout(); }} style={{ color: "#ffb3b3" }}>Logout</a>
          </>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </nav>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login onLogin={() => setAuthed(true)} />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/residents" element={<Residents />} />
        <Route path="/requests" element={<CrudPage title="Document Requests" endpoint="requests" columns={[
          { key: "request_id", label: "Request ID" }, { key: "type", label: "Type" },
          { key: "status", label: "Status", render: (r) => <span className="badge">{r.status}</span> },
          { key: "purpose", label: "Purpose" }, { key: "created_at", label: "Requested" }]} />} />
        <Route path="/officials" element={<CrudPage title="Barangay Officials" endpoint="officials" columns={[
          { key: "position", label: "Position" }, { key: "first_name", label: "First" },
          { key: "last_name", label: "Last" }, { key: "contact_info", label: "Contact" },
          { key: "is_visible", label: "Visible", render: (r) => r.is_visible ? "Yes" : "No" }]} />} />
        <Route path="/announcements" element={<CrudPage title="Announcements" endpoint="announcements" columns={[
          { key: "title", label: "Title" }, { key: "category", label: "Category" },
          { key: "priority", label: "Priority" }, { key: "created_at", label: "Posted" }]} />} />
        <Route path="/programs" element={<CrudPage title="Community Programs" endpoint="programs" columns={[
          { key: "title", label: "Title" }, { key: "event_date", label: "Date" },
          { key: "location", label: "Location" }, { key: "status", label: "Status", render: (r) => <span className="badge">{r.status}</span> }]} />} />
        <Route path="/gallery" element={<CrudPage title="Gallery" endpoint="gallery" columns={[
          { key: "caption", label: "Caption" }, { key: "description", label: "Description" },
          { key: "is_visible", label: "Visible", render: (r) => r.is_visible ? "Yes" : "No" }]} />} />
        <Route path="/tasks" element={<CrudPage title="Tasks" endpoint="tasks" columns={[
          { key: "task_id", label: "Task ID" }, { key: "title", label: "Title" },
          { key: "priority", label: "Priority" }, { key: "status", label: "Status", render: (r) => <span className="badge">{r.status}</span> },
          { key: "progress_percent", label: "Progress" }]} />} />
      </Routes>
      <footer className="footer">
        B.R.I.D.G.E © {new Date().getFullYear()} — Migrated from Barangay Management System. Data protected under RA 10173.
      </footer>
    </>
  );
}
