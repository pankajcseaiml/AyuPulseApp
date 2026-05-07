#!/usr/bin/env python3
"""
Script to update user roles in MongoDB.
Sets all existing users to 'patient' role unless they are admin.
"""
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def update_user_roles():
    # Connect to MongoDB
    mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongodb_url)
    db = client.ayupulse
    users_collection = db.users
    
    print("Checking existing users...")
    
    # Count total users
    total_users = await users_collection.count_documents({})
    print(f"Total users in database: {total_users}")
    
    # List all users
    async for user in users_collection.find():
        user_id = user.get('_id')
        name = user.get('name', 'N/A')
        email = user.get('email', 'N/A')
        current_role = user.get('role', 'doctor')  # Default was 'doctor' in old schema
        print(f"User: {name} ({email}) - Current role: {current_role}")
    
    # Update all users to 'patient' role (except any existing admins)
    print("\nUpdating user roles...")
    result = await users_collection.update_many(
        {"role": {"$ne": "admin"}},  # Don't update admins
        {"$set": {"role": "patient"}}
    )
    
    print(f"Updated {result.modified_count} users to 'patient' role")
    
    # Also update any users with role 'doctor' or 'staff' to 'patient'
    result2 = await users_collection.update_many(
        {"role": {"$in": ["doctor", "staff"]}},
        {"$set": {"role": "patient"}}
    )
    
    print(f"Updated {result2.modified_count} doctor/staff users to 'patient'")
    
    # Show updated users
    print("\nUpdated user list:")
    async for user in users_collection.find():
        user_id = user.get('_id')
        name = user.get('name', 'N/A')
        email = user.get('email', 'N/A')
        updated_role = user.get('role', 'patient')
        print(f"User: {name} ({email}) - Updated role: {updated_role}")
    
    client.close()
    print("\nUser role update completed!")

if __name__ == "__main__":
    asyncio.run(update_user_roles())