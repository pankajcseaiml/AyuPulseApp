import asyncio
import motor.motor_asyncio
from bson import ObjectId

async def check_users():
    # Connect to MongoDB
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.ayupulse
    
    # Get users collection
    users_collection = db.users
    
    # Count users
    count = await users_collection.count_documents({})
    print(f"Total users in database: {count}")
    
    # List all users
    cursor = users_collection.find({})
    async for user in cursor:
        print(f"User: {user.get('email')}, Name: {user.get('name')}, Role: {user.get('role')}")
        # Don't print password hash for security
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_users())