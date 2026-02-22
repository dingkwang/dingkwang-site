"use client";

import { ExternalLink, Github } from "lucide-react";

interface Project {
  title: string;
  description: string;
  repoUrl: string;
  tags: string[];
  videoUrl?: string;
  installCmd?: string;
}

const projects: Project[] = [
  {
    title: "opencode-agent-sdk-python",
    description:
      "A Seamless Switch Python SDK for Agent backends. Swap between local Claude execution and OpenCode remote runtime with a standardized API. Includes policy enforcement and hooks.",
    repoUrl: "https://github.com/dingkwang/opencode-agent-sdk-python",
    tags: ["Python SDK", "Agent Runtime", "Seamless Switch"],
    videoUrl: "/opencode-sdk-demo.mp4",
    installCmd: "pip install opencode-agent-sdk"
  },
  {
    title: "openclaw_superskill",
    description:
      "A collection of advanced, production-ready skills for OpenClaw. Includes specialized automation tools and integrations.",
    repoUrl: "https://github.com/dingkwang/openclaw_superskill",
    tags: ["OpenClaw", "Skills", "Automation"],
  },
  {
    title: "claude-pr-review-team",
    description:
      "AI-powered PR reviewer using Claude. Automates code review with intelligent analysis, providing actionable feedback on pull requests.",
    repoUrl: "https://github.com/dingkwang/claude-pr-review-team",
    tags: ["Claude API", "GitHub Actions", "Code Review"],
  },
  {
    title: "podcastcut-skills",
    description:
      "Claude Code Skills for podcast and video editing. Streamlines media production workflows with AI-assisted cutting and editing.",
    repoUrl: "https://github.com/dingkwang/podcastcut-skills",
    tags: ["Claude Code", "Media Editing", "Skills"],
  },
  {
    title: "deepagents-quickstarts",
    description:
      "Quick-start templates for building deep agents. Provides boilerplate and patterns for developing sophisticated AI agent systems.",
    repoUrl: "https://github.com/dingkwang/deepagents-quickstarts",
    tags: ["AI Agents", "Templates", "Python"],
  },
  {
    title: "tpu_training",
    description:
      "TPU training infrastructure and utilities. Tools and configurations for distributed training on Google Cloud TPUs.",
    repoUrl: "https://github.com/dingkwang/tpu_training",
    tags: ["TPU", "Google Cloud", "Distributed Training"],
  },
  {
    title: "FMCW-DopplerPointTransformerNet",
    description:
      "FMCW LIDAR perception model using Doppler point cloud data with transformer architecture for autonomous driving applications.",
    repoUrl: "https://github.com/dingkwang/FMCW-DopplerPointTransformerNet",
    tags: ["LIDAR", "Transformers", "Perception"],
  },
  {
    title: "dinov2-with-rope",
    description:
      "DINOv2 vision transformer enhanced with Rotary Position Embeddings (RoPE) for improved spatial understanding in vision tasks.",
    repoUrl: "https://github.com/dingkwang/dinov2-with-rope",
    tags: ["Vision Transformer", "DINOv2", "RoPE"],
  },
  {
    title: "podcast-transcriber-mcp",
    description:
      "MCP tool demo with OpenAI Agent SDK. Demonstrates Model Context Protocol integration for podcast transcription workflows.",
    repoUrl: "https://github.com/dingkwang/podcast-transcriber-mcp",
    tags: ["MCP", "OpenAI", "Transcription"],
  },
];

export default function Projects() {
  return (
    <section id="projects" className="py-24 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Section header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            <span className="gradient-text">Featured Projects</span>
          </h2>
          <p className="text-dark-400 text-lg max-w-2xl mx-auto">
            Open-source tools and research at the intersection of AI, LLMs, and
            autonomous systems.
          </p>
        </div>

        {/* Project grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <div
              key={project.title}
              className="card-hover group bg-dark-900 border border-dark-800 rounded-2xl p-6 flex flex-col"
            >
              {/* Project icon */}
              <div className="flex items-center justify-between mb-4">
                <div className="p-2 rounded-lg bg-dark-800">
                  <Github className="w-5 h-5 text-dark-400" />
                </div>
                <a
                  href={project.repoUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="p-2 rounded-lg hover:bg-dark-800 transition-colors"
                  aria-label={`View ${project.title} on GitHub`}
                >
                  <ExternalLink className="w-4 h-4 text-dark-500 group-hover:text-accent transition-colors" />
                </a>
              </div>

              {/* Title */}
              <h3 className="text-lg font-semibold text-dark-100 mb-2 group-hover:text-accent transition-colors">
                <a
                  href={project.repoUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {project.title}
                </a>
              </h3>

              {/* Description */}
              <p className="text-dark-400 text-sm leading-relaxed mb-4 flex-1">
                {project.description}
              </p>

              {/* Install Command */}
              {project.installCmd && (
                <div className="mb-4 bg-dark-950 rounded-lg p-2 border border-dark-800 font-mono text-xs text-dark-300 overflow-x-auto whitespace-nowrap">
                  $ {project.installCmd}
                </div>
              )}

              {/* Video Demo */}
              {project.videoUrl && (
                <div className="mb-4 rounded-lg overflow-hidden border border-dark-800">
                  <video
                    src={project.videoUrl}
                    controls
                    className="w-full aspect-video object-cover"
                    poster="/placeholder-video-poster.jpg" // Optional: add a poster if available
                  />
                </div>
              )}

              {/* Tags */}
              <div className="flex flex-wrap gap-2">
                {project.tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-2.5 py-1 text-xs font-medium rounded-full bg-dark-800 text-dark-300 border border-dark-700"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
