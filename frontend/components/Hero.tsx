"use client";

import { Mail, Linkedin, Github, BookOpen } from "lucide-react";

const socialLinks = [
  {
    icon: Mail,
    href: "mailto:wangdk93@gmail.com",
    label: "Email",
  },
  {
    icon: Linkedin,
    href: "https://www.linkedin.com/in/dingkang-wang-661219a0/",
    label: "LinkedIn",
  },
  {
    icon: BookOpen,
    href: "https://medium.com/@wangdk93",
    label: "Medium",
  },
  {
    icon: Github,
    href: "https://github.com/dingkwang",
    label: "GitHub",
  },
];

export default function Hero() {
  return (
    <section
      id="home"
      className="relative min-h-screen flex items-center justify-center px-4 pt-16"
    >
      {/* Background gradient */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-accent-blue/5 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-purple/5 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10 max-w-3xl mx-auto text-center">
        {/* Name */}
        <h1 className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-4">
          <span className="gradient-text">Dingkang Wang</span>
        </h1>

        {/* Title */}
        <p className="text-xl sm:text-2xl text-dark-300 font-medium mb-6">
          AI Agent Builder | Autonomous Driving Engineer
        </p>

        {/* Description */}
        <p className="text-dark-400 text-lg leading-relaxed mb-8 max-w-2xl mx-auto">
          Software Engineer at{" "}
          <span className="text-dark-200 font-medium">Tesla</span>, building AI
          agents and infrastructure for automated test generation within vehicle
          software CI/CD pipelines. Working at the intersection of{" "}
          <span className="text-accent-blue">LLMs</span>,{" "}
          <span className="text-accent-purple">autonomous driving</span>, and{" "}
          <span className="text-accent-cyan">data-driven systems</span>.
        </p>

        <p className="text-dark-500 text-base mb-10">
          Previously at Aeva (Perception Validation) and FOCUS Lab @ University
          of Florida. Currently exploring reinforcement learning and AI agent
          frameworks.
        </p>

        {/* Social links */}
        <div className="flex items-center justify-center gap-4">
          {socialLinks.map((link) => (
            <a
              key={link.label}
              href={link.href}
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-center gap-2 px-4 py-2.5 rounded-xl bg-dark-900 border border-dark-800 hover:border-accent-blue/50 hover:bg-dark-800 transition-all duration-200"
              aria-label={link.label}
            >
              <link.icon className="w-5 h-5 text-dark-400 group-hover:text-accent-blue transition-colors" />
              <span className="text-sm text-dark-300 group-hover:text-dark-100 transition-colors hidden sm:inline">
                {link.label}
              </span>
            </a>
          ))}
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2">
        <div className="w-6 h-10 rounded-full border-2 border-dark-700 flex items-start justify-center p-1.5">
          <div className="w-1.5 h-3 bg-dark-500 rounded-full animate-bounce" />
        </div>
      </div>
    </section>
  );
}
