export default function SummaryCards({ summary }) {
  if (!summary) return null;
  const a = summary.averages || {};
  return (
    <div className="grid">
      <div className="card"><b>Total Rows</b><div>{summary.total_count}</div></div>
      <div className="card"><b>Avg Flowrate</b><div>{a.Flowrate?.toFixed(2)}</div></div>
      <div className="card"><b>Avg Pressure</b><div>{a.Pressure?.toFixed(2)}</div></div>
      <div className="card"><b>Avg Temperature</b><div>{a.Temperature?.toFixed(2)}</div></div>
    </div>
  );
}
