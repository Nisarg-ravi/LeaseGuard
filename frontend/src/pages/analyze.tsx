import React, { useCallback, useState } from 'react'
import Link from 'next/link'
import Navbar from '@/components/Navbar'
import { useDropzone } from 'react-dropzone'
import { useUploadContract, useAnalyzeContract, useGetContract, useGetAnalysis } from '@/hooks/useApi'
import toast from 'react-hot-toast'
import { ArrowUpTrayIcon, ExclamationCircleIcon, CheckCircleIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'

export default function AnalyzePage() {
  const [contractId, setContractId] = useState<number | null>(null)
  const uploadMutation = useUploadContract()
  const analyzeMutation = useAnalyzeContract()
  const { data: contract } = useGetContract(contractId)
  const { data: analysis } = useGetAnalysis(contractId)

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (acceptedFiles.length === 0) {
      toast.error('Please upload a PDF file')
      return
    }

    const file = acceptedFiles[0]
    if (file.type !== 'application/pdf') {
      toast.error('Only PDF files are allowed')
      return
    }

    try {
      const result = await uploadMutation.mutateAsync(file)
      setContractId(result.id)
      toast.success('Contract uploaded successfully!')
      await analyzeMutation.mutateAsync(result.id)
      toast.success('Analysis complete!')
    } catch (error) {
      toast.error('Failed to upload contract')
    }
  }, [uploadMutation, analyzeMutation])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop })

  return (
    <div className="bg-background text-foreground min-h-screen">
      <Navbar />

      <div className="container py-12">
        {!contractId ? (
          // Upload Section
          <div className="max-w-2xl mx-auto">
            <div className="mb-12">
              <h1 className="mb-4">Analyze Your Rental Contract</h1>
              <p className="text-lg text-muted-foreground">
                Upload your PDF and get instant AI-powered risk assessment
              </p>
            </div>

            <div
              {...getRootProps()}
              className={`card border-2 border-dashed cursor-pointer transition-all ${
                isDragActive ? 'border-primary bg-primary/5' : 'border-border/50'
              }`}
            >
              <input {...getInputProps()} />
              <div className="flex flex-col items-center justify-center py-16">
                <ArrowUpTrayIcon className="w-12 h-12 text-primary mb-4 opacity-50" />
                <p className="font-semibold text-lg mb-2">Drag and drop your PDF here</p>
                <p className="text-muted-foreground">or click to select a file</p>
              </div>
            </div>

            <div className="mt-8 p-4 bg-secondary/50 rounded-2xl border border-border/50">
              <p className="text-sm text-muted-foreground">
                💡 <strong>Tip:</strong> Make sure your file is a PDF. We support single and multi-page documents up to 10MB.
              </p>
            </div>
          </div>
        ) : (
          // Results Section
          <div>
            <div className="mb-12">
              <Link href="/analyze" className="text-primary hover:opacity-70 transition text-sm mb-4 inline-block">
                ← Analyze Another Contract
              </Link>
              <h1>Analysis Results</h1>
            </div>

            {(uploadMutation.isPending || analyzeMutation.isPending) && (
              <div className="card text-center py-12 mb-8">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary mb-4"></div>
                <p className="text-muted-foreground">
                  {uploadMutation.isPending ? 'Uploading...' : 'Analyzing contract...'}
                </p>
              </div>
            )}

            {contract && analysis && (
              <div className="space-y-8">
                {/* Risk Summary Card */}
                <div className="card">
                  <div className="grid md:grid-cols-3 gap-8">
                    <div>
                      <p className="text-muted-foreground text-sm mb-2">Overall Risk Score</p>
                      <p className="text-6xl font-bold text-primary">{analysis.overall_risk_score.toFixed(0)}</p>
                      <p className="text-muted-foreground text-sm mt-2">out of 100</p>
                    </div>
                    <div className="space-y-3">
                      <div>
                        <div className="flex justify-between items-center mb-1">
                          <span className="text-sm font-medium">High Risk</span>
                          <span className="text-danger font-bold">{analysis.high_risk_count}</span>
                        </div>
                        <div className="h-2 bg-secondary rounded-full overflow-hidden">
                          <div className="h-full bg-danger" style={{ width: `${Math.min(analysis.high_risk_count * 20, 100)}%` }}></div>
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between items-center mb-1">
                          <span className="text-sm font-medium">Medium Risk</span>
                          <span className="text-warning font-bold">{analysis.medium_risk_count}</span>
                        </div>
                        <div className="h-2 bg-secondary rounded-full overflow-hidden">
                          <div className="h-full bg-warning" style={{ width: `${Math.min(analysis.medium_risk_count * 20, 100)}%` }}></div>
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between items-center mb-1">
                          <span className="text-sm font-medium">Low Risk</span>
                          <span className="text-success font-bold">{analysis.low_risk_count}</span>
                        </div>
                        <div className="h-2 bg-secondary rounded-full overflow-hidden">
                          <div className="h-full bg-success" style={{ width: `${Math.min(analysis.low_risk_count * 20, 100)}%` }}></div>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center justify-center">
                      <div className="text-center">
                        <CheckCircleIcon className="w-12 h-12 text-success mx-auto mb-2" />
                        <p className="font-semibold">Analysis Complete</p>
                        <p className="text-sm text-muted-foreground">Ready to review</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Summary Section */}
                <div className="card">
                  <h2 className="text-2xl font-semibold mb-4">Summary</h2>
                  <p className="text-muted-foreground whitespace-pre-wrap leading-relaxed">{analysis.summary}</p>
                </div>

                {/* Clauses Section */}
                <div className="card">
                  <h2 className="text-2xl font-semibold mb-6">Clause Breakdown</h2>
                  <div className="space-y-4">
                    {contract.clauses?.slice(0, 10).map((clause) => {
                      const riskIcon = clause.risk_level === 'high' ? (
                        <ExclamationCircleIcon className="w-5 h-5 text-danger" />
                      ) : clause.risk_level === 'medium' ? (
                        <ExclamationTriangleIcon className="w-5 h-5 text-warning" />
                      ) : (
                        <CheckCircleIcon className="w-5 h-5 text-success" />
                      )

                      return (
                        <div key={clause.id} className="border border-border/50 rounded-2xl p-4 hover:-translate-y-1 transition-all">
                          <div className="flex gap-4">
                            <div className="flex-shrink-0 mt-1">{riskIcon}</div>
                            <div className="flex-1">
                              <div className="flex items-start justify-between gap-4">
                                <div>
                                  <h3 className="font-semibold mb-1">Clause {clause.clause_number}</h3>
                                  <p className="text-sm text-muted-foreground">{clause.original_text.substring(0, 200)}...</p>
                                </div>
                                <span className={`px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap flex-shrink-0 ${
                                  clause.risk_level === 'high'
                                    ? 'bg-danger/10 text-danger border border-danger/20'
                                    : clause.risk_level === 'medium'
                                    ? 'bg-warning/10 text-warning border border-warning/20'
                                    : 'bg-success/10 text-success border border-success/20'
                                }`}>
                                  {clause.risk_level.charAt(0).toUpperCase() + clause.risk_level.slice(1)} Risk
                                </span>
                              </div>
                            </div>
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>

                {/* Download Section */}
                <div className="card bg-primary/5 border border-primary/20">
                  <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                    <div>
                      <h3 className="text-lg font-semibold mb-2">Download Full Report</h3>
                      <p className="text-muted-foreground">Get a detailed PDF report with all analysis and recommendations.</p>
                    </div>
                    <a
                      href={`${process.env.NEXT_PUBLIC_API_URL}/api/v1/report/${contractId}`}
                      download
                      className="btn btn-primary flex-shrink-0"
                    >
                      Download PDF
                    </a>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
