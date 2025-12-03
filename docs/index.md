# About This Book

This interactive book is a comprehensive guide to building intelligent, goal-oriented AI systems. As we transition from the era of Generative AI—where models simply respond to prompts—to the era of Agentic AI—where systems actively pursue objectives and interact with their environment—developers need practical patterns and principles to construct reliable, scalable agentic systems. This book provides exactly that: a hands-on collection of **30+ essential design patterns** that cover everything from foundational workflow patterns like prompt chaining and routing, to advanced capabilities such as multi-agent collaboration, memory management, and safety mechanisms.

Each pattern is presented with clear explanations, practical guidelines for when to use it, and real-world examples that demonstrate how to implement these concepts in production systems. Whether you're building simple single-agent workflows or complex multi-agent architectures, this book serves as both a reference guide and a practical handbook for navigating the rapidly evolving landscape of agentic AI development.

## Book Structure

The book is organized into **10 parts** containing **34 modules**:

1. **Introduction & Foundations** (4 modules) - Core concepts, context, and design pattern fundamentals
2. **Core Workflow** (4 modules) - Fundamental patterns for building agent workflows
3. **Tool Use** (4 modules) - Designing the Agent-Computer Interface
4. **Reasoning & Planning** (3 modules) - Enabling agents to plan and reason effectively
5. **Memory** (3 modules) - Managing persistent and external memory for agents
6. **Context Management** (3 modules) - Managing the finite context window and optimizing context usage
7. **Multi-Agent Systems** (2 modules) - Scaling up with multiple agents working together
8. **Advanced Capabilities** (5 modules) - Learning, protocols, goal management, and human interaction
9. **Knowledge & Communication** (2 modules) - Retrieving knowledge and enabling agent communication
10. **Optimization & Safety** (4 modules) - Optimizing performance and ensuring safe operation

The patterns are organized to build concepts progressively, but you can also use this book as a reference, jumping to patterns that address specific challenges you face in your agent development projects.

### Pattern Organization by Part

**Part 1: Introduction & Foundations**
- About - Attribution, source information, and details about this adaptation
- Preface - High-level introduction to the agentic era and the book's purpose
- Introduction - Foundations and core concepts of agentic systems
- What is an Agentic Design Pattern? - Understanding design patterns in the agentic context

**Part 2: Core Workflow**
- Pattern: Prompt Chaining (Pipeline Pattern) - Sequential, manageable workflows
- Pattern: Routing - Dynamic decision-making and conditional logic
- Pattern: Parallelization - Concurrent execution for efficiency
- Pattern: Reflection - Self-evaluation and iterative improvement

**Part 3: Tool Use**
- Pattern: Tool Use - Designing the Agent-Computer Interface (ACI)
- Pattern: Constrained Tool Use - Managing tool availability through programmatic constraints
- Pattern: The SKILL.md Pattern - Organizing specialized agent capabilities using SKILL.md files
- Pattern: Shortlisting - Analyzing large sets of available tools to select the most relevant subset

**Part 4: Reasoning & Planning**
- Reasoning Techniques - Chain-of-Thought, ReAct Loops, and Tree-of-Thought strategies
- Pattern: Planning - Strategic goal decomposition and structured planning
- Pattern: Prioritization - Task assessment and ranking

**Part 5: Memory**
- Memory Management - Overview of memory types and strategies for agents, including persistent memory and external storage
- Pattern: Recitation - Maintaining goal alignment in long-horizon tasks through persistent plans
- Pattern: Filesystem as Context - Treating external persistent storage as unlimited extension of working memory

**Part 6: Context Management**
- Pattern: Context Compression - Techniques for fitting information into the finite context window
- Pattern: Context Editing - Automatically managing conversation context as it grows
- Pattern: Variables Manager - Centralized registry for tracking execution variables with rich metadata

**Part 7: Multi-Agent Systems**
- Multi-Agent Architectures - Orchestrator-Workers, Evaluator-Optimizers, and Swarm patterns
- Pattern: Orchestrator-Worker (Coordinator) - Central coordination of specialized workers

**Part 8: Advanced Capabilities**
- Learning and Adaptation - Continuous improvement through experience
- Model Context Protocol (MCP) - Standardized protocol for tool and data access
- Goal Setting and Monitoring - Establishing objectives and tracking progress
- Pattern: Exception Handling and Recovery - Robust error handling mechanisms
- Pattern: Human-in-the-Loop - Integrating human oversight and feedback

**Part 9: Knowledge & Communication**
- Pattern: Knowledge Retrieval (RAG) - Accessing external knowledge bases
- Pattern: Inter-Agent Communication (A2A) - Agent-to-agent coordination protocols

**Part 10: Optimization & Safety**
- Resource-Aware Optimization - Efficiency and cost management
- Guardrails/Safety Patterns - Safety mechanisms and compliance
- Evaluation and Monitoring - Performance assessment and anomaly detection
- Exploration and Discovery - Novel solution finding and unknown discovery

### Each Pattern Module Includes

* **Pattern Overview** - What it is, when to use it, and why it matters
* **When to Use This Pattern** - Decision criteria with ✅/❌ guidelines
* **Practical Applications & Use Cases** - Real-world scenarios and applications
* **Implementation** - Hands-on code examples demonstrating the pattern
* **Key Takeaways** - Summary of crucial points and best practices
* **Related Patterns** - Connections to other patterns and how they work together
* **References** - Resources for further exploration and deeper learning

### Frameworks Used

Throughout this book, we demonstrate patterns using prominent frameworks:

* **LangChain & LangGraph** - Flexible chaining and stateful graph-based agent construction
* **Google ADK (Agent Development Kit)** - Tools and components for building, evaluating, and deploying agents
* **Crew AI** - Structured framework for orchestrating multiple AI agents

These frameworks represent different approaches to the agent development "canvas," each with its strengths. By showing examples across these tools, you'll gain a broader understanding of how patterns can be applied regardless of your chosen technical environment.

## How to Use This Book

This book is crafted to be a practical and accessible resource. Its primary focus is on clearly explaining each agentic pattern and providing concrete, runnable code examples to demonstrate its implementation.

### For Beginners

Start with **Part 1: Introduction & Foundations** to understand the core concepts and context. Then work through **Part 2: Core Workflow** in order. These build upon each other and establish fundamental concepts. Practice with the code examples to build understanding. Don't rush—take time to experiment with each pattern before moving to the next. As you progress, explore **Part 3: Tool Use** and **Part 4: Reasoning & Planning** to build more sophisticated capabilities.

### For Experienced Developers

Use this as a reference guide. Jump to patterns that address your specific challenges. Each module is self-contained, though cross-references help you understand relationships. Read the Pattern Overview and Key Takeaways for quick understanding, then dive into Implementation sections when you need to build something. The modular structure allows you to quickly find relevant patterns for your current project needs.

### For Teams

Use patterns as a common language for discussing agent architecture. Reference specific patterns when designing systems to ensure consistent approaches across your organization. This shared vocabulary will improve communication and reduce misunderstandings about system design.

### For Learning

Read the Pattern Overview and Key Takeaways for quick understanding. Dive into Implementation sections when you need to build something. Review Related Patterns to understand how patterns work together. We strongly encourage you to run the code examples, experiment with them, and adapt them to build your own intelligent systems.

### Reading Strategies

* **Sequential Reading:** Follow the module order to build concepts progressively
* **Reference Reading:** Jump to specific patterns when you encounter challenges
* **Deep Dive:** Focus on Implementation sections when you need to build
* **Quick Scan:** Read Pattern Overview and Key Takeaways for rapid understanding

## The Emphasis on Practical Application

Throughout this book, the emphasis is on practical application. Every pattern includes runnable code examples that you can execute, modify, and learn from. We encourage you to:

* **Run the examples** - Don't just read them; execute them and see how they work
* **Experiment** - Modify the code, try different inputs, break things and fix them
* **Adapt** - Use the patterns as starting points for your own applications
* **Build** - Apply patterns to real problems you're trying to solve

The code examples are designed to clearly illustrate each pattern's core logic and its implementation, focusing on clarity and practicality over production-ready complexity.

## What You'll Gain

By the end of this book, you will:

* Understand the fundamental concepts behind 30+ essential agentic design patterns
* Possess practical knowledge and code examples to apply them effectively
* Have a common language for discussing agent architecture with your team
* Be able to build more intelligent, capable, and autonomous systems
* Understand when to use each pattern and when to avoid it
* Know how patterns work together to create sophisticated agentic systems
* Master the progression from simple workflows to complex multi-agent architectures
* Learn to manage context, memory, and state effectively in agentic systems
* Gain expertise in safety, monitoring, and optimization for production deployments

## A Note on the Rapidly Evolving Landscape

The field of agentic AI is evolving at an extraordinary pace. New frameworks emerge, models improve, and techniques advance. However, the patterns in this book represent stable, foundational principles that transcend specific implementations. They are the architectural decisions and design approaches that will remain relevant even as specific technologies change.

Think of these patterns as the grammar of agentic systems—the fundamental structures that enable effective communication and problem-solving, regardless of the specific "words" (frameworks, models, tools) you choose to use.

## Let's Begin

This book is your guide to building intelligent, agentic systems. Whether you're just starting your journey into agentic AI or looking to deepen your understanding of proven patterns, we hope this resource empowers you to create systems that are robust, reliable, and effective.

The journey ahead is exciting. You're about to learn patterns that will enable you to build systems that can reason, plan, act, and collaborate. These are the building blocks of the next generation of AI applications.

Let's begin this hands-on journey into building intelligent, agentic systems!




## AI-Assisted Content Generation

In a fitting demonstration of the book's subject matter, much of this adaptation was created with the assistance of AI writing agents. This approach reflects the very principles and patterns discussed throughout the book—using intelligent agents to structure, organize, and present complex information.

The content has been carefully reviewed and validated by the authors to ensure accuracy and quality. However, given the collaborative nature of AI-assisted content creation, there may occasionally be errors, inconsistencies, or areas that could benefit from improvement.

If you encounter any issues, have suggestions for improvement, or notice any errors, we would greatly appreciate your feedback. Please contact the author at **kourgeorge@gmail.com**. Your input helps us maintain and improve the quality of this resource for the entire community.




## Bibliography

Much of the content in this book is based on **"Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems"** by **Antonio Gulli**, published by Springer.

**Source Reference:**
- **Book:** Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems
- **Author:** Antonio Gulli
- **Publisher:** Springer
- **ISBN:** 978-3032014018
- **Available at:** https://www.amazon.com/Agentic-Design-Patterns-Hands-Intelligent/dp/3032014018/

### Journal Articles

Liu, Yue, et al. "Agent Design Pattern Catalogue: A Collection of Architectural Patterns for Foundation Model Based Agents." *Journal of Systems and Software*, vol. 220, 2025, p. 112278. Available at: https://www.sciencedirect.com/science/article/pii/S0164121224003224

### Online Articles and Blog Posts

Ji, Yichao 'Peak'. "Context Engineering for AI Agents: Lessons from Building Manus." *Manus Blog*, July 18, 2025. Available at: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus

Huang, Nick. "How Agents Can Use Filesystems for Context Engineering." *LangChain Blog*, November 21, 2025. Available at: https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering/

Anthropic. "How We Built Our Multi-Agent Research System." *Anthropic Engineering Blog*, June 13, 2025. Available at: https://www.anthropic.com/engineering/multi-agent-research-system

Anthropic. "Building Effective AI Agents." *Anthropic Engineering Blog*, December 19, 2024. Available at: https://www.anthropic.com/engineering/building-effective-agents

Google Cloud. "Choose a Design Pattern for Your Agentic AI System." *Google Cloud Architecture Center*, 2025. Available at: https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system
