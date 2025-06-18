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
| `ingress.hosts` | List of hosts for the ingress | `[{"host": "chart-example.local", "paths": [{"path": "/", "pathType": "ImplementationSpecific"}]}]` |
| `ingress.tls` | TLS configuration for the ingress | `[]` |

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
| `django.backup.s3.accessKey` | S3 access key | `""` |
| `django.backup.s3.secretKey` | S3 secret key | `""` |
| `django.backup.s3.bucketName` | S3 bucket name | `""` |
| `django.backup.s3.region` | S3 region | `""` |
| `django.backup.s3.endpointUrl` | S3 endpoint URL (for S3-compatible services) | `""` |
| `django.backup.local.location` | Local backup location | `"/data/backups"` |

### PostgreSQL Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `postgresql.enabled` | Enable PostgreSQL | `true` |
| `postgresql.auth.database` | PostgreSQL database name | `ja_shortener` |
| `postgresql.auth.username` | PostgreSQL username | `ja_shortener` |
| `postgresql.auth.password` | PostgreSQL password | `ja_shortener_password` |
| `postgresql.primary.persistence.enabled` | Enable PostgreSQL persistence | `true` |
| `postgresql.primary.persistence.size` | PostgreSQL storage size | `8Gi` |
| `postgresql.service.ports.postgresql` | PostgreSQL service port | `5432` |

### Redis Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `redis.enabled` | Enable Redis | `true` |
| `redis.auth.password` | Redis password | `redis_password` |
| `redis.master.persistence.enabled` | Enable Redis persistence | `true` |
| `redis.master.persistence.size` | Redis storage size | `8Gi` |
| `redis.service.ports.redis` | Redis service port | `6379` |

### Persistence Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `persistence.enabled` | Enable persistence | `true` |
| `persistence.storageClass` | Storage class name | `""` |
| `persistence.size` | Persistence volume size | `8Gi` |
| `persistence.accessMode` | Persistence access mode | `ReadWriteOnce` |
| `persistence.annotations` | Persistence annotations | `{}` |

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

## Upgrading

### To 0.2.0

Check the [CHANGELOG](https://github.com/cr0hn/ja-shortener/blob/main/CHANGELOG.md) for breaking changes.

```bash
helm upgrade my-ja-shortener ja-shortener/ja-shortener
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

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://github.com/cr0hn/ja-shortener/blob/main/LICENSE) file for details. 