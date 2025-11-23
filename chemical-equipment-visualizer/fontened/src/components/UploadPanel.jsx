import { useRef, useState } from "react";

export default function UploadPanel({ onUpload }) {
  const fileRef = useRef();
  const [fileName, setFileName] = useState("");

  const handleUpload = () => {
    if (!fileRef.current.files.length) {
      alert("Please select a CSV file.");
      return;
    }
    onUpload(fileRef.current.files[0]);
  };

  return (
    <div className="card">
      <h3>Upload CSV</h3>

      <input
        type="file"
        accept=".csv"
        ref={fileRef}
        onChange={(e) => setFileName(e.target.files[0]?.name || "")}
      />

      {fileName && (
        <p style={{ marginTop: 6, fontSize: 13, opacity: 0.9 }}>
          Selected: <b>{fileName}</b>
        </p>
      )}

      <button className="btn" style={{ marginTop: 10 }} onClick={handleUpload}>
        Upload
      </button>

      <p style={{fontSize:12, opacity:.8, marginTop:10}}>
        Expected columns: Equipment Name, Type, Flowrate, Pressure, Temperature
      </p>
    </div>
  );
}
