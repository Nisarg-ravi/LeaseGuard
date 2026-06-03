"""
Pydantic schemas for contract-related requests and responses.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ClauseBase(BaseModel):
    """Base clause schema."""
    original_text: str
    risk_level: str
    risk_score: float
    explanation: Optional[str] = None
    ml_confidence: Optional[float] = None


class ClauseResponse(ClauseBase):
    """Clause response schema."""
    id: int
    clause_number: int
    contract_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ContractAnalysisResponse(BaseModel):
    """Contract analysis response schema."""
    id: int
    total_clauses: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    overall_risk_score: float
    rule_based_score: float
    ml_score: float
    summary: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ContractBase(BaseModel):
    """Base contract schema."""
    filename: str


class ContractCreate(BaseModel):
    """Contract creation schema."""
    filename: str
    original_filename: str


class ContractResponse(ContractBase):
    """Contract response schema."""
    id: int
    user_id: int
    upload_date: datetime
    risk_score: Optional[float]
    total_pages: Optional[int]
    analysis: Optional[ContractAnalysisResponse]
    clauses: List[ClauseResponse] = []
    
    class Config:
        from_attributes = True


class UploadRequest(BaseModel):
    """Upload request schema."""
    filename: str


class AnalysisRequest(BaseModel):
    """Analysis request schema."""
    contract_id: int


class RiskExplanation(BaseModel):
    """Risk explanation schema."""
    risk_level: str
    reason: str
    severity_score: float
    recommendation: str
