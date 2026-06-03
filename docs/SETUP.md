# Setup Instructions

## Local Development Setup

### Prerequisites
- Python 3.12 or higher
- Node.js 18 or higher
- PostgreSQL 16
- Docker & Docker Compose (optional but recommended)
- Git

---

## Backend Setup

### 1. Create Python Environment
```bash
cd backend
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
DATABASE_URL=postgresql://leaseguard:leaseguard_password@localhost:5432/leaseguard
MINIO_ENDPOINT=localhost:9000
DEBUG=True
```

### 4. Database Setup

#### Option A: Docker (Recommended)
```bash
docker run -d \
  --name leaseguard_postgres \
  -e POSTGRES_USER=leaseguard \
  -e POSTGRES_PASSWORD=leaseguard_password \
  -e POSTGRES_DB=leaseguard \
  -p 5432:5432 \
  postgres:16
```

#### Option B: Local PostgreSQL
```sql
-- Connect as superuser
CREATE USER leaseguard WITH PASSWORD 'leaseguard_password';
CREATE DATABASE leaseguard OWNER leaseguard;
GRANT ALL PRIVILEGES ON DATABASE leaseguard TO leaseguard;
```

### 5. Initialize Database
```bash
python init_db.py
```

### 6. Setup MinIO
```bash
docker run -d \
  --name leaseguard_minio \
  -e MINIO_ROOT_USER=minioadmin \
  -e MINIO_ROOT_PASSWORD=minioadmin \
  -p 9000:9000 \
  -p 9001:9001 \
  minio/minio:latest server /data --console-address ":9001"
```

Access MinIO console at http://localhost:9001

### 7. Run Backend
```bash
uvicorn main:app --reload
```

Backend will be available at: http://localhost:8000
API docs at: http://localhost:8000/docs

---

## Frontend Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Environment Configuration
Create `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Development Server
```bash
npm run dev
```

Frontend will be available at: http://localhost:3000

---

## Using Docker Compose (All-in-One)

### Start Everything
```bash
docker-compose -f docker/docker-compose.yml up -d
```

This starts:
- PostgreSQL database
- MinIO storage
- FastAPI backend
- Next.js frontend

### Check Status
```bash
docker-compose -f docker/docker-compose.yml ps
```

### View Logs
```bash
# All services
docker-compose -f docker/docker-compose.yml logs -f

# Specific service
docker-compose -f docker/docker-compose.yml logs -f backend
docker-compose -f docker/docker-compose.yml logs -f frontend
```

### Stop Services
```bash
docker-compose -f docker/docker-compose.yml down
```

### Remove Everything (including data)
```bash
docker-compose -f docker/docker-compose.yml down -v
```

---

## Verify Installation

### 1. Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "LeaseGuard",
  "version": "1.0.0"
}
```

### 2. Frontend
Open http://localhost:3000 in browser

### 3. API Documentation
Visit http://localhost:8000/docs for interactive API documentation

---

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=app
```

### Frontend Tests
```bash
cd frontend
npm test
npm test -- --coverage
```

---

## Troubleshooting

### PostgreSQL Connection Error
```
Ensure PostgreSQL is running and connection string is correct:
postgresql://leaseguard:leaseguard_password@localhost:5432/leaseguard
```

### MinIO Connection Error
```
Check MinIO is running on localhost:9000
Visit http://localhost:9001 to verify
```

### Port Already in Use
```bash
# Find process using port
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
lsof -i :5432  # Database

# Kill process
kill -9 <PID>
```

### Python Package Issues
```bash
# Clear cache and reinstall
pip cache purge
pip install --no-cache-dir -r requirements.txt
```

### Node Module Issues
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## Development Workflow

### Running Locally (Non-Docker)

**Terminal 1 - Backend**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Terminal 2 - Frontend**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Database (if using Docker)**
```bash
docker run -d \
  --name postgres \
  -e POSTGRES_USER=leaseguard \
  -e POSTGRES_PASSWORD=leaseguard_password \
  -e POSTGRES_DB=leaseguard \
  -p 5432:5432 \
  postgres:16
```

### Code Quality

**Backend**
```bash
# Format code
black backend/

# Lint code
flake8 backend/

# Type checking
mypy backend/
```

**Frontend**
```bash
# Format code
npx prettier --write frontend/src

# Lint code
npm run lint

# Type checking
npm run type-check
```

---

## Environment Variables Reference

### Backend (.env)
```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/db

# MinIO/S3
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_CONTRACTS=contracts
MINIO_BUCKET_REPORTS=reports

# Security
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=False
PROJECT_NAME=LeaseGuard
API_V1_STR=/api/v1

# ML
ML_MODEL_NAME=distilbert-base-uncased
CONFIDENCE_THRESHOLD=0.7

# File Upload
MAX_UPLOAD_SIZE=52428800
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Next Steps

1. Review the [API Documentation](API.md)
2. Explore the [Project Architecture](../README.md)
3. Check the [Deployment Guide](DEPLOYMENT.md)
4. Read through the code in `backend/app/` and `frontend/src/`

---

## Getting Help

- Check error logs first
- Review documentation
- Check existing GitHub issues
- Create a new issue with details

---

**Last Updated**: June 2024
