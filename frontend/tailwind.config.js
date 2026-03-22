/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        'verinews-dark': '#080c10',
        'verinews-surface': '#0e1318',
        'verinews-surface2': '#141b22',
        'verinews-accent': '#00e5a0',
        'verinews-accent2': '#00b8d9',
      },
      fontFamily: {
        'syne': ['Syne', 'sans-serif'],
        'dm': ['DM Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
