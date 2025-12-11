# About This Book

As we transition from the era of Generative AI, where models simply respond to prompts, to the era of Agentic AI, where systems actively pursue objectives and interact with their environment, developers need practical patterns and principles to construct reliable, scalable agentic systems. 
This book provides exactly that: a hands-on collection of **essential design patterns** that cover everything from foundational workflow patterns like prompt chaining and routing, to advanced capabilities such as multi-agent collaboration, memory management, and recovery mechanisms.

This book originated as personal study notes that helped guide and refine my understanding of the domain.
While significant innovation in agentic patterns occurs within specialized communities, most AI developers and systems today rely primarily on ReAct combined with tool use, treating this combination as sufficient for building agents.
Yet the deeper knowledge of design patterns for agentic AI—understanding when to use or avoid specific patterns and how to combine them effectively—remains fragmented across diverse resources.

These design patterns have been collected from a growing corpus of literature on agentic systems, including engineering blogs from leading AI companies like Anthropic, Manus, and LangChain, insights from active developer bloggers, and an increasing number of academic publications and books.
In addition, many patterns in this book were extracted directly from implementations of deep agents like IBM's CUGA (Configurable Generalist Agent) and LangChain's Deep Agents. 
AI code-writing tools enabled analysis of these large codebases, identifying reusable patterns, design components, and principles that we've codified into transferable knowledge for building new agentic applications.

This book is a living resource that will be constantly updated as new design patterns and best practices emerge in the field of agentic AI development. 
As the community continues to build and refine agentic systems, new patterns will be identified, existing patterns will be refined, and our understanding of what works best will evolve. 
We encourage readers to revisit this resource regularly to stay current with the latest developments in software agent development. 
Whether you're returning after a few months or checking in periodically, you'll find that the content continues to grow and improve, reflecting the ongoing maturation of the agentic AI ecosystem.

Each pattern is presented with a motivation, clear explanations, practical guidelines for when to use it, and real-world examples that demonstrate how to implement these concepts in production systems. 
Whether you're building simple single-agent workflows or complex multi-agent architectures, this book serves as both a reference guide and a practical handbook for navigating the rapidly evolving landscape of agentic AI development.

**George Kour, Ph.D.** 

---

## Book Structure

The book is organized into **7 parts** containing **32 modules**:

1. **Introduction & Foundations** (4 modules) - Core concepts, context, and design pattern fundamentals
2. **Core Workflow** (4 modules) - Fundamental patterns for building agent workflows
3. **Tools** (4 modules) - Designing the Agent-Computer Interface
4. **Reasoning & Planning** (4 modules) - Enabling agents to plan and reason effectively
5. **Context and memory** (8 modules) - Managing the finite context window, optimizing context usage, and managing persistent and external memory for agents, including knowledge retrieval
6. **Multi-Agent Systems** (5 modules) - Modern LLM-based multi-agent collaboration patterns
7. **Human input and Recovery** (3 modules) - Learning, adaptation, and human interaction

The patterns are organized to build concepts progressively, but you can also use this book as a reference, jumping to patterns that address specific challenges you face in your agent development projects.

## The Emphasis on Practical Application

Throughout this book, the emphasis is on practical application. Every pattern includes runnable code examples that you can execute, modify, and learn from. We encourage you to:

* **Run the examples** - Don't just read them; execute them and see how they work
* **Experiment** - Modify the code, try different inputs, break things and fix them
* **Adapt** - Use the patterns as starting points for your own applications
* **Build** - Apply patterns to real problems you're trying to solve

The code examples are designed to clearly illustrate each pattern's core logic and its implementation, focusing on clarity and practicality over production-ready complexity.

---

## The Creation Process: A New Paradigm for Book Writing

This book was created through an orchestrated collaboration between human vision and AI capability, representing a shift from traditional solitary writing to a new paradigm of knowledge creation.
AI systems have reached a point where they can produce text that is not merely passable, but often clearer, more structured, and more comprehensive than what humans might produce alone. 
The mechanical task of writing, i.e., transforming ideas into well-formed sentences, organizing concepts into coherent sections, maintaining consistency across chapters, is increasingly becoming automated. 
This is not a replacement of human creativity, but rather its amplification.

In this new paradigm, the human author's role transforms from *writer* to *editor-director*. 
The primary responsibilities shift to higher-order tasks that require human judgment and vision:

- **Collecting and Curating**: Selecting valuable resources from research papers, blog posts, and other sources, then directing AI to incorporate and synthesize them into the narrative.
- **Asking the Right Questions**: Formulating precise, strategically important questions that guide AI tools—whether code-writing assistants, research systems, or content generators—through the content generation process.
- **Validation and Refinement**: Reading, evaluating, and iterating to ensure content aligns with the vision, fits the intended style, and matches the appropriate depth for each subject.
- **Structural Orchestration**: Ensuring coherence across the entire work—logical chapter flow, concepts that build upon each other, and section length that matches significance.

The creation process follows an iterative cycle: the human defines direction and collects materials, AI generates and organizes content, the human validates and refines, and the cycle repeats. This approach enables rapid exploration of ideas, comprehensive coverage, and efficient incorporation of diverse sources, allowing the human to focus on vision, judgment, and creative direction.

### A Fitting Demonstration

This book was created using the same principles it teaches: intelligent agents pursuing objectives, orchestrated workflows, and tools that achieve goals impossible through traditional means alone.

The content has been carefully reviewed and validated by the author to ensure accuracy, quality, and alignment with the intended vision. However, given the collaborative nature of this creation process, there may occasionally be errors, inconsistencies, or areas that could benefit from improvement.

If you encounter any issues, have suggestions for improvement, or notice any errors, we would greatly appreciate your feedback. Please contact the author at **kourgeorge@gmail.com**. Your input helps us maintain and improve the quality of this resource for the entire community.

---

## Let's Begin

This book is your guide to building intelligent, agentic systems. Whether you're just starting your journey into agentic AI or looking to deepen your understanding of proven patterns, we hope this resource empowers you to create systems that are robust, reliable, and effective.
The journey ahead is exciting. You're about to learn patterns that will enable you to build systems that can reason, plan, act, and collaborate. These are the building blocks of the next generation of AI applications.
Let's begin this hands-on journey into building intelligent, agentic systems!

---

## Bibliography

Each module in this book includes its own bibliography with references specific to that pattern or topic. 
This section collects the main sources that have informed the overall content and structure of the book.
Much of the content in this book is based on **"Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems"** by **Antonio Gulli**, published by Springer.

### Journal Articles

- Liu, Yue, et al. "Agent Design Pattern Catalogue: A Collection of Architectural Patterns for Foundation Model Based Agents." *Journal of Systems and Software*, vol. 220, 2025, p. 112278. Available at: https://www.sciencedirect.com/science/article/pii/S0164121224003224

### Papers

- Marreed, Sami, et al. "Towards enterprise-ready computer using generalist agent." *arXiv preprint arXiv:2503.01861* (2025). Available at: https://arxiv.org/abs/2503.01861

### Online Articles and Blog Posts

- Ji, Yichao 'Peak'. "Context Engineering for AI Agents: Lessons from Building Manus." *Manus Blog*, July 18, 2025. Available at: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus

- Huang, Nick. "How Agents Can Use Filesystems for Context Engineering." *LangChain Blog*, November 21, 2025. Available at: https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering/

- Anthropic. "How We Built Our Multi-Agent Research System." *Anthropic Engineering Blog*, June 13, 2025. Available at: https://www.anthropic.com/engineering/multi-agent-research-system

- Anthropic. "Building Effective AI Agents." *Anthropic Engineering Blog*, December 19, 2024. Available at: https://www.anthropic.com/engineering/building-effective-agents

- Google Cloud. "Choose a Design Pattern for Your Agentic AI System." *Google Cloud Architecture Center*, 2025. Available at: https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system

- IBM Research. "Introducing CUGA: The enterprise-ready configurable generalist agent." *IBM Research Blog*, October 15, 2025. Available at: https://research.ibm.com/blog/cuga-agent-framework

- CUGA Project. "CUGA Agent Framework." *GitHub Repository*. Available at: https://github.com/cuga-project/cuga-agent

- LangChain. "Deep Agents overview." *LangChain Documentation*. Available at: https://docs.langchain.com/oss/python/deepagents/overview
