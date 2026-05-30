/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./orbpondering_web/frontend/templates/**/*.html",
  ],
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["synthwave"],
    defaultTheme: "synthwave",
  },
}
