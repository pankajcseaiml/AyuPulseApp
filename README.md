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

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB instance (local or Atlas)

### 1. Clone the Repository
```bash
git clone https://github.com/pankajcseaiml/AyuPulseApp.git
cd AyuPulseApp
```

### 2. Set Up Backend
```bash
cd backend
# Follow detailed instructions in backend/README.md
```

### 3. Set Up Frontend
```bash
cd frontend
# Follow detailed instructions in frontend/README.md
```

### 4. Run Both Servers
1. Start backend: `cd backend && uvicorn app.main:app --reload --port 8000`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser: [http://localhost:5173](http://localhost:5173)

---

## Detailed Documentation

For complete, step-by-step setup instructions, refer to:

- **Backend Setup**: [backend/README.md](backend/README.md) – Detailed Python environment setup, MongoDB configuration, and API documentation
- **Frontend Setup**: [frontend/README.md](frontend/README.md) – Complete React setup, environment configuration, and deployment guide

---

## Application Structure

*   `backend/app/ml`: Contains the entire ML pipeline (preprocessing, models, fusion, explainability).
*   `backend/app/routes`: FastAPI endpoints for Auth, Profile, Patients, Predictions, and Admin.
*   `backend/app/models`: Beanie Document models defining the MongoDB schema.
*   `frontend/src/api`: API wrappers using standard Fetch API to communicate with the backend.
*   `frontend/src/components`: UI components, forms, layout elements.
*   `frontend/src/pages`: Main application views including Dashboard, Results, and New Prediction forms.

---

## Role System

The application supports three user roles:

1. **Patient** – Can create personal predictions and manage their profile
2. **Doctor** – Can manage patients and create predictions for them
3. **Admin** – Full system access including user management

---

## Demo Accounts

For quick testing, use these credentials:

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@example.com` | `admin123` |
| Doctor | `doctor@example.com` | `doctor123` |
| Patient | `patient@example.com` | `patient123` |

---

## API Documentation

Once the backend is running, access the interactive API documentation:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Recent Updates & Fixes

- **Dashboard.tsx**: Fixed TypeScript error (`user?.name` → `user?.full_name`)
- **Backend Models**: Resolved Pylance type annotation errors using `typing.Annotated` syntax
- **Role System**: Streamlined from 4 roles to 3 roles (admin, doctor, patient)
- **Backend Sorting**: Fixed predictions not sorted by `created_at` descending
- **Documentation**: Added comprehensive README files for both backend and frontend

---

## Deployment

The project is ready for deployment to various platforms:

### Recommended Cloud Deployment (Vercel + Railway + MongoDB Atlas)
For a modern, scalable deployment, we recommend:
- **Frontend**: Deploy to [Vercel](https://vercel.com) (React)
- **Backend**: Deploy to [Railway](https://railway.app) (FastAPI)
- **Database**: Use [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (Cloud MongoDB)

Detailed step-by-step instructions are available in [DEPLOYMENT.md](DEPLOYMENT.md).

#### Quick Vercel Frontend Deployment
We've created easy-to-use deployment scripts:

**Windows:**
```bash
deploy-vercel.bat
```

**Linux/Mac:**
```bash
chmod +x deploy-vercel.sh
./deploy-vercel.sh
```

These scripts will guide you through deploying the frontend to Vercel with proper configuration. For detailed Vercel-specific instructions, see [DEPLOY_VERCEL.md](DEPLOY_VERCEL.md).

### GitHub
The project is already configured with Git and can be pushed to your repository:
```bash
git remote add origin https://github.com/pankajcseaiml/AyuPulseApp.git
git push -u origin master
```

### Alternative Deployment Options
- **Backend**: Deploy with gunicorn/uvicorn on platforms like Railway, Render, Heroku, or AWS
- **Frontend**: Build static files and deploy to Vercel, Netlify, or GitHub Pages

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment instructions.

---

## Support

If you encounter issues:
1. Check the detailed README files in `backend/` and `frontend/` directories
2. Review the API documentation at `/docs`
3. Ensure all prerequisites are met

---

## Disclaimer

This application is for **educational and demonstration purposes only**. The predictions and medical insights provided are simulated and should not be used for actual medical diagnosis or treatment decisions. Always consult qualified healthcare professionals for medical advice.

---

## License

This project is licensed under the MIT License.
