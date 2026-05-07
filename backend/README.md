# AyuPulseApp – Backend

Early Heart Disease Risk Prediction System backend built with FastAPI, MongoDB, and ML.

## Features

- **User Authentication**: JWT‑based registration/login with role‑based access (doctor/admin).
- **Patient Management**: CRUD operations for patient records.
- **Multi‑modal Prediction**: Combines chest X‑ray, ECG, and clinical data.
- **Explainable AI**: SHAP values and plain‑English explanations.
- **Modular ML Pipeline**: Separate models for X‑ray, ECG, clinical data, with fusion.
- **File Upload**: Support for image/CSV uploads with validation.
- **Production‑ready**: Environment variables, CORS, error handling.

## Tech Stack

- **FastAPI** – Modern Python web framework
- **MongoDB** – NoSQL database (via Motor async driver)
- **Pydantic** – Data validation and settings management
- **JWT** – JSON Web Tokens for authentication
- **PyTorch** / **scikit‑learn** – Machine learning models
- **SHAP** – Model explainability
- **OpenCV/PIL** – Image preprocessing
- **Uvicorn** – ASGI server

## Project Structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── core/                   # Core configurations
│   │   ├── config.py           # Settings
│   │   ├── security.py         # Password hashing, JWT
│   │   ├── database.py         # MongoDB connection
│   │   ├── exceptions.py       # Custom exception handlers
│   │   └── middleware.py       # Request/response middleware
│   ├── models/                 # MongoDB document models
│   │   ├── user.py
│   │   ├── patient.py
│   │   └── prediction.py
│   ├── schemas/                # Pydantic request/response schemas
│   │   ├── auth.py
│   │   ├── patient.py
│   │   ├── prediction.py
│   │   └── response.py
│   ├── routes/                 # API route handlers
│   │   ├── auth.py
│   │   ├── patients.py
│   │   ├── predictions.py
│   │   ├── health.py
│   │   └── admin.py
│   ├── services/               # Business logic
│   │   └── prediction_service.py
│   ├── ml/                     # Machine learning modules
│   │   ├── preprocessing.py
│   │   ├── xray_model.py
│   │   ├── ecg_model.py
│   │   ├── clinical_model.py
│   │   ├── fusion_model.py
│   │   └── explainability.py
│   └── utils/                  # Utility functions
│       └── file_ops.py
├── uploads/                    # Uploaded files (created at runtime)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (template)
└── README.md                   # This file
```

## Setup

### 1. Prerequisites

- Python 3.9+
- MongoDB running locally (default: `mongodb://localhost:27017`)
- Virtual environment recommended

### 2. Install dependencies

```bash
cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and adjust if needed:

```bash
cp .env .env.local
```

Default values are fine for local development.

### 4. Run the backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

Interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

## API Endpoints

### Public
- `GET /health` – Health check
- `POST /auth/register` – Register a new user
- `POST /auth/login` – Login, receive JWT token

### Protected (require JWT)
- `GET /auth/me` – Get current user info
- `POST /patients` – Create a patient
- `GET /patients` – List patients (with pagination)
- `GET /patients/{id}` – Get a patient
- `PUT /patients/{id}` – Update a patient
- `DELETE /patients/{id}` – Delete a patient
- `GET /patients/search` – Search patients by name, age, gender
- `GET /patients/stats/summary` – Get patient statistics
- `POST /predictions` – Create a prediction (upload X‑ray, ECG, clinical data)
- `GET /predictions` – List predictions (with pagination)
- `GET /predictions/{id}` – Get a prediction
- `DELETE /predictions/{id}` – Delete a prediction
- `GET /predictions/patient/{patient_id}` – Get predictions for a patient
- `GET /predictions/stats/summary` – Get prediction statistics

### Admin (require admin role)
- `GET /admin/users` – List all users (with filtering)
- `GET /admin/users/{user_id}` – Get user details
- `PUT /admin/users/{user_id}` – Update user (role, active status, etc.)
- `DELETE /admin/users/{user_id}` – Delete a user
- `POST /admin/users/{user_id}/toggle-active` – Toggle user active status
- `GET /admin/stats` – Get system statistics (users, patients, predictions)

## Error Handling & Response Schemas

The API uses standardized response formats for both success and error responses.

### Success Responses
All successful responses follow a consistent structure:
- **StandardResponse**: `{ "success": true, "message": "...", "data": {...}, "timestamp": "..." }`
- **PaginatedResponse**: Includes pagination metadata (`total`, `page`, `limit`, `has_next`, `has_prev`)
- **StatsResponse**: For statistics endpoints
- **HealthResponse**: For health checks
- **DeleteResponse**: For delete operations
- **FileUploadResponse**: For file uploads

### Error Responses
All errors return a consistent error format:
- **HTTP 4xx/5xx errors**: `{ "success": false, "error": "...", "code": "...", "detail": "...", "timestamp": "..." }`
- **Validation errors**: Include additional `errors` array with field-specific details

### Custom Exception Handlers
The backend includes comprehensive exception handling:
- `HTTPException`: Standard FastAPI HTTP exceptions
- `AyuPulseException`: Custom application exceptions (NotFound, Unauthorized, Validation, etc.)
- `RequestValidationError`: Pydantic validation errors with detailed field information
- Global exception handler for unexpected errors

### Middleware
- **LoggingMiddleware**: Logs all HTTP requests and responses with timing
- **SecurityHeadersMiddleware**: Adds security headers (X-Content-Type-Options, X-Frame-Options, etc.)

## Prediction Pipeline

1. **Input**: Clinical parameters (JSON), optional X‑ray image, optional ECG image.
2. **Preprocessing**:
   - X‑ray: resize, normalize, convert to tensor.
   - ECG: same as X‑ray.
   - Clinical: scale using trained scaler.
3. **Model Inference**:
   - X‑ray CNN extracts embedding.
   - ECG CNN extracts embedding.
   - Clinical Random Forest outputs probability.
4. **Fusion**: Weighted average of the three modalities.
5. **Explainability**:
   - SHAP values for clinical features.
   - Plain‑English explanation text.
6. **Output**: Risk score (0–1), risk category (Low/Medium/High), confidence, explanation.

## Data Sources

The backend expects the following data directories (already present in the workspace):

- `data/xray/true/` – X‑ray images with heart disease
- `data/xray/false/` – Normal X‑ray images
- `data/ecg/` – ECG images (train/test splits)
- `data/patient_heart_parameters.csv` – Clinical dataset with 15 features + target

## Development Notes

- The ML models are **dummy implementations** for demonstration. In production, replace with trained models.
- File uploads are stored locally in `uploads/`. Consider cloud storage for scalability.
- MongoDB collections are created automatically on first insert.
- Windows paths are handled correctly (use `os.path.join`).

## Testing

The backend includes comprehensive test coverage for key endpoints:

### Test Files
- `test_health.py` – Tests for health and info endpoints
- `test_auth.py` – Tests for user registration, login, and authentication

### Running Tests
```bash
cd backend
pytest app/tests/ -v
```

### Test Features
- Uses FastAPI TestClient for isolated testing
- Tests both success and error scenarios
- Validates response schemas and status codes
- Tests authentication and authorization

## Deployment

For production:

1. Set `DEBUG=False` in config.
2. Use a strong `SECRET_KEY`.
3. Use a production MongoDB (Atlas, or replica set).
4. Serve with Gunicorn + Uvicorn workers.
5. Set up reverse proxy (Nginx/Apache) with HTTPS.

## License

Proprietary – AyuPulseApp.