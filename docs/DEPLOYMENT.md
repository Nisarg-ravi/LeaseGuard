# Deployment Guide

## Prerequisites

- GitHub repository set up
- Vercel account (for frontend)
- Render account (for backend)
- PostgreSQL database provider
- MinIO S3 compatible storage

---

## Frontend Deployment (Vercel)

### 1. Prepare Repository
```bash
# Add deployment files
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### 2. Deploy to Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### 3. Configure Environment
In Vercel dashboard:
1. Go to Project Settings
2. Go to Environment Variables
3. Add:
   ```
   NEXT_PUBLIC_API_URL=https://api.leaseguard.com
   ```

### 4. Custom Domain
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records

---

## Backend Deployment (Render)

### 1. Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2. Create Render Web Service
1. Go to render.com
2. Click "New +" → Web Service
3. Select repository
4. Configure:
   - **Name**: leaseguard-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. Add Environment Variables
In Render dashboard:
```env
DATABASE_URL=postgresql://user:password@db.render.com/leaseguard
MINIO_ENDPOINT=s3.amazonaws.com
MINIO_ACCESS_KEY=your_access_key
MINIO_SECRET_KEY=your_secret_key
MINIO_BUCKET_CONTRACTS=leaseguard-contracts
MINIO_BUCKET_REPORTS=leaseguard-reports
SECRET_KEY=your_secret_key
DEBUG=False
```

### 4. Deploy
Click "Create Web Service" - deployment starts automatically

---

## Database Setup (PostgreSQL)

### Option 1: Render PostgreSQL
1. Go to Render dashboard
2. New → PostgreSQL
3. Configure:
   - **Database**: leaseguard
   - **User**: leaseguard
   - **Region**: Choose closest region

### Option 2: AWS RDS
1. Go to AWS Console
2. RDS → Create Database
3. Engine: PostgreSQL 16
4. Configure backups and storage

### Option 3: Google Cloud SQL
1. Go to Google Cloud Console
2. SQL → Create Instance
3. Engine: PostgreSQL
4. Configure access and backups

### Initialization
Once database is set up:
```bash
# Get database URL
export DATABASE_URL="postgresql://user:password@host:5432/leaseguard"

# Run migrations
python init_db.py
```

---

## Object Storage Setup (MinIO/S3)

### Option 1: AWS S3
```bash
# Create S3 bucket
aws s3 mb s3://leaseguard-contracts
aws s3 mb s3://leaseguard-reports

# Get access keys
# Use IAM → Users → Security Credentials
```

Environment variables:
```env
MINIO_ENDPOINT=s3.amazonaws.com
MINIO_ACCESS_KEY=your_access_key
MINIO_SECRET_KEY=your_secret_key
MINIO_BUCKET_CONTRACTS=leaseguard-contracts
MINIO_BUCKET_REPORTS=leaseguard-reports
```

### Option 2: DigitalOcean Spaces
```bash
# Create Space in DigitalOcean console
# Available at: https://region.digitaloceanspaces.com/

# Get keys from API section
```

Environment variables:
```env
MINIO_ENDPOINT=region.digitaloceanspaces.com
MINIO_ACCESS_KEY=your_access_key
MINIO_SECRET_KEY=your_secret_key
```

### Option 3: MinIO on DigitalOcean App Platform
```yaml
name: leaseguard-storage
services:
- name: minio
  source:
    type: image
    registry: docker
    registry_credentials:
      username: minio
    image: minio/minio:latest
  envs:
  - key: MINIO_ROOT_USER
    value: minioadmin
  - key: MINIO_ROOT_PASSWORD
    value: your_secure_password
  http_port: 9000
```

---

## Monitoring & Logging

### Backend Monitoring (Render)
- Logs visible in Render dashboard
- Set up error alerts in project settings

### Database Monitoring
- Enable automated backups
- Set up performance monitoring
- Configure alerts for high query times

### Error Tracking (Recommended)
```bash
# Install Sentry for error tracking
pip install sentry-sdk

# Configure in main.py
import sentry_sdk
sentry_sdk.init(
    dsn="your_sentry_dsn",
    traces_sample_rate=0.1
)
```

---

## Health Checks

### Frontend
Vercel automatically monitors deployments.

### Backend
Add to Render health check settings:
```
Path: /health
Timeout: 10s
Period: 5m
```

---

## CI/CD Pipeline

### GitHub Actions (Optional)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          curl -X POST https://api.render.com/deploy \
            -H "Authorization: Bearer ${{ secrets.RENDER_API_KEY }}"
      
      - name: Deploy Frontend
        run: |
          vercel deploy --prod --token ${{ secrets.VERCEL_TOKEN }}
```

---

## SSL/TLS Certificates

Both Vercel and Render provide automatic SSL certificates.

### Custom Domain with Vercel
1. Add domain in project settings
2. Update DNS records
3. Certificate auto-provisioned

### Custom Domain with Render
1. Add domain in web service settings
2. Update DNS records
3. Certificate auto-provisioned

---

## Performance Optimization

### Frontend (Vercel)
- Automatic image optimization
- Edge caching
- ISR (Incremental Static Regeneration)

### Backend (Render)
- Connection pooling configured
- ML model cached
- Enable gzip compression

### Database
- Add read replicas for scaling
- Enable query caching
- Optimize indexes

---

## Backup Strategy

### Database
- Daily automated backups (configure in provider)
- Retention: 30 days
- Test restore process monthly

### File Storage
- Enable versioning on S3/Spaces
- Lifecycle policies for old reports
- Cross-region replication (optional)

---

## Security Checklist

- [ ] Environment variables configured securely
- [ ] Database password strong and unique
- [ ] API keys stored in secrets manager
- [ ] HTTPS enforced on all endpoints
- [ ] CORS origins restricted to known domains
- [ ] Database backups encrypted
- [ ] File uploads scanned for malware
- [ ] Rate limiting configured
- [ ] SQL injection prevention verified
- [ ] Authentication ready for next phase

---

## Troubleshooting Deployment

### Backend won't start
```bash
# Check logs
render logs

# Verify environment variables
echo $DATABASE_URL

# Test locally first
python init_db.py
uvicorn main:app
```

### Database connection failed
```bash
# Test connection
psql $DATABASE_URL

# Verify credentials
psql -h host -U user -d leaseguard
```

### MinIO/S3 connection failed
```bash
# Test S3 connection
aws s3 ls --endpoint-url $MINIO_ENDPOINT

# Verify credentials
echo "Key: $MINIO_ACCESS_KEY"
```

### Frontend can't reach API
```bash
# Check API URL in environment
echo $NEXT_PUBLIC_API_URL

# Test API endpoint
curl https://api.leaseguard.com/health
```

---

## Scaling Considerations

### Current Capacity
MVP handles:
- ~100 contracts/day
- ~1000 concurrent users
- ~10GB storage

### Scaling Strategies

**Horizontal Scaling:**
- Multiple backend instances behind load balancer
- Database read replicas
- CDN for static assets

**Vertical Scaling:**
- Larger database instance
- More memory/CPU for ML inference
- Dedicated ML inference server

**Performance:**
- Cache ML model in memory
- Queue long-running analyses
- Compress PDF reports

---

## Disaster Recovery

### Database Recovery
1. Restore from latest backup
2. Verify data integrity
3. Switch to backup database if needed

### Application Recovery
1. Redeploy from GitHub
2. Verify health checks
3. Monitor error logs

### Storage Recovery
1. Use versioning to recover deleted files
2. Restore from backup bucket if available

---

## Post-Deployment

1. Monitor logs for errors
2. Check performance metrics
3. Test all workflows
4. Verify file uploads work
5. Test report generation
6. Monitor database queries
7. Set up alerts
8. Document any issues

---

## Next Steps

- Set up GitHub branch protection
- Configure automated testing
- Set up monitoring dashboards
- Schedule regular backups
- Plan for scaling phase
- Prepare marketing launch

---

**Last Updated**: June 2024
