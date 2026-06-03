// Main page component
import React from 'react';
import Link from 'next/link';
import { ArrowRightIcon, DocumentTextIcon, ShieldCheckIcon, ChartBarIcon } from '@heroicons/react/24/outline';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Navigation */}
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-indigo-600">LeaseGuard</h1>
            </div>
            <div className="flex items-center space-x-4">
              <Link href="/analyze" className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">
                Upload Contract
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Understand Your Rental Agreement
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            LeaseGuard uses AI to analyze rental contracts, identify risky clauses, and explain them in simple English. Protect yourself before signing.
          </p>
          <Link href="/analyze" className="inline-flex items-center bg-indigo-600 text-white px-8 py-3 rounded-lg hover:bg-indigo-700">
            Get Started <ArrowRightIcon className="ml-2 w-5 h-5" />
          </Link>
        </div>

        {/* Features */}
        <div className="mt-20 grid md:grid-cols-3 gap-8">
          <div className="bg-white p-8 rounded-lg shadow">
            <DocumentTextIcon className="w-12 h-12 text-indigo-600 mb-4" />
            <h3 className="text-xl font-semibold mb-3">Extract & Analyze</h3>
            <p className="text-gray-600">Upload your PDF rental contract and get instant AI-powered analysis of all clauses.</p>
          </div>
          <div className="bg-white p-8 rounded-lg shadow">
            <ShieldCheckIcon className="w-12 h-12 text-indigo-600 mb-4" />
            <h3 className="text-xl font-semibold mb-3">Identify Risks</h3>
            <p className="text-gray-600">Discover hidden penalties, unfair clauses, and terms that might work against you.</p>
          </div>
          <div className="bg-white p-8 rounded-lg shadow">
            <ChartBarIcon className="w-12 h-12 text-indigo-600 mb-4" />
            <h3 className="text-xl font-semibold mb-3">Get Risk Score</h3>
            <p className="text-gray-600">Receive a comprehensive risk score and downloadable report with recommendations.</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-indigo-600 text-white py-16">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h3 className="text-3xl font-bold mb-4">Ready to analyze your contract?</h3>
          <p className="text-lg mb-8 opacity-90">Upload your rental agreement now and get instant insights.</p>
          <Link href="/analyze" className="inline-block bg-white text-indigo-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100">
            Upload Contract
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p>&copy; 2024 LeaseGuard. Helping tenants understand rental agreements.</p>
        </div>
      </footer>
    </main>
  );
}
