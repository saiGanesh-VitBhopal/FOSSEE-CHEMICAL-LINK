# Chemical Equipment Parameter Visualizer (FOSSEE Project)

A hybrid full-stack application for visualizing chemical equipment parameters, built using:

- **Django REST API backend**
- **React + Vite web frontend**
- **PyQt5 desktop application**

---

## 📁 Folder Structure

```
chemical-equipment-visualizer/
│
├── backend/               # Django REST API + PDF generation
│   ├── api/
│   ├── config/
│   ├── media/
│   ├── manage.py
│   └── requirements.txt
│
├── desktop-app/           # PyQt5 desktop application
│   ├── main.py
│   ├── requirements.txt
│   └── venv/
│
├── fontened/              # React + Vite frontend (your folder name)
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

# 🚀 1. Backend Setup (Django — Windows PowerShell)

### 📌 Navigate to backend
```powershell
cd backend
```

### 📌 Create virtual environment
```powershell
python -m venv venv
```

### 📌 Activate virtual environment  
(PowerShell may block scripts, so we allow only this session.)

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.env\Scripts\Activate.ps1
```

### 📌 Install backend dependencies
```powershell
pip install django djangorestframework django-cors-headers pandas reportlab matplotlib pillow
```

### 📌 Run migrations
```powershell
python manage.py migrate
```

### (Optional) Create superuser
```powershell
python manage.py createsuperuser
```

### 📌 Start backend server
```powershell
python manage.py runserver
```

Backend URLs:
- API Base → http://127.0.0.1:8000/api/
- Admin Panel → http://127.0.0.1:8000/admin/

---

# 🖥 2. Desktop Application Setup (PyQt5)

### 📌 Go to desktop app folder
```powershell
cd desktop-app
```

### 📌 Create virtual environment
```powershell
python -m venv venv
```

### 📌 Activate environment
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.env\Scripts\Activate.ps1
```

### 📌 Install desktop dependencies
```powershell
pip install PyQt5 requests pandas numpy matplotlib
```

### 📌 Run desktop application
```powershell
python main.py
```

> **Backend MUST be running before launching the desktop app.**

---

# 🌐 3. Web Frontend Setup (React + Vite)

### 📌 Navigate to frontend
```powershell
cd fontened
```

### 📌 Install node modules
```powershell
npm install
```

### 📌 Create API environment file
Create:

```
fontened/.env.development
```

Add this line:

```
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

### 📌 Start development server
```powershell
npm run dev
```

Frontend URL →  
**http://localhost:5173**

---

## 🔐 Login Information  
Your project uses a **simple dummy login** (frontend-only):

- Any username ✔  
- Any password ✔  

---

# 📌 Usage Instructions

1️⃣ Start the **Django backend**  
2️⃣ Start **React web app** OR **Desktop app**  
3️⃣ Upload CSV files  
4️⃣ View:  
- Summary statistics  
- Charts  
- Preview table  
- PDF report  
5️⃣ History auto-stores last 5 uploads

Both frontend clients use this API root:

```
http://127.0.0.1:8000/api
```

---

# 👤 Author
**Nagamalla Sai Ganesh**  
FOSSEE Chemical Visualization Project Submission
