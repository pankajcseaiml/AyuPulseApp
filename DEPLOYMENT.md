# AyuPulseApp Deployment Guide

This guide covers different deployment options for AyuPulseApp.

## 1. Local Development

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB (local or Docker)

### Steps
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AyuPulseApp
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Start Services**
   ```bash
   # Terminal 1: MongoDB
   mongod
   
   # Terminal 2: Backend
   cd backend
   venv\Scripts\activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Terminal 3: Frontend
   cd frontend
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:5174
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 2. Docker Deployment (Deprecated)

> **Note**: Docker deployment files have been removed from this project. The project now runs natively without containerization.

If you need Docker deployment, you can recreate the Docker configuration using:
- `backend/Dockerfile`: Python 3.10-slim based image
- `frontend/Dockerfile`: Node.js 18-alpine based image
- `docker-compose.yml`: Multi-service orchestration with MongoDB

## 3. Production Deployment

### Option A: Traditional Server (Ubuntu 22.04)

1. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install -y python3.10 python3.10-venv nodejs npm nginx mongodb
   ```

2. **Setup backend**
   ```bash
   cd /opt
   git clone <repository-url> ayupulse
   cd ayupulse/backend
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with production values
   ```

3. **Setup frontend**
   ```bash
   cd ../frontend
   npm install
   npm run build
   ```

4. **Configure systemd services**
   ```bash
   # Create backend service
   sudo nano /etc/systemd/system/ayupulse-backend.service
   ```

   ```ini
   [Unit]
   Description=AyuPulse Backend Service
   After=network.target mongodb.service
   
   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/opt/ayupulse/backend
   Environment="PATH=/opt/ayupulse/backend/venv/bin"
   ExecStart=/opt/ayupulse/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

5. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/ayupulse
   ```

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       # Frontend
       location / {
           root /opt/ayupulse/frontend/dist;
           try_files $uri $uri/ /index.html;
       }
       
       # Backend API
       location /api/ {
           proxy_pass http://localhost:8000/;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
       
       # Static files
       location /static/ {
           alias /opt/ayupulse/backend/uploads/;
       }
   }
   ```

6. **Enable and start services**
   ```bash
   sudo systemctl enable ayupulse-backend
   sudo systemctl start ayupulse-backend
   sudo systemctl restart nginx
   ```

### Option B: Cloud Platforms

#### Recommended Stack: Vercel + Railway + MongoDB Atlas
This is the recommended modern deployment stack for AyuPulseApp, providing excellent scalability, ease of use, and cost-effectiveness.

##### Step 1: MongoDB Atlas Setup
1. **Create MongoDB Atlas Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Sign up for a free account (512MB storage, shared cluster)

2. **Create a Cluster**
   - Click "Create a Cluster"
   - Choose the FREE tier (M0 Sandbox)
   - Select your preferred cloud provider (AWS, Google Cloud, or Azure)
   - Choose region closest to your users
   - Click "Create Cluster" (takes 1-3 minutes)

3. **Configure Database Access**
   - Go to "Database Access" → "Add New Database User"
   - Create a username and strong password
   - Set privileges: "Read and write to any database"
   - Click "Add User"

4. **Configure Network Access**
   - Go to "Network Access" → "Add IP Address"
   - For Railway deployment: Add `0.0.0.0/0` (allow from anywhere)
   - Or add specific Railway IP ranges if known

5. **Get Connection String**
   - Go to "Database" → "Connect" → "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your actual password
   - Example: `mongodb+srv://username:password@cluster0.mongodb.net/ayupulse?retryWrites=true&w=majority`

##### Step 2: Railway Backend Deployment
1. **Create Railway Account**
   - Go to [Railway](https://railway.app/)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project" → "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select the AyuPulseApp repository

3. **Configure Backend Service**
   - Railway will auto-detect the Python backend
   - Set the root directory to `backend`
   - Railway will automatically install dependencies from `requirements.txt`

4. **Set Environment Variables**
   Add these variables in Railway dashboard:
   ```
   MONGODB_URL=your_mongodb_atlas_connection_string
   DATABASE_NAME=ayupulse
   SECRET_KEY=your_secure_random_secret_key_here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DEBUG=False
   BACKEND_CORS_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:5173
   MAX_UPLOAD_SIZE=10485760
   ALLOWED_IMAGE_TYPES=image/jpeg,image/png,image/jpg
   PORT=8000
   ```

5. **Deploy**
   - Railway will automatically deploy when you push to GitHub
   - Or trigger manual deployment from dashboard
   - Get your backend URL (e.g., `https://ayupulse-backend.up.railway.app`)

##### Step 3: Vercel Frontend Deployment
1. **Create Vercel Account**
   - Go to [Vercel](https://vercel.com/)
   - Sign up with GitHub

2. **Import Project**
   - Click "Add New" → "Project"
   - Import your GitHub repository
   - Vercel will auto-detect React project

3. **Configure Build Settings**
   - Root directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

4. **Set Environment Variables**
   Add these variables in Vercel dashboard:
   ```
   VITE_API_URL=https://your-railway-backend-url.up.railway.app
   VITE_APP_NAME=AyuPulse
   VITE_APP_VERSION=1.0.0
   ```

5. **Deploy**
   - Click "Deploy"
   - Vercel will build and deploy your frontend
   - Get your frontend URL (e.g., `https://ayupulse.vercel.app`)

6. **Update CORS in Backend**
   - Go back to Railway backend environment variables
   - Update `BACKEND_CORS_ORIGINS` to include your Vercel URL
   - Example: `https://ayupulse.vercel.app,http://localhost:5173`

##### Step 4: Verify Deployment
1. **Test Backend API**
   - Visit: `https://your-railway-backend-url.up.railway.app/docs`
   - Should see FastAPI Swagger documentation

2. **Test Frontend**
   - Visit your Vercel URL
   - Should see AyuPulseApp landing page
   - Try login with demo accounts

3. **Test Database Connection**
   - Create a test user via registration
   - Check MongoDB Atlas dashboard for new data

#### Alternative Cloud Platforms

##### Heroku
```bash
# Backend
heroku create ayupulse-backend
heroku addons:create mongolab:sandbox
heroku config:set SECRET_KEY=your-secret-key
git push heroku main

# Frontend
cd frontend
npm run build
# Deploy build folder to Netlify/Vercel
```

##### AWS Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize EB
eb init -p python-3.10 ayupulse-backend
eb create ayupulse-prod
```

## 4. Environment Variables

### Required Variables
- `MONGODB_URL`: MongoDB connection string
- `DATABASE_NAME`: Database name (default: ayupulse)
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiry (default: 30)

### Optional Variables
- `DEBUG`: Enable debug mode (default: False in production)
- `BACKEND_CORS_ORIGINS`: CORS allowed origins
- `MAX_UPLOAD_SIZE`: Maximum file upload size in bytes
- `ALLOWED_IMAGE_TYPES`: Allowed image MIME types

## 5. Security Considerations

1. **Change default passwords**: Update MongoDB and admin user passwords
2. **Use HTTPS**: Configure SSL certificates for production
3. **Set strong SECRET_KEY**: Use a cryptographically secure random key
4. **Enable firewall**: Restrict access to necessary ports only
5. **Regular updates**: Keep dependencies updated
6. **Backup strategy**: Implement regular database backups

## 6. Monitoring and Maintenance

### Logs
```bash
# Backend logs
journalctl -u ayupulse-backend -f

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

### Health Checks
- API Health: `GET /health`
- Service Info: `GET /info`

### Backup
```bash
# MongoDB backup
mongodump --uri="mongodb://localhost:27017/ayupulse" --out=/backup/ayupulse-$(date +%Y%m%d)

# Restore
mongorestore --uri="mongodb://localhost:27017/ayupulse" /backup/ayupulse-20250101
```

## 7. Troubleshooting

### Common Issues

1. **MongoDB connection failed**
   - Check if MongoDB is running: `systemctl status mongodb`
   - Verify connection string in .env file

2. **CORS errors**
   - Ensure `BACKEND_CORS_ORIGINS` includes frontend URL
   - Check browser console for specific errors

3. **File upload issues**
   - Verify upload directory permissions
   - Check `MAX_UPLOAD_SIZE` configuration

4. **JWT authentication failures**
   - Verify `SECRET_KEY` is consistent
   - Check token expiry time

### Support
For additional support, check:
- API Documentation: http://your-domain.com/docs
- GitHub Issues: <repository-url>/issues
- Application logs: `journalctl -u ayupulse-backend`