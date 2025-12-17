# Context Engineering

## Introduction

Context engineering is the discipline of strategically managing what information appears in the LLM's context window to optimize performance, cost, and reasoning quality.
Just as software engineers optimize memory usage and database queries, context engineers optimize the finite context window—the maximum number of tokens an LLM can process in a single interaction.
The context window represents a fundamental constraint of LLM-based agents.

Unlike human memory, which can recall vast amounts of information, LLMs operate within hard token limits (typically 32K to 1M+ tokens depending on the model). As agents tackle complex, multi-step tasks, they accumulate conversation history, tool results, and intermediate reasoning that can quickly exhaust available context. Without effective context engineering, agents hit hard limits, suffer performance degradation, incur excessive costs, and lose critical information.

This chapter provides a high-level overview of context engineering as a domain. We'll explore the fundamental challenges, key concepts, and the patterns available for managing context effectively. For specific implementation patterns, see the pattern modules referenced throughout this chapter.

> **"Prompt engineering is dead; it has become context engineering."** — Andrej Karpathy

## The Fundamental Challenge

The finite context window creates a fundamental tension: agents need comprehensive information to reason effectively, but must balance this against the constraints of token limits, processing costs, and performance degradation.
This challenge manifests in several ways:

### Token Limits and Hard Boundaries

Every LLM has a maximum context window size—a hard limit on the number of tokens it can process. Exceeding this limit causes errors, truncation, or complete failure. As agents execute multi-step tasks, they accumulate:
- **Conversation history:** Messages from previous turns
- **Tool results:** Outputs from API calls, file operations, code execution
- **Intermediate reasoning:** Thinking blocks, reflections, and planning steps
- **System instructions:** Prompts, tool definitions, and guidelines

Without management, these accumulate until the context window is exhausted.

### The "Lost in the Middle" Problem

Research shows that LLMs have reduced attention to information in the middle of long contexts. Important information placed at the beginning or end receives more attention than information in the middle. This creates challenges for:
- **Long conversations:** Critical early context may be "lost" as conversations extend
- **Complex plans:** High-level goals defined early may be forgotten during execution
- **Multi-step tasks:** Intermediate results may be forgotten in later steps

Context engineering addresses this through strategic positioning and attention manipulation techniques.

### Cost and Performance Impact

Large contexts are expensive to process. Every token in the context window consumes computational resources, directly impacting:
- **API costs:** More tokens = higher costs per request
- **Latency:** Longer contexts = slower processing times
- **Reasoning quality:** Overly long contexts can degrade model performance and focus

Effective context engineering optimizes all three dimensions simultaneously.

### KV-Cache Efficiency

Modern LLM inference uses Key-Value (KV) caches to optimize repeated processing of the same prompt prefix. When the prompt prefix changes (even by a single token), the cache is invalidated, dramatically increasing latency and cost. Context engineering strategies that maintain stable, append-only context structures maximize KV-cache reuse, directly improving performance.

### Context Rot: The Effective Context Window

A critical but often overlooked challenge is **Context Rot**—the phenomenon where an LLM's performance degrades as the context window fills up, even if the total token count is well within the technical limit. For example, a model may advertise a 1 million token context window, but its **effective context window**—where the model performs at high quality—is often much smaller.

> **"Anything beyond ~200k tokens leads to *context rot* — the model forgets what matters."** — Manus Creators

**Current Reality:** As of 2025, most models have effective context windows of less than 256k tokens, even when they technically support much larger limits. The "effective context window" is the real constraint, not the advertised technical limit.

This means agents must be designed to operate efficiently well below the technical token limit to maintain reasoning quality. Context engineering strategies must address Context Rot proactively, not just react to hard token limits.

#### Mitigation Strategies: Compaction vs Summarization

Context reduction is essential to prevent Context Rot. Two distinct methods have emerged as standards, with **reversibility** prioritized over compression:

**Context Compaction (Reversible):**

Context compaction strips out information that is redundant because it exists in the environment. The key feature is reversibility: if the agent needs to access the information later, it can use a tool to retrieve it.

- **Example:** If an agent writes a 500-line code file, the chat history should not contain the entire file content. Instead, it should only contain a lightweight reference like `Output saved to /src/main.py`. If the agent needs to read or modify the file later, it can use a `read_file` tool.

- **When to use:** For information that exists in external systems (files, databases, APIs) and can be retrieved on-demand.

**Summarization (Lossy):**

Summarization uses an LLM to condense conversation history, including tool calls and messages. This is typically triggered at a Context Rot threshold (e.g., 128k tokens). When summarizing, keep the most recent tool calls in their raw, full-detail format to maintain the model's "rhythm" and formatting style.

- **Example:** If context exceeds 128k tokens, summarize the oldest 20 turns using a structured JSON format, while keeping the last 3 turns completely raw to preserve the model's momentum and prevent output quality degradation.

- **When to use:** For conversation history that cannot be externalized and must remain in context.

**Strategy Preference:**

The preferred approach follows this hierarchy: **Raw > Compaction > Summarization**. Only use summarization when compaction no longer yields enough space. This ensures maximum information retention and minimal information loss.

**Pre-Rot Threshold Monitoring:**

Don't wait for the API to throw an error. Define a "pre-rot threshold"—if a model has a 1M token context window, performance often degrades around 256k tokens. Monitor token count and implement compaction or summarization cycles before hitting the "rot" zone to maintain reasoning quality. This proactive approach prevents performance degradation rather than reacting to failures.

## Core Concepts in Context Engineering

Context engineering encompasses several key concepts and techniques:

### Externalization

The most powerful context engineering technique is **externalization**—offloading large or long-term information to persistent storage (filesystem, database) rather than keeping it in the context window. This enables:
- **Unlimited storage:** Information beyond context limits
- **Restorable compression:** Maintaining references (paths, URLs, keys) for on-demand retrieval
- **Just-in-time access:** Retrieving only relevant portions when needed

Externalization is covered in detail in the **Pattern: Filesystem as Context** module (in the Memory part).

### Compression Strategies

For information that must remain in context, compression techniques reduce token usage while preserving essential information:
- **Context Compaction (Reversible):** Removing redundant information that exists in the environment, maintaining references for on-demand retrieval
- **Summarization (Lossy):** Using LLMs to condense conversation history or documents into compact representations while preserving recent context in raw format
- **Pruning:** Removing or truncating less critical information
- **Selective retention:** Keeping only the most relevant or recent content

### Automatic Context Management

Automatic techniques manage context size without manual intervention:
- **Server-side editing:** API-level clearing of tool results, thinking blocks, or old messages
- **Client-side compaction:** SDK-based summarization that replaces full history with structured summaries
- **Threshold-based triggers:** Automatic management when context exceeds configured limits

### Attention Manipulation

Strategic positioning of important information to bias model attention:
- **Recency bias:** Placing critical information at the end of context
- **Recitation:** Actively bringing important plans or goals back into context
- **Stable prefixes:** Maintaining consistent prompt structures for KV-cache optimization

### Metadata vs. Values

Separating metadata (what exists) from full values (the actual data) enables agents to maintain awareness of execution state without consuming excessive tokens. This pattern is covered in **Pattern: Variables Manager**.

## Patterns in This Part

This part of the book covers specific patterns for context engineering:

### Pattern: Attention Engineering

**Attention Engineering** is a specialized prompt design pattern focused on manipulating where and how information appears in an AI model's context to deliberately steer the model's focus. It exploits the model's inherent attention biases (primacy and recency) by strategically positioning critical information at optimal locations in the prompt. This pattern directly addresses the "lost in the middle" problem by ensuring important information receives adequate attention regardless of context length.

**When to use:** Building agents that process long contexts (10K+ tokens), need to ensure critical instructions are reliably followed, or must maintain focus on important information across extended conversations or multi-step tasks.

### Pattern: Context Editing

**Context Editing** provides automatic, hands-off management of conversation context as it grows. It automatically removes or compresses less critical content (tool results, thinking blocks, old messages) to stay within token limits and optimize costs. This pattern operates either server-side (API-level clearing) or client-side (SDK compaction), requiring minimal configuration and operating transparently.

**When to use:** Long-running agents that accumulate extensive conversation history, tool-heavy workflows, or when you want automatic, set-and-forget context management.

### Pattern: Variables Manager

**Variables Manager** maintains a centralized registry of execution variables with rich metadata while providing context-efficient summaries. Instead of passing full values through context, agents work with variable references and retrieve full values only when needed. This pattern separates metadata from values, enabling agents to maintain awareness of execution state through lightweight summaries.

**When to use:** Multi-step workflows with large intermediate values, code execution agents, or multi-agent systems requiring shared state tracking.

## Relationship to Memory Patterns

Context engineering is closely related to memory management, but focuses specifically on optimizing the **short-term memory** (context window) rather than long-term persistent storage. The **Memory** part of this book covers:

- **Memory Management:** Conceptual overview of short-term vs. long-term memory
- **Pattern: Filesystem as Context:** Externalization technique for offloading large data
- **Pattern: Recitation:** Attention manipulation through persistent plan maintenance
- **Pattern: RAG:** Knowledge retrieval for long-term memory

Context engineering patterns work together with memory patterns: externalize large data first (Filesystem as Context), then optimize what remains in context (Context Editing, Variables Manager).

## Key Context Engineering Strategies

Effective context engineering uses a layered approach:

### 1. Externalize First

The most effective strategy is to externalize large data before it enters context. Offload tool results, large documents, or intermediate computations to persistent storage, keeping only lightweight references in context.

### 2. Compress What Remains

For information that must stay in context, use compression techniques:
- Summarize old conversation history
- Prune less critical information
- Use automatic context editing for tool results

### 3. Manipulate Attention

Strategically position important information:
- Place critical plans or goals at the end of context (recency bias)
- Use recitation to actively bring important information back into focus
- Maintain stable context prefixes for KV-cache optimization

### 4. Separate Metadata from Values

Use metadata summaries to maintain awareness without full values:
- Track variable existence and characteristics without including full data
- Retrieve full values only when explicitly needed
- Use structured summaries for observability

## Common Challenges and Solutions

### Challenge: Context Rot (Performance Degradation Before Token Limits)

**Solution:** Define pre-rot thresholds and implement proactive context reduction. Use Context Compaction for reversible reduction (externalizing to filesystem), then Summarization for lossy compression when compaction is insufficient. Monitor token counts and trigger reduction cycles before hitting effective context window limits.

### Challenge: Context Growing Over Time

**Solution:** Implement automatic context editing with threshold-based triggers. Use server-side clearing for tool results or client-side compaction for full history replacement. Combine with externalization strategies to prevent accumulation.

### Challenge: Large Tool Results

**Solution:** Externalize tool results to filesystem before they enter context. Keep only file paths or summaries in context, retrieving full results on-demand.

### Challenge: Maintaining Goal Awareness

**Solution:** Use recitation patterns to actively bring high-level plans back into context. Maintain persistent plan files that are read at each step.

### Challenge: Variable Tracking Across Steps

**Solution:** Use Variables Manager pattern to track execution state through metadata summaries, retrieving full values only when needed.

### Challenge: KV-Cache Invalidation

**Solution:** Maintain stable, append-only context structures. Keep tool definitions and system instructions fixed, appending new content rather than modifying prefixes.

## What's Missing?

While this part covers essential context engineering patterns, several areas represent opportunities for future patterns or deeper exploration:

### Stable, Append-Only Context

While mentioned throughout the book, **Stable, Append-Only Context** is not yet a standalone pattern. This concept involves maintaining consistent prompt prefixes to maximize KV-cache reuse. A dedicated pattern could provide:
- Techniques for structuring stable prefixes
- Strategies for append-only message management
- KV-cache optimization guidelines
- Framework-specific implementations

### Context Window Optimization

A pattern focused specifically on **optimizing context window usage** could cover:
- Token counting and monitoring strategies
- Context window sizing decisions
- Performance profiling and optimization
- Cost analysis and trade-offs

### Attention Engineering

**Attention Engineering** is now a dedicated pattern in this part, providing:
- Systematic approaches to information positioning
- Recency bias exploitation techniques
- Attention scoring and prioritization
- Multi-layer attention strategies

### Context Composition

A pattern for **composing context from multiple sources** could address:
- Strategies for combining external memory with context
- Balancing retrieved information with conversation history
- Context prioritization and ordering
- Multi-source context integration

## Integration with Other Capabilities

Context engineering integrates with other agent capabilities:

- **Tool Use:** Context engineering manages tool results and tool definitions efficiently
- **Reasoning Techniques:** Optimized context improves reasoning quality and focus
- **Planning:** Context engineering maintains plan visibility through recitation and attention manipulation
- **Memory Management:** Context engineering optimizes short-term memory while memory patterns handle long-term storage
- **Multi-Agent Systems:** Context engineering enables orchestrators to manage subagent outputs efficiently

## Key Insights

1. **Context engineering is essential:** Agents operating over time or handling complex tasks require sophisticated context management. Without it, they cannot scale to handle real-world complexity.

2. **Externalization is the most powerful technique:** Offloading large data to persistent storage enables unlimited information handling while keeping contexts focused and efficient.

3. **Layered strategies work best:** Combine externalization (first), compression (second), and attention manipulation (third) for optimal results.

4. **Automatic management enables scale:** Context editing provides hands-off management for production systems, while manual techniques provide fine-grained control.

5. **Metadata separation improves efficiency:** Tracking what exists without including full values enables awareness without token bloat.

6. **KV-cache optimization matters:** Maintaining stable, append-only context structures directly improves latency and reduces costs.

7. **The effective context window is the real constraint:** Context Rot occurs well before technical token limits. Design agents to operate efficiently below advertised limits to maintain reasoning quality.

8. **Reversibility over compression:** Prefer Context Compaction (reversible) over Summarization (lossy) when possible. Only compress when externalization is not feasible.

## Best Practices

Based on lessons learned from building production agent systems (Manus, LangChain, and others), here are key best practices for context engineering:

### Don't Train Your Own Models (Yet)

We are living the "Bitter Lesson" era. The harness you build today will likely be obsolete when the next frontier model drops. If you spend weeks fine-tuning models or training RL policies on specific action spaces, you lock yourself into a local optimum. Instead, use Context Engineering as a flexible interface that adapts to rapidly improving models. Focus your engineering effort on context management, not model training.

### Define Pre-Rot Thresholds

Don't wait for API errors. Monitor token count and implement compaction or summarization cycles proactively. For models with 1M token limits, assume effective context of < 256k tokens. Set thresholds conservatively and trigger context reduction before hitting the rot zone.

### Security and Manual Confirmation

When giving agents browser or shell access, sandbox isolation isn't enough. Implement additional safeguards:
- Enforce rules that tokens not leave the sandbox
- Use human-in-the-loop interrupts for manual confirmation before proceeding with high-risk operations
- Validate all tool calls before execution in production environments

### The "Intern Test" for Evaluation

Static benchmarks like GAIA saturated quickly and didn't align with user satisfaction. Focus on tasks that are computationally verifiable:
- Did the code compile?
- Did the file exist after the command ran?
- Can the sub-agent verify the output of the parent?

Use binary success/fail metrics on real environments rather than subjective LLM-as-a-Judge scores. This provides more reliable feedback for system improvement.

### Embrace Iterative Refinement

Production agent systems evolve rapidly. Manus was rewritten five times in six months. LangChain re-architected Open Deep Research four times. This is normal and expected. As models get smarter, your harness should change accordingly. If your harness is getting more complex while models improve, you are likely over-engineering. Focus on simplification and removing unnecessary complexity.

### The Key Insight: Remove, Don't Add

The biggest performance gains in production systems didn't come from adding complex RAG pipelines or fancy routing logic. Gains came from **removing things**. As models get stronger, don't build more scaffolding—get out of the model's way. 

**Context Engineering is not about adding more context.** It's about finding the minimal effective context required for the next step. Every token should earn its place in the context window. If information can be retrieved on-demand, externalize it. If it's not immediately needed, don't include it.

This philosophy of minimal effective context leads to:
- Lower costs
- Faster processing
- Better reasoning quality
- More maintainable systems
- Easier adaptation to new models

## Next Steps

This chapter provided a high-level overview of context engineering as a domain. For detailed implementation guidance, see:

- **Pattern: Attention Engineering** - Strategic positioning of information to maximize model attention
- **Pattern: Context Editing** - Automatic management of conversation context
- **Pattern: Variables Manager** - Metadata-based variable tracking

For related patterns covering externalization and long-term memory, see the **Memory** part:

- **Pattern: Filesystem as Context** - Externalization technique for large data
- **Pattern: Recitation** - Attention manipulation through persistent plans
- **Memory Management** - Conceptual overview of memory types

Effective context engineering is essential for building production-ready agentic systems. Understanding these concepts and patterns will enable you to build agents that operate efficiently within context limits, maintain focus on critical information, and scale to handle complex, long-horizon tasks.

??? "References"

    - Context Engineering for AI Agents: Part 2 - https://www.philschmid.de/context-engineering-part-2
    - Context Engineering for AI Agents: Lessons from Building Manus
    - Manus AI Agent Harness learnings from Peak Ji
    - LangChain Open Deep Research re-architecture examples
