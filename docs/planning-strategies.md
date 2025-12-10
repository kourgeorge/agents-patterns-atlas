# Planning Strategies

## Introduction

Planning is fundamental to agent autonomy. When an agent receives a high-level goal like "research a topic, summarize findings, and share insights," it must break this into actionable steps, allocate tasks to appropriate tools, and adapt its strategy as conditions change.
Without effective planning, agents become reactive systems that respond to immediate requests but often yield suboptimal results, overlook long-term objectives, or fall into inefficient loops.

Modern LLM agents employ various planning mechanisms. At the token level, Chain-of-Thought (CoT) prompting enables step-by-step reasoning, while Tree-of-Thought (ToT) explores multiple reasoning paths in parallel. ReAct-style agents interleave CoT reasoning with tool calls, but they plan only one step at a time—often overlooking long-term goals and incurring extra LLM calls for each tool use. By contrast, explicit planning frameworks generate structured plans before execution, then execute multiple steps without re-planning. This approach reduces latency and cost: generating one plan then executing multiple steps (rather than calling the LLM per tool) speeds up execution and forces the model to consider the entire task upfront. These approaches range from simple prompt-chaining to sophisticated hierarchical decomposition where high-level managers break goals into subtasks for specialized agents.

This module focuses on **task decomposition strategies**—the tactical techniques for breaking complex goals into manageable subtasks within explicit planning frameworks. Unlike design patterns that describe architectural solutions, strategies provide the specific methods for implementing decomposition. The strategies covered here—Exact, Flexible, and Type-Aware decomposition—determine how agents structure multi-step workflows, manage application boundaries, and coordinate tool usage.

The choice of decomposition strategy significantly impacts agent performance.

> **"Agents hallucinate plans but execute real actions."** — Andrej Karpathy

> **"Plans must be grounded in state, not in dreams."** — Andrej Karpathy

> **"Better agents come from better state, not longer thoughts."** — OpenAI Researchers

An Exact strategy (one subtask per application) provides predictability and clear boundaries, ideal for multi-domain tasks where each application has a distinct role. A Flexible strategy (logical decomposition) adapts to complex workflows that require multiple operations within the same application. These strategies, combined with best practices for abstraction, context preservation, and dependency handling, enable agents to transform high-level objectives into executable, coordinated sequences of actions.

## Task Decomposition Strategies

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

## Decomposition Best Practices & Common Patterns

### High-Level Abstraction Examples

**✅ Good (High-Level):**

- "Find and extract the content of the most recent article about 'Quantum Computing' from TechNews Portal"
- "Generate a brief summary of the Quantum Computing article content"
- "Post the generated article summary to the Social Posting Platform"

**❌ Bad (Low-Level):**

- "Click on search bar, type 'Quantum Computing', press Enter, find first result, click on it, extract text content"
- "Call POST /api/summarize endpoint with article content in JSON payload"
- "Navigate to social media, click compose, paste summary, click post button"

### Context Preservation Examples

**✅ Good (Preserves Context):**

- Intent: "Add the 3 most expensive products to my wishlist"
- Subtask: "Identify and add the 3 most expensive products to my wishlist on the Shopping App"
  - Note: "my wishlist" is preserved, not changed to "the wishlist"

**❌ Bad (Loses Context):**

- Intent: "Add the 3 most expensive products to my wishlist"
- Subtask: "Identify and add the 3 most expensive products to the wishlist"
  - Note: "my" is lost, changing the meaning

### Dependency Handling Examples

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

### List/Iteration Handling

**✅ Good (For Each Pattern):**

- "For each coworker whose share is noted in the retrieved note and has not yet paid, make a payment request with the description 'Work Dinner'"
- "For each Friday listed, schedule an email to the product team at 8 AM with subject 'Reminder: Product Sync Today' and use the template as the email body."

**❌ Bad (Unclear Iteration):**

- "Make payment requests for coworkers"
- Note: Unclear which coworkers, what amount, or what conditions

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

