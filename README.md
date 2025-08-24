# HomeSer - Household Service Platform

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/HomeSer)

## 🎓 Academic Context

This project was developed as part of Phitron's Software Development Technologies (SDT) program, specifically for the Software Development Project (SDP) "Django-Final-Exam" in Milestone 5, Module 27.

HomeSer is a modern, full-featured household service platform built with Django. It connects clients with service providers, offering a seamless experience for browsing, booking, and managing household services.

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
- **AI Analysis**: Repomix for codebase packing and analysis

## Getting Started

### Prerequisites

- Python 3.10 or higher
### Installation

1. Clone the repository:
2. Create a virtual environment:
3. Install Python dependencies:
5. Set up environment variables (see [Environment Variables](#environment-variables))

6. Run database migrations:
7. Create a superuser (optional):
### Environment Variables

Copy the example environment file and update the values:
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
The application will be available at `http://localhost:8000`

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

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
