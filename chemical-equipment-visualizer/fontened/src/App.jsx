// App.jsx (Bootstrap Version)
import { useEffect, useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./styles.css";

import { api } from "./api";
import UploadPanel from "./components/UploadPanel";
import SummaryCards from "./components/SummaryCards";
import PreviewTable from "./components/PreviewTable";
import TypeBarChart from "./components/TypeBarChart";

export default function App({ onLogout }) {
  const [client] = useState(api());
  const [history, setHistory] = useState([]);
  const [active, setActive] = useState(null);

  const refreshHistory = async () => {
    if (!client) return;
    const h = await client.history();
    setHistory(h);
  };

  const selectDataset = async (id) => {
    try {
      const s = await client.summary(id);
      setActive({
        id,
        summary: s.summary,
        columns: s.columns,
        rows: s.preview_rows,
      });
    } catch (err) {
      console.log("Summary load failed:", err);
    }
  };

  useEffect(() => {
    refreshHistory();
  }, []);

  const onUpload = async (file) => {
    try {
      const res = await client.upload(file);
      setActive({
        id: res.id,
        summary: res.summary,
        columns: res.columns,
        rows: res.preview_rows,
      });
      refreshHistory();
    } catch (err) {
      alert("Upload failed. Make sure CSV format is correct.");
    }
  };

  const reportUrl = active ? client?.reportUrl(active.id) : "#";

  return (
    <div className="container py-4">
      {/* HEADER + LOGOUT */}
      <div className="d-flex justify-content-between align-items-center mb-5">
        <div className="text-center flex-grow-1">
          <h2 className="fw-bold text-primary m-0">
            Chemical Equipment Visualizer (Web)
          </h2>
          <hr
            style={{ width: "260px", margin: "8px auto", borderWidth: "2px" }}
          />
        </div>

        <button className="btn btn-danger ms-3" onClick={onLogout}>
          Logout
        </button>
      </div>

      <div className="row">
        {/* LEFT SIDE */}
        <div className="col-md-9">
          <UploadPanel onUpload={onUpload} />

          {active ? (
            <>
              <div className="mt-4">
                <SummaryCards summary={active.summary} />
              </div>

              <div className="mt-4">
                <TypeBarChart summary={active.summary} />
              </div>

              <div className="mt-4">
                <PreviewTable columns={active.columns} rows={active.rows} />
              </div>

              <div className="card shadow mt-4 p-3">
                <a
                  className="btn btn-success w-100 fw-bold"
                  href={reportUrl}
                  target="_blank"
                  rel="noreferrer"
                >
                  Download PDF Report
                </a>
              </div>
            </>
          ) : (
            <p className="text-center text-muted mt-4 fst-italic">
              No dataset loaded. Upload a CSV to begin.
            </p>
          )}
        </div>

        {/* RIGHT SIDE – HISTORY */}
        <div className="col-md-3">
          <div className="card shadow p-3">
            <h5 className="fw-bold mb-3">History (last 5)</h5>

            <ul className="list-unstyled">
              {history.map((h) => (
                <li key={h.id} className="mb-2">
                  <button
                    className="btn btn-outline-primary w-100"
                    onClick={() => selectDataset(h.id)}
                  >
                    #{h.id} — {h.original_filename}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
