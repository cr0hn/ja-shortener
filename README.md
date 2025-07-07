<div align="center">
  <img src="https://github.com/cr0hn/ja-shortener/blob/main/ja_shortener/shortener/static/shortener/logo.png" alt="JAUS Logo" width="300" height="300" style="max-width: 300px; max-height: 300px;">
</div>

# Just Another URL Shortener (JAUS)

A simple, fast, and secure URL shortener service built with Django. This service allows you to create short URLs from long ones, track visits, and manage your shortened URLs through a beautiful admin interface.

## Table of Contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Features](#features)
- [Why this project?](#why-this-project)
- [How it works?](#how-it-works)
- [Screenshots](#screenshots)
- [Quick Start with Docker](#quick-start-with-docker)
  - [Docker Compose](#docker-compose)
  - [Helm Chart](#helm-chart)
    - [Add the Helm repository:](#add-the-helm-repository)
    - [Install the chart:](#install-the-chart)
    - [Customize the installation:](#customize-the-installation)
    - [Upgrade the installation:](#upgrade-the-installation)
    - [Uninstall the chart:](#uninstall-the-chart)
    - [Chart values](#chart-values)
- [Configuration](#configuration)
  - [Backup Configuration](#backup-configuration)
    - [S3 Backup Configuration](#s3-backup-configuration)
    - [Local Backup Configuration](#local-backup-configuration)
  - [Backup Commands](#backup-commands)
    - [Manual Backup](#manual-backup)
    - [Restore Backup](#restore-backup)
    - [List Backups](#list-backups)
  - [Automated Backups](#automated-backups)
    - [Using Cron](#using-cron)
    - [Using Docker with Cron](#using-docker-with-cron)
    - [Using Systemd Timer](#using-systemd-timer)
    - [Kubernetes CronJob](#kubernetes-cronjob)
- [Important Considerations](#important-considerations)
  - [High Availability (HA) Setup](#high-availability-ha-setup)
  - [Production Checklist](#production-checklist)
- [License](#license)
  - [License Terms](#license-terms)
  - [Commercial License](#commercial-license)
- [Author](#author)
- [Contributing](#contributing)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Features

- 🚀 Fast and lightweight
- 🔒 Secure URL shortening
- 📊 Visit tracking
- 🎨 Beautiful admin interface using Unfold
- 🐳 Docker support
- 🔄 Redis caching support
- 📝 Sentry integration for error tracking
- ☸️ Kubernetes support
- 💾 Automatic database backups
  - S3 storage support
  - Local storage support

## Why this project?

I created this project because I needed a simple, lightweight, and quickly deployable URL shortener. While there are many URL shorteners available, I couldn't find one that met my specific requirements:

- Simple and straightforward interface
- Easy to deploy and maintain
- Open source but production-ready
- No unnecessary complexity
- Beautiful but functional admin interface

After searching extensively and not finding a solution that ticked all these boxes, I decided to create my own. This project is the result of that effort - a URL shortener that's both powerful and simple to use.

Whether you're looking to deploy it for personal use or in a production environment, Just Another URL Shortener provides all the essential features without the bloat. It's designed to be maintainable, secure, and efficient.

## How it works?

After installing the project, you can access the admin interface at `http://localhost:8000/admin/` (you must configure the `ADMIN_URL` environment variable to change the default admin URL).

At the admin interface, you can:

- Create new shortened URLs with a single click
- View detailed analytics for each URL, including:

   - Total visits
   - Unique visitors
   - Visit trends over time
   - Geographic distribution of visitors

**No technical knowledge is required** - it's designed to be user-friendly while providing powerful features under the hood.

## Screenshots

Some screenshots of the admin interface:

![Screenshot 1](./screenshots/sc-1.png)
![Screenshot 1](./screenshots/sc-2.png)
![Screenshot 1](./screenshots/sc-2.png)


## Quick Start with Docker

The simplest way to run Just Another URL Shortener is using Docker:

```bash
docker run -d \
  -p 8080:8080 \
  -e SECRET_KEY=your-secret-key \
  -e SUPERUSER_USERNAME=admin \
  -e SUPERUSER_EMAIL=admin@example.com \
  -e SUPERUSER_PASSWORD=admin123 \
  cr0hn/ja-shortener
```

> By default, the application uses SQLite as the database if no `DATABASE_URL` environment variable is provided.

### Docker Compose

> **⚠️ Note:** The Docker image is built with PostgreSQL 15 client tools. While it should work with other PostgreSQL versions, it's optimized and tested with PostgreSQL 15.

For a more complete setup with PostgreSQL and Redis:

```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ja_shortener
      POSTGRES_USER: ja_shortener
      POSTGRES_PASSWORD: ja_shortener_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    command: redis-server --requirepass redis_password
    volumes:
      - redis_data:/data

  ja-shortener:
    image: cr0hn/ja-shortener:latest
    environment:
      - SECRET_KEY=your-secret-key
      - DATABASE_URL=postgresql://ja_shortener:ja_shortener_password@postgres:5432/ja_shortener
      - REDIS_URL=redis://:redis_password@redis:6379/0
      - SUPERUSER_USERNAME=admin
      - SUPERUSER_EMAIL=admin@example.com
      - SUPERUSER_PASSWORD=admin123
    depends_on:
      - postgres
      - redis

volumes:
  postgres_data:
  redis_data:
```

Save as `docker-compose.yml` and run:

```bash
docker-compose up -d
```

### Helm Chart

Just Another URL Shortener is available as a Helm chart on [ArtifactHub](https://artifacthub.io/packages/helm/cr0hn/ja-shortener).

#### Add the Helm repository:

```bash
helm repo add cr0hn https://cr0hn.github.io/ja-shortener/
helm repo update
```

#### Install the chart:

```bash
# Basic installation
helm install ja-shortener cr0hn/ja-shortener

# Installation with custom values
helm install ja-shortener cr0hn/ja-shortener -f values.yaml

# Installation in a specific namespace
helm install ja-shortener cr0hn/ja-shortener -n your-namespace --create-namespace
```

#### Customize the installation:

Create a `values.yaml` file:

```yaml
# Basic configuration
replicaCount: 2

# Django configuration
django:
  secretKey: "your-secret-key"
  admin:
    username: "admin"
    email: "admin@example.com"
    password: "admin123"

# Enable autoscaling
autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80

# Configure ingress
ingress:
  enabled: true
  hosts:
    - host: your-domain.com
      paths:
        - path: /
          pathType: Prefix
```

> **⚠️ Note:** The Helm chart includes Redis by default for High Availability deployments and proper session management.

#### Upgrade the installation:

```bash
helm upgrade ja-shortener cr0hn/ja-shortener -f values.yaml
```

#### Uninstall the chart:

```bash
helm uninstall ja-shortener
```

#### Chart values

You can find the default values for the chart in [Artifact Hub](https://artifacthub.io/packages/helm/cr0hn/ja-shortener) or by running:

## Configuration

The application can be configured using environment variables. Here's a complete list of available options:

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| SECRET_KEY | Django secret key for security | 7dfbc1e6b896492da9cd5ac4b77c11f3167d096998124cfba89e695daebd1047 | Yes |
| DEBUG | Enable debug mode | False | No |
| ALLOWED_HOSTS | List of allowed hosts | * | No |
| CSRF_TRUSTED_ORIGINS | List of trusted origins for CSRF | http://localhost | No |
| DATABASE_URL | Database connection URL | SQLite (development) | No |
| REDIS_URL | Redis connection URL | None (disabled) | No |
| SENTRY_DSN | Sentry DSN for error tracking | None (disabled) | No |
| ADMIN_URL | Custom admin URL path | admin/ | No |
| ENABLE_VISITS_TRACKING | Enable visit tracking | True | No |
| ENABLE_BACKUP | Enable automatic backups | False | No |
| BACKUP_TYPE | Type of backup storage (s3/local) | None | Yes (if ENABLE_BACKUP=True) |
| BACKUP_ACCESS_KEY | AWS Access Key for S3 backups | None | Yes (for S3) |
| BACKUP_SECRET_KEY | AWS Secret Key for S3 backups | None | Yes (for S3) |
| BACKUP_BUCKET_NAME | S3 Bucket name for backups | None | Yes (for S3) |
| BACKUP_DEFAULT_ACL | S3 ACL for backups | private | No |
| BACKUP_REGION | AWS Region for S3 backups | None | Yes (for S3) |
| BACKUP_ENDPOINT_URL | Custom S3 endpoint URL | None | No |
| BACKUP_LOCATION | Local directory for backups | /data/backups | No |
| GUNICORN_WORKERS | Number of Gunicorn workers | 4 | No |
| GUNICORN_LOG_LEVEL | Gunicorn log level | INFO | No |
| SUPERUSER_USERNAME | Superuser username | None | Yes |
| SUPERUSER_EMAIL | Superuser email | None | Yes |
| SUPERUSER_PASSWORD | Superuser password | None | Yes |

### Backup Configuration

> **⚠️ Note:** The backup functionality uses PostgreSQL 15 client tools (`pg_dump`, `psql`). Ensure your PostgreSQL database version is compatible with these tools.

The application uses [django-dbbackup](https://django-dbbackup.readthedocs.io/) for database backups. Here are the available configuration options:

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| ENABLE_BACKUP | Enable automatic backups | False | No |
| BACKUP_TYPE | Type of backup storage (s3/local) | None | Yes (if ENABLE_BACKUP=True) |

#### S3 Backup Configuration

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| BACKUP_ACCESS_KEY | AWS Access Key | None | Yes (for S3) |
| BACKUP_SECRET_KEY | AWS Secret Key | None | Yes (for S3) |
| BACKUP_BUCKET_NAME | S3 Bucket name | None | Yes (for S3) |
| BACKUP_DEFAULT_ACL | S3 ACL for backups | private | No |
| BACKUP_REGION | AWS Region | None | Yes (for S3) |
| BACKUP_ENDPOINT_URL | Custom S3 endpoint URL | None | No |

#### Local Backup Configuration

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| BACKUP_LOCATION | Local directory for backups | /data/backups | No |

### Backup Commands

Once configured, you can use the following commands to manage your backups:

#### Manual Backup

```bash
# Create a database backup
python manage.py dbbackup

# Create a compressed backup
python manage.py dbbackup --compress

# Create an encrypted backup
python manage.py dbbackup --encrypt

# Create a backup with both compression and encryption
python manage.py dbbackup --compress --encrypt
```

#### Restore Backup

```bash
# Restore the latest backup
python manage.py dbrestore

# Restore a specific backup file
python manage.py dbrestore --input-filename=backup-filename.dump

# Restore a compressed backup
python manage.py dbrestore --uncompress

# Restore an encrypted backup
python manage.py dbrestore --decrypt --passphrase=your-passphrase
```

#### List Backups

```bash
# List all backups
python manage.py listbackups

# List only database backups
python manage.py listbackups --content-type=db

# List only compressed backups
python manage.py listbackups --compressed
```

### Automated Backups

To automate backups, you can use cron jobs or systemd timers. Here are some examples:

#### Using Cron

Add to your crontab (`crontab -e`):

```bash
# Daily backup at 2 AM
0 2 * * * cd /path/to/project && python manage.py dbbackup --compress >> /var/log/backups.log 2>&1

# Weekly backup on Sunday at 3 AM
0 3 * * 0 cd /path/to/project && python manage.py dbbackup --compress --servername=weekly >> /var/log/backups.log 2>&1
```

#### Using Docker with Cron

```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ja_shortener
      POSTGRES_USER: ja_shortener
      POSTGRES_PASSWORD: ja_shortener_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  ja-shortener:
    image: cr0hn/ja-shortener:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - DATABASE_URL=postgresql://ja_shortener:ja_shortener_password@postgres:5432/ja_shortener
      - ENABLE_BACKUP=True
      - BACKUP_TYPE=s3
      - BACKUP_ACCESS_KEY=your-aws-access-key
      - BACKUP_SECRET_KEY=your-aws-secret-key
      - BACKUP_BUCKET_NAME=your-backup-bucket
      - BACKUP_REGION=us-east-1
    command: |
      sh -c "echo '0 2 * * * python manage.py dbbackup --compress >> /var/log/backups.log 2>&1' > /etc/crontabs/root && crond -f -l 8"

volumes:
  postgres_data:
```

#### Using Systemd Timer

Create a service file `/etc/systemd/system/ja-shortener-backup.service`:

```ini
[Unit]
Description=Just Another URL Shortener Database Backup
After=network.target

[Service]
Type=oneshot
User=ja_shortener
WorkingDirectory=/path/to/project
ExecStart=/usr/bin/python manage.py dbbackup --compress
```

Create a timer file `/etc/systemd/system/ja-shortener-backup.timer`:

```ini
[Unit]
Description=Run Just Another URL Shortener backup daily

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start the timer:

```bash
sudo systemctl enable ja-shortener-backup.timer
sudo systemctl start ja-shortener-backup.timer
```

#### Kubernetes CronJob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: ja-shortener-backup
  namespace: default
spec:
  schedule: "0 */12 * * *"  # Every 12 hours
  concurrencyPolicy: Forbid
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: cr0hn/ja-shortener:latest
            command: ["python", "manage.py", "dbbackup", "--compress"]
            env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: ja-shortener-secrets
                  key: database-url
            - name: BACKUP_ACCESS_KEY
              valueFrom:
                secretKeyRef:
                  name: ja-shortener-secrets
                  key: backup-access-key
            - name: BACKUP_SECRET_KEY
              valueFrom:
                secretKeyRef:
                  name: ja-shortener-secrets
                  key: backup-secret-key
            - name: BACKUP_BUCKET_NAME
              value: "your-backup-bucket"
            - name: BACKUP_REGION
              value: "us-east-1"
            - name: ENABLE_BACKUP
              value: "true"
            - name: BACKUP_TYPE
              value: "s3"
          restartPolicy: OnFailure

```

## Important Considerations

### High Availability (HA) Setup

When deploying in a High Availability environment, please consider the following:

1. **Session Management**:

- If running multiple instances, you **MUST** configure Redis for session management
- Without Redis, users will be logged out when requests hit different instances
- Example Redis configuration:

```bash
REDIS_URL=redis://your-redis-host:6379/0
```

2. **Database Backups**:

- Regular backups are **crucial** for data safety
- Consider using S3 or similar cloud storage for backup redundancy
- Test restore procedures regularly
- Keep backup encryption keys secure

3. **Load Balancing**:

- Ensure sticky sessions are enabled in your load balancer
- Configure proper health checks
- Consider using a CDN for static files

4. **Security Considerations**:

- Always use HTTPS in production
- Keep your `SECRET_KEY` secure and rotate it periodically
- Regularly update dependencies
- Monitor for suspicious activities

> **⚠️ Note:** The `SECRET_KEY` is used to sign the session cookies. *If you lose it, all users will be logged out.*

5. **Performance**:

- Redis caching is recommended for high-traffic deployments
- Adjust `GUNICORN_WORKERS` based on your server's CPU cores (recommended: CPU cores × 4 - due to asynchronous working threads) for optimal performance
- Monitor memory usage and adjust accordingly

6. **Monitoring**:

- Enabling Sentry for error tracking **is recommended**
- Set up proper logging
- Monitor database connections
- Track URL redirection performance

### Production Checklist

Before going to production, ensure you have:

- [ ] Configured Redis for session management
- [ ] Set up proper database backups
- [ ] Enabled HTTPS
- [ ] Configured proper logging
- [ ] Set up monitoring
- [ ] Tested backup and restore procedures
- [ ] Secured all sensitive credentials
- [ ] Configured proper error handling
- [ ] Set up rate limiting if needed
- [ ] Tested under load

## License

This project is licensed under the Functionary Source License (FSL). See the [LICENSE](LICENSE) file for details.

### License Terms

This project is available under the Functionary Source License (FSL). You are free to:

- Deploy and use the software for any purpose
- Modify the source code
- Run it in production environments
- Use it for personal or business needs

However, you are **NOT allowed to**:

- Sell or resell this software as a service
- Offer URL shortening services commercially using this software
- Create derivative works that compete with this software as a service

If you need to use this software in a way that conflicts with these terms, please contact me at cr0hn<at>cr0hn.com to discuss licensing options.

### Commercial License

For commercial use that conflicts with the FSL terms, a commercial license is available:

**1000€/year + applicable taxes**

> Note: This license does not include support services. 

To purchase a commercial license or discuss custom licensing options, please contact cr0hn<at>cr0hn.com.

## Author

- Daniel García (cr0hn) - cr0hn<at>cr0hn.com
- [LinkedIn](https://www.linkedin.com/in/garciagarciadaniel/)
- [GitHub](https://github.com/cr0hn)
- [Twitter](https://twitter.com/ggdaniel)
- [Blog](https://www.cr0hn.com)

## Changelog

### [v0.1.3]

#### Added

- **URL Shortener Core Functionality**

  - Added new characters to the short code generation algorithm: `-` and `_`
  - Custom short code support with validation
  - Configurable minimum length via `SHORTENER_MINIMAL_LENGTH` setting
  - Added `SHORTENER_HOST` configuration variable to customize the host for shortened URLs
  - Full shortened URLs (including domain) are now displayed in the admin interface for easy copy and paste
  - Smart algorithm that finds the last consecutive code and generates the next one

#### Changed

- **Admin Interface**

  - Short code is now editable in the admin interface
  - Short code is now displayed as a clickable link to the edit page in the admin list view
  - Short code is now displayed with the full shortened URL (including domain) for easy copy and paste

### [v0.1.3]

#### Changed

- **Docker Image**

  - Updated the Docker image to use the latest version of the application

- **Helm Chart**

  - Updated the Helm chart to use the latest version of the application

### [v0.1.1 - v0.1.2]

Minor changes in the Docker image and Helm chart.

### [v0.1.0]

#### Initial Release

- **First version** of Just Another URL Shortener
- Core URL shortening functionality
- Basic admin interface
- Docker containerization
- PostgreSQL and Redis support

---

For detailed information about each release, please refer to the [GitHub releases page](https://github.com/cr0hn/ja-shortener/releases).

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.
