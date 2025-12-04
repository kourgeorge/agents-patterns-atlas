# Context Engineering

## Introduction

Context engineering is the discipline of strategically managing what information appears in the LLM's context window to optimize performance, cost, and reasoning quality. Just as software engineers optimize memory usage and database queries, context engineers optimize the finite context window—the maximum number of tokens an LLM can process in a single interaction.

The context window represents a fundamental constraint of LLM-based agents. Unlike human memory, which can recall vast amounts of information, LLMs operate within hard token limits (typically 32K to 1M+ tokens depending on the model). As agents tackle complex, multi-step tasks, they accumulate conversation history, tool results, and intermediate reasoning that can quickly exhaust available context. Without effective context engineering, agents hit hard limits, suffer performance degradation, incur excessive costs, and lose critical information.

This chapter provides a high-level overview of context engineering as a domain. We'll explore the fundamental challenges, key concepts, and the patterns available for managing context effectively. For specific implementation patterns, see the pattern modules referenced throughout this chapter.

## The Fundamental Challenge

The finite context window creates a fundamental tension: agents need comprehensive information to reason effectively, but must balance this against the constraints of token limits, processing costs, and performance degradation. This challenge manifests in several ways:

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
- **Summarization:** Condensing conversation history or documents into compact representations
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

### Challenge: Context Growing Over Time

**Solution:** Implement automatic context editing with threshold-based triggers. Use server-side clearing for tool results or client-side compaction for full history replacement.

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
