"""
Main contract analysis orchestration service.
"""
import logging
import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime

from app.models import Contract, Clause, ContractAnalysis, RiskLevel
from app.schemas.contract import ContractResponse
from app.services.pdf_service import PDFExtractionService
from app.services.clause_service import ClauseSegmentation
from app.services.rule_detector import RuleBasedDetector
from app.services.ml_classifier import get_risk_classifier
from app.services.explanation_engine import ExplanationEngine

logger = logging.getLogger(__name__)


class ContractAnalysisService:
    """Orchestrates the complete contract analysis workflow."""
    
    def __init__(self, db: Session):
        """
        Initialize the analysis service.
        
        Args:
            db: Database session
        """
        self.db = db
        self.pdf_service = PDFExtractionService()
        self.classifier = get_risk_classifier()
    
    def analyze_contract(self, contract_id: int, pdf_path: str) -> ContractResponse:
        """
        Perform complete analysis of a rental contract.
        
        Args:
            contract_id: Contract ID in database
            pdf_path: Local path to PDF file
            
        Returns:
            Analysis results
        """
        try:
            # Get contract from database
            contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
            if not contract:
                raise ValueError(f"Contract {contract_id} not found")
            
            # Step 1: Extract PDF text
            logger.info(f"Extracting text from PDF: {pdf_path}")
            full_text, page_count = self.pdf_service.extract_text(pdf_path)
            contract.total_pages = page_count
            
            # Step 2: Segment into clauses
            logger.info("Segmenting contract into clauses")
            clause_texts = ClauseSegmentation.segment_clauses(full_text)
            
            if not clause_texts:
                raise ValueError("No clauses could be extracted from the contract")
            
            # Step 3: Analyze each clause
            logger.info(f"Analyzing {len(clause_texts)} clauses")
            high_risk_count = 0
            medium_risk_count = 0
            low_risk_count = 0
            total_rule_score = 0.0
            total_ml_score = 0.0
            
            for clause_num, clause_text in enumerate(clause_texts, 1):
                # Detect rule violations
                violations = RuleBasedDetector.detect_violations(clause_text)
                rule_score = RuleBasedDetector.calculate_score(violations)
                
                # ML classification
                ml_risk_level, ml_confidence = self.classifier.classify_risk(clause_text)
                ml_score = self._risk_level_to_score(ml_risk_level, ml_confidence)
                
                # Combine scores (70% rule-based, 30% ML)
                combined_score = (rule_score * 0.7) + (ml_score * 0.3)
                
                # Determine final risk level
                if combined_score >= 50:
                    risk_level = RiskLevel.HIGH
                    high_risk_count += 1
                elif combined_score >= 25:
                    risk_level = RiskLevel.MEDIUM
                    medium_risk_count += 1
                else:
                    risk_level = RiskLevel.LOW
                    low_risk_count += 1
                
                # Generate explanation
                clause_type = ClauseSegmentation.extract_clause_type(clause_text)
                explanation_dict = ExplanationEngine.generate_explanation(clause_text, clause_type)
                
                # Store clause in database
                clause_violations = [
                    {
                        "rule": v.rule_name,
                        "reason": v.reason,
                        "recommendation": v.recommendation
                    }
                    for v in violations
                ]
                
                clause_db = Clause(
                    contract_id=contract_id,
                    clause_number=clause_num,
                    original_text=clause_text,
                    risk_level=risk_level,
                    risk_score=combined_score,
                    explanation=json.dumps(explanation_dict),
                    rule_based_risks=json.dumps(clause_violations),
                    ml_confidence=ml_confidence
                )
                self.db.add(clause_db)
                
                total_rule_score += rule_score
                total_ml_score += ml_score
            
            # Step 4: Calculate overall analysis
            avg_rule_score = (total_rule_score / len(clause_texts)) if clause_texts else 0
            avg_ml_score = (total_ml_score / len(clause_texts)) if clause_texts else 0
            
            # Combined overall score
            overall_score = (avg_rule_score * 0.7) + (avg_ml_score * 0.3)
            
            # Update contract with overall risk score
            contract.risk_score = overall_score
            
            # Generate summary
            summary = self._generate_summary(
                overall_score,
                high_risk_count,
                medium_risk_count,
                low_risk_count,
                len(clause_texts)
            )
            
            # Create analysis record
            analysis = ContractAnalysis(
                contract_id=contract_id,
                total_clauses=len(clause_texts),
                high_risk_count=high_risk_count,
                medium_risk_count=medium_risk_count,
                low_risk_count=low_risk_count,
                overall_risk_score=overall_score,
                rule_based_score=avg_rule_score,
                ml_score=avg_ml_score,
                summary=summary
            )
            self.db.add(analysis)
            
            # Commit all changes
            self.db.commit()
            
            logger.info(f"Analysis complete. Risk score: {overall_score}")
            
            # Refresh to get relationships
            self.db.refresh(contract)
            
            return contract
            
        except Exception as e:
            logger.error(f"Error during contract analysis: {str(e)}")
            self.db.rollback()
            raise
    
    @staticmethod
    def _risk_level_to_score(risk_level: str, confidence: float) -> float:
        """
        Convert risk level and confidence to numerical score.
        
        Args:
            risk_level: Risk level (low, medium, high)
            confidence: Confidence score (0-1)
            
        Returns:
            Numerical score (0-100)
        """
        level_scores = {
            "high": 75,
            "medium": 50,
            "low": 25
        }
        
        base_score = level_scores.get(risk_level, 25)
        # Adjust by confidence: higher confidence = closer to base score
        adjusted_score = base_score * confidence + 50 * (1 - confidence)
        
        return adjusted_score
    
    @staticmethod
    def _generate_summary(
        risk_score: float,
        high_count: int,
        medium_count: int,
        low_count: int,
        total_clauses: int
    ) -> str:
        """
        Generate a summary of the contract analysis.
        
        Args:
            risk_score: Overall risk score
            high_count: Number of high-risk clauses
            medium_count: Number of medium-risk clauses
            low_count: Number of low-risk clauses
            total_clauses: Total number of clauses
            
        Returns:
            Summary text
        """
        if risk_score >= 80:
            risk_category = "SEVERE RISK"
            recommendation = "Do NOT sign this contract without professional legal review."
        elif risk_score >= 51:
            risk_category = "HIGH RISK"
            recommendation = "Carefully review the flagged clauses and consider negotiating."
        elif risk_score >= 21:
            risk_category = "MODERATE RISK"
            recommendation = "Some clauses may need clarification or negotiation."
        else:
            risk_category = "LOW RISK"
            recommendation = "This contract appears to be generally fair."
        
        summary = (
            f"Overall Risk Assessment: {risk_category}\n"
            f"Risk Score: {risk_score:.1f}/100\n\n"
            f"Clause Breakdown:\n"
            f"- High Risk: {high_count} clause(s)\n"
            f"- Medium Risk: {medium_count} clause(s)\n"
            f"- Low Risk: {low_count} clause(s)\n\n"
            f"Recommendation: {recommendation}"
        )
        
        return summary
    
    def get_contract_analysis(self, contract_id: int) -> Dict[str, Any]:
        """
        Retrieve analysis for a contract.
        
        Args:
            contract_id: Contract ID
            
        Returns:
            Analysis data
        """
        contract = self.db.query(Contract).filter(Contract.id == contract_id).first()
        if not contract:
            raise ValueError(f"Contract {contract_id} not found")
        
        analysis = self.db.query(ContractAnalysis).filter(
            ContractAnalysis.contract_id == contract_id
        ).first()
        
        if not analysis:
            raise ValueError(f"Analysis not found for contract {contract_id}")
        
        clauses = self.db.query(Clause).filter(Clause.contract_id == contract_id).all()
        
        return {
            "contract": contract,
            "analysis": analysis,
            "clauses": clauses
        }
