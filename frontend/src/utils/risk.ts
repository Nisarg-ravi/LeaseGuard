// Risk level utilities
import { RiskLevel } from '@/types';

export const getRiskColor = (score: number): string => {
  if (score >= 80) return 'text-red-600 bg-red-50';
  if (score >= 51) return 'text-amber-600 bg-amber-50';
  if (score >= 21) return 'text-yellow-600 bg-yellow-50';
  return 'text-green-600 bg-green-50';
};

export const getRiskBgColor = (score: number): string => {
  if (score >= 80) return 'bg-red-50 border-red-200';
  if (score >= 51) return 'bg-amber-50 border-amber-200';
  if (score >= 21) return 'bg-yellow-50 border-yellow-200';
  return 'bg-green-50 border-green-200';
};

export const getRiskCategory = (score: number): string => {
  if (score >= 80) return 'SEVERE RISK';
  if (score >= 51) return 'HIGH RISK';
  if (score >= 21) return 'MODERATE RISK';
  return 'LOW RISK';
};

export const getRiskLevelColor = (level: RiskLevel): string => {
  switch (level) {
    case 'high':
      return 'text-red-600 bg-red-50';
    case 'medium':
      return 'text-amber-600 bg-amber-50';
    case 'low':
      return 'text-green-600 bg-green-50';
    default:
      return 'text-gray-600 bg-gray-50';
  }
};
