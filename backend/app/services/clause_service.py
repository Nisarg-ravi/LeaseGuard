"""
Clause segmentation and extraction service.
"""
from typing import List, Tuple
import re
import logging

logger = logging.getLogger(__name__)


class ClauseSegmentation:
    """Service for segmenting rental contracts into logical clauses."""
    
    # Patterns for common clause headers in rental contracts
    CLAUSE_PATTERNS = [
        r"^\s*(SECTION|CLAUSE|ARTICLE|PART)\s+[\d\w]+[:\.\s]",
        r"^\s*(\d+\.|§\s*\d+)",
        r"^\s*[A-Z][A-Z\s]{2,}[:\.]",
        r"(Payment|Deposit|Term|Renewal|Termination|Maintenance|Repairs|"
        r"Utilities|Insurance|Pets|Smoking|Damages|Liability|"
        r"Eviction|Default|Notices|Entry|Guests|Assignment|"
        r"Abandoned Property|Inspection|Dispute|Indemnification|"
        r"Entire Agreement|Severability|Governing Law|Jurisdiction)[:\s]"
    ]
    
    # Minimum clause length in characters
    MIN_CLAUSE_LENGTH = 50
    MAX_CLAUSE_LENGTH = 5000
    
    @classmethod
    def segment_clauses(cls, full_text: str) -> List[str]:
        """
        Segment contract text into individual clauses.
        
        Args:
            full_text: Complete contract text
            
        Returns:
            List of clause strings
        """
        try:
            clauses = []
            lines = full_text.split('\n')
            current_clause = []
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Check if line matches clause pattern
                is_clause_start = False
                for pattern in cls.CLAUSE_PATTERNS:
                    if re.match(pattern, line, re.IGNORECASE):
                        is_clause_start = True
                        break
                
                if is_clause_start and current_clause:
                    # Save previous clause
                    clause_text = '\n'.join(current_clause).strip()
                    if cls.MIN_CLAUSE_LENGTH <= len(clause_text) <= cls.MAX_CLAUSE_LENGTH:
                        clauses.append(clause_text)
                    current_clause = [line]
                else:
                    current_clause.append(line)
            
            # Add last clause
            if current_clause:
                clause_text = '\n'.join(current_clause).strip()
                if cls.MIN_CLAUSE_LENGTH <= len(clause_text) <= cls.MAX_CLAUSE_LENGTH:
                    clauses.append(clause_text)
            
            logger.info(f"Segmented contract into {len(clauses)} clauses")
            return clauses
            
        except Exception as e:
            logger.error(f"Error segmenting clauses: {str(e)}")
            raise ValueError(f"Failed to segment clauses: {str(e)}")
    
    @staticmethod
    def extract_clause_type(clause_text: str) -> str:
        """
        Identify the type of clause.
        
        Args:
            clause_text: The clause text
            
        Returns:
            Clause type identifier
        """
        keywords = {
            "payment": ["payment", "rent", "monthly", "fee"],
            "deposit": ["deposit", "security", "escrow"],
            "term": ["term", "period", "lease", "months"],
            "renewal": ["renewal", "renew", "extend"],
            "termination": ["termination", "terminate", "end"],
            "maintenance": ["maintenance", "repair", "maintain"],
            "utilities": ["utilities", "water", "electric", "gas"],
            "pets": ["pet", "animal", "dog", "cat"],
            "smoking": ["smoke", "smoking", "tobacco"],
            "damages": ["damage", "liable", "liability"],
            "eviction": ["eviction", "evict", "removal"],
            "default": ["default", "breach"],
            "inspection": ["inspect", "inspection", "entry"],
        }
        
        clause_lower = clause_text.lower()
        for clause_type, keywords_list in keywords.items():
            if any(kw in clause_lower for kw in keywords_list):
                return clause_type
        
        return "other"
