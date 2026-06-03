"""
Contract analysis API endpoints.
"""
import logging
import os
import tempfile
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from config import settings
from app.database import get_db
from app.models import Contract, ContractAnalysis
from app.schemas.contract import ContractResponse, ContractAnalysisResponse, AnalysisRequest
from app.services.pdf_service import PDFExtractionService
from app.services.storage_service import StorageService
from app.services.analysis_service import ContractAnalysisService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["contracts"])

# Services
pdf_service = PDFExtractionService()
storage_service = StorageService()


@router.post("/upload", response_model=ContractResponse)
async def upload_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a rental contract PDF.
    
    Args:
        file: PDF file to upload
        db: Database session
        
    Returns:
        Contract metadata
    """
    try:
        # Validate file type
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Validate file size
        content = await file.read()
        if len(content) > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
            )
        
        # Validate PDF
        temp_path = None
        try:
            # Save to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(content)
                temp_path = tmp.name
            
            # Validate PDF
            if not pdf_service.validate_pdf(temp_path):
                raise HTTPException(status_code=400, detail="Invalid or corrupted PDF file")
            
            # Generate unique filename
            object_name = f"contracts/{file.filename}"
            
            # Upload to MinIO
            minio_path = storage_service.upload_file(
                temp_path,
                settings.MINIO_BUCKET_CONTRACTS,
                object_name
            )
            
            # Create contract record
            contract = Contract(
                user_id=1,  # TODO: Get from authenticated user
                filename=object_name,
                original_filename=file.filename,
                minio_path=minio_path
            )
            db.add(contract)
            db.commit()
            db.refresh(contract)
            
            logger.info(f"Contract uploaded: {contract.id}")
            
            return contract
            
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading contract: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze")
async def analyze_contract(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Trigger analysis of an uploaded contract.
    
    Args:
        request: Contract ID to analyze
        background_tasks: Background task scheduler
        db: Database session
        
    Returns:
        Analysis status
    """
    try:
        # Get contract
        contract = db.query(Contract).filter(Contract.id == request.contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        # Check if already analyzed
        existing_analysis = db.query(ContractAnalysis).filter(
            ContractAnalysis.contract_id == request.contract_id
        ).first()
        if existing_analysis:
            raise HTTPException(status_code=400, detail="Contract already analyzed")
        
        # Download from MinIO
        temp_path = None
        try:
            temp_path = tempfile.mktemp(suffix=".pdf")
            storage_service.download_file(
                settings.MINIO_BUCKET_CONTRACTS,
                contract.filename,
                temp_path
            )
            
            # Perform analysis in background
            analysis_service = ContractAnalysisService(db)
            background_tasks.add_task(
                analysis_service.analyze_contract,
                request.contract_id,
                temp_path
            )
            
            return {
                "status": "analyzing",
                "contract_id": request.contract_id,
                "message": "Analysis started. Check back shortly for results."
            }
            
        except Exception as e:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
            raise HTTPException(status_code=500, detail=str(e))
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/contract/{contract_id}", response_model=ContractResponse)
async def get_contract(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """
    Get contract details including analysis results.
    
    Args:
        contract_id: Contract ID
        db: Database session
        
    Returns:
        Contract with analysis
    """
    try:
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        return contract
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving contract: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/{contract_id}", response_model=ContractAnalysisResponse)
async def get_analysis(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """
    Get contract analysis results.
    
    Args:
        contract_id: Contract ID
        db: Database session
        
    Returns:
        Analysis results
    """
    try:
        analysis = db.query(ContractAnalysis).filter(
            ContractAnalysis.contract_id == contract_id
        ).first()
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
