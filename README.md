# Traveloo Scooter Rental App

A comprehensive scooter rental management system built with Django, featuring booking management, payment integration, and real-time GPS tracking.

## Developer
- **Name**: Joseph Jonathan COLLET
- **Role**: Lead Developer

## Features

- 🛵 Scooter Management & Tracking
- 📅 Booking System
- 💳 Payment Processing (MCB Juice Integration)
- 📍 Real-time GPS Tracking
- 🗺️ Geofencing Capabilities
- 📱 WhatsApp Notifications

## Prerequisites

- Python 3.11 or higher
- Git
- PostgreSQL
- MCB Juice API credentials
- Twilio account (for WhatsApp notifications)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Dykel/TravelooApp.git
   cd TravelooApp
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   .\venv\Scripts\activate
   
   # On Unix or MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your configuration
   # Update the following variables:
   # - SECRET_KEY
   # - DATABASE_URL
   # - MCB_JUICE_API_KEY
   # - TWILIO_ACCOUNT_SID
   # - TWILIO_AUTH_TOKEN
   # - GPS_TRACKER_API_KEY
   ```

5. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://localhost:8000`

## Project Structure

```
traveloo-scooter-rental/
├── bookings/           # Booking management
├── payments/           # Payment processing
├── scooters/          # Scooter management
├── tracking/          # GPS tracking and geofencing
├── templates/         # HTML templates
├── traveloo/          # Project settings
└── static/           # Static files
```

## API Documentation

The API documentation is available at `/api/docs/` when running the server.

## Testing

Run the test suite:
```bash
python manage.py test
```

## Deployment

1. Set up your production environment
2. Update `.env` with production settings
3. Follow the deployment guide in `deploy/setup.sh`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
