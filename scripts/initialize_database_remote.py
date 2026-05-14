#!/usr/bin/env python3
"""
Initialize the remote MongoDB database with default users and data.
Uses the same connection string as the backend.
"""
import asyncio
import motor.motor_asyncio
from datetime import datetime
import bcrypt
import os
import sys

# Add backend to path to use the same config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
from app.core.config import settings

async def initialize_database():
    # Use the same MongoDB URL as the backend
    mongodb_url = settings.MONGODB_URL
    print(f"Connecting to MongoDB at: {mongodb_url}")
    
    client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
    db = client.get_default_database()
    
    # Check if users already exist
    users_count = await db.users.count_documents({})
    if users_count > 0:
        print(f"Database already has {users_count} users. Skipping initialization.")
        
        # List existing users
        cursor = db.users.find({})
        async for user in cursor:
            print(f"  - {user.get('email')} (username: {user.get('username')}, role: {user.get('role')})")
        
        client.close()
        return
    
    print("Initializing database with default users...")
    
    # Hash passwords (matching frontend demo credentials)
    admin_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
    doctor_hash = bcrypt.hashpw("doctor123".encode(), bcrypt.gensalt()).decode()
    staff_hash = bcrypt.hashpw("staff123".encode(), bcrypt.gensalt()).decode()
    patient_hash = bcrypt.hashpw("patient123".encode(), bcrypt.gensalt()).decode()
    
    # Create default users with usernames
    default_users = [
        {
            "name": "Admin User",
            "email": "admin@ayupulse.com",
            "username": "admin",
            "hashed_password": admin_hash,
            "role": "admin",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Test Doctor",
            "email": "doctor@ayupulse.com",
            "username": "doctor",
            "hashed_password": doctor_hash,
            "role": "doctor",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Test Staff",
            "email": "staff@ayupulse.com",
            "username": "staff",
            "hashed_password": staff_hash,
            "role": "staff",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Test Patient",
            "email": "patient@ayupulse.com",
            "username": "patient",
            "hashed_password": patient_hash,
            "role": "patient",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    # Insert users
    result = await db.users.insert_many(default_users)
    print(f"Inserted {len(result.inserted_ids)} users:")
    
    for user in default_users:
        print(f"  - {user['email']} (username: {user['username']}, role: {user['role']}) - password: {user['username']}123")
    
    # Create indexes (ignore if they already exist)
    try:
        await db.users.create_index("email", unique=True)
        print("Created unique index on email field.")
    except Exception as e:
        print(f"Note: Email index already exists or error: {e}")
    
    try:
        await db.users.create_index("username", unique=True)
        print("Created unique index on username field.")
    except Exception as e:
        print(f"Note: Username index already exists or error: {e}")
    
    try:
        await db.users.create_index("role")
        print("Created index on role field.")
    except Exception as e:
        print(f"Note: Role index already exists or error: {e}")
    
    client.close()
    print("Database initialization completed successfully!")

if __name__ == "__main__":
    asyncio.run(initialize_database())