# LeaseGuard - Quick Start Guide

## What is LeaseGuard?

LeaseGuard is an AI-powered tool that helps tenants understand rental contracts before signing. Upload a PDF, and get:
- ✅ Risk analysis powered by AI + rules
- ✅ Plain English explanations of legal terms
- ✅ Downloadable risk report
- ✅ Recommendations for negotiation

---

## 🚀 30-Second Setup

### Option 1: Docker Compose (Recommended)
```bash
# On modern Docker Desktop (incl. Windows), use the built-in command:
docker compose -f docker/docker-compose.yml up
# Open http://localhost:3000
```

> Windows note: If you see "'docker-compose' is not recognized...", install Docker Desktop
> (https://www.docker.com/get-started) or use the integrated `docker compose` command shown above.

### Option 2: Manual Setup

**Terminal 1 - Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm run dev
```

**Terminal 3 - Database:**
```bash
# If using Docker:
docker run -d --name postgres \
  -e POSTGRES_USER=leaseguard \
  -e POSTGRES_PASSWORD=leaseguard_password \
  -p 5432:5432 \
  postgres:16
```

---

## 📁 Project Structure

```
backend/           → FastAPI application + services
frontend/          → Next.js React application  
database/          → Database migrations
docker/            → Docker files for containerization
docs/              → Full documentation
ml/                → ML models and rules
```

---

## 🔑 Key Files

### Backend Core
- `backend/main.py` - FastAPI application entry point
- `backend/app/services/` - Business logic (PDF, rules, ML, analysis)
- `backend/app/api/contracts.py` - API endpoints
- `backend/app/models/database.py` - SQLAlchemy models

### Frontend Core
- `frontend/src/pages/` - Next.js pages
- `frontend/src/hooks/useApi.ts` - API integration
- `frontend/src/types/` - TypeScript definitions

---

## 📚 Core Services

| Service | Purpose |
|---------|---------|
| **PDFExtractionService** | Extract text from PDF files |
| **ClauseSegmentation** | Split documents into clauses |
| **RuleBasedDetector** | Pattern-based risk detection |
| **RiskClassifier** | ML-based risk classification |
| **ExplanationEngine** | Convert legal language to plain English |
| **ContractAnalysisService** | Orchestrates full analysis |
| **ReportGenerator** | Creates PDF reports |

---

## 🎯 Workflow

1. User uploads PDF rental contract
2. Backend extracts text and segments into clauses
3. Rule-based detector identifies risky patterns
4. ML classifier scores risk confidence
5. Combined score generated (0-100)
6. Plain English explanations generated
7. PDF report compiled
8. Results returned to frontend

---

## 💻 API Quick Reference

```bash
# Upload contract
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@contract.pdf"

# Analyze (returns contract ID)
# Then poll: GET /api/v1/contract/{id}

# Download report
curl http://localhost:8000/api/v1/report/{id} > report.pdf
```

---

## 🔧 Configuration

### Backend `.env`
```env
DATABASE_URL=postgresql://leaseguard:password@localhost:5432/leaseguard
MINIO_ENDPOINT=localhost:9000
DEBUG=False
```

### Frontend `.env.local`
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🧪 Testing

**Backend Tests:**
```bash
cd backend
pytest tests/ -v
```

**Frontend Tests:**
```bash
cd frontend
npm test
```

---

## 📊 Risk Scoring

- **0-20**: Safe ✅
- **21-50**: Moderate Risk ⚠️
- **51-80**: High Risk 🔴
- **81-100**: Severe Risk 🚨

---

## 🚢 Deployment

### Frontend → Vercel
```bash
vercel --prod
```

### Backend → Render
- Connect GitHub repository
- Set environment variables
- Auto-deploy on push

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for details.

---

## 📖 Full Documentation

- [README.md](README.md) - Complete overview
- [SETUP.md](docs/SETUP.md) - Detailed setup instructions
- [API.md](docs/API.md) - API documentation
- [DEPLOYMENT.md](docs/DEPLOYMENT.md) - Production deployment
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check dependencies
pip install -r backend/requirements.txt --upgrade

# Check database connection
export DATABASE_URL="postgresql://..."
python init_db.py
```

### Frontend won't load
```bash
# Clear cache and reinstall
rm -rf frontend/node_modules
cd frontend
npm install
npm run dev
```

### Database connection error
```bash
# Verify database is running
docker ps | grep postgres

# Test connection
psql $DATABASE_URL
```

---

## ⚡ Performance Tips

- Run with Docker Compose for optimal performance
- Use SSD for database for faster analysis
- Keep uploads < 50MB (large PDFs may slow analysis)
- Batch processing ready for multiple contracts

---

## 🎓 Learning the Code

### Start Here:
1. Read the [ARCHITECTURE.md](ARCHITECTURE.md) for system design
2. Look at `backend/app/services/analysis_service.py` for main flow
3. Check `frontend/src/pages/analyze.tsx` for UI
4. Review `backend/app/api/contracts.py` for API

### Then Explore:
- Rule detection: `backend/app/services/rule_detector.py`
- ML classification: `backend/app/services/ml_classifier.py`
- PDF processing: `backend/app/services/pdf_service.py`
- Report generation: `backend/app/services/report_generator.py`

---

## 🚀 MVP Capabilities

✅ PDF upload and parsing
✅ Intelligent clause extraction
✅ Rule-based risk detection (10 categories)
✅ ML-powered risk classification
✅ Combined risk scoring
✅ Plain English explanations
✅ Professional PDF reports
✅ REST API
✅ React frontend
✅ Docker containerization
✅ Production-ready code

---

## 📝 Next Steps

1. **Try it out**: Upload a sample rental contract
2. **Review results**: Explore risk analysis and explanations
3. **Generate report**: Download the PDF report
4. **Customize**: Modify rules or add new risk categories
5. **Deploy**: Set up on Vercel/Render for production

---

## ✨ Features Worth Exploring

- **Rule Detection**: See how patterns are identified in rules.py
- **ML Scoring**: Zero-shot classification without fine-tuning
- **Explanation Engine**: Template-based plain English generation
- **Report Generation**: ReportLab PDF creation
- **Error Handling**: Comprehensive error handling throughout
- **Type Safety**: Full TypeScript/Pydantic validation

---

## 📞 Support

- Check documentation first
- Review code comments
- Look at test files for examples
- Check GitHub issues

---

## 📄 License

MIT - Open for commercial and personal use

---

**Built for**: Hackathon MVP → Startup Product
**Status**: Production-Ready
**Version**: 1.0.0

---

**Happy Analyzing!** 🎉

For questions or contributions, check the main README.md
