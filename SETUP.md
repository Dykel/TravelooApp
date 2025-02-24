# Traveloo App Setup Guide

This guide will help you set up the Traveloo App on your development machine. You can choose between Windows with WSL (recommended) or Windows native setup.

## Option 1: Setup with WSL (Recommended)

### 1. Prerequisites
```bash
# Update package list
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib git
```

### 2. Clone the Repository
```bash
# Clone the repository
git clone https://github.com/Dykel/TravelooApp.git
cd TravelooApp
```

### 3. Database Setup
```bash
# Start PostgreSQL service
sudo service postgresql start

# Create database
sudo -u postgres createdb traveloo

# Optional: Set up PostgreSQL user
sudo -u postgres psql -c "CREATE USER your_username WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "ALTER USER your_username WITH SUPERUSER;"
```

### 4. Python Environment Setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Environment Configuration
```bash
# Copy environment file
cp .env.example .env

# Edit .env file with your settings
# Required variables:
# - SECRET_KEY
# - DATABASE_URL=postgresql://your_username:your_password@localhost:5432/traveloo
# - MCB_JUICE_API_KEY
# - TWILIO_ACCOUNT_SID
# - TWILIO_AUTH_TOKEN
# - GPS_TRACKER_API_KEY
```

### 6. Django Setup
```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Option 2: Windows Native Setup

### 1. Prerequisites

1. Install Python 3.11+:
   - Download from [Python.org](https://www.python.org/downloads/)
   - Check "Add Python to PATH" during installation

2. Install PostgreSQL:
   - Download from [PostgreSQL.org](https://www.postgresql.org/download/windows/)
   - Remember the password you set during installation

3. Install Git:
   - Download from [Git-scm.com](https://git-scm.com/download/win)

### 2. Clone the Repository
```powershell
# Clone the repository
git clone https://github.com/Dykel/TravelooApp.git
cd TravelooApp
```

### 3. Database Setup
```powershell
# Create database using psql
& 'C:\Program Files\PostgreSQL\16\bin\psql.exe' -U postgres -c "CREATE DATABASE traveloo;"
```

### 4. Python Environment Setup
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Environment Configuration
```powershell
# Copy environment file
copy .env.example .env

# Edit .env file with your settings
# Required variables:
# - SECRET_KEY
# - DATABASE_URL=postgresql://postgres:your_password@localhost:5432/traveloo
# - MCB_JUICE_API_KEY
# - TWILIO_ACCOUNT_SID
# - TWILIO_AUTH_TOKEN
# - GPS_TRACKER_API_KEY
```

### 6. Django Setup
```powershell
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Verifying the Installation

After completing either setup, you should:

1. Access the admin interface at `http://localhost:8000/admin`
2. Log in with your superuser credentials
3. Verify that you can see the following models:
   - Bookings
   - Payments
   - Scooters
   - Tracking

## Common Issues and Solutions

### PostgreSQL Connection Issues
- Verify PostgreSQL is running
- Check your DATABASE_URL in .env
- Ensure PostgreSQL password is correct

### Package Installation Issues
- Upgrade pip: `pip install --upgrade pip`
- Install wheel: `pip install wheel`
- On Windows, use pre-compiled wheels when available

### Port Already in Use
If port 8000 is in use:
```bash
python manage.py runserver 8001
```

## Development Workflow

1. Always activate virtual environment before working:
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # WSL/Linux
   source venv/bin/activate
   ```

2. Pull latest changes:
   ```bash
   git pull origin master
   ```

3. Install any new dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations if needed:
   ```bash
   python manage.py migrate
   ```

## Need Help?

If you encounter any issues during setup, please:
1. Check the common issues section above
2. Review the error message carefully
3. Create an issue on GitHub with:
   - Your operating system and version
   - The exact error message
   - Steps to reproduce the issue
