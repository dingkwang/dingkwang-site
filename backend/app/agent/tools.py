"""Custom tools for the Claude agent to retrieve information about Dingkang Wang."""

import json

TOOLS = [
    {
        "name": "get_github_repos",
        "description": (
            "Returns a list of Dingkang Wang's public GitHub repositories "
            "with descriptions. Use this when the user asks about projects, "
            "repositories, or open-source work."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "get_project_details",
        "description": (
            "Returns detailed information about a specific project by name. "
            "Use this when the user asks for details about a particular project."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "project_name": {
                    "type": "string",
                    "description": "The name of the project to look up.",
                },
            },
            "required": ["project_name"],
        },
    },
    {
        "name": "get_resume",
        "description": (
            "Returns Dingkang Wang's full resume and background information "
            "including work experience, education, skills, and publications. "
            "Use this when the user asks about experience, qualifications, "
            "education, or career history."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]

_GITHUB_REPOS = [
    {
        "name": "claude-pr-review-team",
        "description": (
            "AI-powered code review tool that uses Claude to provide automated, "
            "high-quality pull request reviews for teams. Integrates with GitHub "
            "Actions for seamless CI/CD workflow."
        ),
        "language": "Python",
        "topics": ["ai", "code-review", "claude", "github-actions"],
    },
    {
        "name": "podcastcut-skills",
        "description": (
            "AI-driven podcast editing tool that automatically identifies and "
            "cuts segments of interest from podcast audio using speech recognition "
            "and language models."
        ),
        "language": "Python",
        "topics": ["ai", "podcast", "audio-processing", "nlp"],
    },
    {
        "name": "deepagents-quickstarts",
        "description": (
            "Quickstart templates and examples for building deep learning-based "
            "AI agents. Includes patterns for tool use, multi-agent systems, "
            "and reinforcement learning."
        ),
        "language": "Python",
        "topics": ["ai-agents", "deep-learning", "quickstart"],
    },
    {
        "name": "tpu_training",
        "description": (
            "Framework and utilities for training large-scale deep learning "
            "models on Google TPUs. Includes distributed training strategies "
            "and performance optimization."
        ),
        "language": "Python",
        "topics": ["tpu", "distributed-training", "deep-learning"],
    },
    {
        "name": "FMCW-DopplerPointTransformerNet",
        "description": (
            "A Transformer-based neural network for processing FMCW radar "
            "Doppler point clouds. Designed for autonomous driving perception "
            "tasks such as object detection and velocity estimation."
        ),
        "language": "Python",
        "topics": ["radar", "transformer", "autonomous-driving", "perception"],
    },
    {
        "name": "dinov2-with-rope",
        "description": (
            "Extension of DINOv2 self-supervised vision transformer with "
            "Rotary Position Embedding (RoPE) for improved spatial reasoning "
            "and generalization to varying image resolutions."
        ),
        "language": "Python",
        "topics": ["vision-transformer", "self-supervised", "rope", "dinov2"],
    },
    {
        "name": "podcast-transcriber-mcp",
        "description": (
            "A Model Context Protocol (MCP) server for transcribing podcasts. "
            "Provides podcast transcription as a tool that AI assistants can "
            "call to process and analyze podcast content."
        ),
        "language": "Python",
        "topics": ["mcp", "podcast", "transcription", "ai-tools"],
    },
]

_PROJECT_DETAILS = {
    "claude-pr-review-team": (
        "claude-pr-review-team is an AI-powered code review system built on Claude. "
        "It automates pull request reviews by analyzing code changes, identifying "
        "potential bugs, suggesting improvements, and providing architectural feedback. "
        "The system integrates directly with GitHub Actions, allowing teams to get "
        "automated, high-quality reviews as part of their CI/CD pipeline. "
        "It supports multi-file analysis, understands context across the codebase, "
        "and provides actionable suggestions with code examples."
    ),
    "podcastcut-skills": (
        "podcastcut-skills is an AI-driven podcast editing tool. It uses speech "
        "recognition to transcribe podcast episodes, then employs language models "
        "to identify segments of interest based on user-defined topics or keywords. "
        "The tool can automatically cut and export relevant segments, saving hours "
        "of manual editing. It supports multiple audio formats and can handle "
        "long-form podcast episodes efficiently."
    ),
    "deepagents-quickstarts": (
        "deepagents-quickstarts provides quickstart templates for building AI agents "
        "powered by deep learning. It includes examples for tool-using agents, "
        "multi-agent collaboration systems, and agents that learn from feedback "
        "using reinforcement learning. The repository serves as a practical guide "
        "for developers looking to build sophisticated AI agent systems."
    ),
    "tpu_training": (
        "tpu_training is a framework for training deep learning models on Google "
        "Cloud TPUs. It provides utilities for distributed training, mixed precision, "
        "data pipeline optimization, and checkpoint management. The framework "
        "supports PyTorch/XLA and includes strategies for scaling training across "
        "multiple TPU cores and pods."
    ),
    "fmcw-dopplerpointtransformernet": (
        "FMCW-DopplerPointTransformerNet is a neural network architecture that applies "
        "Transformer-based attention mechanisms to FMCW radar Doppler point clouds. "
        "It is designed for autonomous driving perception, handling tasks like object "
        "detection and velocity estimation from radar data. The model leverages the "
        "unique properties of Doppler information to improve 3D perception, especially "
        "in adverse weather conditions where cameras and LiDAR may struggle."
    ),
    "dinov2-with-rope": (
        "dinov2-with-rope extends Meta's DINOv2 self-supervised vision transformer "
        "by incorporating Rotary Position Embedding (RoPE). RoPE provides relative "
        "positional encoding that enables the model to generalize to different image "
        "resolutions at inference time without retraining. This modification improves "
        "spatial reasoning and makes the model more flexible for downstream tasks "
        "like object detection and segmentation."
    ),
    "podcast-transcriber-mcp": (
        "podcast-transcriber-mcp is a Model Context Protocol (MCP) server that provides "
        "podcast transcription capabilities as a tool for AI assistants. It allows "
        "AI models to call transcription services programmatically, enabling use cases "
        "like podcast summarization, topic extraction, and content analysis. Built "
        "following the MCP specification, it integrates seamlessly with Claude and "
        "other MCP-compatible AI assistants."
    ),
}

_RESUME_INFO = """\
# Dingkang Wang

## Contact
- Email: wangdk93@gmail.com
- GitHub: github.com/dingkwang

## Professional Experience

### Software Engineer - Tesla (Current)
Building AI agents and infrastructure for automated test generation within vehicle
software CI/CD pipelines. Working at the intersection of LLMs, autonomous driving,
and data-driven systems.
- Developing AI-powered tools for automated test case generation
- Building infrastructure to integrate AI agents into CI/CD workflows
- Working with vehicle software systems and testing frameworks

### Perception Validation Engineer - Aeva Technologies (Previous)
Worked on perception validation for FMCW LiDAR systems used in autonomous driving.
- Validated perception algorithms for 4D LiDAR sensor data
- Developed automated testing pipelines for sensor performance
- Contributed to sensor characterization and calibration tools

### Research Assistant - FOCUS Lab, University of Florida (Previous)
Conducted research in computer vision and deep learning at the FOCUS Lab.
- Worked on point cloud processing and 3D perception
- Developed neural network architectures for radar data processing
- Published research on Transformer-based perception models

## Technical Skills
- **Languages**: Python, C++
- **ML/AI**: PyTorch, LangChain, Claude API, OpenAI API, HuggingFace Transformers
- **Infrastructure**: Docker, CUDA, TPU, GitHub Actions
- **Robotics/AV**: ROS, OpenCV
- **Current Focus**: Reinforcement learning, AI agent frameworks

## Current Interests
- Reinforcement learning for AI agents
- AI agent frameworks and multi-agent systems
- LLM-powered developer tools
- Autonomous driving perception systems
"""


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool by name and return its result as a string."""
    if tool_name == "get_github_repos":
        return json.dumps(_GITHUB_REPOS, indent=2)

    if tool_name == "get_project_details":
        project_name = tool_input.get("project_name", "").lower().strip()
        # Try exact match first, then partial match
        for key, details in _PROJECT_DETAILS.items():
            if project_name == key or project_name in key or key in project_name:
                return details
        # If no match, list available projects
        available = ", ".join(_PROJECT_DETAILS.keys())
        return (
            f"Project '{tool_input.get('project_name')}' not found. "
            f"Available projects: {available}"
        )

    if tool_name == "get_resume":
        return _RESUME_INFO

    return f"Unknown tool: {tool_name}"
