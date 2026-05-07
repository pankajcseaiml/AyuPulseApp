// MongoDB initialization script for AyuPulseApp
db = db.getSiblingDB('ayupulse');

// Create collections
db.createCollection('users');
db.createCollection('userprofiles');
db.createCollection('patients');
db.createCollection('predictions');
db.createCollection('auditlogs');

// Create indexes
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ role: 1 });
db.userprofiles.createIndex({ user_id: 1 }, { unique: true });
db.patients.createIndex({ user_id: 1 });
db.patients.createIndex({ created_at: -1 });
db.predictions.createIndex({ user_id: 1 });
db.predictions.createIndex({ created_at: -1 });
db.predictions.createIndex({ risk_category: 1 });
db.auditlogs.createIndex({ timestamp: -1 });
db.auditlogs.createIndex({ user_id: 1 });

// Create initial admin user (password: admin123)
db.users.insertOne({
    name: "Admin User",
    email: "admin@ayupulse.com",
    hashed_password: "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", // bcrypt hash of "admin123"
    role: "admin",
    is_active: true,
    created_at: new Date(),
    updated_at: new Date()
});

// Create initial test users
db.users.insertOne({
    name: "Test Doctor",
    email: "doctor@ayupulse.com",
    hashed_password: "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", // bcrypt hash of "password123"
    role: "doctor",
    is_active: true,
    created_at: new Date(),
    updated_at: new Date()
});

db.users.insertOne({
    name: "Test Staff",
    email: "staff@ayupulse.com",
    hashed_password: "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", // bcrypt hash of "password123"
    role: "staff",
    is_active: true,
    created_at: new Date(),
    updated_at: new Date()
});

db.users.insertOne({
    name: "Test Patient",
    email: "patient@ayupulse.com",
    hashed_password: "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW", // bcrypt hash of "password123"
    role: "patient",
    is_active: true,
    created_at: new Date(),
    updated_at: new Date()
});

print("MongoDB initialization completed successfully!");