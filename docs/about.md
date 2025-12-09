# About This Book

## Intelligence Patterns: An Evolving Handbook on Agentic Design

This book is a comprehensive guide to building intelligent, goal-oriented AI agents. 
As we transition from the era of Generative AI—where models simply respond to prompts—to the era of Agentic AI—where systems actively pursue objectives and interact with their environment—developers need practical patterns and principles to construct reliable, scalable agentic systems. This book provides exactly that: a hands-on collection of **essential design patterns** that cover everything from foundational workflow patterns like prompt chaining and routing, to advanced capabilities such as multi-agent collaboration, memory management, and recovery mechanisms.

These design patterns have been collected from a growing corpus of literature on agentic systems. As agents transition from research laboratories into the hands of software developers, this increasing maturity has given rise to successful patterns and architectural ideas that are proving effective across diverse implementations. 
In addition, through careful analysis and dissection of real-world agent systems—including IBM's CUGA (Configurable Generalist Agent) and LangChain's Deep Agents—we've identified reusable patterns, design components, and principles that can be applied across different agentic systems. By examining how successful agent architectures are constructed, we've codified these best practices into transferable knowledge that can accelerate the development of new agentic applications.

Each pattern is presented with a motivation, clear explanations, practical guidelines for when to use it, and real-world examples that demonstrate how to implement these concepts in production systems. Whether you're building simple single-agent workflows or complex multi-agent architectures, this book serves as both a reference guide and a practical handbook for navigating the rapidly evolving landscape of agentic AI development.


The field of agentic AI is evolving at an extraordinary pace. New frameworks emerge, models improve, and techniques advance. However, the patterns in this book represent stable, foundational principles that transcend specific implementations. They are the architectural decisions and design approaches that will remain relevant even as specific technologies change.


This book is a living resource that will be constantly updated as new design patterns and best practices emerge in the field of agentic AI development. As the community continues to build and refine agentic systems, new patterns will be identified, existing patterns will be refined, and our understanding of what works best will evolve. We encourage readers to revisit this resource regularly to stay current with the latest developments in software agent development. Whether you're returning after a few months or checking in periodically, you'll find that the content continues to grow and improve, reflecting the ongoing maturation of the agentic AI ecosystem.

**George Kour, Ph.D.** 

## Book Structure

The book is organized into **8 parts** containing **29 modules**:

1. **Introduction & Foundations** (3 modules) - Core concepts, context, and design pattern fundamentals
2. **Core Workflow** (4 modules) - Fundamental patterns for building agent workflows
3. **Tools** (4 modules) - Designing the Agent-Computer Interface
4. **Reasoning & Planning** (3 modules) - Enabling agents to plan and reason effectively
5. **Context** (4 modules) - Managing the finite context window and optimizing context usage
6. **Memory** (4 modules) - Managing persistent and external memory for agents, including knowledge retrieval
7. **Multi-Agent Systems** (4 modules) - Scaling up with multiple agents working together
8. **Human input and Recovery** (3 modules) - Learning, adaptation, and human interaction

The patterns are organized to build concepts progressively, but you can also use this book as a reference, jumping to patterns that address specific challenges you face in your agent development projects.


## The Emphasis on Practical Application

Throughout this book, the emphasis is on practical application. Every pattern includes runnable code examples that you can execute, modify, and learn from. We encourage you to:

* **Run the examples** - Don't just read them; execute them and see how they work
* **Experiment** - Modify the code, try different inputs, break things and fix them
* **Adapt** - Use the patterns as starting points for your own applications
* **Build** - Apply patterns to real problems you're trying to solve

The code examples are designed to clearly illustrate each pattern's core logic and its implementation, focusing on clarity and practicality over production-ready complexity.


## The Creation Process: A New Paradigm for Book Writing

This book represents more than a collection of patterns—it embodies a new approach to knowledge creation itself. The writing process that produced this work demonstrates a fundamental shift in how books can be authored: not through traditional solitary writing, but through an orchestrated collaboration between human vision and AI capability.

### The Evolution of Writing

We are witnessing a remarkable transition in the craft of writing. AI systems have reached a point where they can produce prose that is not merely passable, but often clearer, more structured, and more comprehensive than what humans might produce alone. The mechanical task of writing—transforming ideas into well-formed sentences, organizing concepts into coherent sections, maintaining consistency across chapters—is increasingly becoming automated. This is not a replacement of human creativity, but rather its amplification.

### The Human Role: Editor-Director

In this new paradigm, the human author's role transforms from *writer* to *editor-director*. The primary responsibilities shift to higher-order tasks that require human judgment and vision:

**Defining Domain and Style**: The human establishes the intellectual territory, the voice, the tone, and the stylistic conventions that give the work its unique character. This is not something AI can determine—it requires deep understanding of audience, purpose, and personal vision.

**Curating and Collecting**: The human acts as a curator, identifying valuable insights from the web, research papers, blog posts, and other sources. This material is then presented to AI systems with instructions to incorporate, synthesize, and adapt it into the book's narrative.

**Asking the Right Questions**: Perhaps the most critical human skill is knowing what questions to ask. The human directs AI tools—whether code-writing assistants, deep research systems, or specialized content generators—by formulating precise, interesting, and strategically important questions that guide the content generation process.

**Validation and Refinement**: The human reads, evaluates, and iterates. Does the content align with the vision? Does it fit the intended style? Is the depth appropriate for the subject's importance? The human provides feedback, corrections, and refinements, steering the content generation toward an ever-more-perfect realization of the original vision.

**Structural Orchestration**: The human ensures coherence across the entire work—that chapters flow logically, that concepts build upon each other, that the length and depth of each section matches its significance in the overall narrative.

### The Collaborative Workflow

The creation process follows an iterative cycle: the human defines direction and collects materials, AI systems generate and organize content, the human validates and refines, and the cycle repeats. Each iteration brings the work closer to the human's vision while leveraging AI's ability to handle the mechanical aspects of writing at scale.

This approach allows for rapid exploration of ideas, comprehensive coverage of topics, and the ability to incorporate diverse sources efficiently. It enables the human to focus on what matters most: vision, judgment, and the creative direction that gives the work its unique value.

### A Fitting Demonstration

In a fitting demonstration of the book's subject matter, this creation process itself exemplifies the principles discussed throughout these pages—using intelligent agents to pursue objectives, orchestrating workflows, and leveraging tools to achieve goals that would be difficult or impossible through traditional means alone.

The content has been carefully reviewed and validated by the author to ensure accuracy, quality, and alignment with the intended vision. However, given the collaborative nature of this creation process, there may occasionally be errors, inconsistencies, or areas that could benefit from improvement.

If you encounter any issues, have suggestions for improvement, or notice any errors, we would greatly appreciate your feedback. Please contact the author at **kourgeorge@gmail.com**. Your input helps us maintain and improve the quality of this resource for the entire community.


## Let's Begin

This book is your guide to building intelligent, agentic systems. Whether you're just starting your journey into agentic AI or looking to deepen your understanding of proven patterns, we hope this resource empowers you to create systems that are robust, reliable, and effective.

The journey ahead is exciting. You're about to learn patterns that will enable you to build systems that can reason, plan, act, and collaborate. These are the building blocks of the next generation of AI applications.

Let's begin this hands-on journey into building intelligent, agentic systems!


## "Bibliography"

Each module in this book includes its own bibliography with references specific to that pattern or topic. This section collects the main sources that have informed the overall content and structure of the book.
Much of the content in this book is based on **"Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems"** by **Antonio Gulli**, published by Springer.

**Source Reference:**
- **Book:** Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems
- **Author:** Antonio Gulli
- **Publisher:** Springer
- **ISBN:** 978-3032014018
- **Available at:** https://www.amazon.com/Agentic-Design-Patterns-Hands-Intelligent/dp/3032014018/

### Journal Articles

Liu, Yue, et al. "Agent Design Pattern Catalogue: A Collection of Architectural Patterns for Foundation Model Based Agents." *Journal of Systems and Software*, vol. 220, 2025, p. 112278. Available at: https://www.sciencedirect.com/science/article/pii/S0164121224003224

### Preprints

Marreed, Sami, et al. "Towards enterprise-ready computer using generalist agent." *arXiv preprint arXiv:2503.01861* (2025). Available at: https://arxiv.org/abs/2503.01861

### Online Articles and Blog Posts

Ji, Yichao 'Peak'. "Context Engineering for AI Agents: Lessons from Building Manus." *Manus Blog*, July 18, 2025. Available at: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus

Huang, Nick. "How Agents Can Use Filesystems for Context Engineering." *LangChain Blog*, November 21, 2025. Available at: https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering/

Anthropic. "How We Built Our Multi-Agent Research System." *Anthropic Engineering Blog*, June 13, 2025. Available at: https://www.anthropic.com/engineering/multi-agent-research-system

Anthropic. "Building Effective AI Agents." *Anthropic Engineering Blog*, December 19, 2024. Available at: https://www.anthropic.com/engineering/building-effective-agents

Google Cloud. "Choose a Design Pattern for Your Agentic AI System." *Google Cloud Architecture Center*, 2025. Available at: https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system

IBM Research. "Introducing CUGA: The enterprise-ready configurable generalist agent." *IBM Research Blog*, October 15, 2025. Available at: https://research.ibm.com/blog/cuga-agent-framework

CUGA Project. "CUGA Agent Framework." *GitHub Repository*. Available at: https://github.com/cuga-project/cuga-agent

LangChain. "Deep Agents overview." *LangChain Documentation*. Available at: https://docs.langchain.com/oss/python/deepagents/overview
