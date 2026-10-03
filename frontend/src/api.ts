// Axios client -> Django backend (VITE_API_URL from .env/frontend.env).
// Uses Django Token auth (POST /api/auth/login/ -> { token }).
import axios from "axios";

export const api = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL ?? ""}/api`,
  timeout: 15000,
});

const TOKEN_KEY = "bridge_token";
export function setToken(t: string | null) {
  if (t) localStorage.setItem(TOKEN_KEY, t);
  else localStorage.removeItem(TOKEN_KEY);
  api.defaults.headers.common["Authorization"] = t ? `Token ${t}` : "";
}
if (localStorage.getItem(TOKEN_KEY)) setToken(localStorage.getItem(TOKEN_KEY));

export const authApi = {
  login: (username: string, password: string) =>
    api.post<{ token: string }>("/auth/login/", { username, password }).then((r) => {
      setToken(r.data.token);
      return r.data;
    }),
  me: () => api.get("/auth/me/").then((r) => r.data),
  logout: () => setToken(null),
};

export interface Resident {
  id: number;
  resident_id: string;
  household_no: string;
  last_name: string;
  first_name: string;
  middle_name: string;
  birth_date: string;
  gender: string;
  civil_status: string;
  address: string;
  contact: string;
  voter: string;
  classification: string;
  resident_status: string;
  full_name?: string;
}

export const residentsApi = {
  list: () => api.get<{ results: Resident[] }>("/residents/?page_size=200").then((r) => r.data),
  health: () => api.get("/health/").then((r) => r.data),
  dashboard: () => api.get<Record<string, number>>("/dashboard-stats/").then((r) => r.data),
  publicSite: () =>
    api.get<{
      settings: Record<string, string>;
      officials: any[];
      announcements: any[];
      programs: any[];
      gallery: any[];
    }>("/public-site/").then((r) => r.data),
};

// Generic list helper used by CrudPage (requests, officials, announcements, programs, gallery, tasks)
export const listEndpoint = (endpoint: string) =>
  api.get<{ results: any[] }>(`/${endpoint}/?page_size=200`).then((r) => r.data.results ?? []);
