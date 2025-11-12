module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#00a699",
        secondary: "#003b2f",
        accent: "#ffa500",
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
        heading: ["Sora", "sans-serif"],
      },
    },
  },
  plugins: [],
};
