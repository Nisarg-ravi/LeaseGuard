"""
Tests for the rule-based risk detector.
"""
import pytest
from app.services.rule_detector import RuleBasedDetector


class TestRuleBasedDetector:
    """Test suite for rule-based risk detection."""
    
    def test_detect_excessive_deposit(self):
        """Test detection of excessive security deposit."""
        clause = "The security deposit equals 4 months of rent."
        violations = RuleBasedDetector.detect_violations(clause)
        assert len(violations) > 0
        assert any(v.rule_id == "excessive_deposit" for v in violations)
    
    def test_detect_lock_in_period(self):
        """Test detection of extended lock-in period."""
        clause = "The lease cannot be terminated for 24 months."
        violations = RuleBasedDetector.detect_violations(clause)
        assert len(violations) > 0
    
    def test_no_violations(self):
        """Test clean clause with no violations."""
        clause = "Rent shall be paid on the first of each month."
        violations = RuleBasedDetector.detect_violations(clause)
        assert len(violations) == 0
    
    def test_calculate_score(self):
        """Test risk score calculation."""
        clause = "The security deposit is 6 months of rent and the tenant is liable for all damages."
        violations = RuleBasedDetector.detect_violations(clause)
        score = RuleBasedDetector.calculate_score(violations)
        assert 0 <= score <= 100
        assert score > 50  # Should be high risk


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
