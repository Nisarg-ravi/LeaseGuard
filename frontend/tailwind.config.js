module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: 'hsl(222 20% 7%)',
        foreground: 'hsl(210 20% 95%)',
        card: 'hsl(222 18% 10%)',
        'card-foreground': 'hsl(210 20% 95%)',
        primary: '#3b82f6',
        'primary-foreground': 'hsl(0 0% 100%)',
        secondary: 'hsl(222 16% 14%)',
        'secondary-foreground': 'hsl(210 15% 80%)',
        muted: 'hsl(222 14% 18%)',
        'muted-foreground': 'hsl(215 12% 55%)',
        accent: 'hsl(217 91% 65%)',
        'accent-foreground': 'hsl(0 0% 100%)',
        success: '#22c55e',
        warning: '#f59e0b',
        danger: '#ef4444',
        border: 'hsl(222 15% 16%)',
        ring: 'hsl(217 91% 60%)',
        surface: 'hsl(222 17% 12%)',
        'surface-elevated': 'hsl(222 16% 15%)',
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-noise': "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E\")",
      },
      boxShadow: {
        'glow-sm': '0 0 12px -3px hsl(217 91% 60% / 0.3)',
        'glow': '0 0 24px -6px hsl(217 91% 60% / 0.4)',
        'glow-lg': '0 0 48px -12px hsl(217 91% 60% / 0.5)',
        'card': '0 1px 3px hsl(0 0% 0% / 0.4), 0 1px 2px hsl(0 0% 0% / 0.3)',
        'card-hover': '0 8px 24px hsl(0 0% 0% / 0.5), 0 2px 8px hsl(0 0% 0% / 0.3)',
      },
    },
  },
  plugins: [],
}
