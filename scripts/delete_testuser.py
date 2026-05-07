#!/usr/bin/env python3
"""
Delete testuser@gmail.com from the database
"""
import asyncio
import motor.motor_asyncio
from bson import ObjectId

async def delete_testuser():
    # Connect directly to MongoDB
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.ayupulse
    
    # Delete testuser@gmail.com
    result = await db.users.delete_one({'email': 'testuser@gmail.com'})
    
    if result.deleted_count > 0:
        print(f"Deleted {result.deleted_count} user(s) with email testuser@gmail.com")
    else:
        print("User testuser@gmail.com not found")
    
    # Verify deletion
    user = await db.users.find_one({'email': 'testuser@gmail.com'})
    if not user:
        print("Verification: User no longer exists")
    else:
        print("ERROR: User still exists!")
    
    # Also delete any other test users that might cause conflicts
    test_emails = ['test@example.com', 'demo@example.com', 'user@example.com']
    for email in test_emails:
        result = await db.users.delete_one({'email': email})
        if result.deleted_count > 0:
            print(f"Deleted test user with email: {email}")
    
    print("Cleanup completed")

if __name__ == "__main__":
    asyncio.run(delete_testuser())