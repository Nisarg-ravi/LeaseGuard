import React, { useState } from 'react'
import Link from 'next/link'
import Navbar from '@/components/Navbar'
import { ShieldCheckIcon, DocumentTextIcon, SparklesIcon, WalletIcon, BoltIcon, HomeIcon, ChevronDownIcon, CheckIcon } from '@heroicons/react/24/outline'

export default function Home() {
  const [openFaq, setOpenFaq] = useState<number | null>(0)

  const features = [
    { icon: ShieldCheckIcon, title: 'Risk Detection', desc: 'Detect hidden legal and financial risks.' },
    { icon: DocumentTextIcon, title: 'Clause Simplification', desc: 'Translate legal jargon into plain English.' },
    { icon: SparklesIcon, title: 'Recommendations', desc: 'Actionable suggestions before signing.' },
    { icon: WalletIcon, title: 'Deposit Protection', desc: 'Identify deposit-related issues.' },
    { icon: BoltIcon, title: 'AI Summary', desc: 'Understand agreements in seconds.' },
    { icon: HomeIcon, title: 'Tenant Safety', desc: 'Avoid predatory clauses.' },
  ]

  const trustItems = [
    'Powered by AI',
    'Contract Intelligence',
    'Instant Analysis',
    'Secure Uploads',
  ]

  const faqItems = [
    { q: 'Is my contract stored?', a: 'All contracts are encrypted and stored securely. You can delete your data anytime from your account settings.' },
    { q: 'How accurate is the AI?', a: 'Our AI achieves 94% accuracy in identifying legal risks, trained on thousands of rental agreements.' },
    { q: 'What file formats are supported?', a: 'We support PDF files. Word documents can be converted to PDF before uploading.' },
    { q: 'Can landlords use LeaseGuard?', a: 'LeaseGuard is designed for tenants. Landlords can contact us for enterprise licensing.' },
  ]

  const pricingPlans = [
    { name: 'Free', price: '$0', features: ['3 analyses/month', 'Basic risk detection', 'PDF reports'] },
    { name: 'Pro', price: '$9.99', features: ['Unlimited analyses', 'Advanced risk scoring', 'Priority support', 'PDF + Email reports'], highlight: true },
    { name: 'Enterprise', price: 'Custom', features: ['Team accounts', 'API access', 'Custom integrations', 'Dedicated support'] },
  ]

  return (
    <div className="bg-background text-foreground">
      <Navbar />

      {/* Hero Section */}
      <section className="section border-b border-border/50">
        <div className="container">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Left */}
            <div>
              <h1 className="mb-6">AI Rental Agreement Risk Analyzer</h1>
              <p className="text-lg mb-6">Understand hidden clauses before you sign.</p>
              
              <ul className="space-y-3 mb-8">
                <li className="flex gap-3">
                  <CheckIcon className="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
                  <span>Hidden penalties</span>
                </li>
                <li className="flex gap-3">
                  <CheckIcon className="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
                  <span>Lock-in periods</span>
                </li>
                <li className="flex gap-3">
                  <CheckIcon className="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
                  <span>Unfair clauses</span>
                </li>
                <li className="flex gap-3">
                  <CheckIcon className="w-5 h-5 text-success flex-shrink-0 mt-0.5" />
                  <span>Security deposit risks</span>
                </li>
              </ul>

              <div className="flex gap-4 flex-wrap">
                <Link href="/analyze" className="btn btn-primary">
                  Analyze Contract
                </Link>
                <button className="btn btn-outline">
                  View Sample Report
                </button>
              </div>
            </div>

            {/* Right - Dashboard Mockup */}
            <div>
              <div className="card">
                <div className="space-y-6">
                  <div className="space-y-2">
                    <p className="text-muted-foreground text-sm">Risk Score</p>
                    <p className="text-5xl font-bold text-primary">78<span className="text-2xl">/100</span></p>
                  </div>

                  <div className="space-y-3 border-t border-border/50 pt-6">
                    <p className="font-semibold">High Risk Clauses</p>
                    <ul className="space-y-2 text-sm">
                      <li className="flex gap-2">
                        <span className="w-2 h-2 bg-danger rounded-full mt-1.5 flex-shrink-0"></span>
                        <span>Early termination fee</span>
                      </li>
                      <li className="flex gap-2">
                        <span className="w-2 h-2 bg-danger rounded-full mt-1.5 flex-shrink-0"></span>
                        <span>Automatic rent increase</span>
                      </li>
                      <li className="flex gap-2">
                        <span className="w-2 h-2 bg-danger rounded-full mt-1.5 flex-shrink-0"></span>
                        <span>Deposit deduction ambiguity</span>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="section border-b border-border/50 bg-secondary/30">
        <div className="container">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {trustItems.map((item, i) => (
              <div key={i} className="text-center">
                <p className="text-muted-foreground font-medium">{item}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="section border-b border-border/50" id="features">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="mb-4">Powerful Features for Tenants</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              LeaseGuard provides everything you need to understand and protect yourself in rental agreements.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, i) => {
              const Icon = feature.icon
              return (
                <div key={i} className="card">
                  <Icon className="w-8 h-8 text-primary mb-4" />
                  <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                  <p className="text-muted-foreground">{feature.desc}</p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="section border-b border-border/50 bg-secondary/20" id="how-it-works">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="mb-4">Three Simple Steps</h2>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { step: '1', title: 'Upload Contract', desc: 'Select your PDF rental agreement' },
              { step: '2', title: 'AI Analysis', desc: 'Our AI analyzes the document' },
              { step: '3', title: 'Get Risk Report', desc: 'Receive actionable insights' },
            ].map((item, i) => (
              <div key={i} className="card">
                <div className="w-12 h-12 rounded-2xl bg-primary/10 text-primary font-bold text-xl flex items-center justify-center mb-4">
                  {item.step}
                </div>
                <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                <p className="text-muted-foreground">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Demo Report */}
      <section className="section border-b border-border/50 bg-foreground/5">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="mb-4">Sample Analysis Report</h2>
            <p className="text-muted-foreground">See what our analysis looks like</p>
          </div>

          <div className="max-w-2xl mx-auto">
            <div className="bg-foreground/95 text-white rounded-2xl p-8 font-mono text-sm space-y-6 border border-border/50">
              <div>
                <p className="text-primary">Clause:</p>
                <p className="text-secondary/80">Tenant must provide 90 days notice.</p>
              </div>
              <div className="border-t border-foreground/20 pt-6">
                <p className="text-warning">Risk: HIGH</p>
              </div>
              <div className="border-t border-foreground/20 pt-6">
                <p className="text-primary">Explanation:</p>
                <p className="text-secondary/80">This exceeds standard notice periods (typically 30-60 days).</p>
              </div>
              <div className="border-t border-foreground/20 pt-6">
                <p className="text-success">Recommendation:</p>
                <p className="text-secondary/80">Negotiate 30–60 days notice period.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="section border-b border-border/50" id="pricing">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="mb-4">Simple Pricing</h2>
            <p className="text-lg text-muted-foreground">Choose the plan that works for you</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {pricingPlans.map((plan, i) => (
              <div key={i} className={`card ${plan.highlight ? 'ring-2 ring-primary' : ''}`}>
                <h3 className="text-2xl font-semibold mb-2">{plan.name}</h3>
                <p className="text-4xl font-bold mb-6">
                  {plan.price}
                  <span className="text-base text-muted-foreground font-normal">/mo</span>
                </p>
                <ul className="space-y-3 mb-8">
                  {plan.features.map((feature, j) => (
                    <li key={j} className="flex gap-2 text-sm">
                      <CheckIcon className="w-4 h-4 text-success flex-shrink-0 mt-0.5" />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
                <button className={`w-full btn ${plan.highlight ? 'btn-primary' : 'btn-outline'}`}>
                  Get Started
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ */}
      <section className="section border-b border-border/50 bg-secondary/20" id="faq">
        <div className="container">
          <div className="text-center mb-16">
            <h2 className="mb-4">Frequently Asked Questions</h2>
          </div>

          <div className="max-w-2xl mx-auto space-y-4">
            {faqItems.map((item, i) => (
              <div key={i} className="border border-border/50 rounded-2xl overflow-hidden">
                <button
                  onClick={() => setOpenFaq(openFaq === i ? null : i)}
                  className="w-full px-6 py-4 flex justify-between items-center hover:bg-secondary/50 transition"
                >
                  <p className="font-semibold text-left">{item.q}</p>
                  <ChevronDownIcon className={`w-5 h-5 transition-transform ${openFaq === i ? 'rotate-180' : ''}`} />
                </button>
                {openFaq === i && (
                  <div className="px-6 py-4 border-t border-border/50 bg-secondary/30 text-muted-foreground">
                    {item.a}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="section border-b border-border/50">
        <div className="container text-center">
          <h2 className="mb-6">Ready to Understand Your Rental Agreement?</h2>
          <p className="text-lg text-muted-foreground mb-8 max-w-xl mx-auto">
            Analyze your contract in seconds and make informed decisions.
          </p>
          <Link href="/analyze" className="btn btn-primary text-lg px-8 py-4">
            Analyze Contract Now
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 bg-secondary/50">
        <div className="container py-16">
          <div className="grid md:grid-cols-4 gap-12 mb-12">
            <div>
              <p className="font-semibold mb-4">Product</p>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition">Features</a></li>
                <li><a href="#" className="hover:text-foreground transition">Pricing</a></li>
                <li><a href="#" className="hover:text-foreground transition">Security</a></li>
              </ul>
            </div>
            <div>
              <p className="font-semibold mb-4">Resources</p>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition">Blog</a></li>
                <li><a href="#" className="hover:text-foreground transition">Guides</a></li>
                <li><a href="#" className="hover:text-foreground transition">FAQ</a></li>
              </ul>
            </div>
            <div>
              <p className="font-semibold mb-4">Legal</p>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition">Privacy</a></li>
                <li><a href="#" className="hover:text-foreground transition">Terms</a></li>
                <li><a href="#" className="hover:text-foreground transition">Contact</a></li>
              </ul>
            </div>
            <div>
              <p className="font-semibold mb-4">Social</p>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><a href="#" className="hover:text-foreground transition">Twitter</a></li>
                <li><a href="#" className="hover:text-foreground transition">LinkedIn</a></li>
                <li><a href="#" className="hover:text-foreground transition">GitHub</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-border/50 pt-8 flex justify-between items-center text-sm text-muted-foreground">
            <p>&copy; 2024 LeaseGuard. All rights reserved.</p>
            <div className="flex gap-6">
              <a href="#" className="hover:text-foreground transition">Privacy Policy</a>
              <a href="#" className="hover:text-foreground transition">Terms of Service</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
