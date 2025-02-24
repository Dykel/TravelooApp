#!/bin/bash

# Update system packages
sudo apt update
sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib

# Create project directory
sudo mkdir -p /var/www/traveloo
sudo chown $USER:$USER /var/www/traveloo

# Clone repository (replace with your repository URL)
git clone https://github.com/yourusername/traveloo-scooter-rental.git /var/www/traveloo

# Setup virtual environment
cd /var/www/traveloo
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Setup PostgreSQL
sudo -u postgres psql -c "CREATE DATABASE traveloo;"
sudo -u postgres psql -c "CREATE USER traveloo_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "ALTER ROLE traveloo_user SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE traveloo_user SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE traveloo_user SET timezone TO 'Indian/Mauritius';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE traveloo TO traveloo_user;"

# Setup Django
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# Setup Gunicorn
sudo bash -c 'cat > /etc/systemd/system/gunicorn.service << EOL
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=/var/www/traveloo
ExecStart=/var/www/traveloo/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/traveloo/traveloo.sock traveloo.wsgi:application

[Install]
WantedBy=multi-user.target
EOL'

# Setup Nginx
sudo bash -c 'cat > /etc/nginx/sites-available/traveloo << EOL
server {
    listen 80;
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /var/www/traveloo;
    }

    location /media/ {
        root /var/www/traveloo;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/traveloo/traveloo.sock;
    }
}
EOL'

# Enable the Nginx site
sudo ln -s /etc/nginx/sites-available/traveloo /etc/nginx/sites-enabled

# Start services
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl restart nginx

echo "Deployment complete! Don't forget to:"
echo "1. Update the .env file with your production settings"
echo "2. Configure SSL with Let's Encrypt"
echo "3. Update the Nginx configuration with your domain name"
echo "4. Configure your firewall settings"
