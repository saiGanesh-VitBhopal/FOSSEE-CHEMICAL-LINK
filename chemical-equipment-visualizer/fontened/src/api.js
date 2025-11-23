import axios from "axios";

const API_BASE = "http://127.0.0.1:8000/api";

export function api() {
  const instance = axios.create({ baseURL: API_BASE });

  return {
    upload(file) {
      const form = new FormData();
      form.append("file", file);
      return instance.post("/upload/", form).then(r => r.data);
    },
    history() {
      return instance.get("/history/").then(r => r.data);
    },
    summary(id) {
      return instance.get(`/summary/${id}/`).then(r => r.data);
    },
    reportUrl(id) {
      return `${API_BASE}/report/${id}/`;
    }
  };
}
