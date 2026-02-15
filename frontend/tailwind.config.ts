import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          50: "#f5f5f6",
          100: "#e6e6e7",
          200: "#cfcfd2",
          300: "#adaeb3",
          400: "#84858c",
          500: "#696a71",
          600: "#5a5b61",
          700: "#4c4d52",
          800: "#434347",
          900: "#1a1a2e",
          950: "#0f0f1a",
        },
        accent: {
          blue: "#4fc3f7",
          purple: "#b388ff",
          cyan: "#00e5ff",
          green: "#69f0ae",
          orange: "#ffab40",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;
