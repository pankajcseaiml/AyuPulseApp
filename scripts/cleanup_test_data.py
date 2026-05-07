#!/usr/bin/env python3
"""
Cleanup utility for test data in AyuPulseApp.
This script removes test users, predictions, and other test data.
"""

import os
import sys
from datetime import datetime, timedelta
from pymongo import MongoClient

def get_database_connection():
    """Establish MongoDB connection."""
    mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
    database_name = os.getenv('DATABASE_NAME', 'ayupulse')
    
    client = MongoClient(mongodb_url)
    db = client[database_name]
    return db

def list_test_users(db):
    """List all test users."""
    test_users = db.users.find({
        'email': {'$regex': 'test|demo|example', '$options': 'i'}
    })
    
    print("\nTest Users Found:")
    print("-" * 80)
    for user in test_users:
        print(f"ID: {user['_id']}")
        print(f"Name: {user.get('name', 'N/A')}")
        print(f"Email: {user.get('email', 'N/A')}")
        print(f"Role: {user.get('role', 'N/A')}")
        print(f"Created: {user.get('created_at', 'N/A')}")
        print("-" * 80)
    
    return test_users

def delete_old_predictions(db, days_old=7):
    """Delete predictions older than specified days."""
    cutoff_date = datetime.now() - timedelta(days=days_old)
    
    result = db.predictions.delete_many({
        'created_at': {'$lt': cutoff_date}
    })
    
    print(f"Deleted {result.deleted_count} predictions older than {days_old} days.")
    return result.deleted_count

def delete_test_users(db):
    """Delete test users and their associated data."""
    # Find test users
    test_users = list(db.users.find({
        'email': {'$regex': 'test|demo|example', '$options': 'i'}
    }))
    
    deleted_count = 0
    for user in test_users:
        user_id = str(user['_id'])
        
        # Delete associated data
        db.userprofiles.delete_many({'user_id': user_id})
        db.patients.delete_many({'user_id': user_id})
        db.predictions.delete_many({'user_id': user_id})
        
        # Delete the user
        db.users.delete_one({'_id': user['_id']})
        deleted_count += 1
        
        print(f"Deleted user: {user.get('email')} (ID: {user_id})")
    
    print(f"\nTotal deleted: {deleted_count} test users and their associated data.")
    return deleted_count

def cleanup_orphaned_data(db):
    """Clean up orphaned data (profiles, patients, predictions without users)."""
    # Get all user IDs
    user_ids = [str(user['_id']) for user in db.users.find({}, {'_id': 1})]
    
    # Clean orphaned profiles
    profiles_result = db.userprofiles.delete_many({
        'user_id': {'$nin': user_ids}
    })
    
    # Clean orphaned patients
    patients_result = db.patients.delete_many({
        'user_id': {'$nin': user_ids}
    })
    
    # Clean orphaned predictions
    predictions_result = db.predictions.delete_many({
        'user_id': {'$nin': user_ids}
    })
    
    print(f"\nCleaned orphaned data:")
    print(f"  - Profiles: {profiles_result.deleted_count}")
    print(f"  - Patients: {patients_result.deleted_count}")
    print(f"  - Predictions: {predictions_result.deleted_count}")
    
    return {
        'profiles': profiles_result.deleted_count,
        'patients': patients_result.deleted_count,
        'predictions': predictions_result.deleted_count
    }

def get_database_stats(db):
    """Get database statistics."""
    stats = {
        'users': db.users.count_documents({}),
        'profiles': db.userprofiles.count_documents({}),
        'patients': db.patients.count_documents({}),
        'predictions': db.predictions.count_documents({}),
        'audit_logs': db.auditlogs.count_documents({})
    }
    
    print("\nDatabase Statistics:")
    print("-" * 80)
    for collection, count in stats.items():
        print(f"{collection.capitalize()}: {count}")
    print("-" * 80)
    
    return stats

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python cleanup_test_data.py [command]")
        print("Commands: stats, list, cleanup, delete-test, delete-old")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    db = get_database_connection()
    
    if command == 'stats':
        get_database_stats(db)
    
    elif command == 'list':
        list_test_users(db)
    
    elif command == 'cleanup':
        cleanup_orphaned_data(db)
    
    elif command == 'delete-test':
        confirm = input("Are you sure you want to delete all test users and their data? (yes/no): ")
        if confirm.lower() == 'yes':
            delete_test_users(db)
        else:
            print("Operation cancelled.")
    
    elif command == 'delete-old':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        confirm = input(f"Delete predictions older than {days} days? (yes/no): ")
        if confirm.lower() == 'yes':
            delete_old_predictions(db, days)
        else:
            print("Operation cancelled.")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()