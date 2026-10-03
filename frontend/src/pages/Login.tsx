import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { authApi } from "../api";

export default function Login({ onLogin }: { onLogin?: () => void }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const nav = useNavigate();

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await authApi.login(username, password);
      onLogin?.();
      nav("/dashboard");
    } catch (err: any) {
      setError(err?.response?.data?.non_field_errors?.[0] ?? "Login failed. Check credentials.");
    }
  };

  return (
    <div className="card" style={{ maxWidth: 420, margin: "60px auto" }}>
      <h2>Portal Login</h2>
      <form onSubmit={submit} className="form">
        <label>Username <input value={username} onChange={(e) => setUsername(e.target.value)} required autoFocus /></label>
        <label>Password <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required /></label>
        {error && <p style={{ color: "#b00020", fontSize: 13 }}>{error}</p>}
        <button className="btn btn-primary" type="submit">Sign in</button>
        <p style={{ fontSize: 12, color: "var(--muted)", marginTop: 8 }}>
          Migrated from old BMS: old password hashes are not portable. Set a new password via Django admin
          (<code>/admin/</code>) or create a superuser: <code>python manage.py createsuperuser</code>.
        </p>
      </form>
    </div>
  );
}
