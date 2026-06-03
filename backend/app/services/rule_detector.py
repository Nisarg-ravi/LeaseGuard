"""
Rule-based risk detection for rental contracts.
"""
import re
import logging
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class RuleViolation:
    """Represents a rule violation."""
    rule_id: str
    rule_name: str
    risk_level: str
    risk_score: float
    reason: str
    recommendation: str
    matched_text: str


class RuleBasedDetector:
    """Rule-based risk detection engine for rental contracts."""
    
    # Risk rules with patterns and scoring
    RULES = {
        "excessive_deposit": {
            "name": "Excessive Security Deposit",
            "patterns": [
                r"(?:deposit|security)\s+(?:of\s+)?(?:exceeds?|(?:more|greater)\s+than|(?:is\s+)?[>≥])\s*(?:3|three)\s*(?:months?|month\'s)",
                r"(?:deposit|security)\s+(?:equals?|is)\s*(?:4|five|6|six|higher)\s*(?:months?)",
            ],
            "risk_level": "high",
            "base_score": 15,
            "reason": "Deposits typically should not exceed 2-3 months of rent",
            "recommendation": "Negotiate deposit amount to be within 1-2 months of rent"
        },
        
        "lock_in_period": {
            "name": "Extended Lock-in Period",
            "patterns": [
                r"(?:lease|contract)\s+(?:cannot|may\s+not)\s+(?:be\s+)?(?:terminated|broken|ended)\s+(?:for|within)\s+(?:24|36)\s*(?:months?)",
                r"(?:early\s+)?(?:termination|cancellation|breaking)\s+(?:not\s+)?(?:allowed|permitted|possible)",
            ],
            "risk_level": "high",
            "base_score": 20,
            "reason": "Long lock-in periods limit your flexibility and ability to leave",
            "recommendation": "Try to negotiate a shorter lock-in period or early termination option"
        },
        
        "early_termination_penalty": {
            "name": "Harsh Early Termination Penalty",
            "patterns": [
                r"early\s+(?:termination|cancellation|breaking)\s+(?:fee|penalty|charge)\s+(?:of\s+)?(?:50|60|70|80|90|100)\s*%",
                r"(?:penalty|fee)\s+(?:equals?)\s+(?:2|3|6)\s*(?:months?)\s+(?:rent|payment)",
            ],
            "risk_level": "high",
            "base_score": 18,
            "reason": "Excessive penalties discourage you from leaving even in emergency situations",
            "recommendation": "Negotiate penalty to be maximum 1 month's rent or a reasonable exit clause"
        },
        
        "automatic_renewal": {
            "name": "Automatic Renewal Trap",
            "patterns": [
                r"(?:lease|contract)\s+(?:automatically|will\s+automatically)\s+(?:renew|extend|continue)",
                r"(?:renewal|extension)\s+(?:is\s+)?(?:automatic|mandatory)",
                r"(?:unless|except).*(?:notice|notification|inform)\s+(?:is\s+)?(?:provided|given)\s+(?:in\s+)?(?:writing\s+)?(?:at\s+least)\s+(?:60|90|120)\s*(?:days?)",
            ],
            "risk_level": "medium",
            "base_score": 12,
            "reason": "Automatic renewal can trap you in the lease if you forget to notify",
            "recommendation": "Add a clause requiring explicit mutual consent for renewal"
        },
        
        "tenant_responsible_maintenance": {
            "name": "All Maintenance Responsibility on Tenant",
            "patterns": [
                r"(?:tenant|renter)\s+(?:is\s+)?(?:solely\s+)?responsible\s+for\s+(?:all\s+)?(?:structural\s+)?(?:maintenance|repairs)",
                r"(?:landlord|owner)\s+(?:is\s+)?(?:not\s+)?responsible\s+for\s+(?:any\s+)?(?:repairs|maintenance)",
                r"tenant\s+(?:agrees?)\s+(?:to\s+)?(?:repair|maintain)\s+(?:all|any)\s+(?:damages|defects)",
            ],
            "risk_level": "high",
            "base_score": 16,
            "reason": "Landlords are typically responsible for major structural repairs",
            "recommendation": "Negotiate to exclude structural maintenance from tenant responsibility"
        },
        
        "unlimited_liability": {
            "name": "Unlimited Tenant Liability",
            "patterns": [
                r"tenant\s+(?:is\s+)?liable\s+for\s+(?:all\s+)?(?:damages|harm|loss)",
                r"(?:liability|indemnification)\s+(?:is\s+)?(?:unlimited|without\s+limit)",
                r"tenant\s+(?:assumes?|accepts?|agrees?)\s+(?:all\s+)?risk",
            ],
            "risk_level": "high",
            "base_score": 17,
            "reason": "Unlimited liability exposes you to potentially massive financial responsibility",
            "recommendation": "Cap liability to reasonable amounts or normal wear and tear"
        },
        
        "eviction_clause": {
            "name": "Broad Eviction Clause",
            "patterns": [
                r"(?:landlord|owner)\s+(?:may\s+)?(?:evict|remove)\s+(?:tenant|renter)\s+(?:without\s+)?(?:cause|reason)",
                r"(?:for\s+)?(?:any\s+)?breach\s+(?:of\s+)?(?:lease|agreement)\s+(?:result(?:ing|s)\s+in\s+)?immediate\s+eviction",
                r"eviction\s+(?:may|can)\s+(?:be\s+)?(?:initiated|filed)\s+(?:after\s+)?(?:1|2|3)\s*(?:days?)\s+(?:notice|default)",
            ],
            "risk_level": "high",
            "base_score": 19,
            "reason": "Overly broad eviction clauses don't protect your right to due process",
            "recommendation": "Ensure notice period is at least 30-60 days and cause must be substantial"
        },
        
        "notice_period": {
            "name": "Unreasonable Notice Period",
            "patterns": [
                r"(?:notice|notification)\s+(?:period|requirement)\s+(?:is|of)\s+(?:90|120|180)\s*(?:days?)",
                r"(?:must|have\s+to)\s+(?:provide|give)\s+notice\s+(?:at\s+least)\s+(?:120|180)\s*(?:days?)\s+in\s+advance",
            ],
            "risk_level": "medium",
            "base_score": 10,
            "reason": "Extended notice periods limit your ability to move when needed",
            "recommendation": "Negotiate notice period to 30-60 days"
        },
        
        "hidden_fees": {
            "name": "Hidden or Excessive Fees",
            "patterns": [
                r"(?:fee|charge|cost)\s+(?:for|of)\s+(?:application|processing|administrative|cleaning|move-out|carpet)",
                r"(?:additional|miscellaneous)\s+(?:fee|charge|cost)",
                r"(?:utility|water|trash|parking)\s+(?:surcharge|overage\s+fee)",
            ],
            "risk_level": "medium",
            "base_score": 11,
            "reason": "Hidden fees can significantly increase your total rental cost",
            "recommendation": "Request itemized list of all fees and negotiate to reduce or eliminate"
        },
        
        "landlord_entry": {
            "name": "Unrestricted Landlord Entry",
            "patterns": [
                r"(?:landlord|owner)\s+(?:can|may)\s+(?:enter|inspect)\s+(?:property|premises)\s+(?:at\s+)?(?:any\s+)?time",
                r"(?:no|without)\s+(?:notice|notification|permission)\s+required\s+(?:for\s+)?(?:entry|inspection)",
                r"(?:landlord|owner)\s+entry\s+(?:is\s+)?(?:unrestricted|unlimited)",
            ],
            "risk_level": "medium",
            "base_score": 9,
            "reason": "You have right to privacy; landlord should need notice and valid reason",
            "recommendation": "Require 24-48 hour notice and valid reason (repairs, inspection, etc.)"
        },
    }
    
    @classmethod
    def detect_violations(cls, clause_text: str) -> List[RuleViolation]:
        """
        Detect rule violations in a clause.
        
        Args:
            clause_text: The clause text to analyze
            
        Returns:
            List of detected violations
        """
        violations = []
        clause_lower = clause_text.lower()
        
        for rule_id, rule_config in cls.RULES.items():
            for pattern in rule_config["patterns"]:
                matches = re.finditer(pattern, clause_lower, re.IGNORECASE | re.MULTILINE)
                
                for match in matches:
                    violation = RuleViolation(
                        rule_id=rule_id,
                        rule_name=rule_config["name"],
                        risk_level=rule_config["risk_level"],
                        risk_score=rule_config["base_score"],
                        reason=rule_config["reason"],
                        recommendation=rule_config["recommendation"],
                        matched_text=match.group(0)
                    )
                    violations.append(violation)
        
        return violations
    
    @classmethod
    def calculate_score(cls, violations: List[RuleViolation]) -> float:
        """
        Calculate risk score from violations.
        
        Args:
            violations: List of detected violations
            
        Returns:
            Risk score (0-100)
        """
        if not violations:
            return 0.0
        
        total_score = sum(v.risk_score for v in violations)
        # Normalize to 0-100 scale
        # Max possible score with all violations = number of rules * max score per rule
        max_possible = len(cls.RULES) * 20  # Assuming max 20 per rule
        normalized_score = min((total_score / max_possible) * 100, 100.0)
        
        return normalized_score
