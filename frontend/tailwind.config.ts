import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['var(--font-jakarta)', 'sans-serif'],
        serif: ['var(--font-playfair)', 'serif'],
      },
      colors: {
        background: "#F9F9F7",
        foreground: "#1F2937",
        brand: {
          light: "#E8F0EA",
          DEFAULT: "#1A3224",
          dark: "#0F1D15",
        }
      },
    },
  },
  plugins: [],
};
export default config;
