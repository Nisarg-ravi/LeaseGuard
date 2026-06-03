# API Documentation

## Base URL
- Development: `http://localhost:8000`
- Production: `https://api.leaseguard.com` (to be configured)

## Authentication
Currently MVP uses no authentication. JWT will be added for production.

---

## Endpoints

### Health & Info

#### Get Health Status
```
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "LeaseGuard",
  "version": "1.0.0"
}
```

#### Get API Info
```
GET /
```

**Response:**
```json
{
  "name": "LeaseGuard",
  "description": "AI-powered rental contract risk analyzer",
  "docs": "/docs"
}
```

---

## Contract Management

### Upload Contract

Upload a PDF rental contract for analysis.

```
POST /api/v1/upload
Content-Type: multipart/form-data
```

**Parameters:**
- `file` (File, required): PDF file to upload. Max size: 50MB

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "filename": "contracts/rental_agreement_2024.pdf",
  "original_filename": "rental_agreement.pdf",
  "upload_date": "2024-06-03T12:34:56",
  "risk_score": null,
  "total_pages": 5,
  "clauses": []
}
```

**Error Responses:**
- `400 Bad Request`: File is not PDF or too large
- `500 Internal Server Error`: Upload failed

---

### Analyze Contract

Trigger analysis of an uploaded contract.

```
POST /api/v1/analyze
Content-Type: application/json
```

**Request Body:**
```json
{
  "contract_id": 1
}
```

**Response:** `200 OK`
```json
{
  "status": "analyzing",
  "contract_id": 1,
  "message": "Analysis started. Check back shortly for results."
}
```

**Notes:**
- Analysis runs asynchronously in background
- Poll `/api/v1/contract/{id}` to check status
- Once `risk_score` is populated, analysis is complete

**Error Responses:**
- `404 Not Found`: Contract not found
- `400 Bad Request`: Contract already analyzed
- `500 Internal Server Error`: Analysis failed

---

### Get Contract Details

Get contract information including analysis results.

```
GET /api/v1/contract/{contract_id}
```

**Path Parameters:**
- `contract_id` (integer, required): Contract ID

**Response:** `200 OK`
```json
{
  "id": 1,
  "user_id": 1,
  "filename": "contracts/rental_agreement_2024.pdf",
  "original_filename": "rental_agreement.pdf",
  "upload_date": "2024-06-03T12:34:56",
  "risk_score": 62.5,
  "total_pages": 5,
  "analysis": {
    "id": 1,
    "total_clauses": 12,
    "high_risk_count": 2,
    "medium_risk_count": 3,
    "low_risk_count": 7,
    "overall_risk_score": 62.5,
    "rule_based_score": 68.0,
    "ml_score": 52.0,
    "summary": "Overall Risk Assessment: HIGH RISK\nRisk Score: 62.5/100\n...",
    "created_at": "2024-06-03T12:35:00"
  },
  "clauses": [
    {
      "id": 1,
      "clause_number": 1,
      "contract_id": 1,
      "original_text": "The tenant shall pay rent of $1,500 per month...",
      "risk_level": "low",
      "risk_score": 15.0,
      "explanation": "{...json explanation...}",
      "ml_confidence": 0.92,
      "created_at": "2024-06-03T12:35:00"
    },
    {
      "id": 2,
      "clause_number": 2,
      "contract_id": 1,
      "original_text": "Security deposit shall be 4 months of rent...",
      "risk_level": "high",
      "risk_score": 85.0,
      "explanation": "{...json explanation...}",
      "ml_confidence": 0.88,
      "created_at": "2024-06-03T12:35:00"
    }
  ]
}
```

**Error Responses:**
- `404 Not Found`: Contract not found
- `500 Internal Server Error`: Retrieval failed

---

### Get Analysis Results

Get detailed analysis results for a contract.

```
GET /api/v1/analysis/{contract_id}
```

**Path Parameters:**
- `contract_id` (integer, required): Contract ID

**Response:** `200 OK`
```json
{
  "id": 1,
  "total_clauses": 12,
  "high_risk_count": 2,
  "medium_risk_count": 3,
  "low_risk_count": 7,
  "overall_risk_score": 62.5,
  "rule_based_score": 68.0,
  "ml_score": 52.0,
  "summary": "Overall Risk Assessment: HIGH RISK\nRisk Score: 62.5/100\n\nClause Breakdown:\n- High Risk: 2 clause(s)\n- Medium Risk: 3 clause(s)\n- Low Risk: 7 clause(s)\n\nRecommendation: Carefully review the flagged clauses and consider negotiating.",
  "created_at": "2024-06-03T12:35:00",
  "updated_at": "2024-06-03T12:35:00"
}
```

**Error Responses:**
- `404 Not Found`: Contract or analysis not found
- `500 Internal Server Error`: Retrieval failed

---

## Reports

### Download PDF Report

Generate and download a PDF report with complete analysis.

```
GET /api/v1/report/{contract_id}
```

**Path Parameters:**
- `contract_id` (integer, required): Contract ID

**Response:** `200 OK`
- Content-Type: `application/pdf`
- Returns PDF file as attachment

**Report Contents:**
- Contract metadata
- Risk assessment summary
- Clause-by-clause analysis
- Recommendations
- Plain English explanations

**Error Responses:**
- `404 Not Found`: Contract or analysis not found
- `500 Internal Server Error`: Report generation failed

---

## Data Models

### Contract
```json
{
  "id": 1,
  "user_id": 1,
  "filename": "string",
  "original_filename": "string",
  "upload_date": "2024-06-03T12:34:56",
  "risk_score": 62.5,
  "total_pages": 5,
  "clauses": [],
  "analysis": {}
}
```

### ContractAnalysis
```json
{
  "id": 1,
  "total_clauses": 12,
  "high_risk_count": 2,
  "medium_risk_count": 3,
  "low_risk_count": 7,
  "overall_risk_score": 62.5,
  "rule_based_score": 68.0,
  "ml_score": 52.0,
  "summary": "string",
  "created_at": "2024-06-03T12:35:00",
  "updated_at": "2024-06-03T12:35:00"
}
```

### Clause
```json
{
  "id": 1,
  "clause_number": 1,
  "contract_id": 1,
  "original_text": "string",
  "risk_level": "low|medium|high",
  "risk_score": 15.0,
  "explanation": "json_string",
  "ml_confidence": 0.92,
  "created_at": "2024-06-03T12:35:00"
}
```

### RiskLevel Enum
- `"low"` - Score 0-20
- `"medium"` - Score 21-50
- `"high"` - Score 51-80
- `"severe"` - Score 81-100 (implied from contract level)

---

## Error Handling

All endpoints use standard HTTP status codes:

- `200 OK`: Success
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

Error responses include:
```json
{
  "detail": "Error message describing what went wrong"
}
```

---

## Rate Limiting

Currently no rate limiting. Will be added for production.

---

## CORS

CORS is enabled for:
- `http://localhost:3000` (development)
- `http://localhost:8000` (development)
- Production domains (to be configured)

---

## Workflow Example

### 1. Upload Contract
```bash
curl -X POST http://localhost:8000/api/v1/upload \
  -F "file=@rental_agreement.pdf"
```

Response:
```json
{
  "id": 1,
  "filename": "contracts/rental_agreement.pdf",
  "upload_date": "2024-06-03T12:34:56"
}
```

### 2. Analyze Contract
```bash
curl -X POST http://localhost:8000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"contract_id": 1}'
```

Response:
```json
{
  "status": "analyzing",
  "contract_id": 1
}
```

### 3. Poll for Results
```bash
curl http://localhost:8000/api/v1/contract/1
```

Once `risk_score` is not null, analysis is complete.

### 4. Download Report
```bash
curl http://localhost:8000/api/v1/report/1 \
  --output report.pdf
```

---

## Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI documentation where you can:
- View all endpoints
- Read parameter descriptions
- Try endpoints with sample data
- View response schemas

---

**Last Updated**: June 2024
