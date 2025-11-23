📘 Chemical Equipment Parameter Visualizer
Hybrid Web + Desktop Application
(React Web + PyQt5 Desktop + Django REST API)
📝 Project Overview

Chemical Equipment Parameter Visualizer is a hybrid application that runs as:

🌐 Web Application (React.js)

💻 Desktop Application (PyQt5)

🛠 Common Django REST Backend

Users can upload a CSV file containing chemical equipment parameters such as:

Equipment Name

Type

Flowrate

Pressure

Temperature

The backend parses the file using Pandas, computes statistics, stores history of last 5 datasets, and exposes APIs that both Web + Desktop frontends use.

The application visualizes:

Summary Statistics

Type Distribution (Bar Chart)

Data Table (Preview)

PDF Report with Matplotlib Chart

Basic Login Authentication

🚀 Features
🔼 CSV Upload

Upload CSV files from both Web (React) and Desktop (PyQt5).

📊 Data Analysis (Backend)

Django API computes:

Total count of equipment

Average Flowrate, Pressure, Temperature

Type distribution (categorical analytics)

Preview rows of the CSV

📉 Visualization

React (Web): Chart.js

PyQt5 (Desktop): Matplotlib

Interactive bar charts

Clean data tables

🧾 PDF Report Generation

Built using ReportLab

Includes summary table

Includes Matplotlib bar chart saved from backend

Auto-generated & downloadable

🕘 History Management

Backend keeps last 5 datasets only

Older datasets auto-deleted

🔐 Authentication

Simple login page for React (password-only dummy authentication)

Logout functionality

🏗 Tech Stack
Layer	Technology	Purpose
Frontend (Web)	React.js, Bootstrap, Chart.js	Upload CSV + display tables & charts
Frontend (Desktop)	PyQt5, Matplotlib	Desktop visualization + upload
Backend	Django, Django REST Framework	Data processing + API
Data Handling	Pandas	CSV parsing & analytics
Database	SQLite	Store datasets & history
PDF Generator	ReportLab + Matplotlib	Export PDF reports
Version Control	Git + GitHub	Collaboration & submission
📂 Project Structure
project/
│
├── backend/
│   ├── api/
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── models.py
│   │   ├── urls.py
│   ├── config/
│   ├── media/
│   │   └── datasets/
│   ├── manage.py
│
├── fronted/  (React Web App)
│   ├── src/
│   │   ├── App.jsx
│   │   ├── Login.jsx
│   │   ├── api.js
│   │   ├── components/
│   │   ├── styles.css
│
├── desktop-app/  (PyQt5 Desktop App)
│   ├── main.py
│   ├── ui.py
│
├── sample_equipment_data.csv
└── README.md

⚙️ Backend Setup Instructions (Django)
1️⃣ Create Virtual Environment
cd backend
python -m venv venv
venv\Scripts\activate   # Windows

2️⃣ Install Requirements
pip install --upgrade pip
pip install -r requirements.txt

3️⃣ Run Django Server
python manage.py migrate
python manage.py runserver


Backend runs at:

http://127.0.0.1:8000/api/

🌐 Web App Setup (React + Vite)
1️⃣ Install Dependencies
cd fronted
npm install

2️⃣ Run Web App
npm run dev


Default URL:

http://localhost:5173/

🖥 Desktop App Setup (PyQt5)
1️⃣ Install Python Dependencies
pip install PyQt5 matplotlib requests pandas

2️⃣ Run App
cd desktop-app
python main.py

🔗 API Endpoints (Django)
Upload CSV
POST /api/upload/

Get History (last 5)
GET /api/history/

Get Summary
GET /api/summary/<id>/

Download PDF Report
GET /api/report/<id>/

📄 PDF Report Includes

✔ Title
✔ Dataset Info
✔ Summary Table
✔ Bar Chart (Matplotlib)
✔ Auto-clean temporary images

🔐 Authentication (Web)

Simple password-only login (no backend authentication)

Logout button returns to login screen
