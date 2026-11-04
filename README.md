# ♻️ E-Waste Classification & Recycling Recommendation System

An AI-powered web application that identifies electronic waste from photos using deep transfer learning and provides actionable recycling, reuse, safety, and environmental guidance.

---

## 🚀 How to Run the Project

### Prerequisites
- **Python 3.10 – 3.13** installed
- **Node.js** (v18 or higher) installed

---

### Step 1: Start the Backend (Flask API)
Open a terminal in the project root:

```bash
cd backend
pip install -r requirements.txt
python app.py
```
*(Or double-click `run_backend.bat` on Windows)*

> The API will be live on: **http://localhost:5000**

---

### Step 2: Start the Frontend (React UI)
Open a **second terminal** in the project root:

```bash
cd frontend_upload/frontend
npm install
npm run dev
```

> Open your browser at: **http://localhost:5173**

---

## 🎯 Supported Categories
1. 📱 **Mobile Phone** (Smartphones, iPhones, Android devices)
2. 💻 **Laptop** (Laptops, MacBooks, notebook computers)
3. 🔋 **Battery** (Li-ion cells, AA/AAA, power banks)
4. 🔌 **Charger / Cable** (Power adapters, USB cables, charging bricks)
5. 🖥️ **Circuit Board** (PCBs, motherboards, electronic scrap)
6. 📺 **Monitor / TV** (Computer screens, televisions, flat panels)

---

## 🧠 ML Architecture
* **Vision Backbone:** Dual-Backbone Transfer Learning Ensemble (**EfficientNetB0** + **MobileNetV2**)
* **Domain Adaptation:** Targeted e-waste semantic taxonomy and geometric aspect-ratio detection
* **Output:** Category identification, top-3 ranked confidence scores, disposal routes, and environmental impact data
