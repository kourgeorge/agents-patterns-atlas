# Planning Strategies

## Introduction

Planning is fundamental to agent autonomy. 
When an agent receives a high-level goal like "research a topic, summarize findings, and share insights," it must determine how to achieve it—whether through explicit planning, reactive decision-making, or hybrid approaches. 
The choice of planning strategy significantly impacts agent performance, cost, and reliability.

This module explores the **strategic approaches to planning** in agentic systems—the tactical decisions about when, how, and to what depth agents should plan. 
Unlike design patterns that describe architectural solutions, strategies provide the specific methods and trade-offs for implementing planning in different contexts.

Planning strategies range from reactive approaches (planning one step at a time) to explicit planning (creating structured plans before execution), with various hybrid approaches in between. 
The choice depends on task complexity, uncertainty, resource constraints, and the need for global optimization.

Modern LLM agents employ various planning mechanisms. 
At the token level, Chain-of-Thought (CoT) prompting enables step-by-step reasoning, while Tree-of-Thought (ToT) explores multiple reasoning paths in parallel. 
ReAct-style agents interleave CoT reasoning with tool calls, but they plan only one step at a time—often overlooking long-term goals and incurring extra LLM calls for each tool use. By contrast, explicit planning frameworks generate structured plans before execution, then execute multiple steps without re-planning. 
This approach reduces latency and cost: generating one plan then executing multiple steps (rather than calling the LLM per tool) speeds up execution and forces the model to consider the entire task upfront.


> **"Agents hallucinate plans but execute real actions."** — Andrej Karpathy

## Planning Paradigms

### Reactive Planning (ReAct-style)

**What it is:** Planning one step at a time, interleaving reasoning with action. The agent reasons about the current state, decides the next action, executes it, observes results, and repeats.

**When to use:**
- Simple, short-horizon tasks
- Highly dynamic environments where plans become obsolete quickly
- Low-latency requirements where planning overhead is prohibitive
- Tasks where the solution path is unclear and must be discovered incrementally

**Characteristics:**
- Minimal upfront planning cost
- High adaptability to changing conditions
- Can get stuck in local decision loops
- Multiple LLM calls per task (one per action)

**Example:** A ReAct agent reasoning step-by-step: "I need to find information. I'll search for it. [Action: search] [Observation: results] Now I'll extract the key points. [Action: extract]..."

### Explicit Planning (Plan-then-Execute)

**What it is:** Creating a structured, multi-step plan before execution, then executing the plan sequentially or in parallel.

**When to use:**
- Complex, multi-step tasks requiring coordination
- Tasks where global optimization improves outcomes
- Long-horizon tasks where reactive approaches struggle
- When plan verification is important before execution

**Characteristics:**
- Single planning phase, then execution
- Enables global optimization of action sequences
- Lower total LLM calls (one plan, multiple executions)
- Less adaptable if conditions change during execution
- See **Task Decomposition** and **Planner-Checker** patterns for implementation

**Example:** A planner creates a DAG of subtasks: "1. Research topic, 2. Summarize findings, 3. Generate report, 4. Review and refine." Then an executor carries out each step.

### Hybrid Planning

**What it is:** Combining explicit planning with reactive adaptation. Create an initial plan, but allow reactive adjustments when conditions change.

**When to use:**
- Tasks requiring both structure and adaptability
- Environments with moderate uncertainty
- When initial planning is beneficial but conditions may change

**Characteristics:**
- Initial explicit plan provides structure
- Reactive adjustments handle unexpected situations
- Balances optimization with adaptability
- More complex to implement

**Example:** An agent creates a plan for a multi-step task, but when a step fails, it reactively adjusts the plan rather than failing entirely.

## Planning Horizons

### Short-Term Planning

**What it is:** Planning only the immediate next steps (1-3 actions ahead).

**When to use:**
- Highly dynamic environments
- Tasks where long-term planning is unreliable
- Real-time systems requiring immediate responses

**Trade-offs:**
- Fast decision-making
- Limited ability to optimize globally
- May miss long-term opportunities

### Long-Term Planning

**What it is:** Planning the entire task sequence from start to finish before execution.

**When to use:**
- Complex tasks requiring coordination
- When global optimization is critical
- Stable environments where plans remain valid

**Trade-offs:**
- Better global optimization
- Higher upfront cost
- Less adaptable to changes

### Hierarchical Planning

**What it is:** Planning at multiple levels of abstraction—high-level strategic goals broken into tactical steps, which are further broken into operational actions.

**When to use:**
- Very complex tasks spanning multiple levels
- Tasks requiring both strategic thinking and tactical execution
- Multi-agent systems where different agents handle different planning levels

**Example:**
- **Strategic Level:** "Complete research project"
- **Tactical Level:** "1. Literature review, 2. Data collection, 3. Analysis, 4. Writing"
- **Operational Level:** "Search database → Extract papers → Summarize findings"

## Planning Granularity

### High-Level Strategic Planning

**What it is:** Planning at the goal/objective level, describing "what" needs to be accomplished rather than "how."

**When to use:**
- Complex tasks requiring decomposition
- When implementation details should be handled by specialized components
- Multi-agent coordination where high-level plans are delegated

**Example:** "Research AI trends, summarize findings, and create presentation" (high-level) vs "Click search bar, type query, press Enter..." (low-level)

### Detailed Tactical Planning

**What it is:** Planning specific actions, tool calls, and implementation details.

**When to use:**
- Simple tasks where detailed planning is feasible
- When precise control is required
- Single-agent tasks where the agent handles all details

**Example:** "1. Call search API with query 'AI trends', 2. Parse JSON response, 3. Extract top 5 results, 4. Format as markdown..."

**Best Practice:** In task decomposition, keep subtasks at high-level abstraction. Low-level details are handled by specialized executors (see **Task Decomposition** pattern).

## Task Decomposition Strategies

When using explicit planning with task decomposition, choose a decomposition strategy based on task characteristics. For comprehensive details on task decomposition, see the [Task Decomposition](../task-decomposition/module.md) pattern.

### Exact Strategy: One Subtask Per Application

**When to Use:** When each application has a distinct, well-defined role and the task naturally maps to one operation per application.

**Characteristics:**
- Generates exactly the same number of subtasks as applications provided
- Each application gets exactly one subtask
- Enforces strict application boundaries
- Predictable and deterministic

**Example:**

```python
# Input: 3 applications
applications = [
    {"name": "News Portal", "type": "web"},
    {"name": "Summarizer", "type": "api"},
    {"name": "Social Media", "type": "api"}
]

# Task: "Find article about AI, summarize it, and share on social media"

# Output: Exactly 3 subtasks
subtasks = [
    {"task": "Find article about AI", "type": "web", "app": "News Portal"},
    {"task": "Summarize the article", "type": "api", "app": "Summarizer"},
    {"task": "Share summary on social media", "type": "api", "app": "Social Media"}
]
```

**Benefits:**
- Clear task boundaries
- Easy to parallelize (each app handles one subtask)
- Predictable execution flow
- Well-suited for multi-domain tasks

### Flexible Strategy: Logical Decomposition

**When to Use:** When the workflow requires multiple operations within the same application, or when logical task flow doesn't align with strict one-per-app boundaries.

**Characteristics:**
- Decomposes based on logical workflow requirements
- Allows multiple subtasks per application
- Subtasks must alternate between different applications (no consecutive same-app)
- More adaptable to complex workflows

**Example:**

```python
# Input: 2 applications
applications = [
    {"name": "File System", "type": "api"},
    {"name": "Team Management", "type": "api"}
]

# Task: "Create project folder, add files, get team list, set permissions"

# Output: Logical decomposition (File System used twice)
subtasks = [
    {"task": "Create project folder", "type": "api", "app": "File System"},
    {"task": "Add initial documentation files", "type": "api", "app": "File System"},
    {"task": "Retrieve team members list", "type": "api", "app": "Team Management"},
    {"task": "Configure folder permissions for team", "type": "api", "app": "File System"}
]
# Note: File System → File System → Team Management → File System (alternating pattern)
```

**Benefits:**
- Adapts to task complexity
- Supports multi-step workflows within applications
- More natural task flow
- Better for sequential operations

### Type-Aware Decomposition

Tasks are classified by type to enable specialized planning:

- **`web` type:** Browser-based interactions, UI navigation, form filling
- **`api` type:** Service calls, data retrieval, programmatic operations

Each subtask includes type information so the appropriate planner handles it:
- Web planner for browser interactions
- API planner for service calls

### Multi-Application Handling

When multiple applications are involved:

**Exact Strategy:**
- All applications must be utilized
- One subtask per application
- Applications are used in logical sequence

**Flexible Strategy:**
- Applications are selected based on subtask requirements
- Applications can be reused if workflow requires it
- Focus on logical workflow over strict app boundaries

> **"Plans must be grounded in state, not in dreams."** — Andrej Karpathy

## Decomposition Best Practices

When implementing task decomposition, follow these best practices:

### High-Level Abstraction

**✅ Good (High-Level):**
- "Find and extract the content of the most recent article about 'Quantum Computing' from TechNews Portal"
- "Generate a brief summary of the Quantum Computing article content"
- "Post the generated article summary to the Social Posting Platform"

**❌ Bad (Low-Level):**
- "Click on search bar, type 'Quantum Computing', press Enter, find first result, click on it, extract text content"
- "Call POST /api/summarize endpoint with article content in JSON payload"
- "Navigate to social media, click compose, paste summary, click post button"

### Context Preservation

**✅ Good (Preserves Context):**
- Intent: "Add the 3 most expensive products to my wishlist"
- Subtask: "Identify and add the 3 most expensive products to my wishlist on the Shopping App"
  - Note: "my wishlist" is preserved, not changed to "the wishlist"

**❌ Bad (Loses Context):**
- Intent: "Add the 3 most expensive products to my wishlist"
- Subtask: "Identify and add the 3 most expensive products to the wishlist"
  - Note: "my" is lost, changing the meaning

### Dependency Handling

**✅ Good (Explicit Dependencies):**
- Subtask 1: "Retrieve the email thread sent yesterday regarding participation in the whiteboard tool subscription and extract the names/emails of teammates who responded positively."
- Subtask 2: "Resolve the contact information of each confirmed participant (name/email) into phone numbers or Venmo handles"
  - Note: Explicitly references "confirmed participant (name/email)" from previous step
- Subtask 3: "Calculate each participant's equal share of the $120 subscription cost (i.e., $30 per person including the user), and send a public Venmo payment request to each participant with the description 'Whiteboard Tool Subscription'."
  - Note: Uses "each participant" from previous steps and includes calculation details

**❌ Bad (Implicit Dependencies):**
- Subtask 1: "Get email thread"
- Subtask 2: "Resolve contact information"
  - Note: Unclear what contact information or from where
- Subtask 3: "Send payment requests"
  - Note: Unclear to whom, for what amount, or why

### Answer Expectation Handling

**✅ Good (Explicit Answer):**
- Intent: "How much money have I sent or received to my roommates on Venmo since March 1st of this year?"
- Subtask: "Calculate the total amount of money sent to and received from the identified roommates on Venmo since March 1st of this year"
  - Note: Explicitly states what will be calculated and delivered

**❌ Bad (Missing Answer):**
- Intent: "How much money have I sent or received to my roommates on Venmo since March 1st of this year?"
- Subtask: "Retrieve Venmo transactions for roommates"
  - Note: Doesn't indicate that a calculation/total will be provided

### Single Application Pattern

**✅ Good (No Decomposition):**
- Intent: "Star the top five most starred repos in Gitlab"
- Applications: [{"name": "Gitlab", "type": "web"}]
- Output: Single subtask with intent verbatim
  - "Star the top five most starred repos in Gitlab" (type='web', app='Gitlab')

**❌ Bad (Unnecessary Decomposition):**
- Intent: "Star the top five most starred repos in Gitlab"
- Output: Multiple subtasks like "Search for repos", "Sort by stars", "Select top 5", "Star each repo"
  - Note: Single application can handle this atomically


## Adaptive Planning and Replanning

Adaptive planning transforms agents from rigid executors of predetermined sequences into dynamic systems that learn from experience and adjust their strategies based on execution outcomes. Unlike static planning that creates a plan once and follows it blindly, adaptive planning continuously monitors execution, detects when plans become invalid or suboptimal, and adjusts course accordingly. This capability is essential for operating in real-world environments where conditions change, assumptions prove wrong, and failures occur.

The core principle of adaptive planning is that plans are hypotheses about how to achieve goals—hypotheses that must be tested and refined through execution. When execution reveals that a plan is failing or no longer optimal, adaptive agents don't simply fail or retry the same approach. Instead, they analyze what went wrong, learn from the failure, and generate improved plans that incorporate lessons learned.

### When to Replan

Replanning decisions require balancing the cost of planning overhead against the cost of continuing with a suboptimal plan. Agents must detect when their current plan is no longer viable or when new opportunities emerge that justify replanning.

**Step failures** trigger replanning when a planned action fails and cannot be recovered through simple retry logic. For example, if an agent plans to use a specific API endpoint that returns a 404 error, it shouldn't just retry the same call. Instead, it should analyze the failure, determine whether the endpoint is permanently unavailable or the request format was wrong, and replan to use an alternative approach or correct the request. The key is distinguishing between transient errors (retry) and fundamental plan flaws (replan).

**New information** discovered during execution often invalidates planning assumptions. An agent might plan to process a dataset assuming it contains certain fields, but upon inspection, discover the schema is different. Or it might plan a multi-step workflow assuming certain tools are available, only to learn during execution that some tools require authentication that wasn't set up. When critical assumptions prove false, continuing with the original plan leads to failure, making replanning necessary.

**Goal changes** occur when users modify objectives mid-execution. A user might initially request "summarize this document" but then add "and compare it to last month's report." The original plan becomes incomplete and must be extended or replaced. Similarly, users might refine requirements, add constraints, or change priorities, all requiring plan adjustments.

**Resource constraints** can change dynamically during execution. A tool that was available during planning might become unavailable, budget limits might be reached, or time constraints might tighten. When resource availability changes significantly, the original plan may no longer be feasible, requiring replanning to work within new constraints.

**Deadline pressure** can make previously optimal plans suboptimal. An agent might have planned a thorough, multi-step analysis, but as a deadline approaches, it needs to replan for a faster, more streamlined approach that sacrifices some quality for speed.

### Replanning Strategies

The choice of replanning strategy depends on the scope of the failure and the cost of different approaches. Each strategy represents a different trade-off between planning overhead and plan quality.

**Full Replanning** discards the current plan entirely and creates a new one from scratch, treating the original plan as a failed experiment. This approach is necessary when fundamental assumptions are wrong, major failures occur that invalidate the entire plan structure, or goal changes are so significant that the original plan is irrelevant. For example, if an agent planned to use a specific cloud service for data processing, but that service is completely unavailable, full replanning is needed to find alternative approaches. The cost is high—full planning overhead must be paid again—but the benefit is a plan that's not constrained by the failed approach.

**Partial Replanning** preserves completed work and only adjusts the remaining steps. This is more efficient when failures are localized to specific parts of the plan or when new constraints affect only future steps. For instance, if an agent successfully completed steps 1-3 of a 5-step plan, but step 4 fails because a tool is unavailable, partial replanning would keep steps 1-3 intact and only replan steps 4-5 with alternative approaches. The cost is lower since only the remaining portion requires planning, but this approach assumes that completed work is still valid and that the failure doesn't indicate a fundamental flaw in the overall approach.

**Incremental Planning** plans only a few steps ahead, then plans the next steps as execution progresses. This is a proactive form of adaptive planning that anticipates the need for adjustments. Rather than planning the entire sequence upfront, the agent plans 2-3 steps, executes them, observes outcomes, then plans the next 2-3 steps based on what was learned. This approach is valuable in highly uncertain or dynamic environments where long-term plans become obsolete quickly. The cost is moderate—multiple planning phases are needed—but the benefit is continuous adaptation to changing conditions without the overhead of full replanning.

### Learning from Failures

Adaptive planning becomes more effective when agents learn from past failures and incorporate that knowledge into future planning. Rather than treating each failure as an isolated event, learning-enabled agents build a knowledge base of failure patterns, common pitfalls, and successful recovery strategies.

**Failure Analysis** involves examining why a plan failed, not just that it failed. An agent might analyze that a particular tool combination consistently fails, that certain task sequences are unreliable, or that specific assumptions are often wrong. This analysis transforms failures into learning opportunities. For example, if an agent repeatedly fails when trying to use two APIs in sequence, it might learn that these APIs have compatibility issues and should be used separately or with a different sequencing strategy.

**Pattern Recognition** across multiple planning attempts enables agents to identify recurring failure modes. An agent might notice that plans involving certain types of tools tend to fail more often, that longer plans are more likely to encounter issues, or that specific decomposition strategies work better for certain task types. Recognizing these patterns allows agents to proactively avoid known failure modes in future planning.

**Adaptive Strategy Selection** uses historical performance to choose planning strategies. An agent might learn that for certain task types, incremental planning works better than full planning, or that flexible decomposition strategies have higher success rates than exact strategies for complex workflows. This meta-learning—learning how to plan—improves planning effectiveness over time.

**Plan Libraries with Failure Knowledge** extend simple plan reuse by including information about when plans failed and why. A plan library entry might note "This plan works well for simple tasks but fails for tasks requiring more than 5 steps" or "This plan assumes tool X is available; if not, use alternative plan Y." This knowledge prevents repeating past mistakes and guides plan selection and adaptation.

## Planning with Uncertainty

### Handling Incomplete Information

**Strategies:**
- **Conservative Planning:** Plan for worst-case scenarios, include fallbacks
- **Optimistic Planning:** Plan for best-case, adapt if needed
- **Probabilistic Planning:** Consider multiple scenarios with probabilities
- **Information Gathering:** Include steps to gather missing information before committing to actions

### Planning Under Constraints

**Resource Constraints:**
- Budget limits (plan to minimize LLM calls or use cheaper models)
- Time limits (plan shorter sequences, prioritize critical steps)
- Tool availability (plan with fallback tools if primary tools unavailable)

**Example:** A complexity-based router (see **Routing** pattern) can route simple tasks to fast/cheap models and complex tasks to powerful models, optimizing cost while maintaining quality.

## Planning Efficiency Strategies

### Planning Depth vs. Execution Speed

**Trade-off:** Deeper planning (more detailed, longer plans) improves execution quality but increases planning latency and cost.

**Strategies:**
- **Shallow Planning:** Quick, high-level plans for simple tasks
- **Deep Planning:** Detailed plans for complex, critical tasks
- **Adaptive Depth:** Adjust planning depth based on task complexity (see complexity-based routing)

### Caching and Reuse

**Plan Templates:**
- Reuse plan structures for similar tasks
- Customize templates rather than planning from scratch

**Plan Libraries:**
- Maintain a library of successful plans for common task types
- Retrieve and adapt existing plans rather than generating new ones

## Decision Framework: Choosing a Planning Strategy

### Task Complexity
- **Simple (1-2 steps):** Reactive planning or no planning needed
- **Moderate (3-5 steps):** Explicit planning with shallow depth
- **Complex (6+ steps, multiple tools):** Explicit planning with deeper decomposition

### Environment Dynamics
- **Static:** Long-term explicit planning
- **Moderate:** Hybrid planning with reactive adjustments
- **Highly Dynamic:** Reactive planning or very short-term explicit planning

### Uncertainty Level
- **Low:** Detailed explicit planning
- **Moderate:** Explicit planning with fallbacks and replanning capability
- **High:** Reactive planning or incremental planning

### Resource Constraints
- **Budget:** Minimize LLM calls (explicit planning with single plan phase)
- **Latency:** Reactive planning or very shallow explicit planning
- **Tools:** Plan with tool availability in mind, include fallbacks

### Coordination Needs
- **Single Agent:** Any planning approach
- **Multi-Agent:** Hierarchical planning with delegation
- **Tool Orchestration:** Explicit planning with tool assignment

## Key Takeaways

- **Core Concept:** Planning strategies determine when, how, and to what depth agents should plan, significantly impacting performance, cost, and reliability.

- **Planning Paradigms:**
  - **Reactive Planning:** Plan one step at a time, highly adaptable but can get stuck locally
  - **Explicit Planning:** Plan entire sequence upfront, enables global optimization but less adaptable
  - **Hybrid Planning:** Combine explicit planning with reactive adjustments

- **Planning Horizons:** Choose short-term (1-3 steps), long-term (full sequence), or hierarchical (multiple abstraction levels) based on task complexity and environment dynamics.

- **Planning Granularity:** High-level strategic planning describes "what" (goals), while detailed tactical planning describes "how" (specific actions). In task decomposition, keep subtasks at high-level abstraction.

- **Task Decomposition Strategies:** 
  - **Exact Strategy:** One subtask per application—predictable, clear boundaries, good for multi-domain tasks
  - **Flexible Strategy:** Logical decomposition—adaptable, supports complex workflows, allows multiple operations per app

- **Adaptive Planning:** Implement replanning triggers (failures, new information, goal changes) and strategies (full, partial, incremental) to handle dynamic environments. Learn from failures by analyzing why plans failed, recognizing failure patterns, and incorporating lessons learned into future planning to avoid repeating mistakes.

- **Planning Efficiency:** Balance planning depth with execution speed, use caching and plan reuse, and optimize for resource constraints.

- **Best Practice:** Match planning strategy to task characteristics—complex tasks benefit from explicit planning, simple tasks from reactive planning, uncertain environments from hybrid or incremental planning.

- **Common Pitfall:** Over-planning simple tasks wastes resources; under-planning complex tasks leads to suboptimal execution. Choose the right strategy for the context.

## Related Patterns

This module informs and is informed by:

- **Task Decomposition** - Decomposition strategies are part of explicit planning
- **Planner-Checker** - Architectural pattern implementing explicit planning with verification
- **Routing** - Can be used for complexity-based planning decisions
- **Prioritization** - Informs planning by determining task order
- **Reflection** - Can evaluate and improve plans
- **ReAct** - Reactive planning paradigm (see Reasoning & Planning module)

??? "References"

    - ReAct: Synergizing Reasoning and Acting in Language Models
    - Plan-and-Execute: Beyond ReAct: A Planner-Centric Framework for Complex Tool-Augmented LLM Reasoning
    - CoReaAgents: A Collaboration and Reasoning Framework Based on LLM-Powered Agents
    - Task Decomposition Pattern (this book)
    - Planner-Checker Pattern (this book)
    - Routing Pattern (this book)
