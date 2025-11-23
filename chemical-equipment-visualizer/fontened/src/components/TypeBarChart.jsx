import { Bar } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from "chart.js";
ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function TypeBarChart({ summary }) {
  if (!summary) return null;
  const dist = summary.type_distribution || [];
  const labels = dist.map(d => d.type);
  const values = dist.map(d => d.count);

  const data = {
    labels,
    datasets: [
      {
        label: "Count",
        data: values,
        backgroundColor: "rgba(54, 162, 235, 0.6)"
      }
    ]
  };

  const options = {
    responsive: true,
    plugins: { legend: { position: "top" } },
    scales: { y: { beginAtZero: true } }
  };

  return (
    <div className="card">
      <h3>Equipment Type Distribution</h3>
      <Bar data={data} options={options} />
    </div>
  );
}
