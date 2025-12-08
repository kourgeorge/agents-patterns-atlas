# Pattern: Recitation

## Motivation

When working on a long project, you keep a task list visible—on your desk, whiteboard, or screen—to stay focused on your goals. As you complete tasks, you update the list, but the main objectives remain visible. This prevents you from losing sight of the big picture amid daily details. The Persistent Task List pattern does the same for agents: maintaining a running plan in context to prevent goal drift during long, complex tasks.

## Pattern Overview
**What it is:** A mechanism where the agent maintains a running plan (like a todo.md file) and continuously appends the updated plan to the end of the context.

**When to use:** When designing long-horizon AI agents that need to sustain goals and avoid forgetting high-level objectives over multiple steps.

**Why it matters:** This deliberate "recitation" manipulates the model's attention, pushing the global plan into the most recent context and mitigating the "lost in the middle" problem that occurs in long contexts.

The Persistent Task List (Recitation) pattern addresses a fundamental challenge in long-horizon agent design: maintaining focus on high-level objectives as the agent executes many intermediate steps. As agents process complex, multi-step tasks, the context window fills with detailed execution history, tool results, and intermediate reasoning. This accumulation can cause the agent's original goals and plan to become "lost in the middle" of the context, leading to goal drift and reduced effectiveness.

Recitation is a context engineering strategy that actively manages the LLM's finite attention window. By continuously appending the updated plan to the end of the context, the pattern ensures that high-level objectives remain within the model's recent attention span. This manipulation of attention is deliberate and strategic—the plan is not just stored but actively recited into the context at each iteration, biasing the model's focus toward global objectives.

The pattern is particularly effective because LLMs exhibit recency bias, paying more attention to information that appears later in the context. By keeping the plan recent, the agent maintains alignment with its original goals even as it navigates complex, branching workflows with hundreds of steps.

### Key Concepts
- **Persistent Task List:** A running plan or to-do list that tracks the agent's high-level objectives and progress, typically stored in a persistent file or state.
- **Recitation:** The deliberate act of appending the updated plan to the end of the context at each iteration to manipulate attention.
- **Context Engineering:** Strategic manipulation of the context window to bias the model's attention toward important information.
- **Long-Horizon Tasks:** Complex tasks that span many steps, requiring the agent to maintain focus on objectives over extended execution.
- **Goal Alignment:** Ensuring the agent's actions remain aligned with its original high-level goals throughout execution.

### How It Works: Step-by-step Explanation

1. **Maintain the Plan:** The agent is instructed to maintain a running to-do list or plan, often externalized to a persistent file (e.g., todo.md) or stored in the agent's state.

2. **Update Progress:** At each step in the agent's iterative loop, it updates the task list by checking off completed subtasks.

3. **Recite into Context:** The updated plan is then appended to the end of the context for the next iteration. This constant overwriting or appending ensures the objectives are always within the model's recent attention span.

4. **Bias Attention:** By keeping the plan recent, the model's focus is biased toward the global objectives, reducing goal misalignment and avoiding the agent drifting off-topic.

## When to Use This Pattern

### ✅ Use when:
- Building long-horizon agents that must sustain goals over many steps.
- Mitigating the risk of the agent forgetting its high-level goals or getting "lost in the middle."
- The agent needs to dynamically pull information back into context to remind itself what it is supposed to be doing.
- Working on open-ended problems where the agent generates and manages its own steps.

### ❌ Avoid when:
- The task is simple or single-turn, as the overhead of managing and reciting the task list is unnecessary and increases token cost.
- The agent is purely reactive and does not require explicit step-by-step planning.
- The context window is short and cannot accommodate the additional plan recitation overhead.

### Decision Guidelines
Use this pattern as a critical context engineering strategy to ensure the agent remains focused on its high-level goals throughout a complex or long-running workflow. It is especially effective in open-ended problems where the agent generates and manages its own steps. Consider the trade-off: recitation adds token cost but prevents costly goal drift and rework. For tasks requiring sustained focus over 10+ steps, the benefits typically outweigh the costs.

## Practical Applications & Use Cases

The Persistent Task List (Recitation) pattern is essential for maintaining goal alignment in complex, multi-step agent workflows.

- **Autonomous Research:** An agent tasked with writing a comprehensive research report uses a plan to track phases like information gathering, synthesis, and revision over hundreds of steps.

- **Code Generation:** Systems like Claude Code use a no-op Todo list tool as a context engineering strategy to keep the agent on track during multi-file, multi-step coding tasks.

- **Workflow Persistence:** Manus AI utilizes this pattern by making its agent create and continuously update a todo.md file as subtasks are completed, ensuring goal persistence.

- **Filesystem Integration:** Writing a plan to the filesystem allows the agent to pull this information back into the context window later on, enabling goal persistence across sessions.

- **Multi-Agent Orchestration:** Orchestrator agents maintain and recite plans as they delegate tasks to worker agents, ensuring the overall objective remains clear despite distributed execution.

## Implementation

### Prerequisites
```bash
pip install deepagents
# or
pip install langchain langchain-openai
# or
pip install google-adk
```

### Basic Example: Planning Tool (Conceptual)

The deepagents package incorporates a built-in Write to-dos tool, which is a key component of its deep agent architecture. Although conceptually acting as a planning tool, it is often a no-op function, meaning its primary purpose is manipulating context and attention rather than performing an external action. Its detailed description provided to the LLM guides the agent on how to manage tasks, prioritize them, and update their status in real time (e.g., pending, in progress, completed).

```python
# Conceptual Tool Implementation (based on deepagents)

def write_to_dos_tool(new_todos: str) -> str:
    """
    Updates the agent's internal state with a new to-do list, which is 
    then included in the context for the next iteration (Recitation).
    
    Args:
        new_todos: The full text of the updated to-do list.
    """
    # In a real system, this updates the agent's internal state dictionary 
    # (e.g., state['to_dos'] = new_todos) and returns an Observation.
    
    # The agent reads the description and knows to output an updated list 
    # via this tool call when its plan changes.
    
    print(f"DEBUG: Reciting updated task list to context:\n{new_todos}")
    return "Task list updated in memory/state."

# The Recitation pattern is realized when the agent framework 
# ensures the content of 'new_todos' is included in the prompt
# for every subsequent LLM call.
```

### Advanced Example: Filesystem-Based Recitation

```python
from typing import Dict, List
from pathlib import Path
import json

class RecitationAgent:
    def __init__(self, todo_file: str = "todo.md"):
        self.todo_file = Path(todo_file)
        self.todo_file.touch(exist_ok=True)
        self.context_history = []
    
    def read_todo(self) -> str:
        """Read the persistent task list from filesystem."""
        try:
            return self.todo_file.read_text()
        except FileNotFoundError:
            return "# Task List\n\nNo active tasks."
    
    def update_todo(self, updated_todos: str) -> str:
        """Update the task list and return confirmation."""
        self.todo_file.write_text(updated_todos)
        return f"Task list updated. Current plan:\n\n{updated_todos}"
    
    def build_context(self, user_message: str) -> List[Dict[str, str]]:
        """Build context with recitation pattern."""
        # Read the current plan
        current_plan = self.read_todo()
        
        # Build context: history + new message + recited plan
        messages = self.context_history.copy()
        messages.append({"role": "user", "content": user_message})
        
        # Recitation: Append plan to end of context
        messages.append({
            "role": "system",
            "content": f"## Current Plan (Recited)\n\n{current_plan}\n\nRemember: This plan represents your high-level objectives. Update it as you make progress."
        })
        
        return messages
    
    def process_step(self, user_message: str, llm_response: str):
        """Process a step and update context history."""
        # Add to history (append-only for KV-Cache optimization)
        self.context_history.append({"role": "user", "content": user_message})
        self.context_history.append({"role": "assistant", "content": llm_response})
        
        # Check if response contains updated todos
        if "write_to_dos" in llm_response or "update_todo" in llm_response.lower():
            # Extract and update todos (simplified - in production, use structured extraction)
            # This would typically be handled by a tool call parser
            pass

# Usage
agent = RecitationAgent("agent_todo.md")

# Initial planning
initial_plan = """# Research Project Plan

- [ ] Gather sources on topic X
- [ ] Analyze key findings
- [ ] Draft report sections
- [ ] Review and refine
"""
agent.update_todo(initial_plan)

# Each step recites the plan
context = agent.build_context("I've gathered 5 sources. What's next?")
# The plan is automatically appended to context, keeping goals in focus
```

**Explanation:**
This example demonstrates the Recitation pattern with filesystem persistence. The agent maintains a todo.md file that is read at each step and appended to the context. This ensures the plan remains in the model's recent attention span, preventing goal drift during long-horizon tasks.

### Framework-Specific Examples

#### LangGraph: Recitation Node
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    todo_list: str
    scratchpad: str

def recite_plan_node(state: AgentState) -> AgentState:
    """Node that recites the plan into context."""
    # Read current plan from state
    plan = state.get("todo_list", "# No active plan")
    
    # Append plan to messages (recitation)
    state["messages"].append({
        "role": "system",
        "content": f"## Current Plan\n\n{plan}\n\nKeep this plan in mind as you work."
    })
    
    return state

def reasoning_node(state: AgentState) -> AgentState:
    """Main reasoning node that processes tasks."""
    # LLM processes with plan in recent context
    # ... LLM call with state["messages"] ...
    return state

# Build graph with recitation
workflow = StateGraph(AgentState)
workflow.add_node("recite_plan", recite_plan_node)
workflow.add_node("reasoning", reasoning_node)
workflow.add_edge("recite_plan", "reasoning")
workflow.add_edge("reasoning", "recite_plan")  # Loop back to re-recite
workflow.set_entry_point("recite_plan")
```

#### Google ADK: State-Based Recitation
```python
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

def get_plan_from_state(state: dict) -> str:
    """Retrieve plan from agent state."""
    return state.get("todo_list", "# No active plan")

# Agent with recitation in instruction
agent = LlmAgent(
    name="RecitationAgent",
    model="gemini-2.0-flash",
    instruction="""You are a task-oriented agent. 
    
    At the start of each turn, you will see your current plan (todo list) 
    recited in the context. This plan represents your high-level objectives.
    
    As you complete tasks:
    1. Update the plan by marking tasks as complete
    2. Add new subtasks as needed
    3. The updated plan will be recited in the next turn
    
    Always keep the plan updated and use it to guide your actions.""",
    output_key="last_response"
)

# Runner manages state and can inject plan into context
runner = Runner(
    agent=agent,
    app_name="recitation_app",
    session_service=InMemorySessionService()
)

# Custom context builder that recites plan
def build_context_with_recitation(session_state: dict, user_input: str):
    plan = session_state.get("todo_list", "# No active plan")
    return f"{user_input}\n\n## Current Plan (Recited)\n\n{plan}"
```

#### Manus AI Pattern: Filesystem Todo.md
```python
from pathlib import Path
import re

class ManusStyleRecitation:
    def __init__(self, workspace_dir: str = "./workspace"):
        self.workspace = Path(workspace_dir)
        self.todo_file = self.workspace / "todo.md"
        self.workspace.mkdir(exist_ok=True)
    
    def ensure_todo_exists(self):
        """Ensure todo.md exists, create if not."""
        if not self.todo_file.exists():
            self.todo_file.write_text("# Task List\n\n## Active Tasks\n\n- [ ] Initial task\n")
    
    def read_and_recite(self) -> str:
        """Read todo.md and format for recitation."""
        self.ensure_todo_exists()
        content = self.todo_file.read_text()
        return f"## Current Task Plan (from todo.md)\n\n{content}\n\n---\n\nThis plan is maintained in todo.md. Update it as you progress."
    
    def update_todo(self, new_content: str):
        """Update todo.md with new plan."""
        self.todo_file.write_text(new_content)
        return f"Updated todo.md. Plan now contains {len(new_content.split(chr(10)))} lines."
    
    def extract_todo_update(self, agent_response: str) -> str:
        """Extract todo update from agent response (simplified)."""
        # In production, use structured tool calls
        # This is a simplified regex-based extraction
        pattern = r"```markdown\s*(#.*?)\s*```"
        match = re.search(pattern, agent_response, re.DOTALL)
        if match:
            return match.group(1)
        return None

# Usage
recitation = ManusStyleRecitation()

# At each agent step:
current_plan = recitation.read_and_recite()
# Append current_plan to end of context before LLM call

# After LLM responds:
# Check if response contains todo update, then:
# recitation.update_todo(updated_plan)
```

## Alternative Approach: Planner Sub-Agent with Structured Output

While the traditional Recitation pattern uses filesystem-based `todo.md` files that are constantly rewritten and appended to context, there is a more token-efficient alternative that has shown significant improvements in production systems.

**The Problem with Persistent Todo.md Files:**

In early versions of systems like Manus, plans were maintained through `todo.md` files that were constantly rewritten and appended to context at every turn. This approach:
- Consumes tokens in every single turn (~30% token overhead in early Manus versions)
- Requires parsing and updating markdown files
- Adds complexity to the conversation history
- May become verbose as plans evolve

**The Alternative: Planner Sub-Agent Pattern**

Instead of maintaining a persistent `todo.md` file, use a dedicated Planner sub-agent that returns a structured Plan object. This follows the **Agent-as-Tool** pattern, where planning becomes a deterministic function call rather than a persistent conversation state.

**How It Works:**

1. **Planner as Tool:** The main agent invokes a `call_planner(goal="...")` tool when it needs to create or update a plan
2. **Structured Output:** The Planner sub-agent returns a structured Plan object (e.g., JSON schema) with clear task breakdown
3. **On-Demand Injection:** The Plan object is injected into context only when explicitly needed, rather than consuming tokens in every turn
4. **Deterministic Interface:** The Planner follows the Agent-as-Tool pattern, enabling cacheable, predictable planning operations

**Benefits:**

- **Token Efficiency:** Plans consume tokens only when actively used, not in every turn (~30% token savings demonstrated)
- **Structured Data:** JSON-structured plans are easier to parse and validate than markdown
- **Modularity:** Planner can be swapped, updated, or versioned independently
- **Cache Optimization:** Deterministic planner calls enable better caching strategies
- **Clearer Separation:** Planning logic is isolated from execution logic

**When to Use Each Approach:**

**Use Traditional Recitation (todo.md) when:**
- Plans need to be human-readable and editable
- You want to track plan evolution through filesystem history
- Plans are part of the agent's persistent state that should survive sessions
- You need simple, text-based plan representation

**Use Planner Sub-Agent when:**
- Token efficiency is critical
- Plans are used infrequently or only at specific decision points
- You want structured, validated plan schemas
- Planning logic should be modular and swappable
- You're following the Agent-as-Tool pattern for consistency

**Implementation Example:**

```python
from typing import List, Dict, Any
from pydantic import BaseModel

class Task(BaseModel):
    id: str
    description: str
    status: str  # "pending", "in_progress", "completed"
    dependencies: List[str] = []

class Plan(BaseModel):
    goal: str
    tasks: List[Task]
    current_task_id: str
    progress: float  # 0.0 to 1.0

def call_planner(goal: str, current_state: Dict[str, Any] = None) -> Plan:
    """
    Planner sub-agent that creates a structured plan.
    Returns a Plan object that can be injected into context when needed.
    """
    # Planner agent analyzes goal and current state
    # Returns structured Plan object
    return Plan(
        goal=goal,
        tasks=[
            Task(id="1", description="Research topic X", status="pending"),
            Task(id="2", description="Draft outline", status="pending", dependencies=["1"]),
            Task(id="3", description="Write sections", status="pending", dependencies=["2"]),
        ],
        current_task_id="1",
        progress=0.0
    )

# Main agent uses planner on-demand
plan = call_planner("Write research paper on AI agents")
# Plan is injected into context only when needed, not every turn
```

**Key Insight:**

Both approaches are valid. The choice depends on your system's priorities: traditional Recitation emphasizes simplicity and human-readability, while the Planner sub-agent approach prioritizes token efficiency and modularity. Many production systems evolve from the traditional approach to the Planner sub-agent pattern as they optimize for scale.

## Key Takeaways

- **Core Concept:** Recitation is a context engineering strategy used to actively manage the LLM's finite context window by biasing its attention toward high-level goals.

- **Best Practice:** The plan should be frequently overwritten or appended to the end of the prompt to maximize the effect of recency bias.

- **Alternative Approach:** Using a Planner sub-agent that returns structured Plan objects can save ~30% tokens compared to persistent `todo.md` files, as plans are injected only when needed rather than every turn.

- **Common Pitfall:** Avoid using this pattern for simple, single-turn tasks where the overhead outweighs the benefits. Also, ensure the plan doesn't become too verbose, as it adds to token costs.

- **Performance Note:** This pattern is essential for avoiding the performance degradation associated with the "lost in the middle" problem in very long contexts. The tool used for managing the to-do list can be a logical no-op, as its function is simply to update the conversational context or state.

- **Implementation Note:** The recitation mechanism works best when combined with stable, append-only context structures to maximize KV-Cache efficiency.

## Related Patterns

This pattern works well with:
- **Filesystem as Context:** The task list itself is often stored in an external persistent store (like a filesystem) so it can be reliably referenced and updated across many steps.

- **Stable, Append-Only Context:** Recitation aligns with the need to keep the prompt prefix stable; the plan is appended to the context history rather than modifying the core instructions.

- **Memory Management:** Recitation is a specific memory management technique for maintaining goal alignment in long-horizon tasks.

This pattern is often combined with:
- **Planning:** The Recitation pattern is the execution mechanism for ensuring the plan generated by the Planning pattern is followed throughout a long task.

- **Orchestrator (Coordinator) Pattern:** The central Orchestrator agent typically maintains and recites the plan as it delegates and synthesizes results from worker agents.

- **Goal Setting and Monitoring:** Recitation ensures that goals set at the beginning remain visible and actionable throughout execution.

- **Agent-as-Tool Pattern:** The alternative Planner sub-agent approach follows the Agent-as-Tool pattern, treating planning as a deterministic function call rather than persistent conversation state.

??? "References"

- Agentic AI System Design Patterns
- Context Engineering for AI Agents: Lessons from Building Manus
- Context Engineering for AI Agents: Part 2 - https://www.philschmid.de/context-engineering-part-2
- Implementing deepagents: a technical walkthrough
- Deep Agents
- How agents can use filesystems for context engineering
- Agentic Design Patterns Engineering Playbook
- Manus AI Agent Harness learnings from Peak Ji

