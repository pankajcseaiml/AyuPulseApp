# AyuPulseApp Deployment Guide

This guide covers deployment instructions for the AyuPulseApp backend and frontend applications.

## Backend Deployment (Railway / Render)
- Set environment variables: `MONGODB_URL`, `SECRET_KEY`, `BACKEND_CORS_ORIGINS`.
- Build command: `pip install -r requirements.txt`.
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

## Frontend Deployment (Vercel)
- Set environment variable: `VITE_API_URL` pointing to backend.
- Build command: `npm run build`.
- Output directory: `dist`.
