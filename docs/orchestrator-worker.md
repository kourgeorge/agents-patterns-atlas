# Pattern: Orchestrator-Worker (Coordinator)

## Motivation

A conductor coordinates an orchestra, assigning parts to different sections while maintaining the overall vision. 
A project manager breaks down a complex project, delegates specialized tasks to team members, and synthesizes their contributions into a cohesive result. 
The Orchestrator-Worker pattern mirrors this: a central coordinator breaks down complex goals, delegates to specialized workers, and integrates their outputs into a unified solution.

## Pattern Overview
**What it is:** A central agent, often called the Coordinator or Lead Agent, dynamically breaks down a complex goal into smaller subtasks, delegates them to specialized worker agents, and synthesizes the workers' outputs to produce the final result.

**When to use:** For complex tasks that cannot be handled by a single agent, especially when the required subtasks are unpredictable and dynamic, rather than fixed. It's the most common pattern for complex tasks.

**Why it matters:** It enables **specialization** (assigning tasks to dedicated agents with specific skills), **parallelization** (often running subtasks concurrently for speed), and **resilience** (isolating failures to individual agents).

The Orchestrator-Worker pattern, also known as the "Coordinator pattern", represents one of the most fundamental and widely-used multi-agent architectures. 
Unlike rigid, predefined workflows, this pattern enables dynamic task decomposition where the orchestrator agent analyzes the high-level goal and determines the necessary subtasks at runtime. 
This flexibility makes it particularly powerful for handling complex, unpredictable tasks that require diverse expertise.
The pattern's strength lies in its ability to leverage specialization. 
Each worker agent can be optimized for a specific domain—research, writing, coding, analysis, or review—resulting in higher quality outputs than a single generalist agent could produce. 
The orchestrator acts as a strategic coordinator, managing the overall workflow, handling dependencies between subtasks, and synthesizing results into a coherent final output.
This pattern is especially valuable for long-horizon tasks where the orchestrator can maintain high-level context and goals while workers focus on specific execution details. The separation of concerns also enables better context management, as the orchestrator can isolate context for specific agents, preventing information overload and improving efficiency.

### Key Concepts

- **Orchestrator (Coordinator/Lead Agent):** The central agent that receives high-level goals, decomposes them into subtasks, delegates to workers, and synthesizes results.
- **Worker Agents:** Specialized agents that execute specific subtasks using domain expertise and specialized tools.
- **Dynamic Task Decomposition:** The orchestrator determines subtasks at runtime based on the input, rather than using fixed workflows.
- **Specialization:** Each worker agent focuses on a specific domain or capability, improving overall system effectiveness.
- **Parallelization:** Independent subtasks can be executed concurrently by different workers, reducing overall latency.
- **Hierarchical Organization:** Workers can themselves become orchestrators for sub-subtasks, creating nested multi-agent structures.
- **Context Isolation:** The orchestrator can manage and isolate context for specific agents, improving efficiency and preventing information overload.

### How It Works: Step-by-step Explanation

1. **Receive and Decompose:** The Orchestrator receives a high-level user request. It uses an AI model for reasoning to analyze and dynamically break the request into smaller, manageable pieces (subtasks).
2. **Delegate:** The Orchestrator dispatches each subtask to the most appropriate specialized worker agent. The Orchestrator must provide clear, non-overlapping objectives to the subagents to avoid duplication of work or gaps in coverage.
3. **Execute and Return:** Worker agents execute their specific task, often using specialized tools (e.g., querying a database or calling an API). They return their findings to the Orchestrator.
4. **Synthesize:** The Orchestrator integrates the outputs from all worker agents to compile and return the final, coherent response to the user.

## When to Use This Pattern

### ✅ Use when:

- **Complex, multifaceted tasks:** Tasks that require diverse expertise or multiple distinct capabilities that no single agent can handle effectively.
- **Dynamic task requirements:** When subtasks cannot be predetermined and must be determined at runtime based on the input.
- **Specialization needed:** Different aspects of the task require specialized knowledge or skills (e.g., research, writing, coding, review).
- **Parallel processing possible:** Multiple independent sub-tasks can be executed concurrently by different agents.
- **Long-horizon tasks:** Tasks that span many steps where maintaining high-level context is essential.
- **Context window limitations:** Tasks where the full context exceeds a single agent's context window capacity.
- **Resilience requirements:** When isolating failures to individual agents is important for system reliability.

### ❌ Avoid when:

- **Simple single-agent tasks:** Tasks that can be effectively handled by a single, well-configured agent.
- **Fixed workflows:** When tasks follow a rigid, predetermined sequence that doesn't benefit from dynamic decomposition.
- **Tight coupling required:** Tasks where sub-tasks are so tightly coupled that coordination overhead exceeds benefits.
- **Low-latency requirements:** When the overhead of multi-agent coordination and communication is prohibitive.
- **Resource constraints:** When computational or cost constraints (increased model calls) make multiple agents impractical.
- **Minimal complexity:** When the added complexity of multi-agent coordination doesn't provide sufficient benefit.

### Decision Guidelines
Use the Orchestrator-Worker pattern when the benefits of specialization, parallelization, and dynamic task decomposition outweigh the added complexity and coordination overhead. 
This pattern is ideal for complex tasks where subtasks are unpredictable and require diverse expertise. Consider: task complexity (complex = orchestrator-worker), specialization needs (diverse expertise = multiple workers), and dynamic requirements (unpredictable = dynamic decomposition). 
However, be aware of trade-offs: this pattern increases model calls, which raises latency, token throughput, and operational costs compared to a single-agent system. 
For simple or tightly-coupled tasks, a single agent or simpler workflow may be more efficient.


## Practical Applications & Use Cases

The Orchestrator-Worker pattern is the most common pattern for complex LLM-based agentic tasks, enabling sophisticated systems that can handle multifaceted problems.

### General Use Cases

- **Customer Service:** A coordinator agent analyzes a customer's request (e.g., order status, refund, technical support) and routes the task to the appropriate specialized agent (billing specialist, technical support agent, product information agent).
- **Research and Report Generation:** An orchestrator breaks down research into sub-topics, delegates to specialized researcher agents who work in parallel, then a writer agent synthesizes findings into a comprehensive report.
- **Content Creation Workflows:** A planner agent creates an outline, writer agents draft sections in parallel, and an editor agent reviews and refines the content for quality and consistency.
- **Multi-file Software Projects:** An orchestrator analyzes requirements, identifies affected files, and delegates changes to specialized agents (frontend, backend, database, testing).

## Modern Framework Patterns

### Role-Based Specialization (ChatDev/MetaGPT Style)

Modern orchestrator-worker systems leverage role-based specialization, where each worker agent has a well-defined role with specialized prompts and Standard Operating Procedures (SOPs). 
This approach, demonstrated by ChatDev and MetaGPT, enables agents to achieve expert-level performance in their domains.

**Example Role Structure (MetaGPT-style):**

- **Architect Agent:** Analyzes requirements, designs system architecture, creates technical specifications
- **Programmer Agent:** Implements code based on specifications, writes unit tests
- **Reviewer Agent:** Reviews code for quality, correctness, and adherence to standards
- **Tester Agent:** Designs and executes test cases, reports bugs

### Dynamic Agent Orchestration (AgentVerse Style)

Dynamic orchestration allows the system to adapt team composition based on task requirements. The orchestrator can spawn new specialist agents as needed and release them when tasks complete, optimizing resource usage.

Key Principles:

- **Adaptive Team Composition:** Team structure evolves during problem-solving
- **Agent Lifecycle Management:** Agents are created, activated, and released dynamically
- **Emergent Behaviors:** System exhibits emergent social behaviors (leadership, cooperation) without explicit programming
- **Resource Optimization:** System optimizes agent allocation based on current needs

### Managed Conversations (AutoGen Style)

Managed conversations enable flexible communication patterns where orchestrators coordinate structured dialogues between agents. This approach supports complex problem-solving through multi-turn agent interactions.

Key Principles:

- **Flexible Communication Patterns:** Developers define custom orchestration patterns
- **Structured Dialogues:** Agents engage in structured conversations with clear protocols
- **Multi-Turn Interactions:** Complex problems solved through iterative agent dialogues
- **Result Integration:** Orchestrator synthesizes outputs from multiple agent interactions

### Central Controller Pattern (HuggingGPT Style)

A central LLM controller orchestrates multiple specialized models or agents, planning subtasks, delegating to appropriate specialists, and integrating results. This pattern transforms LLMs into general-purpose orchestrators.

**Key Principles:**
- **LLM-as-Manager:** Language model serves as orchestrator, planning and coordinating specialists
- **Tool/Model Delegation:** Controller delegates to specialized models, APIs, or tools as needed
- **Handoff Protocols:** Clear protocols ensure results pass correctly between agents
- **Global Planning:** Controller creates global plans optimizing action sequences

## Implementation

### Prerequisites
```bash
pip install langchain langchain-openai langgraph
# or
pip install google-adk
# or
pip install crewai  # Multi-agent orchestration framework
```

??? "Basic Example: Orchestrator-Worker Pattern"

    This example demonstrates a basic orchestrator-worker system where the orchestrator dynamically decomposes tasks and delegates to specialized workers:

    ```python
    from langchain_openai import ChatOpenAI
    from langgraph.graph import StateGraph, END
    from typing import TypedDict, List, Dict
    import json

    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    class OrchestratorState(TypedDict):
        goal: str
        plan: str
        subtasks: List[Dict]
        worker_results: Dict[str, str]
        final_output: str

    def orchestrator_decompose(state: OrchestratorState) -> OrchestratorState:
        """Orchestrator receives goal and decomposes into subtasks."""
        goal = state["goal"]
        
        # Use LLM to dynamically create a plan and break down into subtasks
        decomposition_prompt = f"""You are an orchestrator agent. Analyze the following goal and break it down into specific, non-overlapping subtasks.

    Goal: {goal}

    For each subtask, determine:
    1. The subtask description
    2. The type of worker needed (research, write, code, analyze, review)
    3. What information is needed as input
    4. What output is expected

    Return a JSON list of subtasks with keys: description, worker_type, input_needed, expected_output."""
        
        response = llm.invoke(decomposition_prompt)
        subtasks = json.loads(response.content)
        
        # Save plan to state (for recitation pattern)
        plan = f"Goal: {goal}\nSubtasks: {len(subtasks)}\n" + "\n".join([f"- {t['description']}" for t in subtasks])
        
        return {
            **state,
            "plan": plan,
            "subtasks": subtasks,
            "worker_results": {}
        }

    def research_worker(state: OrchestratorState) -> OrchestratorState:
        """Specialized research worker agent."""
        # Get current subtask
        current_subtask = state["subtasks"][0] if state["subtasks"] else None
        if not current_subtask or current_subtask["worker_type"] != "research":
            return state
        
        research_prompt = f"""You are a research specialist. Conduct research on the following topic:
        
    {current_subtask['input_needed']}

    Provide comprehensive findings with key points, sources, and relevant information."""
        
        result = llm.invoke(research_prompt)
        
        worker_results = state.get("worker_results", {})
        worker_results["research"] = result.content
        
        # Remove completed subtask
        remaining_subtasks = state["subtasks"][1:]
        
        return {
            **state,
            "worker_results": worker_results,
            "subtasks": remaining_subtasks
        }

    def write_worker(state: OrchestratorState) -> OrchestratorState:
        """Specialized writing worker agent."""
        current_subtask = state["subtasks"][0] if state["subtasks"] else None
        if not current_subtask or current_subtask["worker_type"] != "write":
            return state
        
        # Get research results
        research_results = state["worker_results"].get("research", "")
        
        write_prompt = f"""You are a writing specialist. Based on the following research, write a comprehensive summary:
        
    Research Findings:
    {research_results}

    Write a clear, well-structured summary that synthesizes the key information."""
        
        result = llm.invoke(write_prompt)
        
        worker_results = state["worker_results"]
        worker_results["write"] = result.content
        
        remaining_subtasks = state["subtasks"][1:]
        
        return {
            **state,
            "worker_results": worker_results,
            "subtasks": remaining_subtasks,
            "final_output": result.content
        }

    def orchestrator_synthesize(state: OrchestratorState) -> OrchestratorState:
        """Orchestrator synthesizes all worker results into final output."""
        goal = state["goal"]
        worker_results = state["worker_results"]
        plan = state.get("plan", "")
        
        synthesis_prompt = f"""You are an orchestrator agent. Synthesize the following worker results into a final, coherent response to the original goal.

    Original Goal: {goal}

    Plan:
    {plan}

    Worker Results:
    {json.dumps(worker_results, indent=2)}

    Create a comprehensive final output that integrates all worker contributions and directly addresses the original goal."""
        
        result = llm.invoke(synthesis_prompt)
        
        return {
            **state,
            "final_output": result.content
        }

    def route_to_worker(state: OrchestratorState) -> str:
        """Route to appropriate worker based on current subtask."""
        if not state["subtasks"]:
            return "synthesize"
        
        worker_type = state["subtasks"][0]["worker_type"]
        if worker_type == "research":
            return "research_worker"
        elif worker_type == "write":
            return "write_worker"
        else:
            return "synthesize"

    # Build graph
    graph = StateGraph(OrchestratorState)
    graph.add_node("orchestrator", orchestrator_decompose)
    graph.add_node("research_worker", research_worker)
    graph.add_node("write_worker", write_worker)
    graph.add_node("synthesize", orchestrator_synthesize)

    graph.set_entry_point("orchestrator")
    graph.add_conditional_edges("orchestrator", route_to_worker)
    graph.add_edge("research_worker", "write_worker")
    graph.add_conditional_edges("write_worker", route_to_worker)
    graph.add_edge("synthesize", END)

    # Execute
    result = graph.invoke({"goal": "Create a comprehensive report on renewable energy trends"})
    print(result["final_output"])
    ```

**Explanation:**
This example demonstrates the core orchestrator-worker pattern: the orchestrator dynamically decomposes the goal into subtasks, delegates to specialized workers (research, writing), and synthesizes the results. The orchestrator maintains the plan and coordinates the workflow, while workers focus on their specialized domains.

??? "Advanced Example: Hierarchical Orchestrator with Context Management"

    This advanced example shows nested orchestrators and context management using external memory:

    ```python
    from pathlib import Path
    from typing import Dict, List
    import json

    class HierarchicalOrchestrator:
        def __init__(self, workspace_dir: str = "./workspace"):
            self.workspace = Path(workspace_dir)
            self.workspace.mkdir(exist_ok=True)
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
            self.plan_file = self.workspace / "orchestrator_plan.md"
        
        def save_plan_to_memory(self, goal: str, plan: str):
            """Save plan to external memory before spawning subagents (context management)."""
            self.plan_file.write_text(f"# Orchestrator Plan\n\nGoal: {goal}\n\n{plan}")
            return f"Plan saved to {self.plan_file}. Use read_plan() to retrieve."
        
        def read_plan(self) -> str:
            """Read plan from external memory (recitation pattern)."""
            if self.plan_file.exists():
                return self.plan_file.read_text()
            return "No plan found."
        
        def decompose_with_planning(self, goal: str) -> Dict:
            """Orchestrator creates plan and decomposes goal."""
            # Create comprehensive plan
            plan_prompt = f"""You are a lead orchestrator agent. Analyze this goal and create a strategic plan:

    Goal: {goal}

    Create a detailed plan that includes:
    1. High-level strategy
    2. Required subtasks
    3. Dependencies between subtasks
    4. Required worker types
    5. Expected outcomes

    Return as structured plan."""
            
            plan_response = self.llm.invoke(plan_prompt)
            plan = plan_response.content
            
            # Save plan to memory (context management)
            self.save_plan_to_memory(goal, plan)
            
            # Decompose into subtasks
            decomposition_prompt = f"""Based on this plan, break down into specific subtasks:

    Plan:
    {plan}

    Create a list of subtasks with clear, non-overlapping objectives."""
            
            decomposition_response = self.llm.invoke(decomposition_prompt)
            
            # Parse subtasks (simplified)
            subtasks = self._parse_subtasks(decomposition_response.content)
            
            return {
                "goal": goal,
                "plan": plan,
                "subtasks": subtasks
            }
        
        def delegate_to_worker(self, subtask: Dict, context: Dict) -> str:
            """Delegate subtask to appropriate worker with isolated context."""
            worker_type = subtask.get("worker_type", "general")
            
            # Isolate context for this worker (only relevant information)
            worker_context = {
                "subtask": subtask,
                "relevant_info": context.get("relevant_info", ""),
                "goal": context.get("goal", "")
            }
            
            # Route to specialized worker
            if worker_type == "research":
                return self._research_worker(worker_context)
            elif worker_type == "write":
                return self._write_worker(worker_context)
            elif worker_type == "code":
                return self._code_worker(worker_context)
            else:
                return self._general_worker(worker_context)
        
        def _research_worker(self, context: Dict) -> str:
            """Specialized research worker."""
            prompt = f"""You are a research specialist. Conduct research on:

    {context['subtask']['description']}

    Goal context: {context['goal']}

    Provide comprehensive research findings."""
            
            result = self.llm.invoke(prompt)
            return result.content
        
        def _write_worker(self, context: Dict) -> str:
            """Specialized writing worker."""
            prompt = f"""You are a writing specialist. Write:

    {context['subtask']['description']}

    Based on: {context.get('relevant_info', '')}

    Create well-structured, clear content."""
            
            result = self.llm.invoke(prompt)
            return result.content
        
        def _code_worker(self, context: Dict) -> str:
            """Specialized coding worker."""
            prompt = f"""You are a coding specialist. Implement:

    {context['subtask']['description']}

    Requirements: {context.get('relevant_info', '')}

    Provide complete, working code with comments."""
            
            result = self.llm.invoke(prompt)
            return result.content
        
        def _general_worker(self, context: Dict) -> str:
            """General worker for unspecified tasks."""
            prompt = f"""Execute this task:

    {context['subtask']['description']}

    Context: {context.get('relevant_info', '')}"""
            
            result = self.llm.invoke(prompt)
            return result.content
        
        def synthesize_results(self, goal: str, worker_results: Dict[str, str]) -> str:
            """Orchestrator synthesizes all worker results."""
            # Read plan from memory (recitation)
            plan = self.read_plan()
            
            synthesis_prompt = f"""You are an orchestrator agent. Synthesize worker results into a final output.

    Original Goal: {goal}

    Plan (from memory):
    {plan}

    Worker Results:
    {json.dumps(worker_results, indent=2)}

    Create a comprehensive final output that:
    1. Directly addresses the original goal
    2. Integrates all worker contributions
    3. Maintains coherence and quality
    4. Follows the strategic plan"""
            
            result = self.llm.invoke(synthesis_prompt)
            return result.content
        
        def _parse_subtasks(self, content: str) -> List[Dict]:
            """Parse subtasks from LLM response (simplified)."""
            # In production, use structured output or better parsing
            lines = content.split('\n')
            subtasks = []
            for line in lines:
                if line.strip() and ('-' in line or line[0].isdigit()):
                    subtasks.append({
                        "description": line.strip().lstrip('- ').lstrip('0123456789. '),
                        "worker_type": "general"  # Would be determined by LLM
                    })
            return subtasks[:5]  # Limit for example

    # Usage
    orchestrator = HierarchicalOrchestrator()

    # Orchestrator decomposes goal
    decomposition = orchestrator.decompose_with_planning(
        "Create a comprehensive analysis of AI agent architectures"
    )

    # Execute subtasks (can be parallelized)
    worker_results = {}
    for subtask in decomposition["subtasks"]:
        result = orchestrator.delegate_to_worker(
            subtask,
            {"goal": decomposition["goal"], "relevant_info": ""}
        )
        worker_results[subtask["description"]] = result

    # Orchestrator synthesizes
    final_output = orchestrator.synthesize_results(
        decomposition["goal"],
        worker_results
    )
    ```

**Explanation:**
This advanced example demonstrates hierarchical orchestrators with context management. The orchestrator saves its plan to external memory before spawning workers (enabling better context management), delegates with isolated context for each worker, and synthesizes results. Workers can themselves become orchestrators for complex subtasks, creating nested structures.

### Framework-Specific Examples

??? "Google ADK: Orchestrator with Sub-Agents"

    ```python
    from google.adk.agents import Agent
    from google.adk.runners import Runner

    # Define specialized worker agents
    researcher = Agent(
        name="Researcher",
        model="gemini-2.0-flash",
        instruction="You are a research specialist. Conduct thorough research on assigned topics.",
        tools=[search_tool, web_scraper_tool]
    )

    writer = Agent(
        name="Writer",
        model="gemini-2.0-flash",
        instruction="You are a writing specialist. Create clear, well-structured content.",
        tools=[writing_tool, formatting_tool]
    )

    coder = Agent(
        name="Coder",
        model="gemini-2.0-flash",
        instruction="You are a coding specialist. Write clean, functional code.",
        tools=[code_editor_tool, test_runner_tool]
    )

    # Create orchestrator (coordinator)
    orchestrator = Agent(
        name="Orchestrator",
        model="gemini-2.0-flash",
        instruction="""You are an orchestrator agent that coordinates complex tasks.

    Your responsibilities:
    1. Analyze high-level goals and break them into subtasks
    2. Delegate subtasks to appropriate worker agents (Researcher, Writer, Coder)
    3. Provide clear, non-overlapping objectives to workers
    4. Synthesize worker results into final output

    Available workers:
    - Researcher: For research and information gathering tasks
    - Writer: For content creation and writing tasks
    - Coder: For coding and software development tasks

    Always maintain the high-level goal and ensure worker outputs align with it.""",
        sub_agents=[researcher, writer, coder]
    )

    # Runner executes orchestrator
    runner = Runner(
        agent=orchestrator,
        app_name="orchestrator_app"
    )

    # Orchestrator dynamically decomposes and delegates
    result = runner.run("Create a comprehensive guide on agentic AI patterns")
    ```

??? "LangGraph: Dynamic Orchestration"

    ```python
    from langgraph.graph import StateGraph, END
    from typing import TypedDict, List, Dict
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    class OrchestratorState(TypedDict):
        goal: str
        plan: str
        subtasks: List[Dict]
        worker_results: Dict[str, str]
        current_worker: str
        final_output: str

    def orchestrator_node(state: OrchestratorState) -> OrchestratorState:
        """Orchestrator decomposes goal into subtasks."""
        goal = state["goal"]
        
        # Dynamic decomposition
        prompt = f"Break down this goal into subtasks: {goal}"
        response = llm.invoke(prompt)
        
        # Parse and create subtasks
        subtasks = parse_subtasks(response.content)
        
        return {
            **state,
            "plan": response.content,
            "subtasks": subtasks
        }

    def worker_node(state: OrchestratorState) -> OrchestratorState:
        """Generic worker node that routes to specialized workers."""
        if not state["subtasks"]:
            return {**state, "current_worker": "done"}
        
        current_subtask = state["subtasks"][0]
        worker_type = current_subtask.get("type", "general")
        
        # Execute with specialized prompt
        prompt = create_worker_prompt(worker_type, current_subtask, state["goal"])
        result = llm.invoke(prompt)
        
        # Store result
        worker_results = state.get("worker_results", {})
        worker_results[current_subtask["id"]] = result.content
        
        # Remove completed subtask
        remaining = state["subtasks"][1:]
        
        return {
            **state,
            "worker_results": worker_results,
            "subtasks": remaining,
            "current_worker": worker_type
        }

    def synthesize_node(state: OrchestratorState) -> OrchestratorState:
        """Orchestrator synthesizes all results."""
        prompt = f"""Synthesize these worker results for goal: {state['goal']}
        
    Results: {json.dumps(state['worker_results'], indent=2)}"""
        
        result = llm.invoke(prompt)
        
        return {
            **state,
            "final_output": result.content
        }

    def should_continue(state: OrchestratorState) -> str:
        """Determine next step."""
        if state["subtasks"]:
            return "worker"
        elif state.get("final_output"):
            return "end"
        else:
            return "synthesize"

    # Build graph
    graph = StateGraph(OrchestratorState)
    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("worker", worker_node)
    graph.add_node("synthesize", synthesize_node)

    graph.set_entry_point("orchestrator")
    graph.add_edge("orchestrator", "worker")
    graph.add_conditional_edges("worker", should_continue)
    graph.add_edge("synthesize", END)
    ```

    #### CrewAI: Multi-Agent Orchestration
    ```python
    from crewai import Agent, Task, Crew
    from crewai.tools import tool

    # Define specialized agents (workers)
    researcher = Agent(
        role='Research Specialist',
        goal='Conduct thorough research on assigned topics',
        backstory='You are an expert researcher with deep knowledge in multiple domains.',
        verbose=True
    )

    writer = Agent(
        role='Writing Specialist',
        goal='Create clear, well-structured content',
        backstory='You are an expert writer skilled at synthesizing information into compelling narratives.',
        verbose=True
    )

    # Define tasks
    research_task = Task(
        description='Research the topic: AI agent architectures',
        agent=researcher
    )

    writing_task = Task(
        description='Write a comprehensive guide based on research findings',
        agent=writer,
        context=[research_task]  # Depends on research task
    )

    # Create crew (orchestrator coordinates)
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        verbose=True
    )

    # Execute - orchestrator manages workflow
    result = crew.kickoff()
    ```

??? "ChatDev-Style Role-Based Development Team"

    This example demonstrates role-based specialization inspired by ChatDev, where specialized agents work together through structured communication:

    ```python
    from langchain_openai import ChatOpenAI
    from typing import Dict, List
    import json

    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    class RoleBasedDeveloperTeam:
        """ChatDev-style development team with role-specialized agents."""
        
        def __init__(self):
            self.llm = llm
            self.conversation_history = []
        
        def designer_agent(self, requirement: str, context: str = "") -> Dict:
            """Software Designer: Analyzes requirements and creates design."""
            prompt = f"""You are a Software Designer. Your role is to analyze requirements and create a technical design.

    Requirement: {requirement}
    {context}

    Create a detailed design document including:
    1. System architecture overview
    2. Key components and their responsibilities
    3. Data structures needed
    4. API interfaces if applicable

    Return your design as a structured document."""
            
            response = self.llm.invoke(prompt)
            design = response.content
            
            self.conversation_history.append({
                "role": "Designer",
                "content": design
            })
            
            return {"role": "Designer", "design": design}
        
        def programmer_agent(self, design: str, requirement: str) -> Dict:
            """Programmer: Implements code based on design."""
            prompt = f"""You are a Programmer. Your role is to implement code based on the design.

    Original Requirement: {requirement}

    Design Document:
    {design}

    Implement the code following the design. Provide:
    1. Complete, working code
    2. Comments explaining key logic
    3. Error handling where appropriate

    Return your implementation."""
            
            response = self.llm.invoke(prompt)
            code = response.content
            
            self.conversation_history.append({
                "role": "Programmer",
                "content": code
            })
            
            return {"role": "Programmer", "code": code}
        
        def tester_agent(self, code: str, requirement: str, design: str) -> Dict:
            """Tester: Tests the implementation and reports issues."""
            prompt = f"""You are a Tester. Your role is to test the implementation.

    Original Requirement: {requirement}

    Design Document:
    {design}

    Implementation:
    {code}

    Test the implementation and provide:
    1. Test cases you would run
    2. Any bugs or issues found
    3. Suggestions for improvement

    Return your test report."""
            
            response = self.llm.invoke(prompt)
            test_report = response.content
            
            self.conversation_history.append({
                "role": "Tester",
                "content": test_report
            })
            
            return {"role": "Tester", "test_report": test_report}
        
        def reviewer_agent(self, code: str, test_report: str) -> Dict:
            """Reviewer: Reviews code quality and provides feedback."""
            prompt = f"""You are a Code Reviewer. Review the code for quality and correctness.

    Code:
    {code}

    Test Report:
    {test_report}

    Provide a code review covering:
    1. Code quality and style
    2. Potential bugs or issues
    3. Performance considerations
    4. Best practices adherence

    Return your review."""
            
            response = self.llm.invoke(prompt)
            review = response.content
            
            self.conversation_history.append({
                "role": "Reviewer",
                "content": review
            })
            
            return {"role": "Reviewer", "review": review}
        
        def develop(self, requirement: str) -> Dict:
            """Orchestrator coordinates the development process."""
            # Phase 1: Design
            design_result = self.designer_agent(requirement)
            design = design_result["design"]
            
            # Phase 2: Implementation
            code_result = self.programmer_agent(design, requirement)
            code = code_result["code"]
            
            # Phase 3: Testing
            test_result = self.tester_agent(code, requirement, design)
            test_report = test_result["test_report"]
            
            # Phase 4: Review
            review_result = self.reviewer_agent(code, test_report)
            review = review_result["review"]
            
            # Synthesize final output
            synthesis_prompt = f"""Synthesize the development process into final deliverable.

    Requirement: {requirement}

    Design: {design}

    Implementation: {code}

    Test Report: {test_report}

    Code Review: {review}

    Create a comprehensive final deliverable including the implementation and all documentation."""
            
            final_response = self.llm.invoke(synthesis_prompt)
            
            return {
                "requirement": requirement,
                "design": design,
                "code": code,
                "test_report": test_report,
                "review": review,
                "final_deliverable": final_response.content,
                "conversation_history": self.conversation_history
            }

    # Usage
    team = RoleBasedDeveloperTeam()
    result = team.develop("Create a simple REST API for managing a todo list")
    print(result["final_deliverable"])
    ```

**Explanation:**
This example demonstrates ChatDev-style role-based development where specialized agents (Designer, Programmer, Tester, Reviewer) work through structured phases. Each agent has a clear role with specialized prompts, and they communicate through a shared conversation history. The orchestrator coordinates the phases, ensuring each agent completes their task before moving to the next.

??? "MetaGPT-Style SOP-Encoded Roles"

    This example shows how to encode Standard Operating Procedures into agent prompts:

    ```python
    class SOPEncodedAgent:
        """Agent with Standard Operating Procedure encoded in prompt."""
        
        ARCHITECT_SOP = """You are an Architect Agent. Your Standard Operating Procedure:

    1. REQUIREMENT ANALYSIS
    - Carefully read and understand the requirements
    - Identify key functional and non-functional requirements
    - Clarify ambiguities with stakeholders if needed

    2. SYSTEM DESIGN
    - Design high-level system architecture
    - Identify major components and their interactions
    - Define data flow and interfaces
    - Consider scalability and maintainability

    3. DOCUMENTATION
    - Create comprehensive design document
    - Include diagrams if helpful (describe in text)
    - Specify technical stack and rationale
    - Document design decisions and trade-offs

    4. REVIEW CHECKLIST
    - Verify design addresses all requirements
    - Check for potential issues or bottlenecks
    - Ensure design is clear and implementable
    - Validate technical choices are appropriate"""

        PROGRAMMER_SOP = """You are a Programmer Agent. Your Standard Operating Procedure:

    1. DESIGN REVIEW
    - Thoroughly read the design document
    - Understand architecture and component interactions
    - Identify implementation tasks and dependencies

    2. IMPLEMENTATION
    - Write clean, maintainable code
    - Follow coding standards and best practices
    - Implement error handling and edge cases
    - Add comments for complex logic

    3. TESTING
    - Write unit tests for key functionality
    - Test edge cases and error conditions
    - Verify code works as specified

    4. SELF-REVIEW
    - Review your own code before submission
    - Check for bugs, performance issues
    - Ensure code matches design specifications"""

        def __init__(self, role: str, sop: str):
            self.role = role
            self.sop = sop
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        def execute_task(self, task: str, context: str = "") -> str:
            """Execute task following the SOP."""
            prompt = f"""{self.sop}

    Current Task: {task}

    Context from previous work:
    {context}

    Follow your Standard Operating Procedure to complete this task. Document your process and decisions."""
            
            response = self.llm.invoke(prompt)
            return response.content

    # Usage
    architect = SOPEncodedAgent("Architect", SOPEncodedAgent.ARCHITECT_SOP)
    programmer = SOPEncodedAgent("Programmer", SOPEncodedAgent.PROGRAMMER_SOP)

    # Orchestrator coordinates
    requirement = "Build a task management system"
    design = architect.execute_task(f"Design system for: {requirement}")
    code = programmer.execute_task(f"Implement based on design", design)
    ```

**Explanation:**
This example demonstrates MetaGPT's approach of encoding Standard Operating Procedures directly into agent prompts. Each agent follows a structured procedure that ensures consistent, expert-level performance. The SOP guides the agent's behavior and decision-making process.

## Context Management in Orchestrator-Worker Systems

Effective context management is critical for orchestrator-worker systems to avoid Context Pollution and maintain efficiency. 
The orchestrator must balance between providing sufficient context for workers to function effectively and minimizing token overhead.

### The Core Principle: Minimal Effective Context

**"Share memory by communicating, don't communicate by sharing memory."**
This principle, adapted from GoLang concurrency design, is fundamental to orchestrator-worker context management. Instead of sharing entire context histories with workers, orchestrators should pass only the minimal information needed for each task.

### Discrete Tasks vs Complex Reasoning

**Discrete Tasks with Clear Inputs/Outputs:**
For tasks with clear, well-defined inputs and outputs (e.g., "Search this documentation for X", "Generate a report from this data"), spin up a fresh worker agent with:

- Clean, isolated context
- Only the specific instruction and necessary input data
- No shared conversation history
- Structured output schema for the result

**Example:** A search worker doesn't need to see the orchestrator's planning process or other workers' results. It only needs:

- The search query
- The documentation to search
- Expected output format

**Complex Reasoning That Requires Full Context:**

Only share full memory/context history when the worker MUST understand the entire problem trajectory. For example:

- **Debugging agents** that need to see previous error attempts to avoid repeating mistakes
- **Iterative refinement workers** that build upon previous iterations
- **Review agents** that need to understand the full decision-making process

Even in these cases, minimize shared context to only the essential trajectory, not entire conversation histories.

### Context Isolation Strategies

**1. Save Plans to External Memory:**

Before spawning workers, orchestrators should save their plans to external memory (e.g., filesystem). This enables:

- Workers to reference the plan without it consuming orchestrator context
- Plan persistence across agent invocations
- Better context separation between orchestrator and workers

**2. Pass Structured Instructions:**

Instead of sharing raw context, orchestrators should provide:

- Clear task descriptions
- Specific input requirements
- Expected output schemas
- Relevant constraints or guidelines

**3. Isolate Worker Contexts:**

Each worker operates with its own context window, containing only:

- Worker-specific system instructions
- The assigned task and inputs
- Required output format
- No unnecessary orchestrator context or other workers' results

**4. Use Structured Communication:**

Workers return structured results (JSON, validated schemas) rather than free-form text, enabling:

- Easy parsing and integration
- Reduced context overhead when passing results between agents
- Clear contracts between orchestrator and workers

### Avoiding Context Pollution

**Don't Share Context Unless Necessary:**

- Avoid duplicating orchestrator context across all workers
- Don't pass full conversation histories to workers for discrete tasks
- Use external memory for shared state that multiple agents need

**Treat Shared Context as Expensive:**

- Shared context is an expensive dependency that should be minimized
- Forking context between agents breaks KV-cache, increasing latency and cost
- Each agent processing different context prefixes invalidates caches for others

**Prefer Structured Handoffs:**

- Use structured messages and schemas instead of raw context sharing
- Pass specific instructions rather than full histories
- Externalize large data and pass only references

??? "Example: Context-Efficient Delegation"

    ```python
    def delegate_to_worker(self, subtask: Dict, minimal_context: Dict) -> str:
        """
        Delegate subtask with minimal, isolated context.
        Avoids Context Pollution by only sharing essential information.
        """
        # Isolated context for worker - only what's needed
        worker_context = {
            "task_description": subtask["description"],
            "input_data": subtask.get("input_data", ""),
            "expected_output": subtask["expected_output"],
            "constraints": subtask.get("constraints", [])
        }
        
        # Don't pass orchestrator's full planning context
        # Don't pass other workers' results
        # Don't pass full conversation history
        
        # Spawn worker with clean context
        worker_prompt = f"""You are a {subtask['worker_type']} agent.

    Task: {worker_context['task_description']}

    Input: {worker_context['input_data']}

    Expected Output: {worker_context['expected_output']}

    Constraints: {worker_context['constraints']}

    Complete this task and return a structured result."""
        
        # Worker executes with minimal context
        result = self.llm.invoke(worker_prompt)
        
        # Return structured result (not full context)
        return result.content
    ```

### Benefits of Context-Efficient Management

- **Reduced Token Overhead:** Workers operate with minimal context, reducing token consumption
- **Better KV-Cache Efficiency:** Isolated contexts enable better caching
- **Improved Scalability:** Systems can handle more workers without context bloat
- **Lower Costs:** Reduced token usage directly translates to lower API costs
- **Faster Execution:** Smaller contexts process faster
- **Clearer Separation:** Isolated contexts improve system modularity and debuggability

### Relationship to Other Patterns

- **Context Pollution:** This section directly addresses Context Pollution prevention
- **Agent-as-Tool:** Structured worker interfaces follow the Agent-as-Tool pattern
- **Filesystem as Context:** External memory stores shared plans and data
- **Context Compression:** Orchestrators compress worker results before integration

## Key Takeaways

- **Core Concept:** The Orchestrator-Worker pattern enables dynamic task decomposition where a central orchestrator breaks down goals into subtasks and delegates to specialized workers.
- **Key Benefits:** Specialization, parallelization, and resilience are the primary advantages, enabling complex tasks that exceed single-agent capabilities.
- **Dynamic Flexibility:** Unlike fixed workflows, the orchestrator determines subtasks at runtime, making it adaptable to unpredictable task requirements.
- **Context Management:** The orchestrator can save plans to memory before spawning workers, enabling better context isolation and management. Follow the principle "Share memory by communicating, don't communicate by sharing memory" to prevent Context Pollution. Pass minimal effective context to workers, using structured instructions rather than full context histories.
- **Trade-offs:** This pattern increases model calls, latency, token throughput, and operational costs compared to single-agent systems. Use when benefits outweigh costs.
- **Best Practice:** Provide clear, non-overlapping objectives to workers to avoid duplication and ensure complete coverage. Maintain the high-level goal throughout execution.
- **Common Pitfall:** Over-coordination can add unnecessary overhead. Ensure workers have clear roles and minimal coupling. Avoid using this pattern for simple tasks that a single agent can handle.
- **Hierarchical Potential:** Workers can themselves become orchestrators for complex subtasks, creating nested multi-agent structures for very complex problems.

??? "References"

    ### Modern Frameworks

    - **ChatDev (2023):** Communicative Agents for Software Development - https://arxiv.org/html/2307.07924v5
    - **MetaGPT (2024):** Multi-Agent System with Standard Operating Procedures - https://arxiv.org/html/2308.00352v7
    - **AgentVerse (2023):** Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors - https://arxiv.org/abs/2308.10848
    - **AutoGen (2024):** Multi-Agent Conversation Framework - Microsoft Research
    - **HuggingGPT (2023):** Solving AI Tasks with ChatGPT and its Friends in Hugging Face - Microsoft Research

    ### Frameworks and Tools

    - LangGraph Multi-Agent: https://langchain-ai.github.io/langgraph/how-tos/multi-agent/
    - Google ADK Agents: https://google.github.io/adk-docs/agents/
    - CrewAI Framework: https://docs.crewai.com/ (Multi-agent orchestration framework)

    ### Research and Patterns

    - Agentic AI System Design Patterns
    - Multi-Agent Collaboration Mechanisms: A Survey of LLMs - https://arxiv.org/html/2501.06322v1
    - Anthropic's Research System: LeadResearcher and Subagents Architecture
    - Context Engineering for AI Agents: Part 2 - https://www.philschmid.de/context-engineering-part-2

