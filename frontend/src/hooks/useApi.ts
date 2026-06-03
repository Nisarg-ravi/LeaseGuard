// Custom hooks for API calls
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS } from '@/services/api';
import { Contract, ContractAnalysis } from '@/types';

const client = axios.create({
  baseURL: API_BASE_URL,
});

export const useUploadContract = () => {
  return useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append('file', file);
      const response = await client.post(API_ENDPOINTS.UPLOAD, formData);
      return response.data as Contract;
    },
  });
};

export const useAnalyzeContract = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (contractId: number) => {
      const response = await client.post(API_ENDPOINTS.ANALYZE, { contract_id: contractId });
      return response.data;
    },
    onSuccess: (_, contractId) => {
      queryClient.invalidateQueries({ queryKey: ['contract', contractId] });
    },
  });
};

export const useGetContract = (contractId: number | null) => {
  return useQuery({
    queryKey: ['contract', contractId],
    queryFn: async () => {
      if (!contractId) return null;
      const response = await client.get(`${API_ENDPOINTS.CONTRACT}/${contractId}`);
      return response.data as Contract;
    },
    enabled: contractId !== null,
  });
};

export const useGetAnalysis = (contractId: number | null) => {
  return useQuery({
    queryKey: ['analysis', contractId],
    queryFn: async () => {
      if (!contractId) return null;
      const response = await client.get(`${API_ENDPOINTS.ANALYSIS}/${contractId}`);
      return response.data as ContractAnalysis;
    },
    enabled: contractId !== null,
  });
};
