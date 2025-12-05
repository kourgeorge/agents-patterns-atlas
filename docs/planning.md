# Pattern: Planning

## Motivation

When planning a trip, you break it down into steps: choose destination, book flights, reserve hotels, create an itinerary, pack. You consider dependencies (can't pack before deciding what to bring) and adapt when obstacles arise (flight cancelled, hotel unavailable). Planning in agents works the same way: taking a high-level goal and autonomously creating a structured sequence of actions, then adapting as conditions change.

## Pattern Overview
**What it is:** Planning is the ability for an agent to formulate a sequence of actions to move from an initial state towards a goal state, breaking down complex tasks into smaller, manageable steps.

**When to use:** Use planning when you need to delegate a complex goal where the "how" needs to be discovered dynamically, rather than following a predetermined workflow.

**Why it matters:** Planning enables agents to move beyond reactive behavior to goal-oriented, strategic problem-solving. It transforms high-level objectives into structured, executable sequences while maintaining adaptability to changing conditions and obstacles.

Intelligent behavior often involves more than just reacting to immediate input. It requires foresight, breaking down complex tasks into smaller steps, and strategizing how to achieve a desired outcome. At its core, planning allows an agent to formulate a sequence of actions to move from an initial state towards a goal state.

In the context of AI, a planning agent is like a specialist to whom you delegate a complex goal. When you ask it to "organize a team offsite," you're defining the what—the objective and its constraints—but not the how. The agent's core task is to autonomously chart a course to that goal. It must first understand the initial state (e.g., budget, number of participants, desired dates) and the goal state (a successfully booked offsite), and then discover the optimal sequence of actions to connect them. The plan is not known in advance; it is created in response to the request.

A hallmark of this process is adaptability. An initial plan is merely a starting point, not a rigid script. The agent's real power is its ability to incorporate new information and steer around obstacles. For instance, if the preferred venue becomes unavailable or a chosen caterer is fully booked, a capable agent doesn't simply fail. It adapts. It registers the new constraint, re-evaluates its options, and formulates a new plan, perhaps by suggesting alternative venues or dates.

However, it is crucial to recognize the trade-off between flexibility and predictability. Dynamic planning is a specific tool, not a universal solution. When a problem's solution is already well-understood and repeatable, constraining the agent to a predetermined, fixed workflow is more effective. This approach limits the agent's autonomy to reduce uncertainty and the risk of unpredictable behavior, guaranteeing a reliable and consistent outcome. Therefore, the decision to use a planning agent versus a simple task-execution agent hinges on a single question: does the "how" need to be discovered, or is it already known?

### Key Concepts
- **Goal Decomposition:** Planning breaks high-level goals into discrete, executable sub-tasks that can be sequenced logically. Decomposition strategies adapt based on task complexity and available applications.
- **Task Decomposition Strategies:** Different approaches for breaking down tasks:
  - **Exact Strategy:** One subtask per application (enforces strict application boundaries)
  - **Flexible Strategy:** Logical decomposition (allows multiple subtasks per application when workflow requires it)
- **Type-Aware Decomposition:** Tasks are classified by type (`web` for browser interactions, `api` for service calls), enabling specialized planning for each domain.
- **Multi-Application Handling:** When multiple applications are involved, decomposition can distribute work across applications or create sequential workflows that span application boundaries.
- **State Space Navigation:** The agent must understand initial state, goal state, and the actions that transition between states.
- **Adaptive Replanning:** Plans are not rigid; agents must adapt when obstacles arise or new information becomes available.
- **Dependency Management:** Planning must account for task dependencies, ensuring prerequisites are completed before dependent tasks.
- **Plan Execution Control:** A plan controller tracks progress, manages subtask execution, and determines when to conclude the overall task.

### How It Works
Planning works through a structured process that integrates task decomposition, execution control, and adaptive replanning:

**1. Goal Analysis & Application Discovery**
The agent understands the desired outcome, constraints, and available applications. Each application is characterized by:
- **Name and description:** What the application does
- **Type:** `web` (browser-based) or `api` (service-based)
- **URL:** Starting point for web applications

**2. Task Decomposition**
The agent breaks down the goal into high-level subtasks using one of two strategies:

**Exact Strategy (One Subtask Per Application):**
- When multiple applications are provided, generates exactly one subtask per application
- Enforces strict application boundaries
- Useful when each application has a distinct, well-defined role
- Example: 3 applications → exactly 3 subtasks

**Flexible Strategy (Logical Decomposition):**
- Decomposes based on logical workflow requirements
- Allows multiple subtasks per application when needed
- Subtasks must alternate between different applications (no consecutive same-app subtasks)
- More adaptable to complex workflows
- Example: May use App A → App B → App A if the workflow requires it

**Decomposition Rules:**
- **Single Application:** If only one application, return the intent verbatim (no decomposition)
- **Type Assignment:** Each subtask is assigned a type (`web` or `api`) and an application
- **High-Level Abstraction:** Subtasks describe "what" not "how" (no low-level actions like "click", "type", "call endpoint")
- **Context Preservation:** Subtasks reference data from previous steps when dependencies exist
- **User Context:** Personal pronouns and identifiers are preserved across subtasks

**3. Plan Generation**
The decomposition creates a structured plan with:
- List of subtasks with descriptions
- Type and application assignment for each subtask
- Thoughts explaining the decomposition strategy

**4. Plan Execution Control**
A plan controller manages execution:
- **Progress Tracking:** Monitors each subtask status (`not-started`, `in-progress`, `completed`)
- **Variable Management:** Tracks data collected during execution for use in subsequent steps
- **Next Action Selection:** Determines which subtask to execute next based on progress and dependencies
- **Task Conclusion:** Decides when all subtasks are complete and the overall goal is achieved

**5. Execution & Adaptation**
- Each subtask is executed by specialized planners (web planner for browser tasks, API planner for service tasks)
- The plan controller monitors progress and adapts when obstacles arise
- Variables from completed subtasks inform subsequent subtask execution
- The plan concludes when all subtasks are completed or the goal is achieved

**Information Gathering:**
Effective planning requires gathering relevant information before plan generation. The State Assessment phase should include targeted information-seeking operations to discover available resources, tools, APIs, and constraints. For instance, an agent should first discover what tools and APIs are available before planning how to use them, ensuring the plan is grounded in actual capabilities rather than assumptions.

**Planning Modes:**
- **Explicit Planning:** Generates a detailed plan document before execution (useful for complex, multi-step tasks)
- **Implicit Planning:** Planning happens dynamically during execution (more reactive, generates next step based on current state)

## When to Use This Pattern

### ✅ Use this pattern when:
- **Complex, multi-step goals:** The task requires a sequence of interdependent actions that must be discovered and coordinated.
- **Dynamic environments:** Conditions change during execution, requiring plan adaptation.
- **Goal discovery needed:** The "how" to achieve the goal is not predetermined and must be discovered.
- **Long-horizon tasks:** The task spans multiple steps where intermediate planning improves outcomes.
- **Resource coordination:** The task requires coordinating multiple resources, tools, or agents in a specific sequence.

### ❌ Avoid this pattern when:
- **Fixed workflows suffice:** The solution path is well-understood and can be hardcoded as a workflow.
- **Simple, single-step tasks:** The task can be completed in one or two steps without needing a plan.
- **Predictability is critical:** You need guaranteed, consistent behavior that fixed workflows provide.
- **Real-time constraints:** The overhead of planning adds unacceptable latency for time-sensitive tasks.

### Decision Guidelines

**When to Use Planning:**
Use planning when the benefits of adaptability and goal discovery outweigh the costs of increased complexity and potential unpredictability. Consider:
- **Task Complexity:** More complex = more benefit from planning
- **Environment Variability:** More variable = more need for adaptive planning
- **Solution Path:** Unknown = use planning, known = use workflow

**Choosing Decomposition Strategy:**

**Use Exact Strategy when:**
- Each application has a distinct, well-defined role
- Task naturally maps to one operation per application
- You need predictable, deterministic decomposition
- Parallel execution is desired (each app handles one subtask)
- Multi-domain tasks with clear boundaries

**Use Flexible Strategy when:**
- Workflow requires multiple operations within the same application
- Logical task flow doesn't align with strict one-per-app boundaries
- Sequential operations need to be broken down naturally
- Task complexity requires adaptive decomposition
- Applications need to be reused in the workflow

**General Considerations:**
- Planning adds latency and cost but improves outcomes for complex, multi-step tasks
- For single-application tasks, no decomposition is needed (return intent verbatim)
- For critical systems requiring guaranteed behavior, consider hybrid approaches that combine planning with fixed workflow fallbacks

## Practical Applications & Use Cases

Planning is a core computational process in autonomous systems, enabling agents to synthesize sequences of actions to achieve specified goals.

- **Business Process Automation:** Decompose complex workflows like employee onboarding into sequenced sub-tasks with dependencies.
- **Robotics and Navigation:** Generate paths or action sequences to transition from initial to goal state while optimizing for metrics.
- **Content Generation:** Formulate plans for complex outputs like research reports with distinct phases for gathering, summarizing, and structuring.
- **Customer Support:** Create systematic plans for multi-step problem resolution including diagnosis, solution implementation, and escalation.
- **Project Management:** Break down high-level projects into task sequences with dependencies and resource allocation.

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

## Implementation

### Core Components

**Task Decomposition Agent:**
```python
from typing import List, Literal
from pydantic import BaseModel, Field

class Subtask(BaseModel):
    task: str
    app: str
    type: Literal['web', 'api']

class DecompositionPlan(BaseModel):
    thoughts: str
    task_decomposition: List[Subtask]

class DecompositionAgent:
    def __init__(self, llm, strategy: Literal['exact', 'flexible']):
        self.llm = llm
        self.strategy = strategy
    
    async def decompose(
        self, 
        intent: str, 
        applications: List[dict]
    ) -> DecompositionPlan:
        """Decompose task into subtasks based on strategy."""
        # Single app: return intent as-is
        if len(applications) == 1:
            return DecompositionPlan(
                thoughts="Single application, no decomposition needed",
                task_decomposition=[
                    Subtask(
                        task=intent,
                        app=applications[0]["name"],
                        type=applications[0]["type"]
                    )
                ]
            )
        
        # Multi-app: use strategy
        prompt = self._build_prompt(intent, applications, self.strategy)
        response = await self.llm.ainvoke(prompt)
        return DecompositionPlan.model_validate_json(response.content)
```

**Plan Controller:**
```python
from typing import Literal

class PlanControllerOutput(BaseModel):
    thoughts: List[str]
    subtasks_progress: List[Literal['completed', 'not-started', 'in-progress']]
    next_subtask: str
    next_subtask_type: Literal['web', 'api', None]
    next_subtask_app: str
    conclude_task: bool
    final_answer: str

class PlanController:
    def __init__(self, llm):
        self.llm = llm
    
    async def control(
        self,
        plan: DecompositionPlan,
        execution_history: List[dict],
        variables: dict
    ) -> PlanControllerOutput:
        """Determine next action based on plan progress."""
        # Analyze progress, select next subtask, or conclude
        prompt = self._build_prompt(plan, execution_history, variables)
        response = await self.llm.ainvoke(prompt)
        return PlanControllerOutput.model_validate_json(response.content)
```

### Basic Example: Task Decomposition

```python
# Decompose a task into subtasks
intent = "Find article about AI, summarize it, and share on social media"

applications = [
    {"name": "News Portal", "type": "web", "url": "https://news.example.com"},
    {"name": "Summarizer", "type": "api"},
    {"name": "Social Media", "type": "api"}
]

# Mock implementation for demonstration
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

async def decompose_task(intent: str, apps: list) -> dict:
    prompt = ChatPromptTemplate.from_template(
        "Decompose task: {intent}
Applications: {apps}
Return JSON with task_decomposition."
    )
    chain = prompt | llm | JsonOutputParser()
    result = chain.invoke({"intent": intent, "apps": str(apps)})
    return result

# Example usage
import asyncio
async def main():
    plan = await decompose_task(intent, applications)
    print(plan)

if __name__ == "__main__":
    asyncio.run(main())

# Output:
# {
#   "thoughts": "Three distinct operations across three applications",
#   "task_decomposition": [
#     {"task": "Find article about AI", "type": "web", "app": "News Portal"},
#     {"task": "Summarize the article", "type": "api", "app": "Summarizer"},
#     {"task": "Share summary on social media", "type": "api", "app": "Social Media"}
#   ]
# }
```

### Advanced Example: Plan Execution with Controller

```python
# Mock implementation for demonstration
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Simplified example
intent = "Find article about AI, summarize it, and share on social media"
applications = [
    {"name": "News Portal", "type": "web"},
    {"name": "Summarizer", "type": "api"},
    {"name": "Social Media", "type": "api"}
]

async def main():
    # Mock plan
    plan = {
        "task_decomposition": [
            {"task": "Find article about AI", "type": "web", "app": "News Portal"},
            {"task": "Summarize the article", "type": "api", "app": "Summarizer"},
            {"task": "Share summary on social media", "type": "api", "app": "Social Media"}
        ]
    }
    
    # Simplified execution
    execution_history = []
    variables = {}
    
    for subtask in plan["task_decomposition"]:
        # Mock execution
        result = f"Executed: {subtask['task']}"
        execution_history.append({
            "subtask": subtask["task"],
            "result": result,
            "status": "completed"
        })
        print(f"Completed: {subtask['task']}")
    
    print("Task complete!")

if __name__ == "__main__":
    asyncio.run(main())
```

### Example: Flexible Strategy

```python
# Task requiring multiple operations in same app
intent = "Create project folder, add files, get team list, set permissions"

applications = [
    {"name": "File System", "type": "api"},
    {"name": "Team Management", "type": "api"}
]

decomposer = DecompositionAgent(llm, strategy="flexible")
import asyncio


async def main():
    plan = await decomposer.decompose(intent, applications)

if __name__ == "__main__":
    asyncio.run(main())
```

### Workflow Integration

```python
# Simplified planning workflow example
from typing import List

async def planning_workflow(intent: str, applications: List[dict]):
    # Mock implementation
    plan = {
        "task_decomposition": [
            {"task": "Find article", "type": "web", "app": "News Portal"},
            {"task": "Summarize", "type": "api", "app": "Summarizer"}
        ]
    }
    
    # Simplified execution
    execution_history = []
    variables = {}
    
    for subtask in plan["task_decomposition"]:
        result = f"Executed: {subtask['task']}"
        execution_history.append({"subtask": subtask["task"], "result": result})
        print(f"Completed: {subtask['task']}")
    
    return "Task complete"

async def main():
    intent = "Find article about AI and summarize it"
    applications = [
        {"name": "News Portal", "type": "web"},
        {"name": "Summarizer", "type": "api"}
    ]
    result = await planning_workflow(intent, applications)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Key Takeaways

- **Core Concept:** Planning enables agents to formulate sequences of actions to achieve goals, breaking complex tasks into manageable steps through task decomposition.

- **Decomposition Strategies:** Choose the right strategy based on task characteristics:
  - **Exact Strategy:** One subtask per application - predictable, clear boundaries, good for multi-domain tasks
  - **Flexible Strategy:** Logical decomposition - adaptable, supports complex workflows, allows multiple operations per app

- **Type-Aware Planning:** Classify tasks as `web` (browser interactions) or `api` (service calls) to enable specialized planning for each domain.

- **Multi-Application Handling:** When multiple applications are involved, decomposition can distribute work across applications (exact) or create sequential workflows (flexible) based on the chosen strategy.

- **Plan Execution Control:** A plan controller tracks progress, manages subtask execution, selects next actions based on dependencies, and determines when to conclude the overall task.

- **Information Gathering:** Planning should be informed by relevant context gathered through targeted information-seeking operations (e.g., discovering available tools, APIs, constraints) before plan generation, but should avoid over-gathering unnecessary information.

- **Best Practice:** Use explicit planning for complex, long-horizon tasks; use implicit planning for reactive, adaptive scenarios.

- **Common Pitfall:** Over-planning simple tasks adds unnecessary complexity; use fixed workflows when the solution path is known. For single-application tasks, return the intent verbatim without decomposition.

- **Performance Note:** Planning adds latency and cost but improves outcomes for complex, multi-step tasks requiring coordination. Decomposition strategies balance predictability (exact) with flexibility (flexible).

## Related Patterns

This pattern works well with:
- **Goal Setting and Monitoring** - Goals provide the target for planning, monitoring tracks plan execution
- **Reflection** - Plans can be evaluated and refined through reflection
- **Routing** - Planning can determine which routes to take in a workflow

This pattern is often combined with:
- **Tool Use** - Plans specify which tools to use and in what sequence
- **Multi-Agent** - Planning can coordinate multiple agents working on different plan steps

## References

- CrewAI Documentation: https://docs.crewai.com/
- Google DeepResearch: https://deepresearch.google/
- Planning in AI Systems: https://en.wikipedia.org/wiki/Automated_planning_and_scheduling

