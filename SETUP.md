# AutoRescue Setup Guide

## ✅ Setup Complete!

### Database Configuration
- **Database Name**: `autorescue_v2`
- **Host**: `localhost`
- **Port**: `3306`
- **User**: `root`
- **Password**: (empty)
- **Driver**: MySQL via PyMySQL

### ✅ What's Been Fixed:

1. **Database**: Now configured for XAMPP MySQL
2. **Models**: Added proper relationships and validation
   - `users.py` - User table with timestamps
   - `request.py` - ServiceRequest with foreign keys
   - `mechanic.py` - Mechanic profile with ratings
3. **App Routes**: Fixed with error handling and JSON responses
   - Register with validation
   - Login with password checking
   - Request mechanic with location
   - Accept request endpoint
4. **Dependencies**: All installed correctly

### 🚀 Quick Start:

#### 1. Start XAMPP
```
- Open XAMPP Control Panel
- Start Apache
- Start MySQL
```

#### 2. Access Database (Optional)
```
- Go to: http://localhost/phpmyadmin
- Database: autorescue_v2
- View tables: users, service_requests, mechanics
```

#### 3. Start Flask App
```powershell
cd C:\AutoRescue
python app.py
```

#### 4. Access Application
```
- Open browser: http://127.0.0.1:5000
- Click "Register" or "Login"
```

### 👤 Test Login Credentials:

**Customer Account:**
- Email: `customer@example.com`
- Password: `password123`

**Mechanic Account:**
- Email: `mechanic@example.com`
- Password: `password123`

**Admin Account:**
- Email: `admin@example.com`
- Password: `admin123`

### 📊 Database Tables Created:

1. **users** - All user accounts (customers, mechanics, admins)
2. **service_requests** - Service requests from customers
3. **mechanics** - Mechanic shop details and ratings

### 🔧 Troubleshooting:

**Issue**: "Connection refused" error
```
→ Make sure XAMPP MySQL is running
→ Check config.py has correct database name: autorescue_v2
```

**Issue**: "Module not found"
```
→ Run: pip install -r requirements.txt
```

**Issue**: "No such table"
```
→ Run: python init_db.py
```

### 📝 File Structure:
```
AutoRescue/
├── app.py                    # Main Flask app
├── config.py                 # XAMPP MySQL config
├── init_db.py               # Database initialization
├── requirements.txt         # Dependencies
├── models/
│   ├── users.py            # User model
│   ├── request.py          # ServiceRequest model
│   └── mechanic.py         # Mechanic model
├── templates/              # HTML templates
├── static/                 # CSS, JS files
└── uploads/               # File uploads
```

### 🎯 Next Steps:

1. Update HTML templates with proper forms
2. Implement customer dashboard
3. Implement mechanic dashboard
4. Add location-based mechanic matching
5. Add payment integration

### ❌ Errors Fixed:
- ✅ String latitude/longitude → Float conversion
- ✅ Missing error handling in routes
- ✅ Removed string returns, added JSON responses
- ✅ Added input validation
- ✅ Added database rollback on errors
- ✅ Added timestamp fields to models
- ✅ Added proper foreign key relationships

---
**Everything is ready to go!** 🚗✨
