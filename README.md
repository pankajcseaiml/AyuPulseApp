# AyuPulseApp 🩺

AyuPulse is a comprehensive, production-grade web application for early heart disease risk prediction. It combines **15 clinical parameters**, **chest X-ray analysis**, and **ECG analysis** into a single cohesive risk score using advanced multi-modal machine learning.

AyuPulse provides **full explainability** (via SHAP and GradCAM), family management, and medical reporting, giving healthcare providers and patients transparent insights into cardiovascular health.

## Technology Stack

### Backend
*   **Framework:** FastAPI (`fastapi`, `uvicorn`)
*   **Database:** MongoDB via `beanie` and `motor`
*   **Machine Learning:** PyTorch (`torch`, `torchvision`), XGBoost (`xgboost`)
*   **Explainability:** `shap`, OpenCV (`opencv-python-headless`) for GradCAM
*   **Authentication:** JWT with `python-jose` and `passlib`

### Frontend
*   **Framework:** React 19 + TypeScript (Vite)
*   **Routing:** React Router v7
*   **Styling:** TailwindCSS with custom theming (Sora & DM Sans fonts)
*   **Forms:** React Hook Form
*   **Charts:** Recharts

---

## Features

1.  **Multi-Modal ML Pipeline:** 
    *   Rule-based / XGBoost Clinical model with simulated SHAP.
    *   EfficientNet-B0 backbone for X-Ray analysis with GradCAM.
    *   ResNet-18 backbone for ECG analysis with GradCAM.
    *   Adaptive weighted-average fusion system.
2.  **Explainable AI:** Heatmaps for imaging (GradCAM) and feature contribution charts (SHAP) for clinical data.
3.  **Comprehensive Profiles:** Support for individual profiles and family dependents (patients).
4.  **Medical Reports:** Auto-generated text summaries mapping clinical values to medical reference ranges (e.g., JNC8, ATP III).
5.  **Admin Dashboard:** System-wide statistics and user management.

---

## Setup Instructions

### 1. Prerequisites
*   Python 3.10+
*   Node.js 18+
*   MongoDB instance (local or Atlas)

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:
```env
PROJECT_NAME="AyuPulseApp API"
VERSION="1.0.0"
MONGODB_URL="mongodb://localhost:27017"
MONGODB_DB_NAME="ayupulse_db"
SECRET_KEY="your-super-secret-key-change-this"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
UPLOAD_DIR="uploads"
BACKEND_CORS_ORIGINS='["http://localhost:5173", "http://localhost:3000"]'
```

Start the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
# Or: npm install recharts date-fns (if they are missing)

# Ensure the backend URL is set, if different from localhost:8000
# Create .env file in frontend/:
# VITE_API_URL=http://localhost:8000
```

Start the frontend server:
```bash
npm run dev
```

The application will be accessible at `http://localhost:5173`.

---

## Application Structure

*   `backend/app/ml`: Contains the entire ML pipeline (preprocessing, models, fusion, explainability).
*   `backend/app/routes`: FastAPI endpoints for Auth, Profile, Patients, Predictions, and Admin.
*   `backend/app/models`: Beanie Document models defining the MongoDB schema.
*   `frontend/src/api`: API wrappers using standard Fetch API to communicate with the backend.
*   `frontend/src/components`: UI components, forms, layout elements.
*   `frontend/src/pages`: Main application views including Dashboard, Results, and New Prediction forms.

---

## Disclaimer
AyuPulse is built as a screening tool and demonstration of explainable AI in healthcare. It is **not** a diagnostic tool. Always consult a healthcare professional.
