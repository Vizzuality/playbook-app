/** @type {import('tailwindcss').Config} */
let colors = require("tailwindcss/colors");

module.exports = {
  content: ["./templates/**/*.html", "./static/**/*.js", "./*.py"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["inter", "sans-serif"],
      },
      colors: {
        ...colors,
        vizzuality: "#2ba4a0",
      },
    },
  },
  variants: {
    extend: {
      display: ["group-hover"],
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};
