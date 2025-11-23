# Chemical Equipment Parameter Visualizer  
Hybrid Web + Desktop Application  
React.js • PyQt5 • Django REST Framework

## 🔍 Overview
A hybrid application that allows users to upload CSV files containing chemical equipment parameters and visualize the data through charts, tables, and PDF reports.  
Both the **React Web App** and **PyQt5 Desktop App** use a **common Django backend**.

---

## 🚀 Features
- CSV Upload (Web + Desktop)
- Summary statistics (count + averages)
- Type distribution chart  
  - Web → Chart.js  
  - Desktop → Matplotlib  
- Data preview table
- PDF report generation (ReportLab + Matplotlib)
- History: keeps last 5 datasets
- Simple login + logout for Web

---

## 🧩 Tech Stack
- **Frontend (Web):** React + Vite + Chart.js  
- **Frontend (Desktop):** PyQt5 + Matplotlib  
- **Backend:** Django + DRF  
- **Database:** SQLite  
- **Data Processing:** Pandas  
- **PDF:** ReportLab  

---
🔧 Backend (Django)

cd backend
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver


🌐 Web App (React)

cd fontened
npm install
npm run dev



🖥 Desktop App (PyQt5)


cd desktop-app
pip install -r requirements.txt
python main.py


📌 API Endpoints


| Method | Endpoint             | Description         |
| ------ | -------------------- | ------------------- |
| POST   | `/api/upload/`       | Upload CSV          |
| GET    | `/api/history/`      | Last 5 datasets     |
| GET    | `/api/summary/<id>/` | Summary for dataset |
| GET    | `/api/report/<id>/`  | PDF Report          |


📝 PDF Report Includes

Dataset info

Summary statistics

Type distribution bar chart

Auto-clean temporary chart files


👤 Author

Nagamalla Sai Ganesh



## 📂 Project Structure

```txt
chemical-equipment-visualizer/
│
├── backend/               # Django backend (API + PDF + history)
│   ├── api/
│   ├── config/
│   ├── media/
│   ├── manage.py
│   └── requirements.txt
│
├── desktop-app/           # PyQt5 desktop application
│   ├── venv/
│   ├── main.py
│   └── requirements.txt
│
├── fontened/              # React web app (your folder name)
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── Login.jsx
│   │   ├── main.jsx
│   │   ├── styles.css
│   │   ├── App.css
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
└── README.md


