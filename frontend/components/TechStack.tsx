"use client";

interface TechCategory {
  name: string;
  items: string[];
}

const techCategories: TechCategory[] = [
  {
    name: "AI / ML",
    items: [
      "Python",
      "PyTorch",
      "LangChain",
      "Claude API",
      "OpenAI",
      "HuggingFace",
    ],
  },
  {
    name: "Infrastructure",
    items: ["Docker", "CUDA", "Google Cloud", "TPU", "GitHub Actions"],
  },
  {
    name: "Autonomous Driving",
    items: ["ROS", "OpenCV", "C++"],
  },
  {
    name: "Tools",
    items: ["Git", "Linux", "Jupyter", "VS Code"],
  },
];

export default function TechStack() {
  return (
    <section id="techstack" className="py-24 px-4 bg-dark-900/30">
      <div className="max-w-6xl mx-auto">
        {/* Section header */}
        <div className="text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4">
            <span className="gradient-text">Tech Stack</span>
          </h2>
          <p className="text-dark-400 text-lg max-w-2xl mx-auto">
            Technologies and tools I work with across AI, infrastructure, and
            autonomous systems.
          </p>
        </div>

        {/* Categories grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {techCategories.map((category) => (
            <div
              key={category.name}
              className="bg-dark-900 border border-dark-800 rounded-2xl p-6"
            >
              {/* Category name */}
              <h3 className="text-lg font-semibold text-dark-200 mb-4">
                {category.name}
              </h3>

              {/* Tech badges */}
              <div className="flex flex-wrap gap-2.5">
                {category.items.map((item) => (
                  <span
                    key={item}
                    className="px-3.5 py-1.5 text-sm font-medium rounded-lg border bg-dark-800/50 text-dark-300 border-dark-700 transition-all duration-200 hover:scale-105 hover:text-accent hover:border-accent/30"
                  >
                    {item}
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
