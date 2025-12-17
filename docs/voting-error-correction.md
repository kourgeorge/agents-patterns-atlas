# Pattern: Voting-Based Error Correction

## Motivation

When a jury deliberates, they don't rely on a single person's judgment. Multiple jurors independently evaluate the evidence, then vote to reach a decision. This collective judgment is more reliable than any individual's assessment—errors are caught, biases are balanced, and the correct answer emerges through consensus.

Similarly, when LLM agents solve atomic subtasks, multiple agents can independently work on the same problem, then vote to select the correct solution. This voting mechanism enables error correction at every step, preventing errors from propagating through long task sequences. Unlike discussion-based consensus (where agents debate), voting is deterministic and efficient—perfect for correcting errors in atomic, verifiable subtasks.

> **"The high level of modularity resulting from the decomposition allows error correction to be applied at each step through an efficient multi-agent voting scheme."** — Meyerson et al., MAKER (2025)

## Pattern Overview

### Problem

Even with high per-step accuracy, errors compound exponentially over long task sequences. A single error in step 100 can derail a million-step task. Traditional error correction approaches (retry, replanning) are reactive—they detect errors after they occur and attempt to recover. But for very long tasks, reactive error correction is insufficient. We need proactive error correction that prevents errors from occurring in the first place, or catches them immediately before they propagate.

### Solution

Voting-Based Error Correction uses multiple independent agents to solve the same atomic subtask, then votes to select the correct solution before proceeding. This deterministic voting mechanism:

- **Prevents errors:** Multiple independent solutions catch errors before they propagate
- **Corrects errors:** Voting selects the correct solution even when some agents make mistakes
- **Works at scale:** Efficient for atomic subtasks, enabling error correction at every step
- **Deterministic:** Unlike discussion-based consensus, voting produces consistent, predictable results

The key insight is that for atomic, verifiable subtasks, multiple independent agents can solve the same problem, and voting can reliably select the correct solution even when some agents err.

### Key Concepts

- **Independent Agents:** Multiple agents solve the same subtask independently, without seeing each other's solutions. This independence is critical—if agents see each other's work, errors can correlate and voting becomes ineffective.
- **Voting Mechanisms:** Different voting strategies for selecting the correct solution:

    - **First-to-k Voting:** First candidate solution to receive k votes wins. Fast but can be influenced by early incorrect solutions.
    - **First-to-ahead-by-k Voting:** First candidate to lead by k votes wins. More robust, requires a candidate to consistently outperform others.
    - **Majority Voting:** Candidate with most votes wins. Simple but may not converge for close races.

- **Candidate Solutions:** Each independent agent produces a candidate solution. Candidates are compared and voted on to select the winner.
- **Vote Counting:** A discriminator agent (or automated mechanism) evaluates candidates and assigns votes. Votes can be based on correctness, quality, or other criteria.
- **Convergence:** Voting continues until a candidate reaches the voting threshold (k votes or k-vote lead). This ensures a clear winner before proceeding.

### How It Works

Voting-Based Error Correction operates through a structured voting process:

**1. Independent Solution Generation**

Multiple agents (typically 3-7) independently solve the same atomic subtask:

- Each agent receives the same input and instructions
- Agents work in isolation (no communication between agents)
- Each produces a candidate solution

**2. Candidate Collection**

All candidate solutions are collected:

- Solutions are formatted consistently for comparison
- Metadata (agent ID, confidence, reasoning) may be included
- Candidates are prepared for voting

**3. Voting Process**

A discriminator (or voting mechanism) evaluates candidates:

- **Discriminator Agent:** An LLM evaluates each candidate and assigns votes
- **Voting Criteria:** Correctness, quality, adherence to requirements
- **Vote Assignment:** Each discriminator call can assign votes to one or more candidates

**4. Vote Counting**

Votes are counted and compared:

- Track votes for each candidate
- Check if any candidate has reached the voting threshold
- For first-to-ahead-by-k: check if any candidate leads by k votes

**5. Convergence Check**

Continue voting until convergence:
- If threshold reached: select winner and proceed
- If not converged: collect more votes (additional discriminator calls or agent solutions)
- Optional: timeout or max vote limit to prevent infinite loops

**6. Winner Selection**

Once convergence is reached:
- Select the winning candidate
- Use this solution for the current step
- Proceed to the next atomic subtask

## When to Use This Pattern

### ✅ Use this pattern when:

- **Atomic subtasks:** Subtasks are small, focused, and independently solvable
- **Verifiable outputs:** Subtask outputs can be evaluated for correctness
- **Error correction needed:** Errors must be caught and corrected before propagating
- **Long task sequences:** Tasks with many steps where error compounding is a concern
- **Deterministic results needed:** Unlike discussion-based consensus, voting produces consistent results
- **Independent agents available:** Multiple agents can solve the same subtask independently

### ❌ Avoid this pattern when:

- **Complex, creative tasks:** Tasks requiring creative synthesis or negotiation (use discussion-based consensus instead)
- **Tight coupling:** Subtasks with complex dependencies that prevent independent solving
- **Cost constraints:** Voting adds computational cost (multiple agents + discriminator)
- **Real-time constraints:** Voting introduces latency that violates timing requirements
- **Single correct answer unclear:** Tasks where "correctness" is subjective or ambiguous
- **Correlated errors:** If agents are likely to make the same mistakes, voting is ineffective

### Decision Guidelines

Use Voting-Based Error Correction when:

- **Atomic subtasks:** Can you break tasks into small, independently solvable units?
- **Error correction critical:** Do errors need to be caught before they propagate?
- **Deterministic needed:** Do you need consistent, predictable results (vs. discussion-based consensus)?
- **Cost acceptable:** Is the computational cost of multiple agents + voting acceptable?

For creative tasks or when discussion/debate is valuable, use **Swarm/Consensus Architecture** instead. For simple tasks with few steps, traditional error handling may be sufficient.

## Practical Applications & Use Cases

Voting-Based Error Correction enables reliable execution of long task sequences:

### Million-Step Problem Solving

**Scenario:** Solving the Towers of Hanoi with 20 disks requires 1,048,576 moves. Each move must be correct, or the solution fails.

**Solution:** For each move (atomic subtask), 3-5 agents independently determine the correct move. A discriminator votes on the candidates, and the move with the most votes (or first to reach threshold) is selected. This enables solving the problem with zero errors despite requiring over a million steps.

### Step-by-Step Reasoning

**Scenario:** Complex mathematical proofs or logical reasoning requiring thousands of steps, where a single error invalidates the entire solution.

**Solution:** Each reasoning step is an atomic subtask. Multiple agents independently perform the step, vote on the correct result, and proceed only when consensus is reached.

### Data Validation at Scale

**Scenario:** Validating millions of data records, where each record requires multiple validation checks, and errors must be caught at the record level.

**Solution:** Each validation check is an atomic subtask. Multiple agents independently validate, vote on the result, and only valid records proceed to the next check.

### Code Generation with Verification

**Scenario:** Generating code for complex systems where each function must be correct, and errors in early functions compound.

**Solution:** Each function is an atomic subtask. Multiple agents independently generate the function, vote on the best implementation, and only the selected function is integrated.

## Implementation

### Core Components

??? "Voting Agent"

    ```python
    from typing import List, Dict, Optional
    from pydantic import BaseModel
    from enum import Enum

    class VotingStrategy(str, Enum):
        FIRST_TO_K = "first_to_k"
        FIRST_TO_AHEAD_BY_K = "first_to_ahead_by_k"
        MAJORITY = "majority"

    class Candidate(BaseModel):
        """A candidate solution from an independent agent."""
        agent_id: str
        solution: str
        confidence: Optional[float] = None
        reasoning: Optional[str] = None

    class VoteResult(BaseModel):
        """Result of voting on candidates."""
        winner: Candidate
        vote_counts: Dict[str, int]
        total_votes: int
        converged: bool

    class VotingErrorCorrection:
        """Voting-based error correction for atomic subtasks."""
        
        def __init__(
            self,
            discriminator_llm,
            strategy: VotingStrategy = VotingStrategy.FIRST_TO_AHEAD_BY_K,
            k: int = 2,
            max_votes: int = 20
        ):
            self.discriminator_llm = discriminator_llm
            self.strategy = strategy
            self.k = k
            self.max_votes = max_votes
        
        async def vote_on_solutions(
            self,
            candidates: List[Candidate],
            subtask_description: str
        ) -> VoteResult:
            """Vote on candidate solutions to select the correct one."""
            
            if len(candidates) == 0:
                raise ValueError("No candidates provided")
            
            if len(candidates) == 1:
                return VoteResult(
                    winner=candidates[0],
                    vote_counts={candidates[0].agent_id: 1},
                    total_votes=1,
                    converged=True
                )
            
            vote_counts = {c.agent_id: 0 for c in candidates}
            total_votes = 0
            
            # Continue voting until convergence
            while total_votes < self.max_votes:
                # Get vote from discriminator
                vote = await self._get_vote(candidates, subtask_description, vote_counts)
                
                # Update vote counts
                vote_counts[vote] += 1
                total_votes += 1
                
                # Check for convergence
                if self._check_convergence(vote_counts, total_votes):
                    winner_id = self._select_winner(vote_counts)
                    winner = next(c for c in candidates if c.agent_id == winner_id)
                    return VoteResult(
                        winner=winner,
                        vote_counts=vote_counts,
                        total_votes=total_votes,
                        converged=True
                    )
            
            # Max votes reached, select winner by majority
            winner_id = self._select_winner(vote_counts)
            winner = next(c for c in candidates if c.agent_id == winner_id)
            return VoteResult(
                winner=winner,
                vote_counts=vote_counts,
                total_votes=total_votes,
                converged=False
            )
        
        async def _get_vote(
            self,
            candidates: List[Candidate],
            subtask_description: str,
            current_votes: Dict[str, int]
        ) -> str:
            """Get a vote from the discriminator agent."""
            candidates_text = "\n\n".join([
                f"Candidate {i+1} (Agent: {c.agent_id}, Current Votes: {current_votes.get(c.agent_id, 0)}):\n{c.solution}"
                for i, c in enumerate(candidates)
            ])
            
            prompt = f"""You are a discriminator agent evaluating candidate solutions.

    Subtask: {subtask_description}

    Candidate Solutions:
    {candidates_text}

    Evaluate each candidate and vote for the best solution. Consider:
    - Correctness
    - Quality
    - Adherence to requirements

    Return only the agent_id of the best candidate (e.g., "agent_1")."""
            
            response = await self.discriminator_llm.ainvoke(prompt)
            vote = response.content.strip()
            
            # Validate vote
            if vote not in [c.agent_id for c in candidates]:
                # Default to first candidate if invalid
                return candidates[0].agent_id
            
            return vote
        
        def _check_convergence(self, vote_counts: Dict[str, int], total_votes: int) -> bool:
            """Check if voting has converged based on strategy."""
            if total_votes == 0:
                return False
            
            if self.strategy == VotingStrategy.FIRST_TO_K:
                # Check if any candidate has k votes
                return max(vote_counts.values()) >= self.k
            
            elif self.strategy == VotingStrategy.FIRST_TO_AHEAD_BY_K:
                # Check if any candidate leads by k votes
                sorted_votes = sorted(vote_counts.values(), reverse=True)
                if len(sorted_votes) < 2:
                    return sorted_votes[0] >= self.k
                return (sorted_votes[0] - sorted_votes[1]) >= self.k
            
            elif self.strategy == VotingStrategy.MAJORITY:
                # Check if any candidate has majority
                max_votes = max(vote_counts.values())
                return max_votes > (total_votes / 2)
            
            return False
        
        def _select_winner(self, vote_counts: Dict[str, int]) -> str:
            """Select winner based on vote counts."""
            return max(vote_counts.items(), key=lambda x: x[1])[0]
    ```

??? "Independent Agent Solver"

    ```python
    class IndependentAgentSolver:
        """Solves atomic subtasks with multiple independent agents."""
        
        def __init__(self, llm, num_agents: int = 3):
            self.llm = llm
            self.num_agents = num_agents
        
        async def solve_independently(
            self,
            subtask_description: str,
            input_data: dict
        ) -> List[Candidate]:
            """Have multiple agents independently solve the same subtask."""
            
            async def solve_one(agent_id: str) -> Candidate:
                prompt = f"""You are agent {agent_id} solving an atomic subtask.

    Subtask: {subtask_description}
    Input: {input_data}

    Solve this subtask independently. Provide your solution."""
                
                response = await self.llm.ainvoke(prompt)
                return Candidate(
                    agent_id=agent_id,
                    solution=response.content,
                    reasoning=None
                )
            
            # Solve with multiple independent agents
            agents = [f"agent_{i+1}" for i in range(self.num_agents)]
            candidates = await asyncio.gather(*[
                solve_one(agent_id) for agent_id in agents
            ])
            
            return candidates
    ```

??? "Complete Example"

    ```python
    import asyncio
    from typing import List

    async def voting_error_correction_workflow(
        subtask_description: str,
        input_data: dict,
        llm
    ):
        """Complete workflow for voting-based error correction."""
        
        # Step 1: Multiple agents independently solve the subtask
        solver = IndependentAgentSolver(llm, num_agents=5)
        candidates = await solver.solve_independently(subtask_description, input_data)
        
        # Step 2: Vote on candidates to select the correct solution
        voter = VotingErrorCorrection(
            discriminator_llm=llm,
            strategy=VotingStrategy.FIRST_TO_AHEAD_BY_K,
            k=2,
            max_votes=20
        )
        
        vote_result = await voter.vote_on_solutions(candidates, subtask_description)
        
        # Step 3: Use the winning solution
        return {
            "winner": vote_result.winner.solution,
            "vote_counts": vote_result.vote_counts,
            "total_votes": vote_result.total_votes,
            "converged": vote_result.converged
        }

    # Usage
    async def main():
        subtask = "Determine the next move in Towers of Hanoi: Move disk from peg A to peg B"
        input_data = {
            "current_state": {"A": [1, 2], "B": [], "C": [3]},
            "target_state": {"A": [], "B": [1, 2, 3], "C": []}
        }
        
        # Requires LLM initialization
        # llm = ChatOpenAI(model="gpt-4o", temperature=0)
        # result = await voting_error_correction_workflow(subtask, input_data, llm)
        # print(f"Winner: {result['winner']}")
        # print(f"Votes: {result['vote_counts']}")

    if __name__ == "__main__":
        asyncio.run(main())
    ```

    ### Advanced: Red-Flagging Integration

    Voting can be improved by red-flagging unreliable candidates before voting:

    ```python
    from red_flagging import RedFlaggingAgent

    class EnhancedVotingErrorCorrection(VotingErrorCorrection):
        """Voting with red-flagging to filter unreliable candidates."""
        
        def __init__(self, *args, red_flag_agent=None, **kwargs):
            super().__init__(*args, **kwargs)
            self.red_flag_agent = red_flag_agent or RedFlaggingAgent(self.discriminator_llm)
        
        async def vote_on_solutions(
            self,
            candidates: List[Candidate],
            subtask_description: str
        ) -> VoteResult:
            """Vote on candidates with red-flagging to filter unreliable ones."""
            
            # Step 1: Red-flag unreliable candidates
            filtered_candidates = []
            for candidate in candidates:
                is_reliable = await self.red_flag_agent.check_reliability(
                    candidate.solution,
                    subtask_description
                )
                if is_reliable:
                    filtered_candidates.append(candidate)
            
            # If all candidates are red-flagged, use all (fallback)
            if len(filtered_candidates) == 0:
                filtered_candidates = candidates
            
            # Step 2: Vote on filtered candidates
            return await super().vote_on_solutions(filtered_candidates, subtask_description)
    ```

## Voting Strategies Comparison

| Strategy | How It Works | Pros | Cons | When to Use |
|----------|--------------|------|------|-------------|
| **First-to-k** | First candidate to reach k votes wins | Fast convergence | Can be influenced by early incorrect solutions | When speed is critical and errors are rare |
| **First-to-ahead-by-k** | First candidate to lead by k votes wins | More robust, requires consistent performance | Slower convergence, requires more votes | When accuracy is critical (recommended) |
| **Majority** | Candidate with most votes wins | Simple, intuitive | May not converge for close races | When you have many candidates and clear winners |

**Recommendation:** Use **First-to-ahead-by-k** for critical tasks where accuracy is paramount. The additional votes required are justified by the improved robustness.

## Key Takeaways

- **Core Concept:** Voting-Based Error Correction uses multiple independent agents to solve the same atomic subtask, then votes to select the correct solution before proceeding.
- **Key Benefit:** Prevents errors from propagating by catching and correcting them at each step through deterministic voting.
- **Independence is Critical:** Agents must solve independently. If agents see each other's work, errors correlate and voting becomes ineffective.
- **Voting Strategies:** First-to-ahead-by-k is more robust than first-to-k, requiring candidates to consistently outperform others.
- **Works with Atomic Subtasks:** Voting is efficient for small, verifiable subtasks. For complex, creative tasks, use discussion-based consensus instead.
- **Best Practice:** Use 3-7 independent agents, first-to-ahead-by-k voting with k=2, and integrate red-flagging to filter unreliable candidates.
- **Common Pitfall:** Correlated errors (agents making the same mistakes) break voting. Ensure agents are truly independent and use red-flagging to detect unreliable solutions.
- **Integration:** Works with **Extreme Decomposition** (provides atomic subtasks) and **Red-Flagging** (improves voting quality).

## Related Patterns

This pattern works well with:

- **Extreme Decomposition** - Provides atomic subtasks that can be independently solved and voted on
- **Red-Flagging** - Proactive error detection improves voting quality by filtering unreliable candidates
- **Exception Handling** - Voting is a form of proactive error correction, complementing reactive error handling

This pattern differs from:

- **Swarm/Consensus Architecture** - Voting is deterministic and efficient; consensus uses discussion/debate which is more flexible but less predictable
- **Self-Consistency** - Self-Consistency votes on final answers; Voting-Based Error Correction votes on each atomic step
- **Multi-Agent Debate** - Debate uses structured argumentation; voting uses deterministic selection

??? "References"

    - **MAKER (2025):** Solving a Million-Step LLM Task with Zero Errors - Meyerson et al. - https://arxiv.org/html/2511.09030v1
    - **First-to-ahead-by-k Voting:** More robust voting mechanism requiring consistent performance
    - **Massively Decomposed Agentic Processes (MDAPs):** Framework combining extreme decomposition with voting-based error correction

