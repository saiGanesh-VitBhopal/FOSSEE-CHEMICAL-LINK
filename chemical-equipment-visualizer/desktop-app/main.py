import sys
import io
import requests
import pandas as pd
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QFileDialog, QTableWidget, QTableWidgetItem, QListWidget
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


API_BASE = "http://127.0.0.1:8000/api"


class ChartCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        super().__init__(self.fig)
        self.axes = self.fig.add_subplot(111)

    def plot_bar(self, labels, values):
        self.axes.clear()
        self.axes.bar(labels, values)
        self.axes.set_title("Equipment Type Distribution")
        self.axes.set_xlabel("Type")
        self.axes.set_ylabel("Count")
        self.fig.tight_layout()
        self.draw()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer (Desktop)")
        self.resize(1100, 700)

        self.username = ""
        self.password = ""

        self.build_ui()
        self.set_auth_fields("admin", "adminpass")  # change to your credentials

    def set_auth_fields(self, u, p):
        self.user_input.setText(u)
        self.pass_input.setText(p)

    def build_ui(self):
        layout = QVBoxLayout(self)

        top = QHBoxLayout()
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.load_history)

        top.addWidget(QLabel("Auth:"))
        top.addWidget(self.user_input)
        top.addWidget(self.pass_input)
        top.addWidget(self.connect_btn)

        layout.addLayout(top)

        # Controls row
        controls = QHBoxLayout()

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)
        self.report_btn = QPushButton("Download PDF Report")
        self.report_btn.clicked.connect(self.download_report)

        controls.addWidget(self.upload_btn)
        controls.addWidget(self.report_btn)
        layout.addLayout(controls)

        # Middle split: left main, right history
        mid = QHBoxLayout()

        # Left column
        left = QVBoxLayout()

        # Summary labels
        self.summary_label = QLabel("Summary: (upload or select from history)")
        left.addWidget(self.summary_label)

        # Chart
        self.chart = ChartCanvas(self)
        left.addWidget(self.chart, stretch=2)

        # Table preview
        self.table = QTableWidget()
        left.addWidget(self.table, stretch=3)

        # Right column (history)
        right = QVBoxLayout()
        right.addWidget(QLabel("History (last 5)"))
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.select_history_item)
        right.addWidget(self.history_list)

        mid.addLayout(left, stretch=3)
        mid.addLayout(right, stretch=1)

        layout.addLayout(mid)

        self.active_id = None
        self.columns = []
        self.rows = []

    # --- API helpers ----
    def _auth(self):
        return (self.user_input.text().strip(), self.pass_input.text().strip())

    def api_get(self, path):
        r = requests.get(API_BASE + path, auth=self._auth())
        r.raise_for_status()
        return r.json()

    def api_post_file(self, path, file_path):
        with open(file_path, "rb") as f:
            files = {"file": (file_path.split("/")[-1], f, "text/csv")}
            r = requests.post(API_BASE + path, files=files, auth=self._auth())
        r.raise_for_status()
        return r.json()

    # --- UI actions ----
    def load_history(self):
        try:
            items = self.api_get("/history/")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))
            return

        self.history_list.clear()
        for it in items:
            self.history_list.addItem(f'#{it["id"]} — {it["original_filename"]}')

        if items:
            self.load_summary(items[0]["id"])

    def select_history_item(self, item):
        text = item.text()
        # Format: "#<id> — ..."
        try:
            id_str = text.split("—")[0].strip().replace("#", "")
            self.load_summary(int(id_str))
        except:
            pass

    def load_summary(self, dataset_id):
        try:
            res = self.api_get(f"/summary/{dataset_id}/")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))
            return

        self.active_id = res["id"]
        self.columns = res["columns"]
        self.rows = res["preview_rows"]

        s = res["summary"]
        avg = s["averages"]
        self.summary_label.setText(
            f"Summary — Rows: {s['total_count']}, "
            f"Avg Flowrate: {avg['Flowrate']:.2f}, "
            f"Avg Pressure: {avg['Pressure']:.2f}, "
            f"Avg Temperature: {avg['Temperature']:.2f}"
        )

        # Chart
        labels = [d["type"] for d in s["type_distribution"]]
        values = [d["count"] for d in s["type_distribution"]]
        self.chart.plot_bar(labels, values)

        # Table
        self.table.clear()
        self.table.setColumnCount(len(self.columns))
        self.table.setRowCount(len(self.rows))
        self.table.setHorizontalHeaderLabels(self.columns)
        for r_idx, row in enumerate(self.rows):
            for c_idx, col in enumerate(self.columns):
                self.table.setItem(r_idx, c_idx, QTableWidgetItem(str(row.get(col, ""))))
        self.table.resizeColumnsToContents()

    def upload_csv(self):
        path, _ = QFileDialog.getOpenFileName(self, "Choose CSV file", filter="CSV Files (*.csv)")
        if not path:
            return
        try:
            res = self.api_post_file("/upload/", path)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Upload Error", str(e))
            return

        self.load_history()  # refresh
        self.load_summary(res["id"])

    def download_report(self):
        if not self.active_id:
            QtWidgets.QMessageBox.information(self, "Info", "Select or upload a dataset first.")
            return
        url = f"{API_BASE}/report/{self.active_id}/"
        try:
            r = requests.get(url, auth=self._auth(), stream=True)
            r.raise_for_status()
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Report", f"dataset_{self.active_id}_report.pdf", "PDF (*.pdf)")
            if not save_path:
                return
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            QtWidgets.QMessageBox.information(self, "Saved", f"Report saved to:\n{save_path}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Download Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
