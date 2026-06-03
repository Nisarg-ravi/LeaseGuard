"""
Plain English explanation engine for rental contract clauses.
"""
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class ExplanationEngine:
    """Generates plain English explanations for contract clauses."""
    
    # Clause type explanations and concerns
    EXPLANATIONS = {
        "payment": {
            "template": "This clause describes how you will pay rent.",
            "concerns": "Make sure you understand the exact amount, due date, and accepted payment methods.",
            "questions": [
                "What is the exact rent amount?",
                "When is it due each month?",
                "What payment methods are accepted?",
                "Are there late fees and how much?"
            ]
        },
        
        "deposit": {
            "template": "This clause covers the security deposit (money held for potential damages).",
            "concerns": "Deposits should typically not exceed 2-3 months of rent. Make sure it's refundable.",
            "questions": [
                "How much is the deposit?",
                "Is it refundable or non-refundable?",
                "How long after move-out will you get it back?",
                "What deductions can the landlord make?"
            ]
        },
        
        "term": {
            "template": "This clause defines the lease duration and when it starts/ends.",
            "concerns": "Understand your exact commitment period and when the lease ends.",
            "questions": [
                "How long is the lease?",
                "What is the start and end date?",
                "Can you break the lease early?",
                "What are the consequences if you leave early?"
            ]
        },
        
        "renewal": {
            "template": "This clause describes what happens when your lease is about to end.",
            "concerns": "Watch out for automatic renewal clauses that trap you into another lease.",
            "questions": [
                "Does the lease automatically renew?",
                "How much notice must you give to not renew?",
                "What is the notice deadline?",
                "Can the rent be increased upon renewal?"
            ]
        },
        
        "termination": {
            "template": "This clause explains how either party can end the lease agreement.",
            "concerns": "Make sure termination is possible and the penalties are reasonable.",
            "questions": [
                "Can you terminate early?",
                "What is the notice period required?",
                "Are there termination fees or penalties?",
                "What conditions allow termination without penalty?"
            ]
        },
        
        "maintenance": {
            "template": "This clause defines who is responsible for repairs and upkeep of the property.",
            "concerns": "Landlords typically handle structural repairs; tenants handle cosmetic.",
            "questions": [
                "Who is responsible for what repairs?",
                "Are you responsible for structural maintenance?",
                "How quickly must repairs be made?",
                "What happens if repairs aren't made?"
            ]
        },
        
        "utilities": {
            "template": "This clause specifies which utilities (water, electric, gas) you are responsible for.",
            "concerns": "Understand which utilities you pay for and estimated costs.",
            "questions": [
                "Which utilities do you pay for?",
                "Are utilities included in rent or separate?",
                "What is the typical utility bill?",
                "Who pays if utilities are shared?"
            ]
        },
        
        "pets": {
            "template": "This clause describes the rules about keeping pets in the rental property.",
            "concerns": "Know whether pets are allowed and what deposits or fees apply.",
            "questions": [
                "Are pets allowed?",
                "Are there size or breed restrictions?",
                "Is there a pet deposit or fee?",
                "What are pet-related damages your responsibility?"
            ]
        },
        
        "smoking": {
            "template": "This clause defines where smoking is allowed or prohibited.",
            "concerns": "Non-smoking clauses are increasingly common; understand restrictions.",
            "questions": [
                "Is smoking allowed?",
                "Are there designated smoking areas?",
                "What are penalties for unauthorized smoking?",
                "How is the property inspected for smoking damage?"
            ]
        },
        
        "damages": {
            "template": "This clause specifies who is liable for damages to the property.",
            "concerns": "Make sure liability is limited and applies only to damage beyond normal wear.",
            "questions": [
                "What counts as 'damage' vs. normal wear and tear?",
                "Are you liable for all damages?",
                "What is the maximum amount you can be charged?",
                "Does insurance cover landlord liability claims?"
            ]
        },
        
        "eviction": {
            "template": "This clause describes the conditions and process for removing tenants.",
            "concerns": "Eviction clauses should require cause and provide due process.",
            "questions": [
                "Under what conditions can you be evicted?",
                "What notice must be given?",
                "Can you be evicted without going to court?",
                "What are your rights if evicted?"
            ]
        },
        
        "default": {
            "template": "This clause defines what actions constitute a breach of the lease.",
            "concerns": "Understand what actions could lead to eviction or penalties.",
            "questions": [
                "What actions count as 'default'?",
                "Is a notice period given before action is taken?",
                "What remedies are available?",
                "Can the issue be fixed before legal action?"
            ]
        },
        
        "inspection": {
            "template": "This clause describes landlord's right to inspect the property.",
            "concerns": "You have a right to privacy; inspections should require notice and valid reason.",
            "questions": [
                "Can the landlord enter anytime?",
                "How much notice is required?",
                "For what reasons can the property be inspected?",
                "What are your rights during inspections?"
            ]
        },
        
        "other": {
            "template": "This clause covers other terms and conditions of the rental agreement.",
            "concerns": "Review this clause carefully to understand any special terms.",
            "questions": [
                "What is the main purpose of this clause?",
                "How does it affect your rights as a tenant?",
                "Are there any unusual or unfair provisions?",
                "What should you do about this clause?"
            ]
        }
    }
    
    @staticmethod
    def generate_explanation(clause_text: str, clause_type: str = "other") -> Dict[str, str]:
        """
        Generate a plain English explanation for a clause.
        
        Args:
            clause_text: The original clause text
            clause_type: The type of clause (e.g., "payment", "deposit")
            
        Returns:
            Dictionary with explanation, concerns, and key questions
        """
        if clause_type not in ExplanationEngine.EXPLANATIONS:
            clause_type = "other"
        
        config = ExplanationEngine.EXPLANATIONS[clause_type]
        
        return {
            "clause_type": clause_type,
            "plain_english_summary": config["template"],
            "key_concerns": config["concerns"],
            "key_questions": config["questions"],
            "original_text": clause_text
        }
    
    @staticmethod
    def generate_risk_explanation(risk_level: str, reason: str, recommendation: str) -> Dict[str, str]:
        """
        Generate risk explanation in plain language.
        
        Args:
            risk_level: Risk level (low, medium, high)
            reason: Reason for the risk
            recommendation: Recommended action
            
        Returns:
            Dictionary with explanation
        """
        risk_descriptions = {
            "low": "This clause appears to be standard and fair.",
            "medium": "This clause has some potentially unfavorable terms. Consider negotiating.",
            "high": "This clause contains potentially risky or unfair terms. Strongly consider negotiating."
        }
        
        return {
            "risk_level": risk_level,
            "description": risk_descriptions.get(risk_level, "Unknown risk level"),
            "reason": reason,
            "recommendation": recommendation,
            "action_items": [
                "Discuss with a trusted friend or family member",
                "Research similar leases in your area",
                "Ask the landlord about this specific clause",
                "Consider consulting with a tenant rights organization"
            ]
        }
