![Book Banner](banner.png)

> **"We are entering a world where computers behave like people: browsing, clicking, copying, pasting, planning."** — Andrej Karpathy 

Agentic AI systems face a fundamental challenge when dealing with **long horizon tasks**-those complex objectives that require agents to plan and execute extended sequences of actions to achieve desired results. 
Unlike simple, single-step interactions, these tasks demand sophisticated coordination across multiple reasoning steps, planning phases, and action executions.

Early examples of long horizon agents that require multiple coordinated steps have emerged in the form of *"deep research agents"*, implemented by major LLM providers such as ChatGPT and Claude. 
These systems demonstrate the power of structured agentic approaches when tackling complex research tasks that span multiple queries, information retrieval steps, analysis phases, and synthesis operations.

However, the need for structured agentic design extends far beyond research applications. 
Many real-world tasks—from software development and data analysis to content creation and system administration—require agents to orchestrate long chains of planning, reasoning, and action steps. 
These agents demand architectural patterns and design structures that can support and coordinate such complex operational sequences.

Current ReAct-style agents, which rely primarily on local, step-by-step decision making, often struggle with such long horizon problems. 
While effective for straightforward tasks, their reactive nature limits their ability to maintain coherent long-term strategies, manage complex dependencies between actions, and effectively consolidate information across extended execution trajectories. 
This limitation becomes particularly evident when tasks require:

- Multi-step planning and reasoning chains
- Coordinated execution across multiple tools and resources
- Context management over extended sequences
- Integration and synthesis of intermediate results

To address these challenges, there is a critical need for **organizing the operational process** of agents. 
The intelligence design patterns presented in this book provide structured solutions to systematically organize the thinking, planning, execution, and consolidation phases of long horizon trajectories. 

The patterns in this book directly address the fundamental limitations of reasoning in LLMs and, more broadly, in artificial intelligence systems. 
By providing systematic approaches to organizing agent behavior, these patterns enable more reliable, coherent, and effective long horizon task execution. They transform agents from reactive systems that make isolated decisions into structured systems capable of sustained, goal-directed behavior across extended operational sequences.

> **"Building smart systems requires minds trained to understand thinking itself—how minds process information, how teams coordinate work, and how organizations scale intelligence."** - The Author

---

## Book Origins and Evolution

This book originated from study notes compiled to organize and refine understanding of the agentic AI domain. 
These design patterns have been collected from a growing corpus of literature on agentic systems, including engineering blogs from leading AI companies like Anthropic, Manus, and LangChain, insights from active developer bloggers, and an increasing number of academic publications and books. 
In addition, many patterns in this book were extracted directly from implementations of deep agents like IBM's CUGA (Configurable Generalist Agent) and LangChain's Deep Agents.

This book is a living resource that will be constantly updated as new design patterns and best practices emerge in the field of agentic AI development. 
As the community continues to build and refine agentic systems, new patterns will be identified, existing patterns will be refined, and our understanding of what works best will evolve. 
We encourage readers to revisit this resource regularly to stay current with the latest developments in software agent development. 
Whether you're returning after a few months or checking in periodically, you'll find that the content continues to grow and improve, reflecting the ongoing maturation of the agentic AI ecosystem.

---

## Book Structure

The book is organized into **7 parts** containing **32 modules**, building concepts progressively from foundational patterns to advanced multi-agent architectures:

1. **Introduction & Foundations** (4 modules) - Core concepts, context, and design pattern fundamentals
2. **Core Workflow** (4 modules) - Fundamental patterns for building agent workflows
3. **Tools** (4 modules) - Designing the Agent-Computer Interface
4. **Reasoning & Planning** (5 modules) - Enabling agents to plan and reason effectively
5. **Context and Memory** (8 modules) - Managing the finite context window, optimizing context usage, and managing persistent and external memory for agents, including knowledge retrieval
6. **Multi-Agent Systems** (5 modules) - Modern LLM-based multi-agent collaboration patterns
7. **Human Input and Recovery** (3 modules) - Learning, adaptation, and human interaction

The book parts and patterns are organized to build concepts progressively, but you can also use this book as a reference, jumping to patterns that address specific challenges you face in your agent development projects.

---

## Contact and Feedback

If you encounter any issues, have suggestions for improvement, or notice any errors, we would greatly appreciate your feedback. Please contact the author at **kourgeorge@gmail.com**. Your input helps us maintain and improve the quality of this resource for the entire community.

---

## How to Use This Book

Throughout this book, the emphasis is on practical application. Every pattern includes runnable code examples that you can execute, modify, and learn from. We encourage you to:

* **Run the examples** - Don't just read them; execute them and see how they work
* **Experiment** - Modify the code, try different inputs, break things and fix them
* **Adapt** - Use the patterns as starting points for your own applications
* **Build** - Apply patterns to real problems you're trying to solve

The code examples are designed to clearly illustrate each pattern's core logic and its implementation, focusing on clarity and practicality over production-ready complexity.

### For Beginners

If you're new to agentic systems, we recommend reading the modules sequentially. The book is structured to build concepts progressively:

- Start with understanding what agents are and how they differ from workflows
- Learn foundational workflow patterns before moving to advanced capabilities
- Understand single-agent patterns before exploring multi-agent systems

### For Experienced Developers

If you're already familiar with agentic systems, you can use this book as a reference guide:
- Jump directly to patterns that solve specific problems you're facing
- Use the "When to Use" sections in each pattern module to quickly identify relevant solutions
- Explore advanced patterns like multi-agent coordination or context engineering when needed

Each pattern module follows a consistent structure:

- **Pattern Overview:** What the pattern is and why it matters
- **When to Use:** Guidance on recognizing when this pattern applies
- **Practical Applications:** Real-world use cases
- **Implementation:** Code examples showing how to realize the pattern
- **Key Takeaways:** Summary of the pattern's core concepts

---

## How to Cite This Book

Kour, G. (2025). *Intelligence Patterns: Reusable Elements of Agentic Design*. 

### BibTeX

```bibtex
@book{kour2025intelligence,
  title={Intelligence Patterns: Reusable Elements of Agentic Design},
  author={Kour, George},
  year={2025},
  note={Living resource, continuously updated}
}
```

**Note:** Since this is a living resource that is continuously updated, please include the date you accessed the material in your citation. 
For specific patterns or sections, consider referencing the relevant module or pattern name in addition to the book citation.

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
