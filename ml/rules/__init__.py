"""
Rule definitions for risk detection.
"""

RISK_RULES = {
    "excessive_deposit": {
        "description": "Security deposit exceeds recommended amount",
        "threshold": "3+ months",
        "severity": "high",
        "recommendation": "Negotiate to 1-2 months of rent"
    },
    "lock_in_period": {
        "description": "Long lease lock-in without exit options",
        "threshold": "24+ months",
        "severity": "high",
        "recommendation": "Ask for early termination clause"
    },
    "early_termination_penalty": {
        "description": "Excessive penalties for breaking lease",
        "threshold": "50%+ of rent",
        "severity": "high",
        "recommendation": "Negotiate penalty cap"
    },
    "automatic_renewal": {
        "description": "Lease automatically renews without consent",
        "threshold": "automatic",
        "severity": "medium",
        "recommendation": "Require explicit renewal consent"
    },
    "tenant_maintenance": {
        "description": "All maintenance shifted to tenant",
        "threshold": "100% tenant responsibility",
        "severity": "high",
        "recommendation": "Limit to cosmetic damages only"
    },
    "unlimited_liability": {
        "description": "Tenant liable for unlimited damages",
        "threshold": "unlimited",
        "severity": "high",
        "recommendation": "Cap liability at security deposit"
    },
    "eviction_clause": {
        "description": "Overly broad eviction without cause",
        "threshold": "any breach",
        "severity": "high",
        "recommendation": "Require just cause and process"
    },
    "notice_period": {
        "description": "Unreasonable termination notice period",
        "threshold": "90+ days",
        "severity": "medium",
        "recommendation": "Negotiate to 30-60 days"
    },
    "hidden_fees": {
        "description": "Additional fees not in main rent",
        "threshold": "multiple fees",
        "severity": "medium",
        "recommendation": "Get itemized list and negotiate"
    },
    "landlord_entry": {
        "description": "Unrestricted landlord access",
        "threshold": "no notice required",
        "severity": "medium",
        "recommendation": "Require 24-48 hour notice"
    }
}
