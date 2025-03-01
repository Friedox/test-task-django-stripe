# Django Stripe Payment Project

This project is a Django application that integrates with the Stripe payment system to create payment forms for products. The application is deployed using Docker and Ansible.

## Features

- Django backend with Stripe API integration
- Dockerized setup with Nginx as a reverse proxy
- Ansible-based deployment for easy server setup
- SSL support with a self-signed certificate
- Admin panel to manage models

## Installation & Deployment

### Prerequisites

Ensure you have the following installed on your local machine:

- Ansible
- Docker & Docker Compose
- SSH access to the server

### 1. Clone the repository

```sh
git clone git@github.com:Friedox/test-task-django-stripe.git
cd test-task-django-stripe
```

### 2. Setup `.env` File

Create a `.env` file in the project root with the following variables:

```ini
DEBUG=True
DJANGO_SECRET_KEY=your_very_secret_key_here

# Stripe settings for USD (default)
STRIPE_PUBLIC_KEY=your_stripe_public_key_here
STRIPE_SECRET_KEY=your_stripe_secret_key_here

# Stripe settings for EUR transactions (if needed)
STRIPE_PUBLIC_KEY_EUR=your_stripe_public_key_eur_here
STRIPE_SECRET_KEY_EUR=your_stripe_secret_key_eur_here

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123

ALLOWED_HOSTS=yourdomain.com
```

### 3. Configure Ansible Inventory

Create an `inventory.ini` file with your server details:

```ini
[django_server]
your_server_ip ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/id_ed25519
```

### 4. Run the Deployment

Run the following command from your local machine to deploy the project:

```sh
ansible-playbook -i inventory.ini setup.yml
```

This will:

- Install required dependencies on the server
- Clone the project
- Generate an SSL certificate
- Start Docker containers

### 5. Access the Application

Once deployed, access the application via:

```sh
https://your_server_ip/admin
```

Login using:

- **Username:** `admin`
- **Password:** `admin123`

## API Endpoints

- **GET /buy/{id}** - Returns Stripe session ID for a selected item
- **GET /item/{id}** - Displays an HTML page with item details and a "Buy" button

## Running Locally with Docker

If you want to run the project locally using Docker:

```sh
docker-compose up --build
```

The application will be accessible at `http://localhost:8000`.

## Notes

- Ensure you have valid Stripe API keys before testing payments.
- Update `ALLOWED_HOSTS` in `.env` to match your server domain/IP.
- The project is configured with a self-signed SSL certificate by default. Consider using Let's Encrypt for production.

## License

This project is licensed under the MIT License.

