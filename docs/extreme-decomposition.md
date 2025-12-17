# Pattern: Extreme Decomposition

## Motivation

When building a skyscraper, engineers don't design it as a single monolithic structure. They break it down into thousands of individual components—each beam, bolt, and panel is designed, manufactured, and verified independently. This extreme decomposition enables quality control at every level: a single defective component can be identified and replaced without compromising the entire structure.

Similarly, when LLM agents tackle tasks requiring millions of steps, traditional decomposition approaches fail. A 1% per-step error rate means failure after only 100 steps. But by decomposing tasks into minimal, atomic subtasks—each handled by a focused microagent—we can apply error correction at every step, enabling tasks that would be impossible with traditional approaches.

> **"[Extreme decomposion] may provide a way to efficiently solve problems at the level of organizations and societies."** — Meyerson et al., MAKER (2025)

## Pattern Overview

### Problem

LLM agents face a fundamental scaling challenge: even with high per-step accuracy (e.g., 99%), error rates compound exponentially over long task sequences. 
A task requiring 1,000,000 steps with a 1% per-step error rate has essentially zero probability of success without error correction. 
Traditional task decomposition approaches break tasks into high-level subtasks (e.g., "research topic", "write report"), but errors still compound across these larger units. Without extreme decomposition into minimal, atomic subtasks, agents cannot reliably execute tasks requiring thousands or millions of steps.

### Solution

Extreme Decomposition breaks tasks into minimal, atomic subtasks—each so small and focused that it can be independently verified and corrected. 
Each atomic subtask is assigned to a microagent with a tiny, focused role. This extreme granularity enables:

- **Step-level error correction:** Errors can be caught and corrected at each atomic step before they propagate
- **Independent verification:** Each atomic subtask produces a verifiable output that can be validated
- **Voting-based correction:** Multiple microagents can independently solve the same atomic subtask, enabling voting to select the correct solution
- **Scaling to impossible tasks:** Tasks requiring millions of steps become feasible when errors are corrected at every step

The key insight is that by making subtasks small enough to be independently verifiable, we can apply error correction mechanisms (like voting) that would be impractical at higher levels of abstraction.

### Key Concepts

- **Atomic Subtasks:** Minimal, indivisible subtasks that represent the smallest meaningful unit of work. Each atomic subtask is:

    - **Independent:** Can be solved without context from other subtasks (or with minimal, explicit dependencies)
    - **Verifiable:** Produces an output that can be validated for correctness
    - **Focused:** Requires a single, clear decision or operation
- **Microagents:** Specialized agents assigned to handle individual atomic subtasks. Unlike anthropomorphized roles (e.g., "Manager", "Designer"), microagents are:

    - **Tiny roles:** Each handles one atomic operation, not a complex workflow
    - **Deterministic:** Behave like tool-like functions rather than persistent organizational entities
    - **Composable:** Can be combined and reused across different tasks
- **Decomposition Depth:** The number of levels of decomposition. Deeper decomposition (more levels) creates more atomic subtasks but enables better error correction. The optimal depth balances error correction benefits against computational cost.
- **Scaling Laws:** Mathematical relationships showing how decomposition depth affects success probability and cost. With extreme decomposition + voting, success probability can be maintained even for tasks requiring millions of steps.

### How It Works

Extreme Decomposition operates through recursive decomposition until tasks reach atomic granularity:

**1. Recursive Decomposition**

Tasks are recursively broken down until they reach atomic subtasks:

```
High-level task
  → Subtask 1
    → Atomic subtask 1.1
    → Atomic subtask 1.2
  → Subtask 2
    → Atomic subtask 2.1
    → Atomic subtask 2.2
```

Each level of decomposition breaks tasks into smaller, more focused units. Decomposition continues until subtasks are atomic—small enough to be independently solved and verified.

**2. Atomic Subtask Identification**

A subtask is atomic when it:

- Requires a single, clear decision or operation
- Produces a verifiable output
- Can be solved independently (or with minimal, explicit dependencies)
- Is small enough that multiple agents can solve it independently for voting

**3. Microagent Assignment**

Each atomic subtask is assigned to a microagent with:

- **Focused prompt:** Instructions specific to that atomic subtask
- **Minimal context:** Only the information needed for that specific operation
- **Clear output format:** Structured output that can be validated and compared

**4. Error Correction at Each Step**

Because subtasks are atomic and independently verifiable, error correction can be applied at every step:

- Multiple microagents independently solve the same atomic subtask
- Their outputs are compared through voting mechanisms
- The correct solution is selected before proceeding to the next step

**5. Composition**

Atomic subtasks are composed back into higher-level results:

- Atomic subtask outputs are combined to form subtask results
- Subtask results are combined to form the final solution
- Composition happens at each level of the decomposition hierarchy

## When to Use This Pattern

### ✅ Use this pattern when:

- **Very long task sequences:** Tasks requiring thousands or millions of steps where traditional approaches fail due to error compounding
- **High accuracy requirements:** Tasks where even small error rates are unacceptable (e.g., zero errors required)
- **Error correction needed:** Tasks where you can apply voting or other error correction mechanisms at each step
- **Independent verification possible:** Tasks where atomic subtasks produce outputs that can be independently verified
- **Scaling beyond LLM limits:** Tasks that would be impossible with traditional decomposition due to error compounding

### ❌ Avoid this pattern when:

- **Short task sequences:** Tasks with few steps where traditional decomposition is sufficient
- **Cost constraints:** Tasks where the computational cost of extreme decomposition and voting outweighs benefits
- **Simple tasks:** Tasks that don't require the complexity of extreme decomposition
- **No error correction:** Tasks where you cannot apply error correction mechanisms (voting, verification) at each step
- **Tight dependencies:** Tasks where subtasks have complex, tight dependencies that prevent atomic decomposition

### Decision Guidelines

Use Extreme Decomposition when the benefits of step-level error correction justify the computational cost. Consider:

- **Task length:** Longer tasks (1000+ steps) benefit more from extreme decomposition
- **Error tolerance:** Lower error tolerance (e.g., zero errors) requires extreme decomposition
- **Error correction capability:** Can you apply voting or verification at each step?
- **Cost constraints:** Is the computational cost of extreme decomposition acceptable?

For tasks with fewer steps or higher error tolerance, traditional decomposition approaches may be more efficient.

## Practical Applications & Use Cases

Extreme Decomposition enables tasks that would be impossible with traditional approaches:

### Million-Step Problem Solving

**Scenario:** Solving the Towers of Hanoi problem with 20 disks requires over 1,000,000 steps. With a 1% per-step error rate, traditional approaches have essentially zero probability of success.

**Solution:** Extreme decomposition breaks each move into an atomic subtask. Multiple microagents independently determine the correct move, vote on the solution, and proceed only when consensus is reached. This enables solving the problem with zero errors despite requiring over a million steps.

### Long-Horizon Planning

**Scenario:** Creating a detailed project plan with thousands of interdependent steps, where errors in early steps compound and derail the entire plan.

**Solution:** Extreme decomposition breaks planning into atomic decisions (e.g., "Should task A come before task B?"). Each decision is independently verified through voting before being incorporated into the plan, preventing error propagation.

### Complex Multi-Step Reasoning

**Scenario:** Solving complex mathematical proofs or logical problems requiring thousands of reasoning steps, where a single error invalidates the entire solution.

**Solution:** Extreme decomposition breaks reasoning into atomic logical steps. Each step is independently verified, and errors are caught before they propagate to subsequent steps.

### Large-Scale Data Processing

**Scenario:** Processing millions of data records where each record requires multiple validation and transformation steps, and errors must be caught at the record level.

**Solution:** Extreme decomposition treats each record's processing as a sequence of atomic operations. Each operation is independently verified, enabling reliable processing at scale.

## Implementation

### Core Components

??? "Decomposition Agent"

    ```python
    from typing import List, Optional, Literal
    from pydantic import BaseModel, Field

    class AtomicSubtask(BaseModel):
        """An atomic subtask that can be independently solved and verified."""
        id: str
        description: str
        input: dict
        expected_output_type: str
        dependencies: List[str] = Field(default_factory=list)

    class DecompositionResult(BaseModel):
        """Result of decomposing a task."""
        is_atomic: bool
        atomic_subtasks: List[AtomicSubtask] = Field(default_factory=list)
        subtasks: List['DecompositionResult'] = Field(default_factory=list)
        composition_instruction: Optional[str] = None

    class ExtremeDecompositionAgent:
        """Agent that performs extreme decomposition into atomic subtasks."""
        
        def __init__(self, llm, max_depth: int = 10):
            self.llm = llm
            self.max_depth = max_depth
        
        async def decompose(
            self,
            task: str,
            context: dict,
            depth: int = 0
        ) -> DecompositionResult:
            """Recursively decompose task into atomic subtasks."""
            
            # Check if we've reached max depth
            if depth >= self.max_depth:
                # Force atomic at max depth
                return DecompositionResult(
                    is_atomic=True,
                    atomic_subtasks=[
                        AtomicSubtask(
                            id=f"atomic_{depth}",
                            description=task,
                            input=context,
                            expected_output_type="string"
                        )
                    ]
                )
            
            # Check if task is already atomic
            if await self._is_atomic(task, context):
                return DecompositionResult(
                    is_atomic=True,
                    atomic_subtasks=[
                        AtomicSubtask(
                            id=f"atomic_{depth}",
                            description=task,
                            input=context,
                            expected_output_type="string"
                        )
                    ]
                )
            
            # Decompose further
            subtasks = await self._decompose_into_subtasks(task, context)
            
            # Recursively decompose each subtask
            decomposed_subtasks = []
            atomic_subtasks = []
            
            for subtask in subtasks:
                result = await self.decompose(
                    subtask["description"],
                    subtask.get("context", context),
                    depth + 1
                )
                
                if result.is_atomic:
                    atomic_subtasks.extend(result.atomic_subtasks)
                else:
                    decomposed_subtasks.append(result)
                    atomic_subtasks.extend(result._collect_all_atomic())
            
            return DecompositionResult(
                is_atomic=False,
                atomic_subtasks=atomic_subtasks,
                subtasks=decomposed_subtasks,
                composition_instruction=subtasks.get("composition", None)
            )
        
        async def _is_atomic(self, task: str, context: dict) -> bool:
            """Check if a task is atomic (cannot be further decomposed)."""
            prompt = f"""Determine if this task is atomic (cannot be further decomposed).

    Task: {task}
    Context: {context}

    A task is atomic if:
    1. It requires a single, clear decision or operation
    2. It produces a verifiable output
    3. It can be solved independently
    4. It is small enough for multiple agents to solve independently

    Return: true or false"""
            
            response = await self.llm.ainvoke(prompt)
            return "true" in response.content.lower()
        
        async def _decompose_into_subtasks(self, task: str, context: dict) -> List[dict]:
            """Decompose a task into smaller subtasks."""
            prompt = f"""Decompose this task into smaller subtasks.

    Task: {task}
    Context: {context}

    Break the task into the smallest meaningful subtasks. Each subtask should be:
    - Focused on a single operation
    - Independently solvable
    - Producing a verifiable output

    Return a JSON list of subtasks with descriptions and any required context."""
            
            response = await self.llm.ainvoke(prompt)
            # Parse JSON response
            import json
            return json.loads(response.content)
    ```

??? "Microagent"

    ```python
    class Microagent:
        """A microagent that handles a single atomic subtask."""
        
        def __init__(self, llm, subtask: AtomicSubtask):
            self.llm = llm
            self.subtask = subtask
            self.prompt = self._build_prompt()
        
        def _build_prompt(self) -> str:
            """Build focused prompt for atomic subtask."""
            return f"""You are a microagent handling a single atomic subtask.

    Subtask: {self.subtask.description}
    Input: {self.subtask.input}
    Expected Output Type: {self.subtask.expected_output_type}

    Solve this atomic subtask. Provide only the solution, no additional reasoning.

    Output:"""
        
        async def solve(self) -> dict:
            """Solve the atomic subtask."""
            response = await self.llm.ainvoke(self.prompt)
            return {
                "subtask_id": self.subtask.id,
                "output": response.content,
                "status": "completed"
            }
    ```

??? "Composition Agent"

    ```python
    class CompositionAgent:
        """Agent that composes atomic subtask outputs into higher-level results."""
        
        def __init__(self, llm):
            self.llm = llm
        
        async def compose(
            self,
            atomic_outputs: List[dict],
            composition_instruction: str
        ) -> dict:
            """Compose atomic subtask outputs into a higher-level result."""
            prompt = f"""Compose these atomic subtask outputs into a higher-level result.

    Atomic Outputs:
    {json.dumps(atomic_outputs, indent=2)}

    Composition Instruction: {composition_instruction}

    Combine the atomic outputs according to the composition instruction.
    Return the composed result."""
            
            response = await self.llm.ainvoke(prompt)
            return {
                "composed_result": response.content,
                "atomic_outputs": atomic_outputs
            }
    ```

??? "Complete Example"

    ```python
    import asyncio
    from typing import List

    async def extreme_decomposition_workflow(
        task: str,
        context: dict,
        llm
    ):
        """Complete workflow for extreme decomposition."""
        
        # Step 1: Decompose into atomic subtasks
        decomposer = ExtremeDecompositionAgent(llm, max_depth=10)
        decomposition = await decomposer.decompose(task, context)
        
        # Step 2: Solve each atomic subtask (with voting for error correction)
        atomic_outputs = []
        for atomic_subtask in decomposition.atomic_subtasks:
            # Create multiple microagents for voting
            microagents = [
                Microagent(llm, atomic_subtask) 
                for _ in range(3)  # 3 agents for voting
            ]
            
            # Each microagent solves independently
            solutions = await asyncio.gather(*[
                agent.solve() for agent in microagents
            ])
            
            # Vote on the best solution (see Voting-Based Error Correction pattern)
            from voting_error_correction import vote_on_solutions
            selected_solution = await vote_on_solutions(solutions, atomic_subtask)
            
            atomic_outputs.append(selected_solution)
        
        # Step 3: Compose atomic outputs back into final result
        composer = CompositionAgent(llm)
        final_result = await composer.compose(
            atomic_outputs,
            decomposition.composition_instruction or "Combine all outputs"
        )
        
        return final_result

    # Usage
    async def main():
        task = "Solve Towers of Hanoi with 20 disks"
        context = {"disks": 20, "pegs": ["A", "B", "C"]}
        
        # Requires LLM initialization
        # llm = ChatOpenAI(model="gpt-4o", temperature=0)
        # result = await extreme_decomposition_workflow(task, context, llm)
        # print(result)

    if __name__ == "__main__":
        asyncio.run(main())
    ```

## Scaling Laws

Extreme decomposition enables scaling to tasks that would be impossible otherwise. The mathematical relationship shows:

**Without Extreme Decomposition:**
Success probability: `P(success) = (1 - p)^s`, Where `p` = per-step error rate, `s` = number of steps.
For 1,000,000 steps with 1% error rate: `P(success) ≈ 0`

**With Extreme Decomposition + Voting:**
Success probability: `P(success) ≈ 1 - (1 - p_vote)^(s/d)`, Where `p_vote` = error rate after voting (much lower than `p`), `d` = decomposition depth.
With proper voting, `p_vote << p`, enabling success even for million-step tasks.

**Cost Scaling:**

- Cost increases with decomposition depth (more atomic subtasks)
- But enables tasks that would be impossible otherwise
- Optimal depth balances error correction benefits against cost

For detailed scaling analysis, see the **Task Decomposition** pattern module.

## Key Takeaways

- **Core Concept:** Extreme Decomposition breaks tasks into minimal, atomic subtasks—each independently solvable and verifiable—enabling error correction at every step.
- **Key Benefit:** Enables tasks requiring millions of steps by preventing error compounding through step-level error correction.
- **Microagents:** Assign tiny, focused roles to agents rather than anthropomorphized complex roles. Each microagent handles one atomic operation.
- **Decomposition Depth:** Balance between granularity (more atomic subtasks) and cost. Deeper decomposition enables better error correction but increases computational cost.
- **Scaling Laws:** Mathematical relationships show how decomposition depth affects success probability. With proper error correction, tasks requiring millions of steps become feasible.
- **Best Practice:** Decompose until subtasks are atomic (independently solvable, verifiable, focused). Apply error correction (voting) at each atomic step.
- **Common Pitfall:** Over-decomposing simple tasks adds unnecessary cost. Use extreme decomposition only for very long task sequences or high accuracy requirements.
- **Integration:** Works with **Voting-Based Error Correction** (mechanism for step-level correction) and **Red-Flagging** (proactive error detection).

## Related Patterns

This pattern works well with:

- **Voting-Based Error Correction** - Provides the mechanism for correcting errors at each atomic step
- **Red-Flagging** - Proactive error detection improves voting quality
- **Task Decomposition** - Extreme Decomposition is an extension focusing on atomic granularity
- **Multi-Agent** - Microagents are a form of multi-agent architecture with extreme role specialization

This pattern extends:

- **Task Decomposition** - Takes decomposition to extreme granularity for step-level error correction
- **Agent-as-Tool** - Microagents are tool-like, deterministic functions rather than persistent entities

??? "References"

    - **MAKER (2025):** Solving a Million-Step LLM Task with Zero Errors - Meyerson et al. - https://arxiv.org/html/2511.09030v1
    - **Massively Decomposed Agentic Processes (MDAPs):** Framework for extreme decomposition with error correction
    - **Towers of Hanoi Benchmark:** Domain requiring million+ steps with zero errors

