import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def update_roles():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.ayupulse
    
    # Update healthcare_staff -> staff
    result = await db.users.update_many({"role": "healthcare_staff"}, {"$set": {"role": "staff"}})
    print(f"Updated {result.modified_count} healthcare_staff -> staff")
    
    # Update doctor_physician -> doctor
    result = await db.users.update_many({"role": "doctor_physician"}, {"$set": {"role": "doctor"}})
    print(f"Updated {result.modified_count} doctor_physician -> doctor")

    # Update any role that is not patient, doctor, staff, or admin to patient
    valid_roles = ["patient", "doctor", "staff", "admin"]
    result = await db.users.update_many({"role": {"$nin": valid_roles}}, {"$set": {"role": "patient"}})
    print(f"Updated {result.modified_count} invalid roles -> patient")

if __name__ == "__main__":
    asyncio.run(update_roles())
