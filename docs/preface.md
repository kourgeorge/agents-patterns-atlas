# Preface

## Welcome to the Agentic Era

> **"We are entering a world where computers behave like people: browsing, clicking, copying, pasting, planning."** — Andrej Karpathy 


Welcome to **"Intelligence Patterns: An Evolving Handbook on Agentic Design"** - an interactive, breathing guide to building intelligent, goal-oriented AI systems. 
The last few years have witnessed an unprecedented transformation - from simple, reactive programs to sophisticated, autonomous entities capable of understanding context, making decisions, and interacting dynamically with their environment and other systems. 

As AI systems shift from **passive classifiers to active problem-solvers**, engineers face a critical challenge: building intelligent agents requires not just technical skills, but a deeper understanding of *how intelligence works*. 
Large language models (LLMs) augmented with tools, memory, and multi-step reasoning are increasingly deployed as agents capable of planning, acting, and coordinating with humans and other agents. Yet despite rapid progress, the field lacks a **shared conceptual framework** that provides AI agent engineers with a common language that revolves around the key components/mechanisms of intelligence.

The advent of powerful LLMs has provided unprecedented capabilities for understanding and generating human-like content, serving as the cognitive engine for many of these agents. 
However, orchestrating these capabilities into systems that can reliably achieve complex goals requires more than just a powerful model. 
It requires structure, design, and a thoughtful approach to how the agent perceives, plans, acts, and interacts, sometimes even grounded in an understanding of the fundamental principles of intelligence itself.

We argue that modern AI demands people who understand intelligence more than they understand code.
DeepSeek’s leadership consistently highlights that real progress in AI comes from grasping how reasoning, creativity, and cognition work — not from traditional programming expertise alone. 
Building truly smart systems requires minds trained to understand thinking itself, not just to write code.

This book is designed to be your practical guide through this transformation. 
It presents essential design patterns organized into comprehensive parts, covering everything from foundational workflow patterns to advanced multi-agent architectures, memory management, and production-ready safety mechanisms. Each pattern is battle-tested, clearly explained, and accompanied by practical code examples you can run, modify, and learn from.

More importantly, this book provides AI agent engineers with a **shared conceptual language**, enabling you to build intelligent problem solvers with a common understanding of how intelligence works. By grounding agent design in cognitive principles, this framework helps engineers understand the limits of intelligence—from working memory constraints and cognitive load to executive control bottlenecks—while inspiring effective solutions that map naturally onto existing agentic architectures.


## What Are Agentic Systems?

> **"Agents are software 3.0 — programs that you don't write, but steer."** — Andrej Karpathy

At its core, an agentic system is a computational entity designed to perceive its environment (both digital and potentially physical), make informed decisions based on those perceptions and a set of predefined or learned goals, and execute actions to achieve those goals autonomously. 
Unlike traditional software, which follows rigid, step-by-step instructions, agents exhibit a degree of flexibility and initiative.

This shift represents a **fundamental transition in software engineering**: from building systems that manage data flow to building systems that **embody intelligence**. 
Building systems that must themselves decompose general problems, intelligently select solvers for subproblems, and synchronize cognitive states across multiple reasoning steps represents a fundemental different class of engineering problem than coordinating data pipelines or distributed processes. 
It introduces novel challenges directly related to the limits of LLMs—challenges that traditional software engineering never faced. Effective context engineering, for instance, was not a problem in traditional software engineering.


Imagine you need a system to manage customer inquiries. A traditional system might follow a fixed script. 
An agentic system, however, could perceive the nuances of a customer's query, access knowledge bases, interact with other internal systems (like order management), potentially ask clarifying questions, and proactively resolve the issue, perhaps even anticipating future needs. 

Agentic systems are characterized by autonomy, allowing them to act without constant human oversight; proactiveness, initiating actions towards their goals; and reactiveness, responding effectively to changes in their environment. They are fundamentally goal-oriented, constantly working towards objectives. A critical capability is tool use, enabling them to interact with external APIs, databases, or services. They possess memory, retain information across interactions, and can engage in communication with users, other systems, or even other agents.

Effectively realizing these characteristics introduces significant complexity. How does the agent maintain state across multiple steps? How does it decide when and how to use a tool? How is communication between different agents managed? How do you build resilience into the system to handle unexpected outcomes or errors? These are precisely the kinds of questions that cognitive science has been studying for decades, and engineers building agentic systems can now benefit from this accumulated wisdom.

### Generative AI
* **Flow:** `Prompt -> LLM -> Response`
* **Nature:** Passive, one-shot, content-focused.
* **Role:** The human drives the process. The human must verify the output and perform the subsequent action. The model is a fancy autocomplete engine.

### Agentic AI
* **Flow:** `Goal -> Agent (Think -> Act -> Observe Loop) -> Environment -> Goal Achieved`
* **Nature:** Active, iterative, goal-focused.
* **Role:** The agent drives the process. It acts as a collaborator or an employee. It doesn't just answer a question; it navigates a problem space, corrects its own errors, and interacts with external software.

> **"Stateless models can't build relationships — agents can."** — Andrej Karpathy


![Agentic Systems Overview](img1.png)



## Why Patterns Matter in Agent Development

This complexity is precisely why agentic design patterns are indispensable. 
They are not rigid rules, but rather battle-tested templates or blueprints that offer proven approaches to standard design and implementation challenges in the agentic domain. 
By recognizing and applying these design patterns, you gain access to solutions that enhance the structure, maintainability, reliability, and efficiency of the agents you build.


A great question we often hear is: "With AI changing so fast, why write a book that could be quickly outdated?" Our motivation is actually the opposite. 
It's precisely because things are moving so quickly that we need to step back and identify the underlying principles that are solidifying. 
Patterns like RAG, Reflection, Routing, Memory Management, Multi-Agent Coordination, and the others we discuss are becoming fundamental building blocks. More importantly, the cognitive principles underlying these patterns—how working memory works, how attention is allocated, how complex problems are decomposed—these are universal principles of intelligence that transcend specific technologies. 
This book is an invitation to reflect on these core ideas, which provide the foundation we need to build upon. 

## A Perspective on Intelligence

This book approaches the challenge of building intelligent systems from a unique perspective: we strive to understand the mechanisms of building intelligence from the *intelligence* point of view, not merely from the artificial or technical point of view. 
The patterns presented here are not just solutions to transient technical problems—they are solutions that solve fundamental problems of intelligence itself. 
These patterns can inspire us to understand how natural intelligence works, revealing principles that apply equally to biological and artificial minds.
We believe that the most effective agentic systems emerge when engineers understand not just *how* to implement a pattern, but *why* it works from a cognitive perspective.

Throughout this book, you will encounter insights and sayings from pioneers who built agents early in this new era.
Researchers and engineers from organizations like Anthropic, LangChain/LangGraph, Manus, and others who shaped the field. 
These perspectives are included not as decoration, but because they inspire deeper understanding and allow us to see aspects of agentic design from interesting and illuminating angles. 
These voices help us understand both the technical challenges and the deeper questions about intelligence that we are collectively exploring.

