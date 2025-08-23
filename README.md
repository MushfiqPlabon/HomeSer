# HomeSer
This project was create for the Django-Final-Exam assignment of Phitron's SDT track's Software Development Project, Milestone 4, Module 27.

HomeSer is a modern, full-featured Household Service Providing Platform built with Django. It provides a seamless experience for clients to browse, search, and order services, while offering a robust administrative interface for managing services, users, and roles.

This project leverages a modern technology stack including Django REST Framework for the API, Tailwind CSS for the frontend, and is designed for production deployment on Vercel with a Supabase Postgres database.

## Current Development Status

⚠️ **This project is currently in active development state.** While the core functionality is implemented, there may be bugs and incomplete features that need to be addressed before production deployment.
**Note:** The Celery implementation is currently broken and under review.

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
   Copy `.env.example` to `.env` and fill in the required values. This file contains all necessary environment variables for the project.

   ```bash
   cp .env.example .env
   ```

   Then edit the `.env` file with your actual values. Below is a summary of the key variables:

   **Django Core Settings:**
   - `SECRET_KEY`: Your Django secret key. **Generate a new one for production:** `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DEBUG`: Set to `True` for development, `False` for production.
   - `ALLOWED_HOSTS`: Comma-separated list of hostnames that your Django site can serve. E.g., `localhost,127.0.0.1,yourdomain.com`.

   **Database Configuration:**
   - `DATABASE_URL`: Full connection string for your PostgreSQL database (e.g., from Supabase). If left empty, SQLite will be used for development.
     *Example:* `postgresql://user:password@host:port/database_name`
   - *Optional individual DB credentials (only if `DATABASE_URL` is not used):* `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`.

   **Cloudinary Settings (for media storage):**
   - `CLOUDINARY_URL`: Your Cloudinary environment variable.
     *Example:* `cloudinary://api_key:api_secret@cloud_name`
   - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`: Individual credentials if `CLOUDINARY_URL` is not used.

   **Redis Settings (for caching & sessions):**
   - `REDIS_URL`: Your Redis connection URL (e.g., from Upstash). If left empty, a local memory cache will be used.
     *Example:* `redis://username:password@host:port/database`
   - `CACHE_TTL`: Cache timeout in seconds (default: 900).
   - `SESSION_COOKIE_AGE`: Session cookie age in seconds (default: 1209600).

   **Celery Settings (for background tasks):**
   - **NOTE:** The Celery implementation is currently broken and under review. These settings are not functional at the moment.
   - `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, `CELERY_REDIS_USE_SSL`, `CELERY_BROKER_USE_SSL`, `CELERY_BEAT_SCHEDULER`, `CELERY_BROKER_RETRY_ON_STARTUP`.

   **Email Settings:**
   - `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`: Configure these for sending emails (e.g., password reset, notifications).

   **Authentication Settings (SimpleJWT):**
   - `JWT_ACCESS_TOKEN_LIFETIME_MINUTES`: Lifetime of access tokens in minutes (default: 60).
   - `JWT_REFRESH_TOKEN_LIFETIME_DAYS`: Lifetime of refresh tokens in days (default: 1).

   For development, you can often leave most values as defaults or use local services. For production deployment, you'll need to set up accounts with external services like Supabase, Cloudinary, and Upstash.

5. Run database migrations:

   ```
   python manage.py migrate
   ```

6. Collect static files:

   ```
   python manage.py collectstatic
   ```

7. Start the development server:
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
           "neon-blue": "#00ffff",
         },
       },
     },
     plugins: [],
   };
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
   - **Django Core Settings:**
     - `SECRET_KEY`: Your Django secret key (generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`).
     - `DEBUG`: Set to `False` for production.
     - `ALLOWED_HOSTS`: Comma-separated list of your Vercel deployment URLs (e.g., `your-project.vercel.app`).
   - **Database Configuration:**
     - `DATABASE_URL`: Your Supabase Postgres connection URL (format: `postgresql://user:password@host:port/database_name`).
   - **Cloudinary Settings (for media storage):**
     - `CLOUDINARY_URL`: Your Cloudinary environment variable.
       *Example:* `cloudinary://api_key:api_secret@cloud_name`
     - `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`: (Alternatively, if not using `CLOUDINARY_URL`).
   - **Redis Settings (for caching & sessions):**
     - `REDIS_URL`: Your Upstash Redis URL (optional but recommended for caching, format: `redis://username:password@host:port/database`).
     - `CACHE_TTL`: Cache timeout in seconds (default: 900).
     - `SESSION_COOKIE_AGE`: Session cookie age in seconds (default: 1209600).
   - **Email Settings:**
     - `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS`, `DEFAULT_FROM_EMAIL`: Configure these if your application sends emails.
   - **Authentication Settings (SimpleJWT):**
     - `JWT_ACCESS_TOKEN_LIFETIME_MINUTES`: Lifetime of access tokens in minutes (default: 60).
     - `JWT_REFRESH_TOKEN_LIFETIME_DAYS`: Lifetime of refresh tokens in days (default: 1).
   - **Celery Settings (currently broken):**
     - **NOTE:** The Celery implementation is currently broken and under review. Do not set these variables on Vercel at this time.
     - `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND`, `CELERY_REDIS_USE_SSL`, `CELERY_BROKER_USE_SSL`, `CELERY_BEAT_SCHEDULER`, `CELERY_BROKER_RETRY_ON_STARTUP`.
4. Deploy the project.

## API Documentation

The API documentation is available at `/api/docs/swagger/` or `/api/docs/redoc/` when the development server is running.

## Email Verification

This project includes email verification for new user registrations. When a user registers, they will receive an email with an activation link. They must click this link to activate their account before they can log in.

### Configuration

The project uses a dynamic email configuration:
- If email credentials are provided in the `.env` file, it will use real email sending via SMTP
- If no email credentials are provided, it will fall back to printing emails to the console

This works regardless of whether DEBUG is True or False.

For production email sending with Gmail, you need to:

1. Enable 2-Factor Authentication on your Google account
2. Generate an App Password for "Mail" at https://myaccount.google.com/apppasswords
3. Use the 16-character app password in your `.env` file:

```
# Email Settings for Gmail
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

For other email providers, configure the appropriate SMTP settings:

```
# Email Settings for Other Providers
EMAIL_HOST=your-smtp-server.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@yourdomain.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@yourdomain.com
```

### Testing Email Verification

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Navigate to http://localhost:8000/accounts/register/ and register a new user

3. Check your inbox for the activation email (if using real email) or the console output (if using console backend)

4. Copy the activation link from the email and paste it in your browser

5. The account should be activated and you'll be logged in automatically

### Customizing Email Templates

The email templates can be found in:
- `templates/registration/activation_email.html` (HTML version)
- `templates/registration/activation_email.txt` (Plain text version)

You can customize these templates to match your brand.

## API Documentation

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a pull request

## License

This project is licensed under the MIT License.