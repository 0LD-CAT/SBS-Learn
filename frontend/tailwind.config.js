/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],

  theme: {
    extend: {

      colors: {
        primary: "#39B54A",     // зелёная кнопка
        bgPage: "#F4F5F7",      // фон страницы
        borderInput: "#D0D5DD", // граница input
        textSecondary: "#667085"
      },

      borderRadius: {
        xl2: "14px"
      },

      boxShadow: {
        card: "0 2px 8px rgba(0,0,0,0.04)"
      }

    },
  },

  plugins: [],
};