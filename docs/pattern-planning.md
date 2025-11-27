# Planning

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
- **Goal Decomposition:** Planning breaks high-level goals into discrete, executable sub-tasks that can be sequenced logically.
- **State Space Navigation:** The agent must understand initial state, goal state, and the actions that transition between states.
- **Adaptive Replanning:** Plans are not rigid; agents must adapt when obstacles arise or new information becomes available.
- **Dependency Management:** Planning must account for task dependencies, ensuring prerequisites are completed before dependent tasks.

### How It Works
Planning works through a structured process: (1) Goal Analysis—the agent understands the desired outcome and constraints, (2) State Assessment—it evaluates the current state and available resources, (3) Plan Generation—it formulates a sequence of actions to bridge the gap between current and goal states, (4) Plan Execution—it executes the plan step by step, and (5) Monitoring and Adaptation—it monitors progress and adapts the plan when obstacles arise or conditions change.

The planning process can be explicit, where the agent generates a detailed plan document before execution, or implicit, where planning happens dynamically during execution. Explicit planning is useful for complex, multi-step tasks where the full sequence needs to be understood upfront. Implicit planning is more reactive, generating the next step based on current state without a full plan document.

Frameworks support planning through various mechanisms. CrewAI enables agents to create plans as part of their task execution. Google DeepResearch demonstrates planning through multi-step research plans that are generated, reviewed, and executed iteratively. LangGraph and LangChain support planning through state management and conditional workflows that can represent planned sequences.

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
Use planning when the benefits of adaptability and goal discovery outweigh the costs of increased complexity and potential unpredictability. Consider: the complexity of the goal (more complex = more benefit from planning), the variability of the environment (more variable = more need for adaptive planning), and whether the solution path is known (unknown = use planning, known = use workflow). Be aware that planning adds latency and cost, and can introduce unpredictability. For critical systems requiring guaranteed behavior, consider hybrid approaches that combine planning with fixed workflow fallbacks.

## Practical Applications & Use Cases

Planning is a core computational process in autonomous systems, enabling agents to synthesize sequences of actions to achieve specified goals.

- **Business Process Automation:** Decompose complex workflows like employee onboarding into sequenced sub-tasks with dependencies.
- **Robotics and Navigation:** Generate paths or action sequences to transition from initial to goal state while optimizing for metrics.
- **Content Generation:** Formulate plans for complex outputs like research reports with distinct phases for gathering, summarizing, and structuring.
- **Customer Support:** Create systematic plans for multi-step problem resolution including diagnosis, solution implementation, and escalation.
- **Project Management:** Break down high-level projects into task sequences with dependencies and resource allocation.

## Implementation

### Prerequisites
```bash
pip install crewai langchain langchain-openai
# or
pip install google-adk
```

### Basic Example
```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4-turbo")

# Planning agent
planner_agent = Agent(
    role='Project Planner',
    goal='Create and execute plans for complex tasks',
    backstory='You are an expert at breaking down complex goals into actionable plans.',
    llm=llm,
    verbose=True
)

# Task with planning requirement
task = Task(
    description="""1. Create a detailed plan for organizing a team offsite.
    2. Execute the plan step by step.""",
    expected_output="A plan and execution report",
    agent=planner_agent
)

# Execute
crew = Crew(
    agents=[planner_agent],
    tasks=[task],
    process=Process.sequential
)

result = crew.kickoff()
print(result)
```

**Explanation:**
This example demonstrates planning using CrewAI. The agent is instructed to first create a plan, then execute it. The planning happens as part of the agent's task execution, where it breaks down the complex goal into manageable steps before proceeding.

### Advanced Example
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict
import json

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class PlanningAgent:
    def __init__(self):
        self.llm = llm
        self.plan_history = []
    
    def generate_plan(self, goal: str, constraints: Dict) -> Dict:
        """Generate an initial plan for a goal."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a planning expert. Create a detailed plan.
            Return JSON with:
            - "steps": list of {"id": int, "action": str, "dependencies": [int]}
            - "estimated_duration": str
            - "resources_needed": list"""),
            ("user", f"Goal: {goal}\nConstraints: {constraints}")
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        plan = json.loads(response.content)
        self.plan_history.append({"goal": goal, "plan": plan})
        return plan
    
    def adapt_plan(self, current_plan: Dict, obstacle: str) -> Dict:
        """Adapt plan when obstacles arise."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Adapt the plan to handle obstacles.
            Return updated plan JSON."""),
            ("user", f"Current plan: {json.dumps(current_plan)}\nObstacle: {obstacle}")
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        adapted_plan = json.loads(response.content)
        return adapted_plan
    
    def execute_step(self, step: Dict, context: Dict) -> Dict:
        """Execute a single plan step."""
        # Simulate step execution
        return {
            "step_id": step["id"],
            "status": "completed",
            "result": f"Executed: {step['action']}",
            "context": context
        }

# Usage
agent = PlanningAgent()
plan = agent.generate_plan(
    goal="Organize team offsite for 30 people",
    constraints={"budget": 10000, "location": "Lisbon", "dates": "Q2 2025"}
)

print("Generated Plan:")
print(json.dumps(plan, indent=2))

# Adapt if obstacle arises
if obstacle_detected:
    plan = agent.adapt_plan(plan, "Preferred venue unavailable")
```

**Explanation:**
This advanced example implements a PlanningAgent class with plan generation, adaptation, and execution capabilities. It demonstrates structured plan representation with dependencies, obstacle handling through adaptive replanning, and plan history tracking. This shows production-ready planning with JSON-structured plans and adaptation mechanisms.

### Framework-Specific Examples

#### CrewAI
```python
from crewai import Agent, Task, Crew

planner = Agent(
    role='Strategic Planner',
    goal='Create comprehensive plans',
    backstory='Expert in strategic planning',
    verbose=True
)

planning_task = Task(
    description="""Create a detailed plan for: {goal}
    Then execute the plan.""",
    agent=planner
)

crew = Crew(agents=[planner], tasks=[planning_task])
result = crew.kickoff(inputs={"goal": "Launch new product"})
```

#### Google DeepResearch
```python
# DeepResearch demonstrates planning through multi-step research plans
# The system:
# 1. Deconstructs user prompt into research plan
# 2. Presents plan for user review/modification
# 3. Executes iterative search-and-analysis loop
# 4. Dynamically formulates queries based on gathered information
# 5. Consolidates findings into structured summary

# Planning is implicit in the research pipeline structure
```

## Key Takeaways

- **Core Concept:** Planning enables agents to formulate sequences of actions to achieve goals, breaking complex tasks into manageable steps.
- **Best Practice:** Use explicit planning for complex, long-horizon tasks; use implicit planning for reactive, adaptive scenarios.
- **Common Pitfall:** Over-planning simple tasks adds unnecessary complexity; use fixed workflows when the solution path is known.
- **Performance Note:** Planning adds latency and cost but improves outcomes for complex, multi-step tasks requiring coordination.

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

