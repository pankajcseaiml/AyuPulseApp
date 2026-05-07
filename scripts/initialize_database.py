#!/usr/bin/env python3
"""
Initialize the MongoDB database with default users and data.
"""
import asyncio
import motor.motor_asyncio
from datetime import datetime
import bcrypt

async def initialize_database():
    # Connect to MongoDB
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.ayupulse
    
    # Check if users already exist
    users_count = await db.users.count_documents({})
    if users_count > 0:
        print(f"Database already has {users_count} users. Skipping initialization.")
        
        # List existing users
        cursor = db.users.find({})
        async for user in cursor:
            print(f"  - {user.get('email')} ({user.get('role')})")
        
        client.close()
        return
    
    print("Initializing database with default users...")
    
    # Hash passwords
    password_hash = bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode()
    admin_hash = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
    
    # Create default users
    default_users = [
        {
            "name": "Admin User",
            "email": "admin@ayupulse.com",
            "hashed_password": admin_hash,
            "role": "admin",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Test Doctor",
            "email": "doctor@ayupulse.com",
            "hashed_password": password_hash,
            "role": "doctor",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Test Staff",
            "email": "staff@ayupulse.com",
            "hashed_password": password_hash,
            "role": "staff",
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Test Patient",
            "email": "patient@ayupulse.com",
            "hashed_password": password_hash,
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
        print(f"  - {user['email']} ({user['role']}) - password: {'admin123' if user['email'] == 'admin@ayupulse.com' else 'password123'}")
    
    # Create indexes (ignore if they already exist)
    try:
        await db.users.create_index("email", unique=True)
        print("Created unique index on email field.")
    except Exception as e:
        print(f"Note: Email index already exists or error: {e}")
    
    try:
        await db.users.create_index("role")
        print("Created index on role field.")
    except Exception as e:
        print(f"Note: Role index already exists or error: {e}")
    
    client.close()
    print("Database initialization completed successfully!")

if __name__ == "__main__":
    asyncio.run(initialize_database())