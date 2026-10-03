import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { residentsApi } from "../api";

export default function Landing() {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    residentsApi.publicSite().then(setData).catch(() => setData(null));
  }, []);

  const s = data?.settings ?? {};
  const hero = "https://bridge-backend-per3.onrender.com/media/assets/hero1.jpg";

  return (
    <div>
      <div className="hero" style={{ backgroundImage: `linear-gradient(rgba(11,83,148,${(s.hero_overlay_opacity ?? 82) / 100}), rgba(11,83,148,0.75)), url(${hero})` }}>
        <div className="hero-inner">
          {s.welcome_badge && <span className="badge" style={{ background: "var(--accent)", color: "#1a2233", marginBottom: 12 }}>{s.welcome_badge}</span>}
          <h1>{s.welcome_title ?? "WELCOME TO BARANGAY POBLACION"}</h1>
          <p className="hero-sub">{s.welcome_subtitle ?? "Baranggay Resident Information and Digital Government Environment"}</p>
          <div className="hero-btns">
            <Link to="/login" className="btn btn-primary">{s.btn_portal_label ?? "ENTER SYSTEM NOW"}</Link>
            <a href="#announcements" className="btn btn-ghost">{s.btn_announcements_label ?? "VIEW ANNOUNCEMENTS"}</a>
          </div>
        </div>
      </div>

      <div className="container">
        <div className="card" id="officials">
          <h2>Barangay Officials</h2>
          <div className="grid">
            {(data?.officials ?? []).map((o: any) => (
              <div key={o.id} className="official">
                <div className="official-name">{o.first_name} {o.middle_name ?? ""} {o.last_name} {o.suffix ?? ""}</div>
                <div className="badge">{o.position}</div>
              </div>
            ))}
            {(!data?.officials || data.officials.length === 0) && <p style={{ color: "var(--muted)" }}>No officials published.</p>}
          </div>
        </div>

        <div className="card" id="announcements">
          <h2>Announcements</h2>
          {(data?.announcements ?? []).map((a: any) => (
            <div key={a.id} style={{ padding: "10px 0", borderBottom: "1px solid #e6eaf2" }}>
              <strong>{a.title}</strong> <span className="badge">{a.category ?? "General"}</span>
              <p style={{ color: "var(--muted)", fontSize: 14, marginTop: 4 }}>{a.body}</p>
            </div>
          ))}
          {(!data?.announcements || data.announcements.length === 0) && <p style={{ color: "var(--muted)" }}>No announcements yet.</p>}
        </div>

        <div className="card">
          <h2>Community Programs</h2>
          <div className="grid">
            {(data?.programs ?? []).map((p: any) => (
              <div key={p.id} className="official">
                <div className="official-name">{p.title}</div>
                <div style={{ fontSize: 13, color: "var(--muted)" }}>{p.event_date} {p.start_time ?? ""} · {p.location ?? ""}</div>
                <span className="badge">{p.status}</span>
              </div>
            ))}
            {(!data?.programs || data.programs.length === 0) && <p style={{ color: "var(--muted)" }}>No scheduled programs.</p>}
          </div>
        </div>

        <div className="card">
          <h2>Gallery</h2>
          <div className="grid">
            {(data?.gallery ?? []).map((g: any) => (
              <div key={g.id} className="official">
                <div className="official-name">{g.caption}</div>
                <div style={{ fontSize: 13, color: "var(--muted)" }}>{g.description ?? ""}</div>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h2>Contact</h2>
          <p style={{ fontSize: 14, lineHeight: 1.8 }}>
            {s.barangay_name}, {s.municipality}<br />
            {s.contact_address}<br />
            Phone: {s.contact_phone} · Emergency: {s.contact_emergency}<br />
            Email: {s.contact_email} · {s.contact_website}<br />
            Office hours: {s.contact_office_hours}
          </p>
        </div>
      </div>
    </div>
  );
}
