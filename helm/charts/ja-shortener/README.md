# JA Shortener Helm Chart

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.0.0](https://img.shields.io/badge/AppVersion-1.0.0-informational?style=flat-square)

JA Shortener is a simple, fast, and secure URL shortener service built with Django. This Helm chart provides an easy way to deploy JA Shortener on Kubernetes with PostgreSQL and Redis dependencies.

## Features

- 🚀 High-performance URL shortening service
- 🔒 Built-in security features
- 📊 Admin interface for URL management
- 🗄️ PostgreSQL database support
- ⚡ Redis caching for improved performance
- 🔄 Horizontal Pod Autoscaling support
- 🔐 Configurable backup options (S3 or local)
- 📈 Sentry integration for error monitoring

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+
- PV provisioner support in the underlying infrastructure

> **⚠️ Note:** The JA Shortener Docker image is built with PostgreSQL 15 client tools. While it should work with other PostgreSQL versions, it's optimized and tested with PostgreSQL 15.

## Installation

### Add Helm Repository

```bash
helm repo add ja-shortener https://cr0hn.github.io/ja-shortener
helm repo update
```

### Install Chart

```bash
# Install with default values
helm install my-ja-shortener ja-shortener/ja-shortener

# Install with custom values
helm install my-ja-shortener ja-shortener/ja-shortener -f my-values.yaml

# Install in specific namespace
helm install my-ja-shortener ja-shortener/ja-shortener --namespace ja-shortener --create-namespace

# Install with Traefik ingress
helm install my-ja-shortener ja-shortener/ja-shortener -f values-traefik.yaml
```

## Uninstallation

```bash
helm uninstall my-ja-shortener
```

## Configuration

The following table lists the configurable parameters of the JA Shortener chart and their default values.

### Global Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas for the deployment | `1` |
| `nameOverride` | Override the name of the chart | `""` |
| `fullnameOverride` | Override the full name of the chart | `""` |

### Image Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.repository` | JA Shortener image repository | `cr0hn/ja-shortener` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `image.tag` | Image tag (overrides the image tag whose default is the chart appVersion) | `"latest"` |
| `imagePullSecrets` | Docker registry secret names as an array | `[]` |

### Service Account

| Parameter | Description | Default |
|-----------|-------------|---------|
| `serviceAccount.create` | Specifies whether a service account should be created | `true` |
| `serviceAccount.annotations` | Annotations to add to the service account | `{}` |
| `serviceAccount.name` | The name of the service account to use | `""` |

### Security Context

| Parameter | Description | Default |
|-----------|-------------|---------|
| `podAnnotations` | Annotations to add to the pod | `{}` |
| `podSecurityContext` | Security context for the pod | `{}` |
| `securityContext` | Security context for the container | `{}` |

### Service Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `service.type` | Kubernetes service type | `ClusterIP` |
| `service.port` | Service port | `8080` |

### Ingress Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress controller resource | `false` |
| `ingress.className` | IngressClass that will be used to implement the Ingress | `""` |
| `ingress.annotations` | Additional annotations for the Ingress resource | `{}` |
| `ingress.host` | Host for the ingress | `"chart-example.local"` |
| `ingress.hosts` | List of hosts for the ingress | `[{"host": "chart-example.local", "paths": [{"path": "/", "pathType": "ImplementationSpecific"}]}]` |
| `ingress.tls` | TLS configuration for the ingress | `[]` |

**Note:** Currently, the chart only implements Traefik IngressRoute resources. Standard Kubernetes Ingress resources are not yet implemented. Use `traefik.enabled: true` for ingress functionality.

### Traefik Ingress Parameters

JA Shortener supports Traefik as an alternative to standard Kubernetes Ingress. Traefik uses IngressRoute resources instead of standard Ingress resources.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `traefik.enabled` | Enable Traefik IngressRoute (disables standard ingress) | `false` |
| `traefik.entryPoints.web` | Enable Traefik web entry point for HTTP traffic | `true` |
| `traefik.entryPoints.websecure` | Enable Traefik websecure entry point for HTTPS traffic | `true` |
| `traefik.tls` | TLS configuration for Traefik | `[]` |

**Note:** When using Traefik, set `ingress.enabled: false` to avoid conflicts between standard Ingress and Traefik IngressRoute resources. The chart will automatically fail if both are enabled simultaneously.

**Traefik EntryPoints:** The `web` and `websecure` entryPoints are boolean flags that control which Traefik entry points are used. When `true`, the corresponding entry point (`web` for HTTP, `websecure` for HTTPS) will be included in the IngressRoute. You can disable either entry point by setting it to `false`.

### Resource Management

| Parameter | Description | Default |
|-----------|-------------|---------|
| `resources.limits.cpu` | CPU limit for the container | `1000m` |
| `resources.limits.memory` | Memory limit for the container | `1Gi` |
| `resources.requests.cpu` | CPU request for the container | `500m` |
| `resources.requests.memory` | Memory request for the container | `512Mi` |

### Autoscaling Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `autoscaling.enabled` | Enable Horizontal Pod Autoscaler | `false` |
| `autoscaling.minReplicas` | Minimum number of replicas | `1` |
| `autoscaling.maxReplicas` | Maximum number of replicas | `100` |
| `autoscaling.targetCPUUtilizationPercentage` | Target CPU utilization percentage | `80` |
| `autoscaling.targetMemoryUtilizationPercentage` | Target memory utilization percentage | `80` |

### Node Assignment

| Parameter | Description | Default |
|-----------|-------------|---------|
| `nodeSelector` | Node labels for pod assignment | `{}` |
| `tolerations` | Tolerations for pod assignment | `[]` |
| `affinity` | Affinity settings for pod assignment | `{}` |

### Django Application Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `django.secretKey` | Django secret key (change in production!) | `"change-me-in-production"` |
| `django.debug` | Enable Django debug mode | `false` |
| `django.allowedHosts` | Django allowed hosts | `"*"` |
| `django.csrfTrustedOrigins` | CSRF trusted origins | `"http://localhost"` |
| `django.healthPath` | Health check path for liveness/readiness probes | `"health/"` |

### Django Admin Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `django.admin.url` | Admin URL path | `"admin/"` |
| `django.admin.username` | Admin username | `"admin"` |
| `django.admin.email` | Admin email | `"admin@example.com"` |
| `django.admin.password` | Admin password (change in production!) | `"change-me-in-production"` |

### Gunicorn Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `django.gunicorn.workers` | Number of Gunicorn worker processes | `5` |
| `django.gunicorn.logLevel` | Gunicorn log level | `"INFO"` |

### Sentry Integration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `django.sentry.enabled` | Enable Sentry error monitoring | `false` |
| `django.sentry.dsn` | Sentry DSN URL | `""` |

### Backup Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `django.backup.enabled` | Enable backup functionality | `false` |
| `django.backup.type` | Backup type (s3 or local) | `"s3"` |
| `django.backup.schedule` | Cron schedule for backup jobs | `"0 2 * * *"` |
| `django.backup.successfulJobsHistoryLimit` | Number of successful backup jobs to keep | `3` |
| `django.backup.failedJobsHistoryLimit` | Number of failed backup jobs to keep | `1` |
| `django.backup.restartPolicy` | Restart policy for backup jobs | `"OnFailure"` |
| `django.backup.backoffLimit` | Number of retries before marking backup job as failed | `3` |
| `django.backup.s3.accessKey` | S3 access key | `""` |
| `django.backup.s3.secretKey` | S3 secret key | `""` |
| `django.backup.s3.bucketName` | S3 bucket name | `""` |
| `django.backup.s3.region` | S3 region | `""` |
| `django.backup.s3.endpointUrl` | S3 endpoint URL (for S3-compatible services) | `""` |
| `django.backup.local.location` | Local backup location | `"/data/backups"` |

### Internal PostgreSQL Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `postgresql.enabled` | Enable internal PostgreSQL database | `true` |
| `postgresql.auth.database` | PostgreSQL database name | `ja_shortener` |
| `postgresql.auth.username` | PostgreSQL username | `ja_shortener` |
| `postgresql.auth.password` | PostgreSQL password | `ja_shortener_password` |
| `postgresql.primary.persistence.enabled` | Enable PostgreSQL persistence | `true` |
| `postgresql.primary.persistence.size` | PostgreSQL storage size | `5Gi` |
| `postgresql.service.ports.postgresql` | PostgreSQL service port | `5432` |

### External Database Configuration

When using external database, internal PostgreSQL is disabled and not deployed.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `externalDatabase.enabled` | Enable external database (disables internal PostgreSQL) | `false` |
| `externalDatabase.type` | Database type (postgresql, mysql, sqlite) | `"postgresql"` |
| `externalDatabase.host` | External database host | `""` |
| `externalDatabase.port` | External database port | `5432` |
| `externalDatabase.database` | External database name | `""` |
| `externalDatabase.username` | External database username | `""` |
| `externalDatabase.password` | External database password | `""` |
| `externalDatabase.dsn` | Full DATABASE_DSN (overrides individual settings) | `""` |

### Internal Redis Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `redis.enabled` | Enable internal Redis instance | `true` |
| `redis.auth.password` | Redis password | `redis_password` |
| `redis.master.persistence.enabled` | Enable Redis persistence | `true` |
| `redis.master.persistence.size` | Redis storage size | `5Gi` |
| `redis.service.ports.redis` | Redis service port | `6379` |

### External Redis Configuration

When using external Redis, internal Redis is disabled and not deployed.

| Parameter | Description | Default |
|-----------|-------------|---------|
| `externalRedis.enabled` | Enable external Redis (disables internal Redis) | `false` |
| `externalRedis.host` | External Redis host | `""` |
| `externalRedis.port` | External Redis port | `6379` |
| `externalRedis.password` | External Redis password | `""` |
| `externalRedis.database` | External Redis database number | `0` |
| `externalRedis.dsn` | Full REDIS_DSN (overrides individual settings) | `""` |

## Example Values

### Basic Setup

```yaml
# values.yaml
django:
  secretKey: "your-super-secret-key-here"
  allowedHosts: "yourdomain.com"
  csrfTrustedOrigins: "https://yourdomain.com"
  admin:
    username: "admin"
    email: "admin@yourdomain.com"
    password: "your-secure-admin-password"

ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
  hosts:
    - host: short.yourdomain.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: ja-shortener-tls
      hosts:
        - short.yourdomain.com
```

### Traefik Setup

```yaml
# values-traefik.yaml
django:
  secretKey: "your-super-secret-key-here"
  allowedHosts: "short.yourdomain.com"
  csrfTrustedOrigins: "https://short.yourdomain.com"
  healthPath: "health/"  # Custom health check endpoint
  admin:
    username: "admin"
    email: "admin@yourdomain.com"
    password: "your-secure-admin-password"

ingress:
  enabled: false  # Disable standard ingress
  host: "short.yourdomain.com"

traefik:
  enabled: true
  entryPoints:
    web: true
    websecure: true
```

### Traefik Setup with TLS

```yaml
# values-traefik-tls.yaml
django:
  secretKey: "your-super-secret-key-here"
  allowedHosts: "short.yourdomain.com"
  csrfTrustedOrigins: "https://short.yourdomain.com"
  admin:
    username: "admin"
    email: "admin@yourdomain.com"
    password: "your-secure-admin-password"

ingress:
  enabled: false
  host: "short.yourdomain.com"

traefik:
  enabled: true
  entryPoints:
    web: true
    websecure: true
  tls:
    - secretName: ja-shortener-tls
      hosts:
        - short.yourdomain.com
```

### Traefik Setup with HTTPS Only

```yaml
# values-traefik-https-only.yaml
django:
  secretKey: "your-super-secret-key-here"
  allowedHosts: "short.yourdomain.com"
  csrfTrustedOrigins: "https://short.yourdomain.com"
  admin:
    username: "admin"
    email: "admin@yourdomain.com"
    password: "your-secure-admin-password"

ingress:
  enabled: false
  host: "short.yourdomain.com"

traefik:
  enabled: true
  entryPoints:
    web: false        # Disable HTTP
    websecure: true   # Enable HTTPS only
  tls:
    - secretName: ja-shortener-tls
      hosts:
        - short.yourdomain.com
```

### Production Setup with Autoscaling

```yaml
# values-production.yaml
replicaCount: 3

django:
  secretKey: "your-production-secret-key"
  debug: false
  allowedHosts: "short.yourdomain.com"
  csrfTrustedOrigins: "https://short.yourdomain.com"
  
  sentry:
    enabled: true
    dsn: "https://your-sentry-dsn@sentry.io/project"
  
  backup:
    enabled: true
    type: "s3"
    s3:
      accessKey: "your-s3-access-key"
      secretKey: "your-s3-secret-key"
      bucketName: "ja-shortener-backups"
      region: "us-east-1"

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

resources:
  limits:
    cpu: 2000m
    memory: 2Gi
  requests:
    cpu: 1000m
    memory: 1Gi

postgresql:
  auth:
    password: "your-secure-db-password"
  primary:
    persistence:
      size: 20Gi

redis:
  auth:
    password: "your-secure-redis-password"
  master:
    persistence:
      size: 10Gi
```

### High Availability Setup

```yaml
# values-ha.yaml
replicaCount: 5

django:
  secretKey: "your-production-secret-key"
  debug: false
  allowedHosts: "short.yourdomain.com"
  csrfTrustedOrigins: "https://short.yourdomain.com"

autoscaling:
  enabled: true
  minReplicas: 5
  maxReplicas: 20
  targetCPUUtilizationPercentage: 60
  targetMemoryUtilizationPercentage: 70

resources:
  limits:
    cpu: 2000m
    memory: 4Gi
  requests:
    cpu: 1000m
    memory: 2Gi

# High availability for dependencies
postgresql:
  auth:
    password: "your-secure-db-password"
  primary:
    persistence:
      size: 100Gi
  readReplicas:
    replicaCount: 2

redis:
  auth:
    password: "your-secure-redis-password"
  sentinel:
    enabled: true
  master:
    persistence:
      size: 20Gi

# Backup with S3
django:
  backup:
    enabled: true
    type: "s3"
    schedule: "0 3 * * *"  # Daily at 3 AM
    successfulJobsHistoryLimit: 7
    failedJobsHistoryLimit: 3
    s3:
      accessKey: "your-s3-access-key"
      secretKey: "your-s3-secret-key"
      bucketName: "ja-shortener-backups-prod"
      region: "us-east-1"

affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
          - key: app.kubernetes.io/name
            operator: In
            values:
            - ja-shortener
        topologyKey: kubernetes.io/hostname
```

### Development Setup with Local Backups

```yaml
# values-dev.yaml
django:
  debug: true
  secretKey: "dev-secret-key-not-for-production"
  allowedHosts: "*"
  
  backup:
    enabled: true
    type: "local"
    schedule: "0 */6 * * *"  # Every 6 hours
    successfulJobsHistoryLimit: 2
    failedJobsHistoryLimit: 1
    local:
      location: "/data/backups"

resources:
  limits:
    cpu: 500m
    memory: 512Mi
  requests:
    cpu: 100m
    memory: 256Mi

postgresql:
  primary:
    persistence:
      size: 5Gi

redis:
  master:
    persistence:
      size: 2Gi
```

### Backup with MinIO (S3-compatible)

```yaml
# values-minio.yaml
django:
  backup:
    enabled: true
    type: "s3"
    schedule: "0 1 * * *"  # Daily at 1 AM
    s3:
      accessKey: "minio-access-key"
      secretKey: "minio-secret-key"
      bucketName: "ja-shortener-backups"
      region: "us-east-1"
      endpointUrl: "https://minio.yourdomain.com"
```

### Backup Schedule Examples

```yaml
# Different backup schedules
django:
  backup:
    enabled: true
    schedule: "0 2 * * *"          # Daily at 2 AM
    # schedule: "0 */12 * * *"     # Every 12 hours
    # schedule: "0 2 * * 0"        # Weekly on Sunday at 2 AM
    # schedule: "0 2 1 * *"        # Monthly on the 1st at 2 AM
    # schedule: "*/30 * * * *"     # Every 30 minutes (for testing)
```

### External Database Setup

```yaml
# values-external-db.yaml
# Using external PostgreSQL database
postgresql:
  enabled: false  # Disable internal PostgreSQL

externalDatabase:
  enabled: true
  type: "postgresql"
  host: "postgres.example.com"
  port: 5432
  database: "ja_shortener_prod"
  username: "ja_shortener_user"
  password: "secure_password_here"

# Using external Redis
redis:
  enabled: false  # Disable internal Redis

externalRedis:
  enabled: true
  host: "redis.example.com"
  port: 6379
  password: "redis_secure_password"
  database: 0

django:
  secretKey: "your-production-secret-key"
  allowedHosts: "short.yourdomain.com"
  csrfTrustedOrigins: "https://short.yourdomain.com"
```

### Cloud Database Services Setup

```yaml
# values-cloud-db.yaml
# Using AWS RDS PostgreSQL and ElastiCache Redis
postgresql:
  enabled: false

externalDatabase:
  enabled: true
  dsn: "postgresql://username:password@mydb.cluster-xyz.us-east-1.rds.amazonaws.com:5432/ja_shortener"

redis:
  enabled: false

externalRedis:
  enabled: true
  dsn: "redis://my-redis.xyz.cache.amazonaws.com:6379/0"

django:
  secretKey: "your-production-secret-key"
  backup:
    enabled: true
    type: "s3"
    s3:
      bucketName: "my-ja-shortener-backups"
      region: "us-east-1"
```

### Mixed Setup (External Database + Internal Redis)

```yaml
# values-mixed.yaml
# External PostgreSQL but internal Redis
postgresql:
  enabled: false

externalDatabase:
  enabled: true
  type: "postgresql"
  host: "managed-postgres.example.com"
  port: 5432
  database: "ja_shortener"
  username: "app_user"
  password: "database_password"

# Keep internal Redis for caching
redis:
  enabled: true
  auth:
    password: "internal_redis_password"
  master:
    persistence:
      size: 4Gi

django:
  secretKey: "your-secret-key"
  allowedHosts: "myapp.example.com"
```

### Database DSN Format Examples

```yaml
# Different database DSN formats for externalDatabase.dsn

# PostgreSQL
externalDatabase:
  dsn: "postgresql://user:pass@host:5432/dbname"
  # or with SSL
  dsn: "postgresql://user:pass@host:5432/dbname?sslmode=require"

# MySQL
externalDatabase:
  dsn: "mysql://user:pass@host:3306/dbname"

# SQLite (for development)
externalDatabase:
  dsn: "sqlite:///data/db.sqlite3"

# Redis DSN formats for externalRedis.dsn
externalRedis:
  dsn: "redis://host:6379/0"

  # or with password
  dsn: "redis://:password@host:6379/0"

  # or with username and password
  dsn: "redis://username:password@host:6379/0"
```

## External Database Support

JA Shortener supports using external databases instead of the bundled PostgreSQL and Redis charts. This is useful for production deployments where you want to use managed database services like AWS RDS, Google Cloud SQL, or Azure Database.

### When to Use External Databases

- **Production environments** where you need high availability and managed backups
- **Cloud deployments** using managed database services (AWS RDS, Google Cloud SQL, etc.)
- **Existing infrastructure** where databases are already provisioned
- **Cost optimization** by sharing databases across multiple applications
- **Compliance requirements** that mandate specific database configurations

### Configuration Priority

The chart uses the following priority order for database configuration:

1. **External Database DSN** (`externalDatabase.dsn`) - highest priority
2. **External Database individual settings** (`externalDatabase.host`, `port`, etc.)
3. **Internal PostgreSQL** (`postgresql.enabled: true`) - default

For Redis:

1. **External Redis DSN** (`externalRedis.dsn`) - highest priority  
2. **External Redis individual settings** (`externalRedis.host`, `port`, etc.)
3. **Internal Redis** (`redis.enabled: true`) - default

### Important Notes

- When using external databases, set `postgresql.enabled: false` and/or `redis.enabled: false`
- The backup CronJob will work with external PostgreSQL databases
- External databases must be accessible from the Kubernetes cluster
- Ensure proper network policies and security groups are configured
- For production, always use SSL/TLS connections to external databases
- Use DSN (Data Source Name) format for complex connection strings with parameters

### Migration from Internal to External

To migrate from internal to external databases:

1. **Backup your data** using the built-in backup functionality
2. **Set up your external database** and restore the backup
3. **Update your values.yaml** with external database configuration
4. **Upgrade your Helm release** with the new configuration

Example migration:
```bash
# 1. Create a backup
kubectl create job --from=cronjob/my-ja-shortener-backup migration-backup

# 2. Wait for backup completion and download
kubectl wait --for=condition=complete job/migration-backup --timeout=300s

# 3. Update values.yaml with external database config
# 4. Upgrade with new configuration
helm upgrade my-ja-shortener ja-shortener/ja-shortener -f values-external.yaml
```

## Upgrading

### To 0.2.0

Check the [CHANGELOG](https://github.com/cr0hn/ja-shortener/blob/main/CHANGELOG.md) for breaking changes.

```bash
helm upgrade my-ja-shortener ja-shortener/ja-shortener
```

## Automated Backups

> **⚠️ Note:** The automated backup functionality uses PostgreSQL 15 client tools (`pg_dump`). Ensure your PostgreSQL database version is compatible with these tools for proper backup operations.

JA Shortener includes automated backup functionality that can be configured to run on a schedule using Kubernetes CronJobs. The backup system supports both S3-compatible storage and local persistent volumes.

### Features

- **Automated PostgreSQL database backups** using `pg_dump`
- **Flexible scheduling** with cron expressions
- **Multiple storage backends** (S3, MinIO, local storage)
- **Automatic cleanup** of old backups (for local storage)
- **Job history management** with configurable limits
- **Retry logic** with configurable backoff limits

### Backup Types

#### S3-Compatible Storage
Backups are uploaded to S3 or S3-compatible services (like MinIO) with the following naming convention:
```
ja_shortener_backup_YYYYMMDD_HHMMSS.sql
```

#### Local Storage
Backups are stored in a persistent volume with automatic cleanup of files older than 7 days.

### Monitoring Backups

```bash
# Check backup job status
kubectl get cronjobs -l app.kubernetes.io/name=ja-shortener

# View backup job history
kubectl get jobs -l app.kubernetes.io/name=ja-shortener,app.kubernetes.io/component=backup

# Check backup logs
kubectl logs -l app.kubernetes.io/name=ja-shortener,app.kubernetes.io/component=backup

# Manually trigger a backup job
kubectl create job --from=cronjob/my-ja-shortener-backup manual-backup-$(date +%s)
```

### Backup Restore

#### From S3
```bash
# Download backup file
aws s3 cp s3://your-bucket/backups/ja_shortener_backup_20231215_020000.sql ./backup.sql

# Restore to database
kubectl exec -i deployment/my-ja-shortener-postgresql -- psql -U ja_shortener -d ja_shortener < backup.sql
```

#### From Local Storage
```bash
# Copy backup from persistent volume
kubectl cp my-ja-shortener-backup-pod:/data/backups/ja_shortener_backup_20231215_020000.sql ./backup.sql

# Restore to database
kubectl exec -i deployment/my-ja-shortener-postgresql -- psql -U ja_shortener -d ja_shortener < backup.sql
```

## Troubleshooting

### Check Pod Status

```bash
kubectl get pods -l app.kubernetes.io/name=ja-shortener
```

### View Logs

```bash
kubectl logs -l app.kubernetes.io/name=ja-shortener -f
```

### Check Service Connectivity

```bash
kubectl port-forward svc/my-ja-shortener 8080:8080
```

Then access http://localhost:8080

### Database Connection Issues

Check if PostgreSQL is running:
```bash
kubectl get pods -l app.kubernetes.io/name=postgresql
```

Check database connectivity:
```bash
kubectl exec -it deployment/my-ja-shortener -- python manage.py dbshell
```

### Backup Issues

Check backup CronJob status:
```bash
kubectl get cronjobs my-ja-shortener-backup
kubectl describe cronjob my-ja-shortener-backup
```

View failed backup jobs:
```bash
kubectl get jobs -l app.kubernetes.io/component=backup --field-selector status.successful!=1
```

Check backup job logs:
```bash
kubectl logs job/my-ja-shortener-backup-<job-id>
```

Common backup issues:
- **S3 credentials**: Verify AWS credentials and bucket permissions
- **Local storage**: Check if PVC is properly mounted and has sufficient space
- **Database connectivity**: Ensure the backup job can reach PostgreSQL
- **Resource limits**: Backup jobs may need more memory for large databases

### External Database Issues

Check external database connectivity:
```bash
# Test PostgreSQL connection from a pod
kubectl exec -it deployment/my-ja-shortener -- psql "$DATABASE_URL" -c "SELECT version();"

# Test Redis connection from a pod
kubectl exec -it deployment/my-ja-shortener -- redis-cli -u "$REDIS_URL" ping
```

Verify environment variables are set correctly:
```bash
kubectl exec deployment/my-ja-shortener -- env | grep -E "(DATABASE_URL|REDIS_URL)"
```

Common external database issues:
- **Network connectivity**: Ensure external databases are reachable from Kubernetes cluster
- **Firewall rules**: Check security groups/firewall rules allow connections from cluster
- **DNS resolution**: Verify database hostnames resolve correctly
- **SSL/TLS issues**: Check certificate validation for encrypted connections
- **Authentication**: Verify usernames, passwords, and connection strings are correct
- **Database permissions**: Ensure the database user has required permissions (CREATE, DROP, etc.)

Check database connection in application logs:
```bash
kubectl logs deployment/my-ja-shortener | grep -i database
kubectl logs deployment/my-ja-shortener | grep -i redis
```

### Traefik Issues

Check Traefik IngressRoute status:
```bash
kubectl get ingressroute -l app.kubernetes.io/name=ja-shortener
kubectl describe ingressroute my-ja-shortener
```

Verify Traefik is running and configured:
```bash
kubectl get pods -l app.kubernetes.io/name=traefik
kubectl logs -l app.kubernetes.io/name=traefik
```

Common Traefik issues:
- **EntryPoints not configured**: Ensure Traefik entryPoints match your configuration
- **Host mismatch**: Verify the host in `ingress.host` matches your domain
- **TLS certificate issues**: Check if TLS secret exists and is valid
- **Service connectivity**: Ensure Traefik can reach the JA Shortener service
- **Port configuration**: Verify service port matches Traefik configuration
- **EntryPoint configuration**: Verify `web` and `websecure` boolean values are set correctly for your needs

Check Traefik dashboard (if enabled):
```bash
kubectl port-forward svc/traefik 9000:9000
# Access http://localhost:9000
```

## Dependencies

This chart depends on the following subcharts:

- **postgresql** (12.5.7) - PostgreSQL database
- **redis** (17.11.3) - Redis cache

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| cr0hn | <cr0hn@cr0hn.com> | <https://www.cr0hn.com> |

## Source Code

* <https://github.com/cr0hn/ja-shortener>

## License

This project is licensed under the Functionary Source License (FSL) - see the [LICENSE](https://github.com/cr0hn/ja-shortener/blob/main/LICENSE) file for details. 
