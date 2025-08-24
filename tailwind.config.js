/** @type {import('tailwindcss').Config} */
export const content = [
  "./static/js/**/*.js",
  "./templates/**/*.{html,py,js}", // Look for HTML files in a 'templates' folder at the project root
  "./**/templates/**/*.{html,py,js}", // Look for HTML files in the 'events' app's templates folder
  "./static/src/js/**/*.js",
];
export const darkMode = "class";
export const theme = {
  extend: {
    colors: {
      "neon-green": "#39ff14",
      "neon-blue": "#00ffff",
      "neon-pink": "#ff00ff",
      "neon-purple": "#8000ff",
      "neon-orange": "#ff5500",
      "amoled-black": "#000000",
      "dark-gray": "#121212",
      "darker-gray": "#0a0a0a",
    },
    boxShadow: {
      "neon-green": "0 0 5px #39ff14, 0 0 10px #39ff14",
      "neon-blue": "0 0 5px #00ffff, 0 0 10px #00ffff",
      "neon-pink": "0 0 5px #ff00ff, 0 0 10px #ff00ff",
      "neon-purple": "0 0 5px #8000ff, 0 0 10px #8000ff",
      "neon-orange": "0 0 5px #ff5500, 0 0 10px #ff5500",
    },
    animation: {
      "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
    },
  },
};
export const plugins = [];
