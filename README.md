# HomeSer - Household Service Platform

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/HomeSer)

HomeSer is a modern, full-featured household service platform built with Django. It connects clients with service providers, offering a seamless experience for browsing, booking, and managing household services.

## Repository Branches

This repository contains multiple branches for different development approaches:

- **`main`** - The primary branch with the complete Django application (backend + HTML frontend)
- **`back-end`** - Backend-only API branch for integration with modern frontend frameworks (React, Next.js, etc.)
- **`html-front-end`** - Branch with the complete Django application (backend + HTML frontend) for traditional web development

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
- [Development](#development)
  - [Running the Application](#running-the-application)
  - [Tailwind CSS](#tailwind-css)
- [Deployment](#deployment)
  - [Vercel Deployment](#vercel-deployment)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication**: Secure registration and login with email verification
- **Service Management**: Browse, search, and filter household services
- **Shopping Cart**: Add services to cart and manage bookings
- **Order Processing**: Complete checkout process with order history
- **User Profiles**: Customize profiles with bio and social links
- **Admin Dashboard**: Manage services, users, and orders
- **Reviews & Ratings**: Rate and review services
- **Responsive Design**: Works on all device sizes
- **Modern UI**: Neon-themed interface with smooth animations
- **Health Checks**: Built-in health check endpoints for monitoring
- **Asynchronous Tasks**: Background task processing with Celery
- **API Documentation**: Auto-generated API docs with Swagger and Redoc
- **Security**: JWT authentication with HTTP-only cookies

## Tech Stack

- **Backend**: Django 5.2, Django REST Framework
- **Frontend**: HTML Templates, Tailwind CSS 3, FontAwesome, Anime.js
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: JWT via SimpleJWT with secure HTTP-only cookies
- **Storage**: Cloudinary for media files (production)
- **Caching**: Redis (production), In-memory cache (development)
- **Task Queue**: Celery with Redis
- **Deployment**: Vercel Serverless Functions
- **Static Assets**: WhiteNoise for serving static files

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js and npm (for Tailwind CSS)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/HomeSer.git
cd HomeSer
```

2. Create a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Node.js dependencies:
```bash
npm install
```

5. Set up environment variables (see [Environment Variables](#environment-variables))

6. Run database migrations:
```bash
python manage.py migrate
```

7. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

### Environment Variables

Copy the example environment file and update the values:
```bash
cp .env.example .env
```

Key environment variables:
- `SECRET_KEY`: Django secret key (generate a new one for production)
- `DEBUG`: Set to `False` for production
- `DATABASE_URL`: PostgreSQL connection string for production
- `CLOUDINARY_URL`: For media storage in production
- `REDIS_URL`: For caching in production

For local development, you can use default values in the `.env` file.

## Development

### Running the Application

Start the development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

### Tailwind CSS

Compile CSS in development mode (with watch):
```bash
npm run dev
```

Build CSS for production:
```bash
npm run build
```

## Deployment

### Vercel Deployment

This project is optimized for deployment on Vercel's free tier:

1. Fork this repository to your GitHub account
2. Create a new project on Vercel
3. Connect your forked repository to Vercel
4. Configure environment variables in the Vercel dashboard:
   - `SECRET_KEY`: Your Django secret key
   - `DATABASE_URL`: Your PostgreSQL connection URL
   - `CLOUDINARY_URL`: Your Cloudinary environment variable
   - `REDIS_URL`: Your Redis URL (optional)
   - `DEBUG`: Set to `False` for production
   - `ALLOWED_HOSTS`: Your Vercel deployment URLs
   - `SERVERLESS`: Set to `1`

5. Deploy the project

**Important Notes:**
- Static files are automatically collected during the build process
- The `.env` file is for local development only and will not be used in production
- All environment variables must be configured in the Vercel dashboard

## API Documentation

The API documentation is available at:
- Swagger UI: `/api/docs/swagger/`
- Redoc: `/api/docs/redoc/`

## Project Structure

```
HomeSer/
├── HomeSer/              # Main Django application
│   ├── management/       # Custom management commands
│   ├── migrations/       # Database migrations
│   ├── __init__.py      # Package initializer
│   ├── admin.py         # Django admin configuration
│   ├── api_urls.py      # API route definitions
│   ├── asgi.py          # ASGI configuration
│   ├── celery.py        # Celery configuration
│   ├── decorators.py    # Custom decorators
│   ├── forms.py         # Django forms
│   ├── health_check.py  # Health check endpoints
│   ├── jwt_utils.py     # JWT utility functions
│   ├── middleware.py    # Custom middleware
│   ├── models.py        # Data models
│   ├── permissions.py   # Custom permissions
│   ├── serializers.py   # DRF serializers
│   ├── settings.py      # Django settings
│   ├── tasks.py         # Celery tasks
│   ├── tokens.py        # Token management
│   ├── urls.py          # Main URL configuration
│   ├── views.py         # View functions
│   ├── web_urls.py      # Web route definitions
│   └── wsgi.py          # WSGI configuration
├── static/              # Static assets (CSS, JS, images)
│   ├── css/             # CSS files
│   ├── js/              # JavaScript files
│   └── images/          # Image assets
├── staticfiles/         # Collected static files (generated)
├── templates/           # HTML templates
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── package.json         # Node.js dependencies (Tailwind CSS)
└── vercel.json          # Vercel deployment configuration
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.