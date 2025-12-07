# Pattern: Task Decomposition Planning

## Motivation

When planning a trip, you break it down into steps: choose destination, book flights, reserve hotels, create an itinerary, pack. You consider dependencies (can't pack before deciding what to bring) and adapt when obstacles arise (flight cancelled, hotel unavailable). Task decomposition planning in agents works the same way: taking a high-level goal and autonomously breaking it down into a structured sequence of subtasks, each assigned to the appropriate application or service, then orchestrating their execution while adapting as conditions change.

## Pattern Overview
**What it is:** Task decomposition planning is the ability for an agent to analyze a complex goal, break it down into high-level subtasks, assign each subtask to the appropriate application or service, and orchestrate their execution in a logical sequence.

**When to use:** Use task decomposition planning when you need to delegate a complex goal that spans multiple applications or services, where the "how" needs to be discovered dynamically, rather than following a predetermined workflow.

**Why it matters:** Task decomposition planning enables agents to move beyond reactive behavior to goal-oriented, strategic problem-solving. It transforms high-level objectives into structured, executable sequences of subtasks while maintaining adaptability to changing conditions and obstacles. By breaking down complex tasks and assigning them to specialized applications, agents can handle multi-step workflows that would be impossible to execute atomically.

Intelligent behavior often involves more than just reacting to immediate input. It requires foresight, breaking down complex tasks into smaller steps, and strategizing how to achieve a desired outcome. At its core, task decomposition planning allows an agent to analyze a goal, understand what applications and services are available, and create a structured plan that coordinates their use.

In the context of AI, a task decomposition planning agent is like a project manager to whom you delegate a complex goal. When you ask it to "find an article about AI, summarize it, and share it on social media," you're defining the what—the objective—but not the how. The agent's core task is to:
1. **Analyze** the task to understand its requirements and classify its characteristics
2. **Match** the task to available applications (web-based or service-based)
3. **Decompose** the goal into high-level subtasks, each assigned to an appropriate application
4. **Orchestrate** the execution of subtasks, managing dependencies and data flow between them

The plan is not known in advance; it is created in response to the request by analyzing the goal and available resources.

A hallmark of this process is adaptability. An initial decomposition is merely a starting point, not a rigid script. The agent's real power is its ability to incorporate new information and steer around obstacles. For instance, if a preferred application becomes unavailable or a subtask fails, a capable agent doesn't simply fail. It adapts. It registers the new constraint, re-evaluates its options, and may reformulate the decomposition or adjust the execution plan.

However, it is crucial to recognize the trade-off between flexibility and predictability. Dynamic task decomposition is a specific tool, not a universal solution. When a problem's solution is already well-understood and repeatable, constraining the agent to a predetermined, fixed workflow is more effective. This approach limits the agent's autonomy to reduce uncertainty and the risk of unpredictable behavior, guaranteeing a reliable and consistent outcome. Therefore, the decision to use task decomposition planning versus a simple task-execution agent hinges on a single question: does the "how" need to be discovered, or is it already known?

### Key Concepts

**Three-Phase Architecture:**
- **Task Analysis Phase:** Before decomposition, the agent analyzes the task to classify its characteristics, match it to available applications, and understand its requirements.
- **Task Decomposition Phase:** The agent breaks down the high-level goal into subtasks, assigns each to an appropriate application, and determines their sequence.
- **Plan Control Phase:** A plan controller orchestrates execution, tracks progress, manages data flow between subtasks, and determines when to conclude.

**Task Analysis:**
- **Task Classification:** Tasks are analyzed to determine characteristics such as whether they perform updates, require memory, involve loops, or need location search.
- **Application Matching:** The agent matches the user intent to available applications (web-based or service-based) based on their capabilities and descriptions.
- **Intent Paraphrasing:** For complex or ambiguous intents, the agent may paraphrase to clarify requirements before decomposition.
- **Navigation Path Discovery:** For web applications, the agent may identify known navigation paths to accomplish the task efficiently.

**Task Decomposition:**
- **High-Level Abstraction:** Subtasks describe "what" needs to be accomplished, not "how" (no low-level actions like "click", "type", "call endpoint").
- **Type-Aware Assignment:** Each subtask is assigned a type (`web` for browser interactions, `api` for service calls) and an application, enabling specialized execution.
- **Context Preservation:** Personal pronouns, identifiers, and user context are preserved across subtasks (e.g., "my accounts" remains "my accounts").
- **Dependency Handling:** Subtasks explicitly reference data from previous steps when dependencies exist (e.g., "Using the account ID from the previous step...").

**Decomposition Strategies:**
- **Exact Strategy:** One subtask per application (enforces strict application boundaries, predictable and deterministic).
- **Flexible Strategy:** Logical decomposition based on workflow requirements (allows multiple subtasks per application, must alternate between different apps).

For detailed information on decomposition strategies, see the [Planning Strategies](../planning-strategies/module.md) module.

**Single vs. Multi-Application Handling:**
- **Single Application:** If only one application is involved, return the intent verbatim as a single subtask (no decomposition needed).
- **Multi-Application:** Decompose into subtasks based on the chosen strategy, ensuring all applications contribute meaningfully.

**Plan Execution Control:**
- **Progress Tracking:** The plan controller monitors each subtask's status (`not-started`, `in-progress`, `completed`).
- **Variable Management:** Data collected during execution is tracked and made available to subsequent subtasks.
- **Next Action Selection:** The controller determines which subtask to execute next based on progress, dependencies, and execution history.
- **Task Conclusion:** The controller decides when all subtasks are complete and the overall goal is achieved.

### How It Works
Task decomposition planning works through a structured three-phase process that integrates task analysis, decomposition, and execution control:

## Phase 1: Task Analysis

Before decomposition, the agent analyzes the task to understand its requirements and identify available resources:

**1.1 Task Classification**
The agent classifies the task to understand its characteristics:
- **Performs Update:** Does the task modify data or state?
- **Requires Memory:** Does the task need to access or store information in memory?
- **Requires Loop:** Does the task involve iterative operations?
- **Requires Location Search:** Does the task need geographic or location-based information?

**1.2 Application Matching**
The agent matches the user intent to available applications:
- Analyzes the intent against application descriptions and capabilities
- Considers application types: `web` (browser-based) or `api` (service-based)
- May leverage memory or historical patterns to improve matching
- Returns a list of relevant applications that can contribute to the goal

**1.3 Intent Refinement (Optional)**
For complex or ambiguous intents, especially in web applications:
- **Paraphrasing:** The agent may rephrase the intent to clarify requirements
- **Navigation Path Discovery:** For web apps, the agent may identify known efficient paths to accomplish the task

**1.4 Application Discovery**
Each application is characterized by:
- **Name and description:** What the application does
- **Type:** `web` (browser-based) or `api` (service-based)
- **URL:** Starting point for web applications (if applicable)

## Phase 2: Task Decomposition

The agent breaks down the goal into high-level subtasks using one of two strategies:

**2.1 Single Application Handling**
- **Rule:** If only one application is involved, return the intent verbatim as a single subtask
- **Rationale:** No decomposition needed when a single application can handle the entire task
- **Example:** "Star the top five most starred repos in Gitlab" → Single subtask assigned to Gitlab

**2.2 Multi-Application Decomposition**

**Exact Strategy (One Subtask Per Application):**
- When multiple applications are provided, generates exactly one subtask per application
- Enforces strict application boundaries
- Useful when each application has a distinct, well-defined role
- Example: 3 applications → exactly 3 subtasks
- **Mandatory Requirement:** All applications must be utilized, each gets exactly one subtask

**Flexible Strategy (Logical Decomposition):**
- Decomposes based on logical workflow requirements
- Allows multiple subtasks per application when needed
- **Alternating Constraint:** Subtasks must alternate between different applications (no consecutive same-app subtasks)
- More adaptable to complex workflows
- Example: May use App A → App B → App A if the workflow requires it
- **Application Selection:** Choose the most suitable application for each subtask based on capabilities

For comprehensive details on these strategies, including examples and best practices, see the [Planning Strategies](../planning-strategies/module.md) module.

**2.3 Decomposition Rules**

**Abstraction Level Control:**
- **High-Level Focus:** Subtasks describe "what" needs to be accomplished, not "how"
- **Avoid Low-Level Actions:** 
  - For web: avoid "click", "type", "enter", "scroll", "find element"
  - For API: avoid "call endpoint", "send HTTP request", "parse JSON/XML", "authenticate", "token", "payload"
- **Rationale:** Low-level actions are handled by specialized planners; decomposition focuses on goals

**Context & Dependency Handling:**
- **Self-Contained Descriptions:** Each subtask description must be clear and self-contained
- **Explicit Dependencies:** When a subtask depends on previous steps, explicitly reference the data needed
  - Example: "Using the account ID from the previous step, retrieve transaction history"
  - Example: "Summarize the article content found on 'TechNews Portal'"
- **User Context Preservation:** Personal pronouns and identifiers are preserved across subtasks
  - "my accounts" → "my accounts" (not "all accounts")
  - "I", "we", "our" are maintained throughout

**Answer Expectation Handling:**
- If the intent contains question words ("how much", "what is", "tell me", "calculate", etc.), ensure one subtask explicitly provides that answer
- The final subtask should deliver the response using the most relevant application

**Data Scope & Boundaries:**
- Avoid subtasks requiring extraction of excessively large data
- For operations on dynamic lists, use "for each" clauses in subtask descriptions

**2.4 Plan Generation**
The decomposition creates a structured plan with:
- **Thoughts:** Explanation of the decomposition strategy and how each application contributes
- **Task Decomposition:** List of subtasks, each with:
  - `task`: High-level description of what needs to be accomplished
  - `type`: `web` or `api`
  - `app`: Application name assigned to the subtask

## Phase 3: Plan Execution Control

A plan controller orchestrates the execution of the decomposed plan:

**3.1 Progress Tracking**
- Monitors each subtask's status: `not-started`, `in-progress`, `completed`
- Maintains execution history for each subtask
- Tracks overall plan progress

**3.2 Variable Management**
- Captures data and outputs from completed subtasks
- Makes variables available to subsequent subtasks
- Maintains a variables history for context

**3.3 Next Action Selection**
- Analyzes current state: completed subtasks, in-progress subtasks, execution history
- Determines which subtask to execute next based on:
  - Dependencies (prerequisites must be completed)
  - Progress status
  - Available variables
- Routes to appropriate executor:
  - `web` subtasks → Browser Planner Agent
  - `api` subtasks → API Planner Agent

**3.4 Execution & Adaptation**
- Each subtask is executed by specialized planners:
  - **Web Planner:** Handles browser interactions, UI navigation, form filling
  - **API Planner:** Handles service calls, data retrieval, programmatic operations
- The plan controller monitors execution results
- Adapts when obstacles arise:
  - Subtask failures trigger re-evaluation
  - New constraints may require plan adjustment
  - Execution history informs future decisions

**3.5 Task Conclusion**
- The controller decides when to conclude based on:
  - All subtasks completed
  - Goal achieved (even if not all subtasks completed)
  - Unrecoverable failure
- Final answer is synthesized from execution results
- Routes to Final Answer Agent to deliver the result

**Information Gathering:**
Effective task decomposition requires gathering relevant information before decomposition. The Task Analysis phase should include targeted information-seeking operations to discover available resources, tools, APIs, and constraints. For instance, an agent should first discover what tools and APIs are available before planning how to use them, ensuring the decomposition is grounded in actual capabilities rather than assumptions.

## When to Use This Pattern

### ✅ Use this pattern when:
- **Multi-application workflows:** The task requires coordinating multiple applications or services in a specific sequence.
- **Complex, multi-step goals:** The task requires a sequence of interdependent actions that must be discovered and coordinated across different systems.
- **Dynamic environments:** Conditions change during execution, requiring plan adaptation and re-decomposition.
- **Goal discovery needed:** The "how" to achieve the goal is not predetermined and must be discovered through analysis and decomposition.
- **Long-horizon tasks:** The task spans multiple steps where intermediate planning and coordination improve outcomes.
- **Type-aware execution:** The task involves both web-based interactions and API calls that require specialized handling.
- **Data flow between steps:** The task requires passing data or results from one application to another.

### ❌ Avoid this pattern when:
- **Single application tasks:** The task can be handled by a single application (use direct execution instead).
- **Fixed workflows suffice:** The solution path is well-understood and can be hardcoded as a workflow.
- **Simple, single-step tasks:** The task can be completed in one or two steps without needing decomposition.
- **Predictability is critical:** You need guaranteed, consistent behavior that fixed workflows provide.
- **Real-time constraints:** The overhead of analysis, decomposition, and coordination adds unacceptable latency for time-sensitive tasks.
- **No application coordination:** The task doesn't require multiple applications or services to work together.

### Decision Guidelines

**When to Use Planning:**
Use planning when the benefits of adaptability and goal discovery outweigh the costs of increased complexity and potential unpredictability. Consider:
- **Task Complexity:** More complex = more benefit from planning
- **Environment Variability:** More variable = more need for adaptive planning
- **Solution Path:** Unknown = use planning, known = use workflow

**Choosing Decomposition Strategy:**

For detailed guidance on choosing between Exact and Flexible strategies, including when to use each and their characteristics, see the [Planning Strategies](../planning-strategies/module.md) module.

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

Task decomposition planning is essential for autonomous systems that need to coordinate multiple applications or services to achieve complex goals.

- **Multi-Application Workflows:** Coordinate workflows that span multiple applications, such as finding information in a web portal, processing it through an API service, and posting results to social media.

- **Business Process Automation:** Decompose complex workflows like employee onboarding that require coordinating HR systems, email services, file storage, and access management applications.

- **Data Pipeline Orchestration:** Break down data processing tasks that require extracting data from one service, transforming it through another, and loading it into a third system.

- **Content Generation Workflows:** Formulate plans for complex outputs like research reports that require gathering information from web sources, analyzing it through AI services, and structuring it in document management systems.

- **Customer Support Automation:** Create systematic plans for multi-step problem resolution that coordinate ticketing systems, knowledge bases, communication platforms, and CRM systems.

- **E-commerce Operations:** Decompose tasks like "research product, compare prices, purchase, and update wishlist" across shopping sites, price comparison services, payment systems, and user profile services.

- **Project Management Automation:** Break down high-level projects into task sequences that coordinate project management tools, communication platforms, file storage, and reporting systems.

## Implementation

### Core Components

**Three-Phase Architecture:**

**Phase 1: Task Analyzer Agent**
```python
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class TaskAttributes(BaseModel):
    """Task classification attributes."""
    thoughts: List[str]
    performs_update: bool
    requires_memory: bool
    requires_loop: bool
    requires_location_search: bool

class AppMatch(BaseModel):
    """Application matching result."""
    thoughts: str
    relevant_apps: List[str]

class TaskAnalyzerOutput(BaseModel):
    """Output from task analysis phase."""
    attrs: TaskAttributes
    paraphrased_intent: Optional[str] = None
    navigation_paths: Optional[dict] = None

class TaskAnalyzerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.classify_task = self._setup_classifier()
        self.match_apps = self._setup_app_matcher()
        self.paraphrase = self._setup_paraphrase()
        self.navigation_paths = self._setup_navigation_paths()
    
    async def analyze(self, intent: str, available_apps: List[dict]) -> TaskAnalyzerOutput:
        """Analyze task and match to applications."""
        # Classify task characteristics
        attrs = await self.classify_task.ainvoke({"task": intent})
        
        # Match intent to applications
        app_match = await self.match_apps.ainvoke({
            "intent": intent,
            "available_apps": available_apps
        })
        
        # Optional: Paraphrase intent for clarity
        paraphrased = None
        if attrs.performs_update == False:
            paraphrased = await self.paraphrase.ainvoke({"task": intent})
        
        # Optional: Discover navigation paths for web apps
        nav_paths = None
        if attrs.performs_update == False:
            nav_paths = await self.navigation_paths.ainvoke({"task": intent})
        
        return TaskAnalyzerOutput(
            attrs=attrs,
            paraphrased_intent=paraphrased.rephrased_intent if paraphrased else None,
            navigation_paths=nav_paths
        )
```

**Phase 2: Task Decomposition Agent**
```python
from typing import List, Literal
from pydantic import BaseModel, Field

class DecomposedTask(BaseModel):
    """A single decomposed subtask."""
    task: str = Field(..., description="High-level task description")
    app: str = Field(..., description="Application name")
    type: Literal['web', 'api'] = Field(..., description="Task type")

class TaskDecompositionPlan(BaseModel):
    """Complete decomposition plan."""
    thoughts: str = Field(..., description="Decomposition strategy explanation")
    task_decomposition: List[DecomposedTask] = Field(..., description="List of subtasks")
    
    def format_as_list(self) -> List[str]:
        """Format subtasks as list for display."""
        return [
            f"{task.task} (type='{task.type}', app='{task.app}')"
            for task in self.task_decomposition
        ]

class TaskDecompositionAgent:
    def __init__(self, llm, strategy: Literal['exact', 'flexible'] = 'exact'):
        self.llm = llm
        self.strategy = strategy
    
    async def decompose(
        self, 
        intent: str, 
        applications: List[dict],
        current_datetime: str
    ) -> TaskDecompositionPlan:
        """Decompose task into subtasks based on strategy."""
        # Single app: return intent as-is (no decomposition)
        if len(applications) == 1:
            return TaskDecompositionPlan(
                thoughts="Single application, no decomposition needed",
                task_decomposition=[
                    DecomposedTask(
                        task=intent,
                        app=applications[0]["name"],
                        type=applications[0]["type"]
                    )
                ]
            )
        
        # Multi-app: use strategy-based decomposition
        prompt = self._build_prompt(intent, applications, self.strategy, current_datetime)
        response = await self.llm.ainvoke(prompt)
        return TaskDecompositionPlan.model_validate_json(response.content)
    
    def _build_prompt(self, intent: str, apps: List[dict], strategy: str, datetime: str) -> str:
        """Build decomposition prompt based on strategy."""
        # Prompt includes:
        # - Intent
        # - Applications list with descriptions
        # - Current datetime
        # - Strategy-specific instructions (exact vs flexible)
        # - Examples demonstrating the strategy
        # - Rules for abstraction level, context preservation, dependencies
        pass
```

**Phase 3: Plan Controller Agent**
```python
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class PlanControllerOutput(BaseModel):
    """Output from plan controller."""
    thoughts: List[str] = Field(..., description="Controller reasoning")
    subtasks_progress: List[Literal['completed', 'not-started', 'in-progress']] = Field(
        ..., description="Progress status for each subtask"
    )
    next_subtask: str = Field(..., description="Next subtask to execute")
    next_subtask_type: Literal['web', 'api', None] = Field(..., description="Type of next subtask")
    next_subtask_app: str = Field(..., description="Application for next subtask")
    conclude_task: bool = Field(False, description="Whether to conclude the task")
    conclude_final_answer: str = Field("", description="Final answer if concluding")

class PlanControllerAgent:
    def __init__(self, llm):
        self.llm = llm
    
    async def control(
        self,
        plan: TaskDecompositionPlan,
        execution_history: List[dict],
        variables_history: List[dict],
        subtasks_progress: List[str]
    ) -> PlanControllerOutput:
        """Determine next action based on plan progress."""
        prompt = self._build_prompt(
            plan, execution_history, variables_history, subtasks_progress
        )
        response = await self.llm.ainvoke(prompt)
        return PlanControllerOutput.model_validate_json(response.content)
    
    def _build_prompt(
        self,
        plan: TaskDecompositionPlan,
        history: List[dict],
        variables: List[dict],
        progress: List[str]
    ) -> str:
        """Build control prompt with plan, history, and progress."""
        # Prompt includes:
        # - Current decomposition plan
        # - Execution history for each subtask
        # - Variables available from completed subtasks
        # - Current progress status
        # - Instructions for selecting next subtask or concluding
        pass
```

### Complete Example: Three-Phase Task Decomposition Planning

```python
import asyncio
from datetime import datetime

# Example: "Find article about AI, summarize it, and share on social media"
intent = "Find article about AI, summarize it, and share on social media"

# Phase 1: Task Analysis
async def phase1_task_analysis(intent: str):
    """Analyze task and match to applications."""
    analyzer = TaskAnalyzerAgent(llm)
    
    # Classify task characteristics
    attrs = await analyzer.classify_task.ainvoke({"task": intent})
    # Output: TaskAttributes(performs_update=False, requires_memory=False, ...)
    
    # Match to available applications
    available_apps = [
        {"name": "News Portal", "description": "Web portal for technology news articles"},
        {"name": "Summarizer", "description": "Service providing text summarization capabilities"},
        {"name": "Social Media", "description": "Service for posting updates to social media"}
    ]
    
    app_match = await analyzer.match_apps.ainvoke({
        "intent": intent,
        "available_apps": available_apps
    })
    # Output: AppMatch(relevant_apps=["News Portal", "Summarizer", "Social Media"])
    
    # Get matched applications with full details
    matched_apps = [
        {"name": "News Portal", "type": "web", "url": "https://news.example.com"},
        {"name": "Summarizer", "type": "api"},
        {"name": "Social Media", "type": "api"}
    ]
    
    return matched_apps

# Phase 2: Task Decomposition
async def phase2_task_decomposition(intent: str, applications: list):
    """Decompose task into subtasks."""
    decomposer = TaskDecompositionAgent(llm, strategy="exact")
    
    current_datetime = datetime.now().isoformat()
    plan = await decomposer.decompose(intent, applications, current_datetime)
    
    return plan

# Phase 3: Plan Execution Control
async def phase3_plan_control(plan: TaskDecompositionPlan, execution_history: list):
    """Control plan execution."""
    controller = PlanControllerAgent(llm)
    
    # Track variables from completed subtasks
    variables_history = []  # e.g., [{"article_content": "..."}, {"summary": "..."}]
    subtasks_progress = ["not-started"] * len(plan.task_decomposition)
    
    # Controller determines next action
    control_output = await controller.control(
        plan, execution_history, variables_history, subtasks_progress
    )
    
    return control_output

# Complete workflow
async def main():
    # Phase 1: Analyze
    matched_apps = await phase1_task_analysis(intent)
    print(f"Matched applications: {[app['name'] for app in matched_apps]}")
    
    # Phase 2: Decompose
    plan = await phase2_task_decomposition(intent, matched_apps)
    print(f"\nDecomposition Plan:")
    print(f"Thoughts: {plan.thoughts}")
    for i, subtask in enumerate(plan.task_decomposition, 1):
        print(f"{i}. {subtask.task} ({subtask.type}, {subtask.app})")
    
    # Phase 3: Execute and control
    execution_history = []
    for subtask in plan.task_decomposition:
        # Execute subtask (simplified)
        result = f"Executed: {subtask.task}"
        execution_history.append({
            "subtask": subtask.task,
            "result": result,
            "status": "completed"
        })
        
        # Controller determines next action
        control = await phase3_plan_control(plan, execution_history)
        if control.conclude_task:
            print(f"\nTask complete! Final answer: {control.conclude_final_answer}")
            break
        print(f"\nNext: {control.next_subtask}")

if __name__ == "__main__":
    asyncio.run(main())

# Output:
# Matched applications: ['News Portal', 'Summarizer', 'Social Media']
#
# Decomposition Plan:
# Thoughts: Three distinct operations across three applications...
# 1. Find and extract the content of the most recent article about 'AI' from News Portal (web, News Portal)
# 2. Generate a brief summary of the AI article content (api, Summarizer)
# 3. Post the generated article summary to Social Media (api, Social Media)
#
# Next: Find and extract the content of the most recent article about 'AI' from News Portal
# ...
# Task complete! Final answer: Successfully found, summarized, and shared the AI article.
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

- **Core Concept:** Task decomposition planning enables agents to analyze complex goals, break them down into high-level subtasks, assign each to appropriate applications, and orchestrate their execution through a three-phase process: Task Analysis → Task Decomposition → Plan Control.

- **Three-Phase Architecture:**
  - **Task Analysis:** Classify task characteristics, match intent to applications, and refine understanding before decomposition.
  - **Task Decomposition:** Break down goals into high-level subtasks with proper abstraction, context preservation, and dependency handling.
  - **Plan Control:** Orchestrate execution, track progress, manage variables, and determine when to conclude.

- **Single vs. Multi-Application:** 
  - **Single Application:** Return intent verbatim as one subtask (no decomposition needed).
  - **Multi-Application:** Decompose based on chosen strategy, ensuring all applications contribute meaningfully.

- **Decomposition Strategies:** Choose the right strategy based on task characteristics. See the [Planning Strategies](../planning-strategies/module.md) module for detailed guidance:
  - **Exact Strategy:** One subtask per application - predictable, clear boundaries, good for multi-domain tasks where each app has a distinct role.
  - **Flexible Strategy:** Logical decomposition - adaptable, supports complex workflows, allows multiple operations per app (with alternating constraint).

- **Abstraction Level Control:** Subtasks describe "what" needs to be accomplished (high-level goals), not "how" (low-level actions like "click", "type", "call endpoint"). Low-level actions are handled by specialized planners.

- **Context & Dependency Management:** 
  - Preserve user context (pronouns, identifiers) across subtasks.
  - Explicitly reference data from previous steps when dependencies exist.
  - Maintain self-contained subtask descriptions while handling data flow.

- **Type-Aware Assignment:** Classify subtasks as `web` (browser interactions) or `api` (service calls) to enable specialized execution by appropriate planners.

- **Plan Execution Control:** A plan controller tracks progress, manages variables between subtasks, selects next actions based on dependencies and execution history, and determines when to conclude the overall task.

- **Best Practice:** 
  - Use task analysis to gather relevant information about available applications before decomposition.
  - For single-application tasks, skip decomposition and return intent verbatim.
  - Choose decomposition strategy based on whether you need predictability (exact) or flexibility (flexible). See [Planning Strategies](../planning-strategies/module.md) for detailed guidance.

- **Common Pitfall:** 
  - Over-decomposing simple tasks adds unnecessary complexity; use direct execution for single-application tasks.
  - Including low-level actions in subtasks violates abstraction principles; keep subtasks at goal level.
  - Failing to preserve user context (e.g., "my accounts" → "all accounts") breaks user expectations.

- **Performance Note:** Task decomposition planning adds latency and cost through analysis, decomposition, and coordination phases, but significantly improves outcomes for complex, multi-step tasks requiring coordination across multiple applications. The overhead is justified when the task genuinely requires multi-application coordination.

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

