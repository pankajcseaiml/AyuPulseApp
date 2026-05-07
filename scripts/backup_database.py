#!/usr/bin/env python3
"""
Database backup utility for AyuPulseApp.
This script creates a backup of the MongoDB database.
"""

import os
import sys
import subprocess
import datetime
import json
from pathlib import Path

def load_config():
    """Load configuration from environment or config file."""
    config = {
        'mongodb_url': os.getenv('MONGODB_URL', 'mongodb://localhost:27017'),
        'database_name': os.getenv('DATABASE_NAME', 'ayupulse'),
        'backup_dir': os.getenv('BACKUP_DIR', './backups'),
        'retention_days': int(os.getenv('BACKUP_RETENTION_DAYS', '30'))
    }
    return config

def create_backup(config):
    """Create a MongoDB backup."""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = Path(config['backup_dir']) / f"ayupulse_backup_{timestamp}"
    
    # Create backup directory
    backup_path.mkdir(parents=True, exist_ok=True)
    
    # Run mongodump
    cmd = [
        'mongodump',
        '--uri', config['mongodb_url'],
        '--db', config['database_name'],
        '--out', str(backup_path)
    ]
    
    print(f"Creating backup at: {backup_path}")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Backup completed successfully!")
        
        # Create metadata file
        metadata = {
            'timestamp': timestamp,
            'database': config['database_name'],
            'backup_path': str(backup_path),
            'size': get_directory_size(backup_path)
        }
        
        metadata_file = backup_path / 'metadata.json'
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Backup size: {metadata['size']} bytes")
        return backup_path
        
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Error: mongodump not found. Make sure MongoDB tools are installed.")
        return None

def get_directory_size(path):
    """Calculate directory size in bytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size

def cleanup_old_backups(config):
    """Remove backups older than retention period."""
    backup_dir = Path(config['backup_dir'])
    if not backup_dir.exists():
        return
    
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=config['retention_days'])
    
    for item in backup_dir.iterdir():
        if item.is_dir() and item.name.startswith('ayupulse_backup_'):
            # Extract timestamp from directory name
            try:
                timestamp_str = item.name.replace('ayupulse_backup_', '')
                backup_date = datetime.datetime.strptime(timestamp_str[:8], '%Y%m%d')
                
                if backup_date < cutoff_date.date():
                    print(f"Removing old backup: {item.name}")
                    import shutil
                    shutil.rmtree(item)
            except (ValueError, IndexError):
                continue

def list_backups(config):
    """List all available backups."""
    backup_dir = Path(config['backup_dir'])
    if not backup_dir.exists():
        print("No backups found.")
        return
    
    backups = []
    for item in backup_dir.iterdir():
        if item.is_dir() and item.name.startswith('ayupulse_backup_'):
            metadata_file = item / 'metadata.json'
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                backups.append(metadata)
    
    if not backups:
        print("No backups found.")
        return
    
    print(f"\nFound {len(backups)} backup(s):")
    print("-" * 80)
    for backup in sorted(backups, key=lambda x: x['timestamp'], reverse=True):
        size_mb = backup['size'] / (1024 * 1024)
        print(f"Timestamp: {backup['timestamp']}")
        print(f"Database: {backup['database']}")
        print(f"Size: {size_mb:.2f} MB")
        print(f"Path: {backup['backup_path']}")
        print("-" * 80)

def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python backup_database.py [command]")
        print("Commands: create, list, cleanup, restore")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    config = load_config()
    
    if command == 'create':
        create_backup(config)
        cleanup_old_backups(config)
    elif command == 'list':
        list_backups(config)
    elif command == 'cleanup':
        cleanup_old_backups(config)
        print("Cleanup completed.")
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("Usage: python backup_database.py restore [backup_timestamp]")
            sys.exit(1)
        print("Restore functionality not implemented in this script.")
        print("Use: mongorestore --uri=<mongodb_url> --db=<database_name> <backup_path>")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == '__main__':
    main()