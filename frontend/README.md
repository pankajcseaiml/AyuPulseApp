# AyuPulseApp – Frontend

React-based frontend for the AyuPulse cardiovascular risk prediction system. Provides an intuitive interface for healthcare professionals and patients to interact with the AI-powered prediction engine.

## Features

- **Modern Dashboard**: Real-time statistics, recent predictions, and risk trend visualization
- **Multi-step Prediction Form**: Guided workflow for clinical data, X-ray, and ECG uploads
- **Interactive Results**: Detailed risk breakdown with SHAP charts and GradCAM visualizations
- **Patient Management**: Create and manage patient profiles for family members
- **Role-based Access**: Different interfaces for admin, doctor, and patient roles
- **Responsive Design**: Fully responsive layout optimized for desktop and tablet

## Tech Stack

- **React 19** – Frontend library with hooks
- **TypeScript** – Type-safe JavaScript
- **Vite** – Fast build tool and dev server
- **TailwindCSS** – Utility-first CSS framework
- **React Router v7** – Client-side routing
- **Recharts** – Charting library for data visualization
- **React Hook Form** – Form handling with validation
- **Axios** – HTTP client for API calls
- **Context API** – State management for authentication

## Project Structure

```
frontend/
├── public/                    # Static assets
│   ├── favicon.svg
│   └── icons.svg
├── src/
│   ├── api/                  # API service modules
│   │   ├── auth.ts
│   │   ├── patients.ts
│   │   ├── predictions.ts
│   │   ├── profile.ts
│   │   └── base.ts
│   ├── assets/               # Images, fonts, etc.
│   │   ├── hero.png
│   │   └── react.svg
│   ├── components/           # Reusable UI components
│   │   ├── auth/            # Authentication forms
│   │   ├── forms/           # Form components
│   │   ├── layout/          # Layout components
│   │   ├── patient/         # Patient-related components
│   │   └── ui/              # Generic UI components
│   ├── context/             # React context providers
│   │   └── AuthContext.tsx
│   ├── hooks/               # Custom React hooks
│   ├── pages/               # Page components
│   │   ├── Dashboard.tsx
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── NewPredictionPage.tsx
│   │   ├── ResultsPage.tsx
│   │   ├── PatientsPage.tsx
│   │   ├── ProfilePage.tsx
│   │   ├── AdminPage.tsx
│   │   └── LandingPage.tsx
│   ├── services/            # Business logic services
│   │   └── auth.service.ts
│   ├── utils/               # Utility functions
│   ├── App.tsx              # Main app component
│   ├── App.css              # Global styles
│   ├── index.css            # Tailwind imports
│   └── main.tsx             # Application entry point
├── package.json             # Dependencies and scripts
├── vite.config.ts           # Vite configuration
├── tailwind.config.js       # Tailwind configuration
└── tsconfig.json            # TypeScript configuration
```

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Node.js 18+** – Download from [nodejs.org](https://nodejs.org/)
2. **npm 9+** or **yarn** – Comes with Node.js
3. **Backend Server** – The AyuPulse backend must be running (see backend README)
4. **Git** – For cloning the repository

## Step-by-Step Setup Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/pankajcseaiml/AyuPulseApp.git
cd AyuPulseApp/frontend
```

### Step 2: Install Dependencies

```bash
npm install
# or
yarn install
```

### Step 3: Configure Environment Variables

1. Create a `.env` file in the `frontend/` directory:
   ```bash
   # Windows
   copy .env.example .env
   # Linux/Mac
   cp .env.example .env
   ```

2. Edit the `.env` file:
   ```env
   # Backend API URL (default: localhost:8000)
   VITE_API_URL=http://localhost:8000
   
   # Optional: Frontend port (default: 5173)
   # VITE_PORT=5173
   
   # Optional: Enable/disable features
   # VITE_ENABLE_ANALYTICS=false
   ```

   **Important:** Ensure the `VITE_API_URL` matches your backend server address.

### Step 4: Start the Development Server

```bash
npm run dev
# or
yarn dev
```

The application will start and be available at [http://localhost:5173](http://localhost:5173).

### Step 5: Verify Frontend is Running

1. Open your browser and navigate to [http://localhost:5173](http://localhost:5173)
2. You should see the AyuPulse landing page
3. Click "Get Started" to navigate to the login page

## Connecting to Backend

The frontend communicates with the backend API. Ensure:

1. **Backend is running** on the URL specified in `VITE_API_URL`
2. **CORS is configured** in backend to allow requests from frontend origin
3. **API endpoints are accessible** – Test by visiting `http://localhost:8000/health`

## Building for Production

### Create Production Build

```bash
npm run build
# or
yarn build
```

This creates an optimized production build in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
# or
yarn preview
```

This serves the production build locally for testing.

### Deploy to Hosting Service

The `dist/` folder contains static files that can be deployed to:

- **Vercel**: `vercel --prod`
- **Netlify**: `netlify deploy --prod`
- **GitHub Pages**: See deployment guide in root README
- **Any static hosting**: Upload `dist/` contents to your hosting provider

## Available Scripts

- `npm run dev` – Start development server with hot reload
- `npm run build` – Build for production
- `npm run preview` – Preview production build locally
- `npm run lint` – Run ESLint to check code quality
- `npm run type-check` – Run TypeScript type checking

## Application Flow

### 1. Authentication
- **Landing Page** → **Login/Register** → **Dashboard**
- Users can register as patients or use demo accounts
- Doctors and admins require backend creation

### 2. Dashboard
- Overview of recent predictions and statistics
- Quick access to create new prediction
- Navigation to patients, profile, and admin pages

### 3. Creating a Prediction
1. Click "New Prediction" on dashboard
2. **Step 1**: Enter clinical parameters (15 fields)
3. **Step 2**: Upload chest X-ray image (optional)
4. **Step 3**: Upload ECG image (optional)
5. **Step 4**: Review and submit
6. **Results Page**: View risk score, explanations, and recommendations

### 4. Patient Management
- Create patient profiles for family members
- View prediction history for each patient
- Update patient medical information

### 5. Admin Panel (Admin role only)
- User management (create, update, delete users)
- System statistics and monitoring
- Access to all prediction data

## Role System

The application supports three user roles:

### 1. **Patient**
- Create personal predictions
- Manage own profile
- View personal prediction history

### 2. **Doctor**
- All patient capabilities
- Create predictions for patients
- View all patients under their care
- Access to medical reporting features

### 3. **Admin**
- All doctor capabilities
- User management
- System administration
- Access to all data and statistics

## Demo Accounts

For testing, you can use these credentials:

| Role | Email | Password |
|------|-------|----------|
| Admin | `admin@example.com` | `admin123` |
| Doctor | `doctor@example.com` | `doctor123` |
| Patient | `patient@example.com` | `patient123` |

Click the "Demo Login" buttons on the login page for quick access.

## Styling

The application uses **TailwindCSS** with a custom theme:

- **Primary Color**: Navy blue (`#1e3a8a`)
- **Secondary Color**: Teal (`#0d9488`)
- **Fonts**: Sora (headings), DM Sans (body)
- **Components**: Custom button styles, cards, and form elements

To modify styles:
1. Edit `tailwind.config.js` for theme changes
2. Edit `src/index.css` for global styles
3. Use Tailwind utility classes in components

## API Integration

The frontend communicates with the backend via REST API:

- **Authentication**: JWT tokens stored in localStorage
- **API Client**: Axios instance in `src/api/base.ts`
- **Error Handling**: Global interceptors for token refresh and error display
- **Type Safety**: TypeScript interfaces for all API responses

## Troubleshooting

### Common Issues

1. **Backend Connection Failed**
   ```
   Error: Network Error
   ```
   - Check if backend is running: `curl http://localhost:8000/health`
   - Verify `VITE_API_URL` in `.env` file
   - Check CORS configuration in backend

2. **Build Errors**
   ```
   Cannot find module 'recharts'
   ```
   - Reinstall dependencies: `npm install`
   - Clear npm cache: `npm cache clean --force`

3. **TypeScript Errors**
   ```
   Type 'X' is not assignable to type 'Y'
   ```
   - Run type check: `npm run type-check`
   - Check interface definitions in API files

4. **Page Not Loading**
   - Clear browser cache
   - Check console for errors (F12 → Console)
   - Restart development server

### Development Tips

1. **Hot Reload**: Changes to components automatically refresh the page
2. **ESLint**: Fix linting errors with `npm run lint -- --fix`
3. **Type Checking**: Run `npm run type-check` to verify TypeScript types
4. **Browser DevTools**: Use React DevTools extension for component inspection

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License.
