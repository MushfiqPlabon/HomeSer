# 🏡 HomeSer: Your Go-To Household Service Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-green?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.x-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)

Welcome to **HomeSer**! 🎉 This project is a modern, full-stack web application designed to connect users with various household services. Think of it as your one-stop shop for finding reliable help with tasks around your home. Whether you need a plumber, an electrician, a cleaner, or any other household service, HomeSer makes it easy to discover, book, and manage services.

## ✨ Features

HomeSer comes packed with features to provide a seamless experience for both service providers and clients:

- **User Authentication & Authorization:** Secure registration, login, and role-based access (Admin & Client). 🔐
- **Personalized User Profiles:** Users can manage their profiles, including bios, profile pictures, and social links. 👤
- **Service Discovery:** Browse a wide range of household services with detailed descriptions and pricing. 🔍
- **Shopping Cart Functionality:** Easily add multiple services to your cart before checkout. 🛒
- **Order Management:** Track the status of your service orders from pending to completion. 📝
- **Service Reviews & Ratings:** Share your experience and rate services to help others. ⭐
- **Robust API:** A well-documented API for seamless integration and future expansions. 🚀
- **Responsive Design:** Enjoy a smooth experience on any device, from desktops to mobile phones. 📱

## 🛠️ Technologies Used

HomeSer is built with a powerful and modern tech stack:

**Backend:**

- **Python 🐍:** The core programming language.
- **Django 🌐:** A high-level Python web framework that encourages rapid development and clean, pragmatic design.
- **Django REST Framework (DRF) 🏗️:** A flexible toolkit for building Web APIs.
- **Simple JWT 🔑:** JSON Web Token authentication for secure API access.
- **PostgreSQL (via Supabase) 🐘:** A powerful, open-source relational database for robust data storage. (SQLite for local development)
- **Celery 🥕:** (Planned/Used for background tasks) An asynchronous task queue/job queue based on distributed message passing.
- **Whitenoise 💨:** For serving static files efficiently in production.
- **Cloudinary ☁️:** (Optional) For cloud-based image and video management.

**Frontend:**

- **HTML5 & CSS3 🎨:** Standard web technologies for structuring and styling content.
- **Tailwind CSS 🌬️:** A utility-first CSS framework for rapidly building custom designs.
- **JavaScript ✨:** For interactive elements and dynamic content.
- **Anime.js 🎬:** A lightweight JavaScript animation library.

**Deployment & Tools:**

- **Vercel 🚀:** (Suggested) For easy deployment of the web application.
- **DRF Spectacular 📄:** Generates OpenAPI 3.0 schemas for API documentation (Swagger UI/Redoc).
- **`python-dotenv` ⚙️:** For managing environment variables.

## 🚀 Getting Started

Follow these steps to get HomeSer up and running on your local machine.

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** (Recommended: Use `pyenv` or `conda` for environment management)
- **pip** (Python package installer)
- **Node.js & npm** (Node Package Manager)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/HomeSer.git
    cd HomeSer
    ```

2.  **Set up Python Virtual Environment:**

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    Create a `.env` file in the root directory of the project (next to `manage.py`) and add the following:

    ```dotenv
    # .env example
    SECRET_KEY='your_super_secret_django_key_here'
    DEBUG=True
    ALLOWED_HOSTS='localhost,127.0.0.1'
    CSRF_TRUSTED_ORIGINS='http://localhost:8000,http://127.0.0.1:8000'
    CORS_ALLOWED_ORIGINS='http://localhost:8000,http://127.0.0.1:8000'

    # Database (for local SQLite, no need to change)
    # For PostgreSQL/Supabase, uncomment and fill these:
    # DATABASE_URL="postgresql://user:password@host:port/dbname"

    # JWT Settings (optional, defaults are fine for local)
    # JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
    # JWT_REFRESH_TOKEN_LIFETIME_DAYS=1

    # Cloudinary (optional, uncomment if you want to use it for media storage)
    # CLOUDINARY_URL="cloudinary://api_key:api_secret@cloud_name"
    ```

    - **`SECRET_KEY`**: Generate a strong, random string. You can use Django's `get_random_secret_key()` function in a Python shell.
    - For `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and `CORS_ALLOWED_ORIGINS`, adjust them based on your deployment environment. For local development, the provided values are usually sufficient.

5.  **Apply Database Migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser (Admin Account):**

    ```bash
    python manage.py createsuperuser
    ```

    Follow the prompts to create an admin user.

7.  **Install Node.js dependencies & Build Frontend Assets:**
    ```bash
    npm install
    npm run build
    ```
    The `npm run build` command compiles the Tailwind CSS and other frontend assets. For development, you can use `npm run dev` to watch for changes.

### Running the Application

1.  **Start the Django development server:**

    ```bash
    python manage.py runserver
    ```

    The application will be accessible at `http://127.0.0.1:8000/`.

2.  **(Optional) Run Tailwind CSS in watch mode (for development):**
    In a separate terminal, navigate to the project root and run:
    ```bash
    npm run dev
    ```
    This will automatically recompile your CSS whenever you make changes to your Tailwind files.

## 📂 Project Structure

Here's a simplified overview of the project's main directories and their purposes:

```
HomeSer/
├── HomeSer/                # Main Django project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py             # Main URL routing
│   ├── web_urls.py         # Web application specific URLs
│   ├── api_urls.py         # API specific URLs
│   ├── models.py           # Database models
│   ├── views.py            # Django views (logic for web pages)
│   ├── serializers.py      # DRF serializers (for API data handling)
│   └── ...
├── static/                 # Frontend static assets (CSS, JS, Images)
│   ├── css/
│   │   ├── input.css       # Tailwind CSS input file
│   │   └── styles.css      # Additional custom styles
│   └── js/
│       └── scripts.js      # Custom JavaScript
├── templates/              # HTML templates for Django views
│   ├── base.html           # Base template
│   ├── home.html           # Homepage template
│   └── ...
├── venv/                   # Python virtual environment
├── manage.py               # Django's command-line utility
├── requirements.txt        # Python dependencies
├── package.json            # Node.js dependencies and scripts
├── tailwind.config.js      # Tailwind CSS configuration
└── README.md               # This file!
```

## 📸 Screenshots

_(Since I cannot generate images, please replace these placeholders with actual screenshots of your application)_

- **Homepage:**
  ![Homepage Screenshot](https://via.placeholder.com/800x450?text=Homepage+Screenshot)
  _A welcoming view of the HomeSer platform._

- **Services Listing:**
  ![Services Listing Screenshot](https://via.placeholder.com/800x450?text=Services+Listing+Screenshot)
  _Browse available household services._

- **Service Detail Page:**
  ![Service Detail Screenshot](https://via.placeholder.com/800x450?text=Service+Detail+Screenshot)
  _Detailed information about a specific service._

- **User Profile:**
  ![User Profile Screenshot](https://via.placeholder.com/800x450?text=User+Profile+Screenshot)
  _Manage your personal information and settings._

## 🤝 Contributing

We welcome contributions to HomeSer! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'feat: Add new feature X'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please ensure your code adheres to the existing style and conventions.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

If you have any questions or feedback, feel free to reach out to the project maintainers.

---

Made with ❤️ by MushfiqPlabon
