# Traveloo Scooter Rental System

A comprehensive scooter rental management system for Traveloo, based in La Ferme, Rodrigues Island, Mauritius.

## Features

- Custom booking engine
- Financial management (invoices & contracts)
- MCB Juice payment integration
- WhatsApp automated messaging
- Scooter availability calendar
- GPS tracking integration
- Mauritius fiscal compliance

## Technical Stack

- Frontend: HTML5, CSS3, JavaScript
- Backend: Django 5.0
- Database: PostgreSQL
- Server: Ubuntu 20.04+ with Nginx and Gunicorn
- WhatsApp Integration: Twilio
- CI/CD: GitHub Actions

## Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Node.js 18+ (for frontend build)
- Ubuntu 20.04+ (for production)

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/traveloo-scooter-rental.git
   cd traveloo-scooter-rental
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Start development server:
   ```bash
   python manage.py runserver
   ```

## Production Deployment

1. Update system packages:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. Install dependencies:
   ```bash
   sudo apt install python3-pip python3-venv nginx postgresql
   ```

3. Clone and setup:
   ```bash
   git clone https://github.com/your-username/traveloo-scooter-rental.git
   cd traveloo-scooter-rental
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. Configure Nginx and Gunicorn:
   ```bash
   # Configure Nginx sites-available
   # Setup Gunicorn systemd service
   ```

5. Start services:
   ```bash
   sudo systemctl start nginx
   sudo systemctl start gunicorn
   ```

## Environment Variables

Create a `.env` file with the following variables:

```
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ALLOWED_HOSTS=.yourdomain.com
TWILIO_ACCOUNT_SID=your-sid
TWILIO_AUTH_TOKEN=your-token
MCB_JUICE_API_KEY=your-key
```

## Testing

Run tests with:
```bash
pytest
```

## CI/CD Pipeline

The project uses GitHub Actions for:
- Code quality checks
- Automated testing
- Deployment to production

## License

Copyright © 2025 Traveloo. All rights reserved.
