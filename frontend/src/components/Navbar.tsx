import Link from 'next/link'
import { useState } from 'react'
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline'

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="navbar">
      <div className="container flex justify-between items-center h-full">
        <Link href="/" className="text-2xl font-bold text-primary">
          LeaseGuard
        </Link>

        {/* Desktop Menu */}
        <div className="hidden md:flex items-center gap-8">
          <Link href="#features" className="text-muted-foreground hover:text-foreground transition">
            Features
          </Link>
          <Link href="#how-it-works" className="text-muted-foreground hover:text-foreground transition">
            How It Works
          </Link>
          <Link href="#pricing" className="text-muted-foreground hover:text-foreground transition">
            Pricing
          </Link>
          <Link href="#faq" className="text-muted-foreground hover:text-foreground transition">
            FAQ
          </Link>
        </div>

        <div className="hidden md:flex items-center gap-4">
          <button className="btn btn-outline">Log in</button>
          <Link href="/analyze" className="btn btn-primary">
            Analyze Contract
          </Link>
        </div>

        {/* Mobile Menu Button */}
        <button className="md:hidden" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? (
            <XMarkIcon className="w-6 h-6" />
          ) : (
            <Bars3Icon className="w-6 h-6" />
          )}
        </button>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden border-t border-border/50 bg-background/95">
          <div className="container py-4 flex flex-col gap-4">
            <Link href="#features" className="text-muted-foreground hover:text-foreground">Features</Link>
            <Link href="#how-it-works" className="text-muted-foreground hover:text-foreground">How It Works</Link>
            <Link href="#pricing" className="text-muted-foreground hover:text-foreground">Pricing</Link>
            <Link href="#faq" className="text-muted-foreground hover:text-foreground">FAQ</Link>
            <button className="btn btn-outline w-full">Log in</button>
            <Link href="/analyze" className="btn btn-primary w-full">Analyze Contract</Link>
          </div>
        </div>
      )}
    </nav>
  )
}
