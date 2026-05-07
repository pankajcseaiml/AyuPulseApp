# AyuPulseApp - Detailed Project Description

## Overview
**AyuPulseApp** is a comprehensive Early Heart Disease Risk Prediction System that combines modern web technologies with advanced machine learning to provide accurate, explainable cardiovascular risk assessments. The system uses multi-modal data analysis (clinical parameters, chest X-ray images, and ECG signals) to predict heart disease risk with high precision.

## What It Does
The system provides healthcare professionals with a tool to:
1. **Predict heart disease risk** using a fusion of clinical data, X-ray images, and ECG signals
2. **Generate explainable AI insights** with SHAP values and plain-English explanations
3. **Manage patient records** with comprehensive CRUD operations
4. **Track prediction history** for longitudinal patient monitoring
5. **Provide risk visualization** through intuitive dashboards and reports

## Core Functionality

### 1. Multi-Modal Prediction Pipeline
- **Clinical Data Analysis**: 15 clinical parameters including age, gender, smoking status, cholesterol levels, blood pressure, BMI, glucose, etc.
- **X-Ray Image Analysis**: CNN-based model extracts features from chest X-ray images
- **ECG Signal Analysis**: CNN-based model processes ECG images/signals
- **Fusion Model**: Weighted combination of all modalities (Clinical: 50%, X-Ray: 30%, ECG: 20%)

### 2. Explainable AI (XAI)
- **SHAP Values**: Feature importance analysis for clinical parameters
- **Plain-English Explanations**: Human-readable risk factor explanations
- **Confidence Scores**: Model confidence metrics for each prediction
- **Risk Categories**: Low (<0.3), Medium (0.3-0.7), High (>0.7) risk classification

### 3. User Management & Security
- **JWT-based Authentication**: Secure login/registration with role-based access
- **Role System**: Doctor (regular users) and Admin (system administrators)
- **Patient Data Isolation**: Users can only access their own patients' data
- **Secure File Upload**: Validation and sanitization of medical images

## Technical Architecture

### Backend (FastAPI + MongoDB)
- **Framework**: FastAPI with async/await support
- **Database**: MongoDB with Motor async driver
- **Authentication**: JWT tokens with 7-day expiry
- **File Storage**: Local uploads directory with organized structure
- **ML Models**: PyTorch for CNN models, scikit-learn for clinical model
- **API Documentation**: Auto-generated Swagger UI at `/docs`

### Frontend (React + TypeScript + Vite)
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite for fast development
- **Styling**: Tailwind CSS with custom components
- **State Management**: React Context for authentication
- **Routing**: React Router (planned/implied)
- **UI Components**: Custom dashboard cards, forms, and visualization components

### Machine Learning Pipeline
1. **Input Processing**:
   - Clinical data: 15 parameters validated and scaled
   - X-ray images: Resized to 224x224, normalized, converted to tensor
   - ECG images: Same preprocessing as X-ray

2. **Model Inference**:
   - Clinical Model: Random Forest classifier (dummy implementation)
   - X-ray Model: CNN with embedding extraction
   - ECG Model: CNN with embedding extraction

3. **Fusion & Output**:
   - Weighted average of all available modalities
   - Risk score (0-1) and confidence calculation
   - Risk category assignment
   - Explanation generation

## Data Requirements

### Clinical Parameters (15 features):
1. `gender` (int): 0=Female, 1=Male
2. `age` (int): Patient age in years
3. `currentSmoker` (int): Current smoking status (0/1)
4. `cigsPerDay` (float): Cigarettes per day
5. `BPMeds` (float): Blood pressure medication (0/1)
6. `prevalentStroke` (int): History of stroke (0/1)
7. `prevalentHyp` (int): Hypertension (0/1)
8. `diabetes` (int): Diabetes status (0/1)
9. `totChol` (float): Total cholesterol (mg/dL)
10. `sysBP` (float): Systolic blood pressure (mmHg)
11. `diaBP` (float): Diastolic blood pressure (mmHg)
12. `BMI` (float): Body Mass Index (kg/m²)
13. `heartRate` (float): Heart rate (bpm)
14. `glucose` (float): Glucose level (mg/dL)
15. `CP` (int): Chest pain type (0-3)

### Image Requirements:
- **X-ray**: PNG/JPG format, chest X-ray images
- **ECG**: PNG/JPG/CSV/TXT format, ECG signals or images
- **Size Limit**: 10MB per file
- **Supported Formats**: .png, .jpg, .jpeg, .bmp

## API Endpoints

### Public Endpoints:
- `GET /health` - Health check
- `POST /auth/register` - User registration
- `POST /auth/login` - User login (returns JWT)

### Protected Endpoints (require JWT):
- `GET /auth/me` - Current user info
- `POST /patients` - Create patient record
- `GET /patients` - List patients (paginated)
- `GET /patients/{id}` - Get specific patient
- `PUT /patients/{id}` - Update patient
- `DELETE /patients/{id}` - Delete patient
- `GET /patients/search` - Search patients
- `GET /patients/stats/summary` - Patient statistics
- `POST /predictions` - Create prediction (upload X-ray, ECG, clinical data)
- `GET /predictions` - List predictions (paginated)
- `GET /predictions/{id}` - Get specific prediction
- `DELETE /predictions/{id}` - Delete prediction
- `GET /predictions/patient/{patient_id}` - Get predictions for patient
- `GET /predictions/stats/summary` - Prediction statistics

### Admin Endpoints (require admin role):
- `GET /admin/users` - List all users
- `GET /admin/users/{user_id}` - Get user details
- `PUT /admin/users/{user_id}` - Update user
- `DELETE /admin/users/{user_id}` - Delete user
- `POST /admin/users/{user_id}/toggle-active` - Toggle user active status
- `GET /admin/stats` - System statistics

## Project Structure

```
AyuPulseApp/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry
│   │   ├── core/                   # Core configurations
│   │   │   ├── config.py           # Settings
│   │   │   ├── security.py         # Password hashing, JWT
│   │   │   ├── database.py         # MongoDB connection
│   │   │   ├── exceptions.py       # Custom exception handlers
│   │   │   └── middleware.py       # Request/response middleware
│   │   ├── models/                 # MongoDB document models
│   │   │   ├── user.py
│   │   │   ├── patient.py
│   │   │   └── prediction.py
│   │   ├── schemas/                # Pydantic schemas
│   │   │   ├── auth.py
│   │   │   ├── patient.py
│   │   │   ├── prediction.py
│   │   │   └── response.py
│   │   ├── routes/                 # API route handlers
│   │   │   ├── auth.py
│   │   │   ├── patients.py
│   │   │   ├── predictions.py
│   │   │   ├── health.py
│   │   │   └── admin.py
│   │   ├── services/               # Business logic
│   │   │   └── prediction_service.py
│   │   ├── ml/                     # Machine learning
│   │   │   ├── preprocessing.py
│   │   │   ├── xray_model.py
│   │   │   ├── ecg_model.py
│   │   │   ├── clinical_model.py
│   │   │   ├── fusion_model.py
│   │   │   └── explainability.py
│   │   └── utils/                  # Utilities
│   │       └── file_ops.py
│   ├── uploads/                    # Uploaded files
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # Environment variables
│   └── README.md                   # Backend documentation
├── frontend/
│   ├── src/
│   │   ├── App.tsx                 # Main React component
│   │   ├── config.ts               # API configuration
│   │   ├── components/             # React components
│   │   │   └── auth/
│   │   │       ├── LoginForm.tsx
│   │   │       ├── RegisterForm.tsx
│   │   │       └── ForgotPasswordForm.tsx
│   │   ├── context/                # React context
│   │   │   └── AuthContext.tsx
│   │   ├── pages/                  # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   └── Patients.tsx
│   │   ├── services/               # API services
│   │   │   ├── auth.service.ts
│   │   │   └── patient.service.ts
│   │   └── assets/                 # Static assets
│   ├── package.json                # Frontend dependencies
│   └── README.md                   # Frontend documentation
└── data/                           # Sample datasets
    ├── patient_heart_parameters.csv
    ├── xray/                       # X-ray images
    │   ├── true/                   # With heart disease
    │   └── false/                  # Normal
    └── ecg/                        # ECG images
        └── train/                  # Training data
```

## How It Works - Complete Workflow

### 1. User Authentication
- User registers/login via frontend
- JWT token issued and stored in localStorage
- All subsequent requests include token in Authorization header

### 2. Patient Management
- Doctor creates patient record with demographic info
- Patient records stored in MongoDB with unique IDs
- Patients can be searched, updated, or deleted

### 3. Prediction Process
1. **Data Collection**:
   - User selects existing patient or creates new one
   - Enters 15 clinical parameters via form
   - Optionally uploads X-ray and/or ECG images

2. **Backend Processing**:
   - Files saved to uploads directory
   - Clinical data validated against schema
   - ML pipeline executed asynchronously

3. **ML Pipeline Execution**:
   - Preprocessing: Scaling, normalization, tensor conversion
   - Model inference: Clinical, X-ray, ECG models run in parallel
   - Fusion: Weighted combination of model outputs
   - Explanation: SHAP values and text explanations generated

4. **Result Storage & Return**:
   - Prediction saved to database with all metadata
   - Response includes risk score, category, confidence, explanations
   - Frontend displays results with visualizations

### 4. Result Interpretation
- **Risk Score (0-1)**: Higher = greater risk
- **Risk Category**: Low/Medium/High with color coding
- **Confidence**: Model certainty (0-1)
- **Contributing Features**: Top risk factors with SHAP values
- **Recommendations**: Suggested next steps based on risk level

## Technology Stack

### Backend:
- **Python 3.9+** with FastAPI framework
- **MongoDB** (NoSQL database)
- **Motor** (async MongoDB driver)
- **Pydantic** (data validation)
- **PyJWT** (JWT authentication)
- **PyTorch** (deep learning)
- **scikit-learn** (machine learning)
- **SHAP** (explainable AI)
- **OpenCV/PIL** (image processing)
- **Uvicorn** (ASGI server)

### Frontend:
- **React 18** with TypeScript
- **Vite** (build tool)
- **Tailwind CSS** (styling)
- **Lucide React** (icons)
- **React Router** (navigation)
- **Axios** (HTTP client)

### Development Tools:
- **Git** (version control)
- **Pytest** (backend testing)
- **ESLint** (code linting)
- **Postman/Insomnia** (API testing)

## Setup & Deployment Requirements

### Prerequisites:
1. **Python 3.9+** with pip
2. **Node.js 18+** with npm
3. **MongoDB** (local or Atlas)
4. **Virtual environment** (recommended)

### Backend Setup:
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Configure environment variables
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup:
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables (Backend):
```
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=ayupulse
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## Current Status & Limitations

### Implemented Features:
- ✅ Full backend API with authentication
- ✅ Patient CRUD operations
- ✅ Prediction pipeline with dummy ML models
- ✅ File upload handling
- ✅ Basic frontend landing page
- ✅ API documentation (Swagger UI)
- ✅ Error handling and validation
- ✅ Role-based access control

### Current Limitations (as noted in code):
- **ML Models are dummy implementations** - For demonstration only
- **File storage is local** - Not suitable for production at scale
- **Limited frontend pages** - Only landing page implemented
- **Basic authentication** - No email verification, password reset
- **No real-time updates** - Traditional request/response model

### Areas for Enhancement:
1. **ML Model Training**: Replace dummy models with trained models
2. **Cloud Storage**: Integrate AWS S3/Azure Blob for file storage
3. **Frontend Completion**: Implement all pages (dashboard, patients, predictions)
4. **Real-time Features**: WebSocket notifications for long predictions
5. **Advanced Analytics**: Patient trend analysis, cohort studies
6. **Mobile App**: React Native companion app
7. **HIPAA Compliance**: Enhanced security for healthcare data

## Use Cases & Target Audience

### Primary Users:
1. **Cardiologists & Physicians**: For preliminary risk assessment
2. **Hospital Systems**: Integrated into patient management workflows
3. **Telemedicine Platforms**: Remote heart disease screening
4. **Medical Researchers**: Data collection and analysis tool

### Secondary Users:
1. **Patients**: Self-assessment with doctor supervision
2. **Insurance Companies**: Risk assessment for underwriting
3. **Public Health Organizations**: Population health monitoring

## Business Value Proposition

1. **Early Detection**: Identify at-risk patients before symptoms manifest
2. **Cost Reduction**: Reduce expensive diagnostic procedures through screening
3. **Time Efficiency**: Quick assessments (seconds vs. days for traditional tests)
4. **Explainability**: Transparent AI builds trust with medical professionals
5. **Scalability**: Cloud-ready architecture for large-scale deployment
6. **Integration**: REST API allows integration with existing healthcare systems

## Ethical Considerations & Compliance

### Data Privacy:
- Patient data encryption at rest and in transit
- Role-based access control
- Audit logging of all data accesses
- Data anonymization for research purposes

### Medical Disclaimer:
- **Not a diagnostic tool** - For screening and risk assessment only
- **Requires physician interpretation** - All results must be reviewed by medical professionals
- **False positives/negatives possible** - ML models have inherent limitations

### Regulatory Considerations:
- HIPAA compliance needed for US deployment
- GDPR compliance for European users
- Medical device regulations (FDA Class II potentially)

## Conclusion

AyuPulseApp represents a modern approach to cardiovascular risk assessment, combining the latest in web technology with explainable AI. While currently in a demonstration state with dummy ML models, the architecture is production-ready and can be enhanced with trained models and additional features. The system provides a foundation for scalable, secure, and user-friendly heart disease prediction that can be integrated into various healthcare workflows.

The project demonstrates best practices in full-stack development, including:
- Clean architecture with separation of concerns
- Comprehensive API design with proper error handling
- Secure authentication and authorization
- Modular ML pipeline for easy model swapping
- Responsive frontend with modern UX principles