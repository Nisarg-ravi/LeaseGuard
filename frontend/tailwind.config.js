module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: 'hsl(0 0% 100%)',
        foreground: 'hsl(240 10% 4%)',
        card: 'hsl(0 0% 100%)',
        'card-foreground': 'hsl(240 10% 4%)',
        primary: '#2563eb',
        'primary-foreground': 'hsl(0 0% 100%)',
        secondary: '#f1f5f9',
        'secondary-foreground': 'hsl(240 10% 4%)',
        muted: 'hsl(240 5% 65%)',
        'muted-foreground': 'hsl(240 5% 40%)',
        success: '#22c55e',
        warning: '#f59e0b',
        danger: '#ef4444',
        border: 'hsl(240 6% 90%)',
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
      },
    },
  },
  plugins: [],
}
