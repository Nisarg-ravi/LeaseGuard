// Type definitions for contract analysis
export interface Contract {
  id: number;
  user_id: number;
  filename: string;
  original_filename: string;
  upload_date: string;
  risk_score: number | null;
  total_pages: number | null;
  analysis?: ContractAnalysis;
  clauses: Clause[];
}

export interface ContractAnalysis {
  id: number;
  total_clauses: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  overall_risk_score: number;
  rule_based_score: number;
  ml_score: number;
  summary: string;
}

export interface Clause {
  id: number;
  clause_number: number;
  contract_id: number;
  original_text: string;
  risk_level: 'low' | 'medium' | 'high';
  risk_score: number;
  explanation: string;
  ml_confidence: number | null;
}

export interface RiskExplanation {
  risk_level: 'low' | 'medium' | 'high';
  reason: string;
  severity_score: number;
  recommendation: string;
}

export type RiskLevel = 'low' | 'medium' | 'high';
