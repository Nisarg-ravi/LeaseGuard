// Upload and analysis page
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useRouter } from 'next/router';
import toast from 'react-hot-toast';
import { useUploadContract, useAnalyzeContract, useGetContract, useGetAnalysis } from '@/hooks/useApi';

export default function AnalyzePage() {
  const router = useRouter();
  const [contractId, setContractId] = useState<number | null>(null);
  const uploadMutation = useUploadContract();
  const analyzeMutation = useAnalyzeContract();
  const { data: contract } = useGetContract(contractId);
  const { data: analysis } = useGetAnalysis(contractId);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) {
      toast.error('Please upload a PDF file');
      return;
    }

    const file = acceptedFiles[0];
    if (file.type !== 'application/pdf') {
      toast.error('Only PDF files are allowed');
      return;
    }

    try {
      const result = await uploadMutation.mutateAsync(file);
      setContractId(result.id);
      toast.success('Contract uploaded successfully!');
      
      // Start analysis
      await analyzeMutation.mutateAsync(result.id);
      toast.success('Analysis started. This may take a minute...');
    } catch (error) {
      toast.error('Failed to upload contract');
    }
  }, [uploadMutation, analyzeMutation]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl font-bold text-gray-900">Analyze Your Rental Contract</h1>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {!contractId ? (
          // Upload Section
          <div className="bg-white rounded-lg shadow p-12">
            <div
              {...getRootProps()}
              className={`border-4 border-dashed rounded-lg p-12 text-center cursor-pointer transition ${
                isDragActive ? 'border-indigo-600 bg-indigo-50' : 'border-gray-300'
              }`}
            >
              <input {...getInputProps()} />
              <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-8h-8m8 0h8" />
              </svg>
              <p className="mt-4 text-lg font-medium text-gray-900">Drag & drop your PDF here</p>
              <p className="text-gray-600">or click to select a file</p>
            </div>
          </div>
        ) : (
          // Results Section
          <div className="space-y-6">
            {uploadMutation.isPending && <div className="text-center text-indigo-600">Uploading...</div>}
            {analyzeMutation.isPending && <div className="text-center text-indigo-600">Analyzing contract...</div>}

            {contract && analysis && (
              <>
                {/* Risk Summary */}
                <div className="bg-white rounded-lg shadow p-8">
                  <h2 className="text-2xl font-bold mb-6">Risk Assessment Summary</h2>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <p className="text-gray-600 text-sm">Overall Risk Score</p>
                      <p className="text-4xl font-bold text-indigo-600">{analysis.overall_risk_score.toFixed(1)}</p>
                      <p className="text-gray-600">out of 100</p>
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span>High Risk Clauses:</span>
                        <span className="font-semibold">{analysis.high_risk_count}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Medium Risk Clauses:</span>
                        <span className="font-semibold">{analysis.medium_risk_count}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Low Risk Clauses:</span>
                        <span className="font-semibold">{analysis.low_risk_count}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Summary */}
                <div className="bg-white rounded-lg shadow p-8">
                  <h3 className="text-xl font-bold mb-4">Summary</h3>
                  <p className="text-gray-700 whitespace-pre-wrap">{analysis.summary}</p>
                </div>

                {/* Clauses */}
                <div className="bg-white rounded-lg shadow p-8">
                  <h3 className="text-xl font-bold mb-6">Clause Analysis</h3>
                  <div className="space-y-4">
                    {contract.clauses?.slice(0, 5).map((clause, idx) => (
                      <div key={clause.id} className="border rounded-lg p-4 hover:shadow transition">
                        <div className="flex justify-between items-start">
                          <h4 className="font-semibold">Clause {clause.clause_number}</h4>
                          <span className={`px-3 py-1 rounded text-sm font-medium ${
                            clause.risk_level === 'high' ? 'bg-red-100 text-red-800' :
                            clause.risk_level === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                            'bg-green-100 text-green-800'
                          }`}>
                            {clause.risk_level.toUpperCase()}
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-2">{clause.original_text.substring(0, 150)}...</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Download Report */}
                <div className="bg-indigo-600 text-white rounded-lg shadow p-8 text-center">
                  <h3 className="text-xl font-bold mb-4">Ready to get the full report?</h3>
                  <a href={`${process.env.NEXT_PUBLIC_API_URL}/api/v1/report/${contractId}`} 
                     download className="inline-block bg-white text-indigo-600 px-6 py-2 rounded-lg font-semibold hover:bg-gray-100">
                    Download PDF Report
                  </a>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
