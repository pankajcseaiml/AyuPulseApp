# AyuPulseApp – Frontend

Modern React-based frontend for the Early Heart Disease Risk Prediction System.

## Features

- **Responsive Dashboard**: Real-time metrics, charts, and prediction history
- **Role-Based UI**: Tailored interfaces for Admin, Doctor, and Patient roles
- **Multi-step Prediction**: Guided workflow for clinical data, X-ray, and ECG uploads
- **Interactive Results**: Visual risk meters, SHAP charts, and Grad-CAM heatmaps
- **Patient Management**: CRUD operations for patient records
- **Authentication**: JWT-based login with demo accounts
- **Modern UI**: Built with Tailwind CSS, Lucide icons, and Recharts

## Tech Stack

- **React 18** – UI library with hooks
- **TypeScript** – Type-safe development
- **Vite** – Fast build tool and dev server
- **Tailwind CSS** – Utility-first styling
- **React Router** – Client-side routing
- **React Hook Form + Zod** – Form validation
- **Axios** – HTTP client with interceptors
- **Recharts** – Data visualization
- **Lucide React** – Icon library
- **Context API** – State management for auth

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── auth/           # Login, Register, ForgotPassword forms
│   │   ├── forms/          # ClinicalForm, ImageUpload
│   │   ├── layout/         # Navbar, Sidebar, Footer, DashboardLayout
│   │   └── ui/             # Badge, MetricCard, RiskMeter, ShapChart, GradCamViewer
│   ├── context/            # React context providers (AuthContext)
│   ├── pages/              # Route-level components
│   │   ├── Dashboard.tsx
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── AdminPage.tsx
│   │   ├── PatientsPage.tsx
│   │   ├── NewPredictionPage.tsx
│   │   ├── ResultsPage.tsx
│   │   ├── HistoryPage.tsx
│   │   ├── ProfilePage.tsx
│   │   └── LandingPage.tsx
│   ├── services/           # API service classes
│   │   ├── auth.service.ts
│   │   └── patient.service.ts
│   ├── api/                # API client modules
│   │   ├── auth.ts
│   │   ├── patients.ts
│   │   ├── predictions.ts
│   │   ├── admin.ts
│   │   ├── profile.ts
│   │   └── base.ts
│   ├── config.ts           # API endpoints and routes
│   ├── App.tsx             # Root component with routing
│   ├── main.tsx            # Entry point
│   ├── App.css             # Global styles
│   └── index.css           # Tailwind imports
├── public/                 # Static assets
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## Role System

The application supports three user roles:

1. **Admin** – Full system access, user management, system statistics
2. **Doctor** – Create predictions, manage patients, view all patient data
3. **Patient** – View own predictions, personal profile, limited dashboard

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend server running (see backend/README.md)
- MongoDB instance

### Installation

1. Clone the repository
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```
4. Configure environment (if needed):
   - Copy `.env.example` to `.env.local`
   - Update `VITE_API_BASE_URL` to point to your backend

### Development

Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

### Testing

Run the TypeScript compiler:
```bash
npm run type-check
```

## API Integration

The frontend communicates with the backend via REST API. Key endpoints:

- `POST /auth/login` – User authentication
- `GET /auth/me` – Get current user
- `POST /predictions` – Create new prediction
- `GET /predictions` – List user predictions
- `GET /patients` – List patients
- `GET /admin/users` – List users (admin only)

## Demo Accounts

For quick testing, use these demo credentials:

- **Admin**: username `admin`, password `admin123`
- **Doctor**: username `doctor`, password `doctor123`
- **Patient**: username `patient`, password `patient123`

## Key Components

### Dashboard
Displays user-specific metrics, recent predictions, and risk trend charts.

### New Prediction Page
Multi-step form for:
1. Clinical parameters (age, blood pressure, cholesterol, etc.)
2. X-ray image upload with preview
3. ECG image upload with preview
4. Results with risk score and explanations

### Results Page
Shows prediction details including:
- Risk score with visual meter
- SHAP feature importance chart
- Grad-CAM heatmaps for X-ray/ECG
- Plain English explanation
- Reference ranges for clinical parameters

### Admin Page
User management interface for administrators:
- Create new users
- Toggle user active status
- View system statistics

## Styling

The UI uses Tailwind CSS with a custom color palette defined in `tailwind.config.js`:

- Primary: `#3b82f6` (blue-500)
- Secondary: `#10b981` (emerald-500)
- Navy: `#1e293b` (slate-800)
- Background gradients and shadows for depth

## Deployment

The frontend can be deployed as static files. A sample `nginx.conf` is provided for production serving.

## License

Proprietary – For AyuPulse internal use only.
