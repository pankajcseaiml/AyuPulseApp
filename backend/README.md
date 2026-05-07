# AyuPulseApp – Backend

Early Heart Disease Risk Prediction System backend built with FastAPI, MongoDB, and ML.

## Features

- **User Authentication**: JWT‑based registration/login with role‑based access (admin, doctor, patient).
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
│   │   ├── profile.py
│   │   └── admin.py
│   ├── ml/                     # Machine learning pipeline
│   │   ├── clinical_model.py
│   │   ├── ecg_model.py
│   │   ├── xray_model.py
│   │   ├── fusion_model.py
│   │   ├── preprocessing.py
│   │   └── explainability.py
│   └── services/               # Business logic services
│       └── prediction_service.py
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.10+** – Download from [python.org](https://www.python.org/downloads/)
2. **MongoDB** – Either:
   - Local MongoDB installation ([Download](https://www.mongodb.com/try/download/community))
   - MongoDB Atlas cloud instance ([Sign up](https://www.mongodb.com/cloud/atlas/register))
3. **Git** – For cloning the repository ([Download](https://git-scm.com/downloads))

## Step-by-Step Setup Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/pankajcseaiml/AyuPulseApp.git
cd AyuPulseApp/backend
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env  # Windows
   # or
   cp .env.example .env    # Linux/Mac
   ```

2. Edit the `.env` file with your configuration:
   ```env
   PROJECT_NAME="AyuPulseApp API"
   VERSION="1.0.0"
   MONGODB_URL="mongodb://localhost:27017"
   MONGODB_DB_NAME="ayupulse_db"
   SECRET_KEY="your-super-secret-key-change-this-in-production"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   UPLOAD_DIR="uploads"
   BACKEND_CORS_ORIGINS='["http://localhost:5173", "http://localhost:3000"]'
   ```

   **Important Notes:**
   - `MONGODB_URL`: Change to your MongoDB connection string
   - `SECRET_KEY`: Generate a strong secret key for JWT tokens
   - `BACKEND_CORS_ORIGINS`: Add frontend URLs that should be allowed

### Step 5: Initialize MongoDB

Ensure MongoDB is running:

```bash
# Start MongoDB service (Windows)
net start MongoDB

# Or start MongoDB daemon (Linux/Mac)
sudo systemctl start mongod
```

### Step 6: Run Database Initialization (Optional)

If you want to create initial admin user and test data:

```bash
python scripts/initialize_database.py
```

### Step 7: Start the Backend Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 8: Verify Backend is Running

Open your browser and navigate to:

1. **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
2. **Alternative Docs**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
3. **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

You should see the FastAPI interactive documentation with all available endpoints.

## Running in Production

For production deployment, use:

```bash
# Install production dependencies
pip install gunicorn

# Run with gunicorn (Linux/Mac)
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Or with uvicorn directly
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Authentication
- `POST /auth/register` – Register new user
- `POST /auth/login` – Login and get JWT token
- `GET /auth/me` – Get current user info

### Predictions
- `POST /predictions` – Create new prediction
- `GET /predictions` – List user predictions
- `GET /predictions/{id}` – Get prediction details
- `DELETE /predictions/{id}` – Delete prediction
- `GET /predictions/stats/summary` – Get prediction statistics

### Patients
- `POST /patients` – Create patient record
- `GET /patients` – List patients
- `GET /patients/{id}` – Get patient details
- `PUT /patients/{id}` – Update patient
- `DELETE /patients/{id}` – Delete patient

### Admin (Admin role required)
- `POST /admin/users` – Create user
- `GET /admin/users` – List all users
- `PUT /admin/users/{id}` – Update user
- `DELETE /admin/users/{id}` – Delete user
- `GET /admin/stats` – System statistics

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run specific test file
pytest app/tests/test_auth.py

# Run with coverage
pytest --cov=app
```

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB is running: `mongod --version`
   - Check connection string in `.env` file
   - Verify network connectivity

2. **Port Already in Use**
   - Change port in command: `--port 8001`
   - Find and kill process using port 8000

3. **Missing Dependencies**
   - Reinstall requirements: `pip install -r requirements.txt`
   - Check Python version: `python --version`

4. **Environment Variables Not Loaded**
   - Ensure `.env` file is in `backend/` directory
   - Restart the server after changing `.env`

## Demo Accounts

For testing purposes, you can use these demo accounts:

- **Admin**: `admin@example.com` / `admin123`
- **Doctor**: `doctor@example.com` / `doctor123`
- **Patient**: `patient@example.com` / `patient123`

## Support

If you encounter issues:
1. Check the [GitHub Issues](https://github.com/pankajcseaiml/AyuPulseApp/issues)
2. Review the API documentation at `/docs`
3. Ensure all prerequisites are met

## License

This project is licensed under the MIT License.