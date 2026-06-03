// Next.js API services
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  UPLOAD: '/api/v1/upload',
  ANALYZE: '/api/v1/analyze',
  CONTRACT: '/api/v1/contract',
  ANALYSIS: '/api/v1/analysis',
  REPORT: '/api/v1/report',
  HEALTH: '/health',
};
