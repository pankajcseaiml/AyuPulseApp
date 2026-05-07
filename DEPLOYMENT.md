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

#### Heroku
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

#### AWS Elastic Beanstalk
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
- API Health: `GET /api/health`
- Service Info: `GET /api/info`

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