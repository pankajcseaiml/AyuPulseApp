import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def update_staff_to_doctor():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.ayupulse
    
    # Update staff -> doctor
    result = await db.users.update_many({"role": "staff"}, {"$set": {"role": "doctor"}})
    print(f"Updated {result.modified_count} staff -> doctor")
    
    # Verify update
    count = await db.users.count_documents({"role": "staff"})
    print(f"Users with staff role after update: {count}")
    
    # Show all users
    print("\nAll users after update:")
    async for user in db.users.find():
        print(f"  - {user.get('username', 'N/A')}: {user.get('role', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(update_staff_to_doctor())