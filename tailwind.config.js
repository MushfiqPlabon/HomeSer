/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js"
  ],
  darkMode: 'class', // Enable dark mode
  theme: {
    extend: {
      colors: {
        "neon-green": "#39ff14",
        "neon-blue": "#00ffff",
        "neon-pink": "#ff00ff",
        "neon-purple": "#8000ff",
        "neon-orange": "#ff5500",
        "amoled-black": "#000000",
        "dark-gray": "#121212",
        "darker-gray": "#0a0a0a"
      },
      boxShadow: {
        'neon-green': '0 0 5px #39ff14, 0 0 10px #39ff14',
        'neon-blue': '0 0 5px #00ffff, 0 0 10px #00ffff',
        'neon-pink': '0 0 5px #ff00ff, 0 0 10px #ff00ff',
        'neon-purple': '0 0 5px #8000ff, 0 0 10px #8000ff',
        'neon-orange': '0 0 5px #ff5500, 0 0 10px #ff5500'
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite'
      }
    },
  },
  plugins: [],
}