# HotelEase - Hotel Management System

## 📋 Overview

**HotelEase** is a comprehensive web-based Hotel Management System built with Flask and MySQL. It provides a complete solution for managing hotel operations including room bookings, guest management, employee scheduling, service orders, and business analytics.

The system is designed with a modern, responsive UI and includes advanced features like real-time occupancy tracking, VIP guest management, audit logging, and detailed reporting.

---

## ✨ Features

### 🏨 Core Functionality
- **Room Management:** Track room availability, status, and pricing
- **Guest Management:** Register guests, manage contact information, maintain guest history
- **Booking System:** Create and manage room reservations with automatic room status updates
- **Service Orders:** Add additional services to bookings with automatic cost calculation
- **Invoice Generation:** Generate professional invoices for completed bookings
- **Payment Tracking:** Record and manage payment methods and amounts

### 👨‍💼 Admin & Staff Management
- **Employee Directory:** Manage staff information, roles, shifts, and salaries
- **User Authentication:** Secure login system with role-based access control
- **Access Levels:** Admin, Manager, Receptionist, and Staff roles
- **Audit Logging:** Track all database changes with timestamp and action details

### 📊 Analytics & Reporting
- **Business Intelligence Dashboard:** View key metrics and KPIs
- **Revenue Reports:** Track total revenue from room bookings and services
- **Occupancy Analysis:** Monitor room occupancy rates with visual charts
- **VIP Guest Ranking:** Identify top-spending guests with lifetime spending analysis
- **Service Performance:** Analyze high-value services and their revenue contribution
- **Shift Analytics:** View staff shift overlaps and team information

### 🔐 Security & Data Integrity
- **Trigger-Based Validation:** Prevent double-booking with database triggers
- **Stored Procedures:** Automated booking completion and room status updates
- **Transaction Management:** ACID-compliant booking transactions
- **Audit Trail:** Complete audit log of all modifications

### 📱 User Interface
- **Responsive Design:** Mobile-friendly dashboard layout
- **Real-time Charts:** Interactive revenue trend visualization
- **Intuitive Navigation:** Sidebar-based menu system
- **Flash Messages:** User feedback on all operations
- **Bootstrap 5.3:** Modern, professional styling

---

## 🛠️ Technology Stack

### Backend
- **Framework:** Flask 3.0.0
- **Database:** MySQL (PyMySQL 1.1.0)
- **ORM:** SQLAlchemy via Flask-SQLAlchemy 3.1.1
- **Language:** Python 3.x

### Frontend
- **Template Engine:** Jinja2
- **CSS Framework:** Bootstrap 5.3.0
- **Icons:** Font Awesome 6.4.0
- **Charts:** Chart.js
- **Typography:** Google Inter Font

### Database Features
- **Views:** RoomOccupancy, ShiftOverlap, PackagePossibilities
- **Stored Procedures:** CheckAvailability, CompleteBooking
- **Functions:** GetGuestLevel (VIP classification)
- **Triggers:** PreventDoubleBooking, BeforeServiceOrderInsert, LogGuestDeletion

---

## 📦 Project Structure

```
HotelEase_Project/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── hotel.py               # Room, RoomType, Service models
│   │   ├── user.py                # User authentication model
│   │   ├── staff.py               # Employee and Maintenance models
│   │   └── operation.py           # Guest, Booking, Payment, Feedback models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py         # Login/Logout routes
│   │   ├── admin_routes.py        # Admin dashboard & management
│   │   ├── front_desk.py          # Booking & room management
│   │   ├── guest_api.py           # Guest search API
│   │   └── report_routes.py       # Analytics & reporting
│   ├── services/
│   │   └── db_utils.py            # Database utility functions
│   ├── static/
│   │   ├── css/
│   │   │   └── dashboard.css      # Main stylesheet
│   │   ├── js/
│   │   │   └── main.js            # Frontend JavaScript
│   │   └── img/                   # Images folder
│   └── templates/
│       ├── base.html              # Base template with sidebar
│       ├── auth/
│       │   └── login.html         # Login page
│       ├── admin/
│       │   ├── dashboard.html     # Executive overview
│       │   ├── employees.html     # Employee directory
│       │   ├── guests.html        # Guest management
│       │   ├── reports.html       # Analytics dashboard
│       │   └── audit_logs.html    # Audit trail
│       └── reception/
│           ├── room_grid.html     # Room status display
│           ├── booking_form.html  # Booking creation
│           ├── booking_details.html# Booking management
│           └── invoice.html       # Invoice generation
├── config.py                       # Configuration settings
├── run.py                         # Application entry point
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables
└── README.md                     # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd HotelEase_Project
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create/edit `.env` file with your database credentials:

```env
DB_HOST=localhost
DB_USER=root
DB_PASS=your_password
DB_NAME=HotelEase

SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### Step 5: Set Up Database (MySQL)

This project requires a MySQL database. Follow the steps below to create the database, create a dedicated MySQL user, and import the schema, stored procedures, triggers, and optional sample data.

1. **Create the MySQL database and a dedicated user** (run in `mysql` or a client like MySQL Workbench):

```sql
-- create the database with UTF8 support
CREATE DATABASE HotelEase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- create a dedicated user (change password to a secure value)
CREATE USER 'hotease_user'@'localhost' IDENTIFIED BY 'your_secure_password';

-- grant appropriate privileges
GRANT ALL PRIVILEGES ON HotelEase.* TO 'hotease_user'@'localhost';
FLUSH PRIVILEGES;
```

2. **Prepare SQL files**

Place the SQL files that define your schema, views, stored procedures and triggers into a folder at the project root, for example `sql/`.

Recommended files (examples):

- `sql/schema.sql` — table definitions (Users, Guests, Rooms, Bookings, Services, Employees, AuditLog, etc.)
- `sql/views.sql` — view definitions (RoomOccupancy, ShiftOverlap, PackagePossibilities)
- `sql/procs.sql` — stored procedures (CheckAvailability, CompleteBooking)
- `sql/triggers.sql` — triggers (PreventDoubleBooking, BeforeServiceOrderInsert, LogGuestDeletion)
- `sql/sample_data.sql` — optional seed/sample data

3. **Import the SQL files**

From the project root you can import each file using the `mysql` client. Replace the username and file paths as appropriate.

```powershell
# Import schema
mysql -u hotease_user -p HotelEase < sql/schema.sql

# Import views (if separate)
mysql -u hotease_user -p HotelEase < sql/views.sql

# Import stored procedures
mysql -u hotease_user -p HotelEase < sql/procs.sql

# Import triggers
mysql -u hotease_user -p HotelEase < sql/triggers.sql

# (Optional) Import sample data
mysql -u hotease_user -p HotelEase < sql/sample_data.sql
```

4. **Environment variables**

Create or update the `.env` file in the project root with your MySQL connection settings:

```env
DB_HOST=localhost
DB_USER=hotease_user
DB_PASS=your_secure_password
DB_NAME=HotelEase
SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

5. **Notes on stored procedures, triggers and views**

- Some routes rely on stored procedures and triggers (e.g. `CompleteBooking`, `PreventDoubleBooking`) — ensure those SQL definitions are imported before testing those features.
- If you do not have `sql/` files in the repo, ask the project maintainer for the SQL export or generate them from an existing MySQL instance.

6. **Alternative: migrations**

If you prefer to manage schema changes via migrations, add `Flask-Migrate` to the project and create initial migrations. (This README currently assumes direct SQL import.)

### Step 6: Run the Application
```bash
python run.py
```

The application will start on `http://localhost:5000`

---

## 📖 Usage Guide

### Login
1. Navigate to `http://localhost:5000`
2. You'll be redirected to the login page
3. Enter credentials provided by the system administrator
4. Click "Sign In"

### Dashboard
Once logged in, you'll see the executive overview with:
- Total Revenue
- Active Guests
- Room Occupancy
- System Health
- Recent Activity
- Revenue Trends Chart

### Room Management
1. Go to **Room Status** from the sidebar
2. View all rooms with their current status
3. Click **New Booking** to create a reservation

### Booking Management
1. Click **New Booking** from the sidebar
2. Select a guest from the dropdown
3. Choose available room
4. Set check-in and check-out dates
5. Price is calculated automatically
6. Confirm booking

### Guest Management
1. Go to **Guests** from the sidebar
2. View all registered guests
3. Edit or delete guest profiles
4. Track booking history per guest

### Service Orders
1. Open a booking from **Booking Details**
2. Add services (spa, room service, etc.)
3. Specify quantity
4. Service costs calculated automatically

### Invoice Generation
1. Open a booking
2. Click **View Invoice**
3. Review charges and services
4. Print or export invoice

### Analytics & Reports
1. Go to **Analytics & BI** from the sidebar
2. View VIP guest rankings
3. Check high-value services
4. Monitor shift teams and occupancy
5. Print reports

### Audit Logs
1. Go to **Security Logs** from the sidebar
2. Review all database modifications
3. Track deletions, insertions, and updates
4. Check timestamps and details

---

## 🔐 Authentication & Roles

### User Roles
- **Admin:** Full system access, user management, reports
- **Manager:** Guest/booking management, reports
- **Receptionist:** Booking creation, guest check-in/out
- **Staff:** View-only access, service fulfillment

### Login Credentials
Contact your system administrator for login credentials.

---

## 🗄️ Database Schema

### Main Tables
- **Users:** Authentication and user information
- **Guests:** Guest profiles and contact details
- **Rooms:** Room inventory and status
- **RoomTypes:** Room categories and pricing
- **Bookings:** Reservation records
- **Payments:** Payment tracking
- **ServiceOrders:** Services ordered with bookings
- **Services:** Available services catalog
- **Employees:** Staff information
- **AuditLog:** System audit trail

### Database Views
- **RoomOccupancy:** Room booking history
- **ShiftOverlap:** Staff shift coordination
- **PackagePossibilities:** Service package options

### Stored Procedures
- **CheckAvailability:** Verify room availability
- **CompleteBooking:** Finalize booking and update room status

---

## 🐛 Troubleshooting

### Database Connection Issues
- Verify MySQL is running
- Check credentials in `.env` file
- Ensure database exists: `SHOW DATABASES;`
- Test connection: `mysql -u root -p`

### Port Already in Use
```bash
# Change port in run.py or use:
python run.py --port 5001
```

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Database Errors
- Clear old sessions: Check Flask session configuration
- Verify table permissions: `GRANT ALL PRIVILEGES ON HotelEase.* TO 'user'@'localhost';`

---

## 📝 Notes for Developers

### Adding New Features
1. Create model in `app/models/`
2. Add route in `app/routes/`
3. Create template in `app/templates/`
4. Update sidebar navigation in `base.html`

### Database Changes
- Update SQLAlchemy models
- Run migrations or alter tables directly
- Update stored procedures as needed

### Style Modifications
- Edit `app/static/css/dashboard.css`
- Bootstrap classes are available in all templates
- Colors defined in CSS variables

### JavaScript Updates
- All JavaScript consolidated in `app/static/js/main.js`
- Chart.js for data visualization
- Bootstrap JS for components

---

## 🔄 Project Status

### Completed Features ✅
- ✅ User authentication system
- ✅ Room and guest management
- ✅ Booking system with validation
- ✅ Service orders with auto-calculation
- ✅ Invoice generation
- ✅ Admin dashboard with charts
- ✅ Analytics and reporting
- ✅ Audit logging
- ✅ All UI buttons functional

### Upcoming Features 🚀
- Guest registration portal
- Password reset functionality
- Email notifications
- SMS alerts for check-in/out
- Mobile app
- Advanced reporting exports
- Staff scheduling system

---

## 📧 Support

For issues, questions, or feature requests:
1. Check troubleshooting section
2. Review database schema
3. Check Flask error logs
4. Contact system administrator

---

## 📄 License

This project is proprietary hotel management software. All rights reserved.

---

## 👥 Contributors

- **Project Lead:** [Your Name]
- **Database Design:** [Your Name]
- **Frontend Development:** [Your Name]
- **Backend Development:** [Your Name]

---

## 🎯 Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL database created
- [ ] `.env` file configured
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database schema loaded
- [ ] Application running (`python run.py`)
- [ ] Login page accessible at `localhost:5000`
- [ ] Dashboard displays correctly

---

## Version Information

- **Current Version:** 1.0.0
- **Release Date:** January 2026
- **Last Updated:** January 9, 2026
- **Status:** Stable

---

## 📚 Additional Resources

### Learning Materials
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Guide](https://docs.sqlalchemy.org/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)

### Tools Used
- Flask Web Framework
- MySQL Database
- Bootstrap Frontend Framework
- Chart.js for Visualizations
- Font Awesome Icons

---

**Happy Hotel Managing! 🏨**
<<<<<<< HEAD
# HotelEase - Hotel Management System

## 📋 Overview

**HotelEase** is a comprehensive web-based Hotel Management System built with Flask and MySQL. It provides a complete solution for managing hotel operations including room bookings, guest management, employee scheduling, service orders, and business analytics.

The system is designed with a modern, responsive UI and includes advanced features like real-time occupancy tracking, VIP guest management, audit logging, and detailed reporting.

---

## ✨ Features

### 🏨 Core Functionality
- **Room Management:** Track room availability, status, and pricing
- **Guest Management:** Register guests, manage contact information, maintain guest history
- **Booking System:** Create and manage room reservations with automatic room status updates
- **Service Orders:** Add additional services to bookings with automatic cost calculation
- **Invoice Generation:** Generate professional invoices for completed bookings
- **Payment Tracking:** Record and manage payment methods and amounts

### 👨‍💼 Admin & Staff Management
- **Employee Directory:** Manage staff information, roles, shifts, and salaries
- **User Authentication:** Secure login system with role-based access control
- **Access Levels:** Admin, Manager, Receptionist, and Staff roles
- **Audit Logging:** Track all database changes with timestamp and action details

### 📊 Analytics & Reporting
- **Business Intelligence Dashboard:** View key metrics and KPIs
- **Revenue Reports:** Track total revenue from room bookings and services
- **Occupancy Analysis:** Monitor room occupancy rates with visual charts
- **VIP Guest Ranking:** Identify top-spending guests with lifetime spending analysis
- **Service Performance:** Analyze high-value services and their revenue contribution
- **Shift Analytics:** View staff shift overlaps and team information

### 🔐 Security & Data Integrity
- **Trigger-Based Validation:** Prevent double-booking with database triggers
- **Stored Procedures:** Automated booking completion and room status updates
- **Transaction Management:** ACID-compliant booking transactions
- **Audit Trail:** Complete audit log of all modifications

### 📱 User Interface
- **Responsive Design:** Mobile-friendly dashboard layout
- **Real-time Charts:** Interactive revenue trend visualization
- **Intuitive Navigation:** Sidebar-based menu system
- **Flash Messages:** User feedback on all operations
- **Bootstrap 5.3:** Modern, professional styling

---

## 🛠️ Technology Stack

### Backend
- **Framework:** Flask 3.0.0
- **Database:** MySQL (PyMySQL 1.1.0)
- **ORM:** SQLAlchemy via Flask-SQLAlchemy 3.1.1
- **Language:** Python 3.x

### Frontend
- **Template Engine:** Jinja2
- **CSS Framework:** Bootstrap 5.3.0
- **Icons:** Font Awesome 6.4.0
- **Charts:** Chart.js
- **Typography:** Google Inter Font

### Database Features
- **Views:** RoomOccupancy, ShiftOverlap, PackagePossibilities
- **Stored Procedures:** CheckAvailability, CompleteBooking
- **Functions:** GetGuestLevel (VIP classification)
- **Triggers:** PreventDoubleBooking, BeforeServiceOrderInsert, LogGuestDeletion

---

## 📦 Project Structure

```
HotelEase_Project/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── models/
│   │   ├── __init__.py
│   │   ├── hotel.py               # Room, RoomType, Service models
│   │   ├── user.py                # User authentication model
│   │   ├── staff.py               # Employee and Maintenance models
│   │   └── operation.py           # Guest, Booking, Payment, Feedback models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py         # Login/Logout routes
│   │   ├── admin_routes.py        # Admin dashboard & management
│   │   ├── front_desk.py          # Booking & room management
│   │   ├── guest_api.py           # Guest search API
│   │   └── report_routes.py       # Analytics & reporting
│   ├── services/
│   │   └── db_utils.py            # Database utility functions
│   ├── static/
│   │   ├── css/
│   │   │   └── dashboard.css      # Main stylesheet
│   │   ├── js/
│   │   │   └── main.js            # Frontend JavaScript
│   │   └── img/                   # Images folder
│   └── templates/
│       ├── base.html              # Base template with sidebar
│       ├── auth/
│       │   └── login.html         # Login page
│       ├── admin/
│       │   ├── dashboard.html     # Executive overview
│       │   ├── employees.html     # Employee directory
│       │   ├── guests.html        # Guest management
│       │   ├── reports.html       # Analytics dashboard
│       │   └── audit_logs.html    # Audit trail
│       └── reception/
│           ├── room_grid.html     # Room status display
│           ├── booking_form.html  # Booking creation
│           ├── booking_details.html# Booking management
│           └── invoice.html       # Invoice generation
├── config.py                       # Configuration settings
├── run.py                         # Application entry point
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables
└── README.md                     # This file
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- pip (Python package manager)

### Step 1: Clone/Download the Project
```bash
cd HotelEase_Project
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create/edit `.env` file with your database credentials:

```env
DB_HOST=localhost
DB_USER=root
DB_PASS=your_password
DB_NAME=HotelEase

SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### Step 5: Set Up Database

1. **Create MySQL Database:**
   ```sql
   CREATE DATABASE HotelEase;
   USE HotelEase;
   ```

2. **Create Database Schema:**
   - Run your database initialization script (contact project maintainer)
   - Or execute SQL files for tables, views, stored procedures, and triggers

3. **Insert Sample Data (Optional):**
   - Sample users for testing
   - Sample rooms and room types
   - Sample guests and bookings

### Step 6: Run the Application
```bash
python run.py
```

The application will start on `http://localhost:5000`

---

## 📖 Usage Guide

### Login
1. Navigate to `http://localhost:5000`
2. You'll be redirected to the login page
3. Enter credentials provided by the system administrator
4. Click "Sign In"

### Dashboard
Once logged in, you'll see the executive overview with:
- Total Revenue
- Active Guests
- Room Occupancy
- System Health
- Recent Activity
- Revenue Trends Chart

### Room Management
1. Go to **Room Status** from the sidebar
2. View all rooms with their current status
3. Click **New Booking** to create a reservation

### Booking Management
1. Click **New Booking** from the sidebar
2. Select a guest from the dropdown
3. Choose available room
4. Set check-in and check-out dates
5. Price is calculated automatically
6. Confirm booking

### Guest Management
1. Go to **Guests** from the sidebar
2. View all registered guests
3. Edit or delete guest profiles
4. Track booking history per guest

### Service Orders
1. Open a booking from **Booking Details**
2. Add services (spa, room service, etc.)
3. Specify quantity
4. Service costs calculated automatically

### Invoice Generation
1. Open a booking
2. Click **View Invoice**
3. Review charges and services
4. Print or export invoice

### Analytics & Reports
1. Go to **Analytics & BI** from the sidebar
2. View VIP guest rankings
3. Check high-value services
4. Monitor shift teams and occupancy
5. Print reports

### Audit Logs
1. Go to **Security Logs** from the sidebar
2. Review all database modifications
3. Track deletions, insertions, and updates
4. Check timestamps and details

---

## 🔐 Authentication & Roles

### User Roles
- **Admin:** Full system access, user management, reports
- **Manager:** Guest/booking management, reports
- **Receptionist:** Booking creation, guest check-in/out
- **Staff:** View-only access, service fulfillment

### Login Credentials
Contact your system administrator for login credentials.

---

## 🗄️ Database Schema

### Main Tables
- **Users:** Authentication and user information
- **Guests:** Guest profiles and contact details
- **Rooms:** Room inventory and status
- **RoomTypes:** Room categories and pricing
- **Bookings:** Reservation records
- **Payments:** Payment tracking
- **ServiceOrders:** Services ordered with bookings
- **Services:** Available services catalog
- **Employees:** Staff information
- **AuditLog:** System audit trail

### Database Views
- **RoomOccupancy:** Room booking history
- **ShiftOverlap:** Staff shift coordination
- **PackagePossibilities:** Service package options

### Stored Procedures
- **CheckAvailability:** Verify room availability
- **CompleteBooking:** Finalize booking and update room status

---

## 🐛 Troubleshooting

### Database Connection Issues
- Verify MySQL is running
- Check credentials in `.env` file
- Ensure database exists: `SHOW DATABASES;`
- Test connection: `mysql -u root -p`

### Port Already in Use
```bash
# Change port in run.py or use:
python run.py --port 5001
```

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### Database Errors
- Clear old sessions: Check Flask session configuration
- Verify table permissions: `GRANT ALL PRIVILEGES ON HotelEase.* TO 'user'@'localhost';`

---

## 📝 Notes for Developers

### Adding New Features
1. Create model in `app/models/`
2. Add route in `app/routes/`
3. Create template in `app/templates/`
4. Update sidebar navigation in `base.html`

### Database Changes
- Update SQLAlchemy models
- Run migrations or alter tables directly
- Update stored procedures as needed

### Style Modifications
- Edit `app/static/css/dashboard.css`
- Bootstrap classes are available in all templates
- Colors defined in CSS variables

### JavaScript Updates
- All JavaScript consolidated in `app/static/js/main.js`
- Chart.js for data visualization
- Bootstrap JS for components

---

## 🔄 Project Status

### Completed Features ✅
- ✅ User authentication system
- ✅ Room and guest management
- ✅ Booking system with validation
- ✅ Service orders with auto-calculation
- ✅ Invoice generation
- ✅ Admin dashboard with charts
- ✅ Analytics and reporting
- ✅ Audit logging
- ✅ All UI buttons functional

### Upcoming Features 🚀
- Guest registration portal
- Password reset functionality
- Email notifications
- SMS alerts for check-in/out
- Mobile app
- Advanced reporting exports
- Staff scheduling system

---

## 📧 Support

For issues, questions, or feature requests:
1. Check troubleshooting section
2. Review database schema
3. Check Flask error logs
4. Contact system administrator

---

## 📄 License

This project is proprietary hotel management software. All rights reserved.

---

## 👥 Contributors

- **Project Lead:** [Your Name]
- **Database Design:** [Your Name]
- **Frontend Development:** [Your Name]
- **Backend Development:** [Your Name]

---

## 🎯 Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] MySQL database created
- [ ] `.env` file configured
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database schema loaded
- [ ] Application running (`python run.py`)
- [ ] Login page accessible at `localhost:5000`
- [ ] Dashboard displays correctly

---

## Version Information

- **Current Version:** 1.0.0
- **Release Date:** January 2026
- **Last Updated:** January 9, 2026
- **Status:** Stable

---

## 📚 Additional Resources

### Learning Materials
- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Guide](https://docs.sqlalchemy.org/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)

### Tools Used
- Flask Web Framework
- MySQL Database
- Bootstrap Frontend Framework
- Chart.js for Visualizations
- Font Awesome Icons

---

**Happy Hotel Managing! 🏨**
=======
# HotelEase
A comprehensive hotel management system built with Flask and MySQL
>>>>>>> f5118171a380038f0a2ff360edcc984e4e14681c
