# HomeSer

HomeSer is a Household Service Providing Platform built with Django. It allows clients to browse, search, and order household services, while admins can manage services and promote users to admin roles.

## Current Development Status

⚠️ **This project is currently in active development state.** While the core functionality is implemented, there may be bugs and incomplete features that need to be addressed before production deployment.

## Features

- User authentication and role management (Admin and Client roles)
- Service browsing, searching, and sorting by rating
- Cart management and checkout process
- Client profile management with bio, profile picture, and social links
- Admin capabilities to manage services and promote users
- Reviews and ratings for services
- Future-proofed for payment gateway integration
- Enhanced UI/UX with improved typography and FontAwesome icons

## Tech Stack

- **Backend**: Django, Django REST Framework (DRF)
- **Frontend**: Django HTML Templates, Tailwind CSS v3, FontAwesome
- **Database**: SQLite (development), designed for Supabase Postgres (production)
- **Media Storage**: Cloudinary (production)
- **Caching**: Upstash Redis (production) - Optional
- **Authentication**: JWT via djangorestframework-simplejwt, stored in secure, HTTP-only cookies
- **Static Files**: Served by WhiteNoise
- **CI/CD**: GitHub Actions for linting, testing, and security audits
- **Deployment**: Vercel (Free Tier) using the Python Serverless Function runtime

## Getting Started

### Prerequisites

- Python 3.10+ (required for Django 5.0.4)
- Node.js and npm (for Tailwind CSS)
- A Supabase account
- A Cloudinary account
- An Upstash account (optional)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/MushfiqPlabon/HomeSer.git
   cd HomeSer
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Copy `.env.example` to `.env` and fill in the required values:
   ```
   cp .env.example .env
   ```

5. Run database migrations:
   ```
   python manage.py migrate
   ```

6. Seed the database with demo data (optional):
   ```
   python manage.py seed_demo_data
   ```

7. Collect static files:
   ```
   python manage.py collectstatic
   ```

8. Start the development server:
   ```
   python manage.py runserver
   ```

### Tailwind CSS Setup

1. Install Tailwind CSS:
   ```
   npm install -D tailwindcss@3
   npx tailwindcss init
   ```

2. Configure your template paths in `tailwind.config.js`:
   ```js
   /** @type {import('tailwindcss').Config} */
   module.exports = {
     content: ["./templates/**/*.html"],
     theme: {
       extend: {
         colors: {
           "neon-green": "#39ff14",
           "neon-blue": "#00ffff"
         }
       }
     },
     plugins: []
   }
   ```

3. Add the Tailwind directives to your CSS file (`static/css/styles.css`):
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;

   /* Custom styles */
   .text-neon-green {
       color: #39ff14;
   }

   .text-neon-blue {
       color: #00ffff;
   }

   .bg-neon-green {
       background-color: #39ff14;
   }

   .bg-neon-blue {
       background-color: #00ffff;
   }
   ```

4. Start the Tailwind CLI build process:
   ```
   npx tailwindcss -i ./static/css/styles.css -o ./static/css/output.css --watch
   ```

### Vercel Deployment

1. Create a new project on Vercel.
2. Connect your GitHub repository.
3. Set the following environment variables in Vercel:
   - `SECRET_KEY`: Your Django secret key
   - `DATABASE_URL`: Your Supabase Postgres connection URL
   - `CLOUDINARY_URL`: Your Cloudinary URL
   - `REDIS_URL`: Your Upstash Redis URL (optional)
4. Deploy the project.

## API Documentation

The API documentation is available at `/api/docs/swagger/` or `/api/docs/redoc/` when the development server is running.

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment with three jobs:
- **Lint**: Checks code formatting with black, isort, and flake8
- **Test**: Runs tests with pytest
- **Security**: Runs security audits with pip-audit

## Known Development Issues

See `bug_tracking.md` for current bugs that need to be fixed.

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.