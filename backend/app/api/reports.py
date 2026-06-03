"""
Report generation API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Contract, ContractAnalysis, Clause
from app.services.report_generator import ReportGenerator

router = APIRouter(prefix="/api/v1", tags=["reports"])


@router.get("/report/{contract_id}")
async def get_report(
    contract_id: int,
    db: Session = Depends(get_db)
):
    """
    Generate and download PDF report for a contract.
    
    Args:
        contract_id: Contract ID
        db: Database session
        
    Returns:
        PDF file as stream
    """
    try:
        # Get contract
        contract = db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")
        
        # Get analysis
        analysis = db.query(ContractAnalysis).filter(
            ContractAnalysis.contract_id == contract_id
        ).first()
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found. Please run analysis first.")
        
        # Get clauses
        clauses = db.query(Clause).filter(Clause.contract_id == contract_id).all()
        
        # Generate report
        pdf_buffer = ReportGenerator.generate_report(contract, analysis, clauses)
        
        return StreamingResponse(
            iter([pdf_buffer.getvalue()]),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=LeaseGuard_Analysis_{contract_id}.pdf"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
