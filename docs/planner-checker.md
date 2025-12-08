# Pattern: Planner-Checker (Planner-Executor-Checker)

## Motivation

Architects create blueprints before construction begins. 
Software developers write plans before coding. 
Scientists design experiments before running them. 
This separation of planning from execution enables forethought, optimization, and verification that reactive approaches cannot achieve.
The Planner-Checker pattern captures this principle: one agent (or module) creates structured plans, another executes them using tools, and optionally a third verifies outcomes. This decoupling of planning, execution, and verification enables global optimization, better tool orchestration, and systematic error detection that intermingled approaches miss.

## Pattern Overview

**What it is:** A multi-agent or multi-module architecture where planning, execution, and verification are separated into distinct phases handled by specialized components. 
A Planner agent creates structured plans (often as directed acyclic graphs of sub-tasks), an Executor agent carries out plans using external tools, and optionally a Reflect/Checker agent evaluates outcomes and correctness.

**When to use:** For complex, long-horizon tasks requiring multi-step tool use, when global optimization of action sequences is needed, when plans must be verified before execution, or when execution results need systematic checking. 
Particularly valuable for tasks requiring intricate multi-tool workflows where reactive strategies get stuck in local decision loops.

**Why it matters:** Separating planning from execution enables global optimization of action sequences, better tool orchestration, systematic verification, and feedback loops for dynamic correction. Research shows that planner-centric approaches outperform reactive strategies on complex tool-using tasks by creating optimized plans before execution rather than making local decisions reactively.

Unlike reactive approaches like ReAct that interleave reasoning and tool use, the Planner-Checker pattern decouples these concerns. 
The planner thinks globally about the entire task sequence, the executor focuses on tool invocation, and the checker verifies correctness. 
This separation enables better performance on complex, multi-step tasks.

### Key Concepts

- **Plan Agent:** Creates structured, multi-step plans before execution. Analyzes the task globally and outputs a directed acyclic graph (DAG) of sub-tasks, dependencies, and tool assignments. Enables global optimization of action sequences.
- **Tool/Executor Agent:** Carries out the plan by executing sub-tasks sequentially or in parallel, invoking external tools (APIs, databases, code execution) as specified in the plan. Focuses on tool invocation and result collection.
- **Reflect/Checker Agent (Optional):** Evaluates execution outcomes, verifies correctness of each step, and provides feedback for plan adjustment. Catches errors, validates results, and enables dynamic correction.
- **Global Optimization:** Planner creates globally optimized action sequences rather than making reactive local decisions. Overcomes limitations of reactive strategies that get stuck in local decision loops.
- **Feedback Loops:** Results from execution feed back to planner or checker, enabling dynamic plan adjustment and error correction.
- **Tool Augmentation:** Executor agents use external tools (calculators, search engines, APIs) to extend capabilities beyond language model limitations.

### How It Works

The Planner-Checker pattern operates through distinct phases:

1. **Planning Phase:** The Plan Agent analyzes the high-level goal and creates a structured plan:

    - **Task Decomposition:** Breaks goal into sub-tasks
    - **Dependency Analysis:** Identifies dependencies between sub-tasks
    - **Tool Assignment:** Determines which tools are needed for each sub-task
    - **Sequence Optimization:** Creates optimized execution order (often as a DAG)
    - **Output:** Structured plan specifying tasks, dependencies, tools, and execution order

2. **Execution Phase:** The Tool/Executor Agent carries out the plan:

    - **Plan Parsing:** Reads and understands the structured plan
    - **Task Execution:** Executes sub-tasks in the specified order (respecting dependencies)
    - **Tool Invocation:** Calls external tools as specified in the plan
    - **Result Collection:** Collects outputs from tool calls
    - **Progress Tracking:** Monitors execution progress through the plan

3. **Verification Phase (Optional):** The Reflect/Checker Agent evaluates outcomes:

    - **Outcome Evaluation:** Checks if execution results match expected outcomes
    - **Error Detection:** Identifies errors, incorrect results, or failed steps
    - **Correctness Verification:** Validates that each step was executed correctly
    - **Feedback Generation:** Provides feedback for plan adjustment or re-execution

4. **Feedback Loop:** Results and verification feed back to enable:

    - **Plan Adjustment:** Planner refines plan based on execution results
    - **Error Correction:** System retries failed steps or adjusts approach
    - **Dynamic Adaptation:** Plan adapts to unexpected results or new information

## When to Use This Pattern

### ✅ Use when:

- **Complex multi-step tasks:** Tasks requiring multiple sequential or parallel tool invocations
- **Global optimization needed:** Need to optimize entire action sequence rather than making local decisions
- **Tool orchestration complexity:** Tasks requiring intricate coordination of multiple tools
- **Plan verification important:** Need to verify plans before execution or validate outcomes after
- **Long-horizon tasks:** Tasks spanning many steps where reactive strategies struggle
- **Dependency management:** Tasks with complex dependencies between sub-tasks
- **Error detection critical:** Need systematic verification and error detection

### ❌ Avoid when:

- **Simple single-step tasks:** Tasks that don't benefit from planning or multi-agent coordination
- **Highly reactive requirements:** Tasks requiring immediate responses without planning time
- **Resource constraints:** Computational or cost constraints make multi-agent systems impractical
- **Fixed workflows:** Tasks following rigid, predetermined sequences that don't need dynamic planning
- **Low-latency requirements:** Planning phase introduces unacceptable latency

### Decision Guidelines

Use Planner-Checker pattern when the benefits of global optimization, systematic verification, and separation of concerns outweigh the costs (latency from planning phase, complexity, computational expense). 
Consider: task complexity (complex multi-step = benefit from planning), tool orchestration needs (intricate workflows = benefit from structured plans), and verification requirements (critical correctness = benefit from checker). 
For simple tasks or highly reactive requirements, reactive approaches like ReAct may be more efficient.

## Practical Applications & Use Cases

Planner-Checker patterns excel in scenarios requiring complex tool orchestration, multi-step reasoning, or systematic verification:

### Complex Tool-Using Tasks

Tasks requiring coordination of multiple tools in optimized sequences benefit from global planning before execution.

**Example:** Multi-hop reasoning tasks where an agent needs to search databases, query APIs, perform calculations, and synthesize results in a coordinated sequence.

### Software Development Workflows

Development tasks benefit from planning before execution, with code generation, testing, and verification as separate phases.

**Example:** Building a web application where planner creates development plan, executor writes code and runs tests, checker verifies functionality.

### Research and Analysis

Research tasks requiring multiple information sources, analysis steps, and synthesis benefit from structured planning.

**Example:** Research task where planner creates investigation plan, executor gathers data from multiple sources, checker verifies findings.

### Scientific Computation

Tasks requiring complex computational workflows with dependencies benefit from planning and verification.

**Example:** Scientific analysis where planner designs computation pipeline, executor runs calculations, checker validates results.

## Modern Frameworks and Research

### CoReaAgents (2025)

CoReaAgents defines a triad of LLM-powered agents:

- **Plan Agent:** Produces a precise multi-step plan for complex reasoning tasks
- **Tool Agent:** Carries out the plan using external tools
- **Reflect Agent:** Evaluates the outcomes and correctness of each step

This design mirrors how humans approach tasks with forethought, action, and self-correction. By simulating a "planner–solver–checker" workflow, CoReaAgents achieved stronger performance on tool-using tasks than agents that intermingle planning and acting.

### Plan-and-Execute Paradigm (2025)

Research by Wei et al. (2025) introduced a dedicated planning model that outputs a global directed acyclic graph (DAG) of sub-tasks for complex queries. An executor model then follows this optimized plan.

**Key Features:**

- Global optimization of action sequences
- DAG representation of task dependencies
- Separation of planning from execution
- Overcomes reactive strategy limitations

**Research Results:** This approach overcame limitations of purely reactive strategies (which often got stuck in local decision loops) by globally optimizing the action sequence, achieving state-of-the-art performance on benchmarks requiring intricate multi-tool workflows.

### ReAct and Tool Augmentation

The ReAct paradigm (2022) demonstrated LLM agents interleaving reasoning steps with tool calls. Building on this, systems like HuggingGPT show how a language-based agent can serve as a general-purpose orchestrator, planning tool use and delegating to specialists.

**Key Principles:**

- Tool augmentation extends agent capabilities
- Feedback loops enable dynamic correction
- LLM-as-manager concept for tool orchestration

### HuggingGPT (2023)

Uses a ChatGPT-based controller that analyzes user requests, plans sequences of subtasks, and delegates each to appropriate AI models from Hugging Face's model hub. The controller ensures each subtask is handled by a competent model and results pass correctly between agents.

## Implementation

### Prerequisites

```bash
pip install langchain langchain-openai langgraph
```

??? "Basic Example: Planner-Executor Pattern"

    This example demonstrates a basic planner-executor system:

    ```python
    from langchain_openai import ChatOpenAI
    from typing import List, Dict, Any
    import json

    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    class PlanAgent:
        """Agent that creates structured plans."""
        
        def __init__(self):
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        def create_plan(self, goal: str) -> Dict[str, Any]:
            """Create a structured plan for achieving the goal."""
            prompt = f"""You are a planning agent. Create a detailed plan to achieve this goal.

    Goal: {goal}

    Create a structured plan with:
    1. List of sub-tasks (each sub-task should be clear and actionable)
    2. Dependencies between sub-tasks (which tasks depend on others)
    3. Required tools for each sub-task (e.g., search, calculator, code_execution)
    4. Expected outputs for each sub-task

    Return as JSON with structure:
    {{
        "tasks": [
            {{
                "id": 1,
                "description": "task description",
                "dependencies": [list of task IDs this depends on],
                "tools": ["tool1", "tool2"],
                "expected_output": "what this task should produce"
            }}
        ],
        "execution_order": [list of task IDs in execution order]
    }}"""
            
            response = self.llm.invoke(prompt)
            plan_text = response.content
            
            # Extract JSON from response (simplified - in production use structured output)
            try:
                # Find JSON in response
                start = plan_text.find('{')
                end = plan_text.rfind('}') + 1
                plan_json = json.loads(plan_text[start:end])
                return plan_json
            except:
                # Fallback: create simple plan
                return {
                    "tasks": [
                        {"id": 1, "description": goal, "dependencies": [], "tools": [], "expected_output": "result"}
                    ],
                    "execution_order": [1]
                }

    class ExecutorAgent:
        """Agent that executes plans using tools."""
        
        def __init__(self):
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
            self.tool_results = {}
        
        def execute_task(self, task: Dict, context: Dict) -> Any:
            """Execute a single task using available tools."""
            task_desc = task["description"]
            tools = task.get("tools", [])
            dependencies = task.get("dependencies", [])
            
            # Get results from dependent tasks
            dependency_results = {
                dep_id: self.tool_results.get(dep_id, "")
                for dep_id in dependencies
            }
            
            # Build context from dependencies
            context_text = "\n".join([
                f"Task {dep_id} result: {result}"
                for dep_id, result in dependency_results.items()
            ])
            
            # Execute based on tools needed
            if "search" in tools:
                result = self._execute_search(task_desc, context_text)
            elif "calculator" in tools:
                result = self._execute_calculation(task_desc, context_text)
            elif "code_execution" in tools:
                result = self._execute_code(task_desc, context_text)
            else:
                result = self._execute_general(task_desc, context_text)
            
            return result
        
        def _execute_search(self, task: str, context: str) -> str:
            """Simulate search tool (in production, use actual search API)."""
            prompt = f"""You are executing a search task.

    Task: {task}
    Context from previous tasks: {context}

    Simulate searching for information and provide relevant findings."""
            
            response = self.llm.invoke(prompt)
            return response.content
        
        def _execute_calculation(self, task: str, context: str) -> str:
            """Simulate calculation tool."""
            prompt = f"""You are executing a calculation task.

    Task: {task}
    Context from previous tasks: {context}

    Perform the calculation and return the result."""
            
            response = self.llm.invoke(prompt)
            return response.content
        
        def _execute_code(self, task: str, context: str) -> str:
            """Simulate code execution tool."""
            prompt = f"""You are executing a code task.

    Task: {task}
    Context from previous tasks: {context}

    Generate and execute code to complete this task. Return the code and its output."""
            
            response = self.llm.invoke(prompt)
            return response.content
        
        def _execute_general(self, task: str, context: str) -> str:
            """Execute general task."""
            prompt = f"""Execute this task:

    Task: {task}
    Context from previous tasks: {context}

    Complete the task and return the result."""
            
            response = self.llm.invoke(prompt)
            return response.content
        
        def execute_plan(self, plan: Dict) -> Dict[str, Any]:
            """Execute the entire plan."""
            tasks = {task["id"]: task for task in plan["tasks"]}
            execution_order = plan["execution_order"]
            
            results = {}
            
            for task_id in execution_order:
                task = tasks[task_id]
                result = self.execute_task(task, results)
                self.tool_results[task_id] = result
                results[task_id] = result
            
            return results

    def planner_executor(goal: str) -> Dict[str, Any]:
        """Run planner-executor workflow."""
        planner = PlanAgent()
        executor = ExecutorAgent()
        
        # Phase 1: Planning
        plan = planner.create_plan(goal)
        
        # Phase 2: Execution
        results = executor.execute_plan(plan)
        
        # Phase 3: Synthesis
        synthesis_prompt = f"""Synthesize the plan execution results into a final answer.

    Original Goal: {goal}

    Plan: {json.dumps(plan, indent=2)}

    Execution Results: {json.dumps(results, indent=2)}

    Create a comprehensive final answer that addresses the original goal."""
        
        final_answer = llm.invoke(synthesis_prompt)
        
        return {
            "goal": goal,
            "plan": plan,
            "results": results,
            "final_answer": final_answer.content
        }

    # Usage
    result = planner_executor(
        "Research the latest trends in AI agent architectures and create a summary report"
    )
    print(result["final_answer"])
    ```

**Explanation:**
This example demonstrates the basic planner-executor pattern: the Plan Agent creates a structured plan, the Executor Agent executes tasks in order (respecting dependencies), and results are synthesized into a final answer. The planner thinks globally about the task structure, while the executor focuses on tool invocation.

??? "Advanced Example: Planner-Executor-Checker (CoReaAgents Style)"

    This example adds a Reflect/Checker agent to verify outcomes:

    ```python
    class ReflectAgent:
        """Agent that checks execution outcomes and correctness."""
        
        def __init__(self):
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        def check_step(self, task: Dict, result: Any, expected_output: str) -> Dict:
            """Check if a task step was executed correctly."""
            prompt = f"""You are a reflection agent checking task execution.

    Task: {task['description']}
    Expected Output: {expected_output}
    Actual Result: {result}

    Evaluate:
    1. Does the result match the expected output?
    2. Are there any errors or issues?
    3. Is the result correct and complete?
    4. What feedback would you provide?

    Return your evaluation."""
            
            response = self.llm.invoke(prompt)
            
            # Simple correctness check (in production, use structured output)
            is_correct = "correct" in response.content.lower() or "match" in response.content.lower()
            
            return {
                "task_id": task["id"],
                "is_correct": is_correct,
                "evaluation": response.content,
                "feedback": response.content
            }
        
        def check_plan_execution(self, plan: Dict, results: Dict) -> Dict:
            """Check the entire plan execution."""
            evaluations = []
            
            for task in plan["tasks"]:
                task_id = task["id"]
                result = results.get(task_id, "")
                expected = task.get("expected_output", "")
                
                evaluation = self.check_step(task, result, expected)
                evaluations.append(evaluation)
            
            # Overall assessment
            all_correct = all(eval["is_correct"] for eval in evaluations)
            
            return {
                "all_correct": all_correct,
                "step_evaluations": evaluations,
                "overall_feedback": "All steps correct" if all_correct else "Some steps need correction"
            }

    def planner_executor_checker(goal: str) -> Dict[str, Any]:
        """Run full planner-executor-checker workflow."""
        planner = PlanAgent()
        executor = ExecutorAgent()
        checker = ReflectAgent()
        
        # Phase 1: Planning
        plan = planner.create_plan(goal)
        
        # Phase 2: Execution
        results = executor.execute_plan(plan)
        
        # Phase 3: Checking
        check_result = checker.check_plan_execution(plan, results)
        
        # Phase 4: Synthesis (with feedback)
        synthesis_prompt = f"""Synthesize the plan execution results into a final answer.

    Original Goal: {goal}

    Plan: {json.dumps(plan, indent=2)}
    Execution Results: {json.dumps(results, indent=2)}
    Verification: {json.dumps(check_result, indent=2)}

    Create a comprehensive final answer that addresses the original goal.
    Note any issues or corrections needed based on the verification."""
        
        final_answer = llm.invoke(synthesis_prompt)
        
        return {
            "goal": goal,
            "plan": plan,
            "results": results,
            "verification": check_result,
            "final_answer": final_answer.content
        }

    # Usage
    result = planner_executor_checker(
        "Calculate the compound interest on $10,000 at 5% APR over 10 years and explain the calculation"
    )
    print(result["final_answer"])
    ```

**Explanation:**
This example demonstrates the full planner-executor-checker pattern: the Plan Agent creates the plan, the Executor Agent executes it, and the Reflect Agent checks correctness. The checker provides feedback that can be used to adjust the plan or re-execute failed steps.

??? "Advanced Example: DAG-Based Planning (Plan-and-Execute Style)"

    This example demonstrates DAG-based planning with global optimization:

    ```python
    class DAGPlanner:
        """Planner that creates DAG-optimized execution plans."""
        
        def __init__(self):
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        
        def create_dag_plan(self, goal: str) -> Dict[str, Any]:
            """Create a DAG-optimized plan with parallel execution opportunities."""
            prompt = f"""You are an advanced planning agent. Create an optimized plan with a directed acyclic graph (DAG) structure.

    Goal: {goal}

    Create a DAG-optimized plan that:
    1. Identifies tasks that can run in parallel
    2. Minimizes total execution time
    3. Respects dependencies
    4. Optimizes tool usage

    Return as JSON:
    {{
        "tasks": [
            {{
                "id": "task_id",
                "description": "task description",
                "dependencies": ["dep_task_id1", "dep_task_id2"],
                "tools": ["tool1"],
                "estimated_time": 5,
                "can_parallelize": true/false
            }}
        ],
        "execution_graph": {{
            "sequential": [["task1"], ["task2", "task3"], ["task4"]],
            "parallel_groups": [[["task2", "task3"]], ["task4"]]
        }}
    }}"""
            
            response = self.llm.invoke(prompt)
            plan_text = response.content
            
            try:
                start = plan_text.find('{')
                end = plan_text.rfind('}') + 1
                plan_json = json.loads(plan_text[start:end])
                return plan_json
            except:
                # Fallback
                return {
                    "tasks": [{"id": "1", "description": goal, "dependencies": [], "tools": []}],
                    "execution_graph": {"sequential": [["1"]]}
                }

    class ParallelExecutor:
        """Executor that can run tasks in parallel based on DAG."""
        
        def __init__(self):
            self.executor = ExecutorAgent()
        
        def execute_dag_plan(self, plan: Dict) -> Dict[str, Any]:
            """Execute plan respecting DAG structure and parallelization."""
            tasks = {task["id"]: task for task in plan["tasks"]}
            execution_graph = plan.get("execution_graph", {})
            sequential_groups = execution_graph.get("sequential", [])
            
            results = {}
            
            # Execute sequential groups (tasks in each group can run in parallel)
            for group in sequential_groups:
                # For simplicity, execute sequentially within group
                # In production, could parallelize here
                for task_id in group:
                    task = tasks[task_id]
                    
                    # Check dependencies are complete
                    deps_complete = all(
                        dep_id in results 
                        for dep_id in task.get("dependencies", [])
                    )
                    
                    if deps_complete:
                        result = self.executor.execute_task(task, results)
                        results[task_id] = result
            
            return results

    def dag_planner_executor(goal: str) -> Dict[str, Any]:
        """Run DAG-optimized planner-executor workflow."""
        planner = DAGPlanner()
        executor = ParallelExecutor()
        
        # Create DAG-optimized plan
        plan = planner.create_dag_plan(goal)
        
        # Execute with parallelization opportunities
        results = executor.execute_dag_plan(plan)
        
        # Synthesize
        synthesis_prompt = f"""Synthesize results from DAG-optimized execution.

    Goal: {goal}
    Plan: {json.dumps(plan, indent=2)}
    Results: {json.dumps(results, indent=2)}

    Create final answer."""
        
        final_answer = llm.invoke(synthesis_prompt)
        
        return {
            "goal": goal,
            "dag_plan": plan,
            "results": results,
            "final_answer": final_answer.content
        }

    # Usage
    result = dag_planner_executor(
        "Research three different topics in parallel, then synthesize a comparison"
    )
    print(result["final_answer"])
    ```

**Explanation:**
This example demonstrates DAG-based planning where the planner creates an optimized execution graph with parallelization opportunities. The executor respects dependencies while maximizing parallel execution, enabling global optimization of the action sequence.

## Key Takeaways

- **Core Concept:** Planner-Checker pattern separates planning, execution, and verification into distinct phases, enabling global optimization, better tool orchestration, and systematic error detection.
- **Key Benefits:** Global optimization of action sequences, systematic verification, separation of concerns, and feedback loops for dynamic correction. Outperforms reactive strategies on complex multi-tool tasks.
- **Architecture Components:** Plan Agent (creates structured plans), Executor Agent (carries out plans with tools), and optional Reflect Agent (verifies outcomes and correctness).
- **Trade-offs:** Planning phase introduces latency, multi-agent systems increase complexity and cost. Use when benefits of global optimization and verification outweigh these costs.
- **Best Practice:** Design plans as structured DAGs with dependencies, enable parallel execution where possible, and implement feedback loops for dynamic correction.
- **Common Pitfall:** Over-planning simple tasks or creating overly rigid plans that don't adapt to unexpected results. Balance planning with flexibility.
- **Research Evidence:** Studies show planner-centric approaches significantly outperform reactive strategies on complex tool-using tasks by enabling global optimization.

## Related Patterns

This pattern works well with:

- **Pattern: Planning** - Core planning capabilities that inform plan creation
- **Pattern: Tool Use** - Executor agents use tools as specified in plans
- **Pattern: Reflection** - Reflect agents can use reflection techniques for verification
- **Pattern: Orchestrator-Worker** - Planner can orchestrate multiple executor workers

??? "References"

    - **CoReaAgents:** A Collaboration and Reasoning Framework Based on LLM-Powered Agents for Complex Reasoning Tasks - https://www.mdpi.com/2076-3417/15/10/5663
    - **Plan-and-Execute:** Beyond ReAct: A Planner-Centric Framework for Complex Tool-Augmented LLM Reasoning - https://arxiv.org/html/2511.10037v2
    - **ReAct Paradigm:** ReAct: Synergizing Reasoning and Acting in Language Models
    - **HuggingGPT:** Solving AI Tasks with ChatGPT and its Friends in Hugging Face - Microsoft Research

