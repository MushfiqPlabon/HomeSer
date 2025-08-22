# Research Findings

## Django on Vercel Python Runtime

### Sources
- [Vercel Python Runtime Documentation](https://vercel.com/docs/functions/runtimes/python) (Accessed: 2025-08-21)

### Summary
- Vercel supports Python serverless functions which can be used to deploy Django applications.
- The deployment requires a `vercel.json` configuration file to route requests to the WSGI application.
- The build process should handle static file collection and database migrations.

## Django Settings for Vercel

### Sources
- [Django Settings for Vercel](https://docs.djangoproject.com/en/stable/ref/settings/) (Accessed: 2025-08-21)

### Summary
- `ALLOWED_HOSTS` must include `*.vercel.app` to allow requests from Vercel deployments.
- `CSRF_TRUSTED_ORIGINS` should also include `*.vercel.app` to ensure CSRF protection works properly.

## Serving Static Files with WhiteNoise

### Sources
- [WhiteNoise Documentation](http://whitenoise.evans.io/en/stable/) (Accessed: 2025-08-21)

### Summary
- WhiteNoise allows Django to serve its own static files, which is essential for Vercel deployments where external CDNs might not be easily configured.
- It needs to be added to the middleware in `settings.py`.

## DRF SimpleJWT with HTTP-only Cookies

### Sources
- [DRF SimpleJWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) (Accessed: 2025-08-21)
- [Using JWT with HTTP-only Cookies](https://medium.com/@davidstevens_52003/how-to-use-jwt-with-http-only-cookies-in-django-rest-framework-9c8a5dc7e2d2) (Accessed: 2025-08-21)

### Summary
- SimpleJWT can be configured to use HTTP-only cookies for storing tokens, enhancing security.
- Refresh token rotation is supported and recommended for better security practices.

## Connecting to Supabase, Cloudinary, and Upstash

### Sources
- [Supabase Python Client](https://supabase.com/docs/guides/getting-started/tutorials/with-python) (Accessed: 2025-08-21)
- [Cloudinary Python SDK](https://cloudinary.com/documentation/python_integration) (Accessed: 2025-08-21)
- [Upstash Redis Python Client](https://upstash.com/docs/redis/overall/gettingstarted) (Accessed: 2025-08-21)

### Summary
- Each service provides Python clients or SDKs that can be integrated into Django settings.
- Environment variables should be used to configure connections securely.

## Using Tailwind CSS v3 with Django

### Sources
- [Tailwind CSS Documentation](https://v3.tailwindcss.com/docs/guides/django) (Accessed: 2025-08-21)

### Summary
- Tailwind CSS can be integrated with Django by installing it via npm and configuring the paths to template files.
- The CSS build process should be part of the static file generation.

## Vercel Free Tier Limitations

### Sources
- [Vercel Pricing](https://vercel.com/pricing) (Accessed: 2025-08-21)

### Summary
- The free tier has limitations on execution time for serverless functions, which may affect long-running tasks.
- Cold start times can impact performance.