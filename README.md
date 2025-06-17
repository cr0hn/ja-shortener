# Just An URL Shortener

A simple, fast, and secure URL shortener service built with Django. This service allows you to create short URLs from long ones, track visits, and manage your shortened URLs through a beautiful admin interface.

## Features

- 🚀 Fast and lightweight
- 🔒 Secure URL shortening
- 📊 Visit tracking
- 🎨 Beautiful admin interface using Unfold
- 🐳 Docker support
- 🔄 Redis caching support
- 📝 Sentry integration for error tracking
- 🔄 Redis caching support

## Screenshots

![Screenshot 1](./screenshots/sc-1.png)
![Screenshot 1](./screenshots/sc-2.png)
![Screenshot 1](./screenshots/sc-2.png)


## Quick Start with Docker

**Basic expected

```bash
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e SUPERUSER_USERNAME=your-username \
  -e SUPERUSER_EMAIL=your-email \
  -e SUPERUSER_PASSWORD=your-password
  cr0hn/ja-shortener
```

**Extended example**

```bash
docker run -d \
  -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e SUPERUSER_USERNAME=your-username \
  -e SUPERUSER_EMAIL=your-email \
  -e DATABASE_URL=postgres://your-username:your-password@your-host:your-port/your-database \
  -e REDIS_URL=redis://your-host:your-port/your-database \
  -e SENTRY_DSN=your-sentry-dsn \
  -e ADMIN_URL=admin/ \
  -e ENABLE_VISITS_TRACKING=True \
  -e GUNICORN_WORKERS=5 \
  -e GUNICORN_LOG_LEVEL=INFO \
  -e SUPERUSER_PASSWORD=your-password \
  -e DEBUG=False \
  -e ALLOWED_HOSTS=your-domain.com \
  -e CSRF_TRUSTED_ORIGINS=https://your-domain.com \
  cr0hn/ja-shortener
```

## Configuration


The application can be configured using environment variables. Here's a complete list of available options:

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| SECRET_KEY | Django secret key for security | Random generated key | Yes |
| DEBUG | Enable debug mode | False | No |
| ALLOWED_HOSTS | List of allowed hosts | * | No |
| CSRF_TRUSTED_ORIGINS | List of trusted origins for CSRF | http://localhost | No |
| DATABASE_URL | Database connection URL | SQLite (development) | No |
| REDIS_URL | Redis connection URL | None (disabled) | No |
| SENTRY_DSN | Sentry DSN for error tracking | None (disabled) | No |
| ADMIN_URL | Custom admin URL path | admin/ | No |
| ENABLE_VISITS_TRACKING | Enable visit tracking | True | No |
| GUNICORN_WORKERS | Number of Gunicorn workers | 5 | No |
| GUNICORN_LOG_LEVEL | Gunicorn log level | INFO | No |
| SUPERUSER_USERNAME | Superuser username | None | Yes |
| SUPERUSER_EMAIL | Superuser email | None | Yes |
| SUPERUSER_PASSWORD | Superuser password | None | Yes |

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the Functionary Source License (FSL). See the [LICENSE](LICENSE) file for details.

## Author

- Daniel García (cr0hn) - cr0hn@cr0hn.com











