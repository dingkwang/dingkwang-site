import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Dingkang Wang - AI Agent Builder",
  description:
    "Software Engineer at Tesla, building AI agents and infrastructure for automated test generation. Working at the intersection of LLMs, autonomous driving, and data-driven systems.",
  keywords: [
    "Dingkang Wang",
    "AI Agent",
    "Tesla",
    "Software Engineer",
    "Autonomous Driving",
    "LLM",
    "Machine Learning",
  ],
  authors: [{ name: "Dingkang Wang" }],
  openGraph: {
    title: "Dingkang Wang - AI Agent Builder",
    description:
      "Software Engineer at Tesla, building AI agents and infrastructure for automated test generation.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${inter.className} bg-dark-950 text-dark-100 antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
