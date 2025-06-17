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
- 💾 Automatic database backups
  - S3 storage support
  - Local storage support

## Screenshots

Some screenshots of the admin interface:

![Screenshot 1](./screenshots/sc-1.png)
![Screenshot 1](./screenshots/sc-2.png)
![Screenshot 1](./screenshots/sc-2.png)


## Quick Start with Docker

**Basic expected**

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

### Backup Configuration

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
version: '3.8'

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
    environment:
      - SECRET_KEY=your-secret-key
      - DATABASE_URL=postgresql://ja_shortener:ja_shortener_password@postgres:5432/ja_shortener
      - ENABLE_BACKUP=True
      - BACKUP_TYPE=s3
      - BACKUP_ACCESS_KEY=your-aws-access-key
      - BACKUP_SECRET_KEY=your-aws-secret-key
      - BACKUP_BUCKET_NAME=your-backup-bucket
      - BACKUP_REGION=us-east-1
    depends_on:
      - postgres

  backup-cron:
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
    command: >
      sh -c "echo '0 2 * * * python manage.py dbbackup --compress >> /var/log/backups.log 2>&1' > /etc/crontabs/root &&
             crond -f -l 8"

volumes:
  postgres_data:
```

#### Using Systemd Timer

Create a service file `/etc/systemd/system/ja-shortener-backup.service`:

```ini
[Unit]
Description=Ja Shortener Database Backup
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
Description=Run Ja Shortener backup daily

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

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the Functionary Source License (FSL). See the [LICENSE](LICENSE) file for details.

## Commercial License

For commercial use or if you need a commercial license, please contact me at cr0hn<at>cr0hn.com.

## Author

- Daniel García (cr0hn) - cr0hn<at>cr0hn.com











