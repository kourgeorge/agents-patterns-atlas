# Pattern: Red-Flagging

## Motivation

When a doctor reviews test results, they look for warning signs—red flags—that indicate potential problems. 
Elevated markers, unusual patterns, or contradictory readings signal that something might be wrong, even before a definitive diagnosis. 
By detecting these red flags early, doctors can investigate further, order additional tests, or adjust treatment before problems escalate.
Similarly, when LLM agents generate solutions, their outputs can contain warning signs—confusion, circular reasoning, contradictions, or incoherence—that indicate unreliability. 
By detecting these red flags before using the solution, we can filter unreliable outputs, request regenerations, or weight them differently in voting. 
This proactive error detection is especially critical in voting-based systems, where correlated errors (multiple agents making the same mistake) can break the voting mechanism.

> **"Red-flagging: Recognizing Signs of Unreliability"** — Meyerson et al., MAKER (2025)

## Pattern Overview

### Problem

LLM agents can produce outputs that appear correct on the surface but contain subtle errors, confusion, or unreliability. 
These unreliable outputs can:

- **Propagate errors:** Unreliable outputs used in subsequent steps cause errors to compound
- **Waste resources:** Unreliable outputs trigger unnecessary retries or corrections downstream
- **Reduce accuracy:** Using unreliable outputs reduces overall system accuracy
- **Break voting mechanisms:** If multiple agents produce similarly unreliable outputs, voting fails to catch errors

Traditional error detection is reactive—it catches errors after they occur. 
But for long task sequences, we need proactive detection that identifies unreliable outputs before they're used.

### Solution

Red-Flagging proactively detects signs of unreliability in agent outputs before they're used. 
A red-flagging agent (or mechanism) analyzes outputs for warning signs:

- **Confusion indicators:** Uncertainty, contradictory statements, "I'm not sure"
- **Circular reasoning:** Repeating the same points without progress
- **Incoherence:** Illogical statements, non-sequiturs, disconnected thoughts
- **Contradictions:** Self-contradictory statements within the output
- **Incomplete reasoning:** Missing steps, gaps in logic, abrupt conclusions

When red flags are detected, the system can:

- **Filter the output:** Exclude it from voting or downstream use
- **Request regeneration:** Ask the agent to regenerate the solution
- **Weight differently:** Reduce the weight of red-flagged outputs in voting
- **Trigger additional verification:** Request more agents to solve the subtask

This proactive detection prevents unreliable outputs from being used, improving overall system reliability.

### Key Concepts

- **Red Flags:** Warning signs in agent outputs that indicate potential unreliability. Common red flags include:

    - Confusion and uncertainty
    - Circular reasoning
    - Contradictions
    - Incoherence
    - Incomplete reasoning

- **Red-Flagging Agent:** An agent (often an LLM) that analyzes outputs for red flags. The agent is trained or prompted to recognize patterns indicating unreliability.
- **Reliability Score:** A quantitative measure of output reliability (e.g., 0.0-1.0). Outputs below a threshold are considered unreliable.
- **Filtering Strategy:** How to handle red-flagged outputs:

    - **Hard Filter:** Completely exclude red-flagged outputs
    - **Soft Filter:** Weight red-flagged outputs differently (e.g., lower weight in voting)
    - **Regeneration:** Request the agent to regenerate the solution
- **Correlation Detection:** Identifying when multiple agents produce similarly unreliable outputs (correlated errors), which breaks voting mechanisms.

### How It Works

Red-Flagging operates through proactive analysis of agent outputs:

**1. Output Analysis**

After an agent produces a solution, a red-flagging agent analyzes it:

- **Pattern Detection:** Looks for red flag patterns (confusion, circular reasoning, contradictions)
- **Coherence Check:** Evaluates logical consistency and completeness
- **Quality Assessment:** Checks if the output meets quality standards

**2. Red Flag Detection**

The red-flagging agent identifies specific red flags:

- **Confusion Indicators:** Phrases like "I'm not sure", "maybe", "perhaps", contradictory statements
- **Circular Reasoning:** Repeating the same points, going in circles without progress
- **Contradictions:** Self-contradictory statements within the output
- **Incoherence:** Illogical statements, non-sequiturs, disconnected thoughts
- **Incomplete Reasoning:** Missing steps, gaps in logic, abrupt conclusions

**3. Reliability Scoring**

The red-flagging agent assigns a reliability score:

- **High Reliability (0.8-1.0):** No red flags, clear reasoning, coherent output
- **Medium Reliability (0.5-0.8):** Minor issues, some uncertainty, but generally sound
- **Low Reliability (0.0-0.5):** Multiple red flags, significant issues, unreliable output

**4. Filtering Decision**

Based on the reliability score and filtering strategy:

- **Hard Filter:** If reliability < threshold, exclude the output
- **Soft Filter:** If reliability < threshold, reduce weight in voting
- **Regeneration:** If reliability < threshold, request regeneration
- **Pass Through:** If reliability >= threshold, use the output normally

**5. Correlation Detection**

For voting systems, detect correlated errors:

- Compare red flags across multiple agent outputs
- If multiple agents show similar red flags, this indicates correlated errors
- Trigger additional agents or different approaches to break correlation

## When to Use This Pattern

### ✅ Use this pattern when:

- **Voting-based systems:** Voting mechanisms need reliable inputs; red-flagging filters unreliable candidates
- **Long task sequences:** Unreliable outputs in early steps compound errors downstream
- **High accuracy requirements:** Tasks where even subtle errors are unacceptable
- **Proactive error prevention:** Need to catch errors before they're used, not after
- **Correlation concerns:** Systems where correlated errors (multiple agents making the same mistake) are a risk
- **Quality control:** Need to ensure outputs meet quality standards before use

### ❌ Avoid this pattern when:

- **Simple, reliable tasks:** Tasks where agents rarely produce unreliable outputs
- **Cost constraints:** Red-flagging adds computational cost (additional LLM calls)
- **Real-time constraints:** Red-flagging adds latency that violates timing requirements
- **Creative tasks:** Tasks where "unreliability" is subjective or part of the creative process
- **Low-stakes tasks:** Tasks where occasional unreliable outputs are acceptable

### Decision Guidelines

Use Red-Flagging when:

- **Voting systems:** Are you using voting-based error correction? Red-flagging improves voting quality.
- **Error correlation risk:** Are multiple agents likely to make similar mistakes? Red-flagging helps detect correlation.
- **Proactive needed:** Do you need to catch errors before they're used? Red-flagging is proactive.
- **Cost acceptable:** Is the computational cost of red-flagging acceptable?

For simple tasks or when reactive error handling is sufficient, red-flagging may add unnecessary overhead.

## Practical Applications & Use Cases

Red-Flagging improves reliability in systems using voting or multi-agent approaches:

### Voting-Based Error Correction

**Scenario:** Multiple agents independently solve atomic subtasks, then vote to select the correct solution. Some agents produce unreliable outputs with confusion or circular reasoning.

**Solution:** Before voting, red-flag unreliable outputs. Filter them out or weight them differently, ensuring only reliable candidates participate in voting. This prevents unreliable outputs from influencing the vote.

### Long-Horizon Task Execution

**Scenario:** Executing a task with thousands of steps, where unreliable outputs in early steps cause errors to compound.

**Solution:** Red-flag outputs at each step. If an output is unreliable, request regeneration or trigger additional agents before proceeding. This prevents unreliable outputs from propagating.

### Multi-Agent Consensus

**Scenario:** Multiple agents discuss and reach consensus, but some agents contribute unreliable inputs that skew the discussion.

**Solution:** Red-flag agent contributions before they're incorporated into the discussion. Filter unreliable contributions or request clarification, improving consensus quality.

### Code Generation with Verification

**Scenario:** Generating code where unreliable outputs (confused logic, incomplete reasoning) cause bugs that are hard to detect.

**Solution:** Red-flag generated code before compilation or testing. Request regeneration for unreliable outputs, reducing bugs and improving code quality.

## Implementation

### Core Components

??? "Red-Flagging Agent"

    ```python
    from typing import List, Optional
    from pydantic import BaseModel, Field
    from enum import Enum

    class RedFlagType(str, Enum):
        CONFUSION = "confusion"
        CIRCULAR_REASONING = "circular_reasoning"
        CONTRADICTION = "contradiction"
        INCOHERENCE = "incoherence"
        INCOMPLETE = "incomplete"

    class RedFlag(BaseModel):
        """A detected red flag in an output."""
        type: RedFlagType
        description: str
        severity: float = Field(ge=0.0, le=1.0)  # 0.0 = minor, 1.0 = severe
        location: Optional[str] = None  # Where in the output the flag was detected

    class ReliabilityAssessment(BaseModel):
        """Assessment of output reliability."""
        reliability_score: float = Field(ge=0.0, le=1.0)
        red_flags: List[RedFlag] = Field(default_factory=list)
        is_reliable: bool
        reasoning: str

    class RedFlaggingAgent:
        """Agent that detects red flags in outputs."""
        
        def __init__(self, llm, reliability_threshold: float = 0.7):
            self.llm = llm
            self.reliability_threshold = reliability_threshold
        
        async def check_reliability(
            self,
            output: str,
            task_description: str,
            context: Optional[dict] = None
        ) -> ReliabilityAssessment:
            """Check output for red flags and assess reliability."""
            
            prompt = self._build_prompt(output, task_description, context)
            response = await self.llm.ainvoke(prompt)
            
            # Parse structured response
            assessment = self._parse_assessment(response.content)
            
            # Determine if reliable
            assessment.is_reliable = assessment.reliability_score >= self.reliability_threshold
            
            return assessment
        
        def _build_prompt(
            self,
            output: str,
            task_description: str,
            context: Optional[dict]
        ) -> str:
            """Build prompt for red-flagging analysis."""
            context_str = f"\nContext: {context}" if context else ""
            
            return f"""You are a red-flagging agent that detects signs of unreliability in outputs.

    Task: {task_description}
    {context_str}

    Output to analyze:
    {output}

    Analyze this output for red flags indicating unreliability. Look for:

    1. **Confusion Indicators:**
    - Uncertainty ("I'm not sure", "maybe", "perhaps")
    - Contradictory statements
    - Lack of confidence

    2. **Circular Reasoning:**
    - Repeating the same points without progress
    - Going in circles
    - No forward movement in reasoning

    3. **Contradictions:**
    - Self-contradictory statements
    - Conflicting information within the output

    4. **Incoherence:**
    - Illogical statements
    - Non-sequiturs
    - Disconnected thoughts

    5. **Incomplete Reasoning:**
    - Missing steps
    - Gaps in logic
    - Abrupt conclusions

    Return a JSON object with:
    - reliability_score: float (0.0-1.0, where 1.0 is most reliable)
    - red_flags: list of objects with type, description, severity (0.0-1.0), and optional location
    - reasoning: explanation of the assessment

    Example:
    {{
    "reliability_score": 0.85,
    "red_flags": [
        {{
        "type": "confusion",
        "description": "Contains uncertainty markers",
        "severity": 0.3,
        "location": "middle section"
        }}
    ],
    "reasoning": "Output is generally reliable but shows some uncertainty in the middle section."
    }}"""
        
        def _parse_assessment(self, response: str) -> ReliabilityAssessment:
            """Parse LLM response into ReliabilityAssessment."""
            import json
            try:
                data = json.loads(response)
                red_flags = [
                    RedFlag(**flag) for flag in data.get("red_flags", [])
                ]
                return ReliabilityAssessment(
                    reliability_score=data.get("reliability_score", 0.5),
                    red_flags=red_flags,
                    is_reliable=False,  # Will be set by caller
                    reasoning=data.get("reasoning", "")
                )
            except Exception as e:
                # Fallback if parsing fails
                return ReliabilityAssessment(
                    reliability_score=0.5,
                    red_flags=[],
                    is_reliable=False,
                    reasoning=f"Failed to parse assessment: {e}"
                )
    ```

??? "Filtering Strategies"

    ```python
    from typing import List, Optional
    from voting_error_correction import Candidate

    class FilteringStrategy:
        """Strategies for handling red-flagged outputs."""
        
        @staticmethod
        async def hard_filter(
            candidates: List[Candidate],
            red_flag_agent: RedFlaggingAgent,
            task_description: str
        ) -> List[Candidate]:
            """Hard filter: exclude all red-flagged candidates."""
            reliable_candidates = []
            
            for candidate in candidates:
                assessment = await red_flag_agent.check_reliability(
                    candidate.solution,
                    task_description
                )
                if assessment.is_reliable:
                    reliable_candidates.append(candidate)
            
            # If all candidates are filtered, return all (fallback)
            return reliable_candidates if reliable_candidates else candidates
        
        @staticmethod
        async def soft_filter(
            candidates: List[Candidate],
            red_flag_agent: RedFlaggingAgent,
            task_description: str
        ) -> List[tuple[Candidate, float]]:
            """Soft filter: weight candidates by reliability score."""
            weighted_candidates = []
            
            for candidate in candidates:
                assessment = await red_flag_agent.check_reliability(
                    candidate.solution,
                    task_description
                )
                # Use reliability score as weight
                weight = assessment.reliability_score
                weighted_candidates.append((candidate, weight))
            
            return weighted_candidates
        
        @staticmethod
        async def detect_correlation(
            candidates: List[Candidate],
            red_flag_agent: RedFlaggingAgent,
            task_description: str
        ) -> bool:
            """Detect if multiple candidates show similar red flags (correlated errors)."""
            assessments = []
            
            for candidate in candidates:
                assessment = await red_flag_agent.check_reliability(
                    candidate.solution,
                    task_description
                )
                assessments.append(assessment)
            
            # Check if multiple candidates have similar red flags
            if len(assessments) < 2:
                return False
            
            # Count candidates with red flags
            red_flagged_count = sum(1 for a in assessments if not a.is_reliable)
            
            # If majority are red-flagged, likely correlation
            return red_flagged_count > (len(assessments) / 2)
    ```

??? "Complete Example"

    ```python
    import asyncio
    from typing import List

    async def red_flagging_workflow(
        candidates: List[Candidate],
        task_description: str,
        llm
    ):
        """Complete workflow for red-flagging with filtering."""
        
        # Step 1: Red-flag all candidates
        red_flag_agent = RedFlaggingAgent(llm, reliability_threshold=0.7)
        
        # Step 2: Hard filter unreliable candidates
        reliable_candidates = await FilteringStrategy.hard_filter(
            candidates,
            red_flag_agent,
            task_description
        )
        
        # Step 3: Check for correlation (if multiple candidates are unreliable)
        is_correlated = await FilteringStrategy.detect_correlation(
            candidates,
            red_flag_agent,
            task_description
        )
        
        if is_correlated:
            # Correlation detected - may need different approach
            print("Warning: Correlated errors detected. Consider different agents or approach.")
        
        # Step 4: Use filtered candidates for voting
        return reliable_candidates

    # Usage
    async def main():
        candidates = [
            Candidate(agent_id="agent_1", solution="Correct solution with clear reasoning."),
            Candidate(agent_id="agent_2", solution="I'm not sure, maybe this is correct? Perhaps..."),
            Candidate(agent_id="agent_3", solution="Another correct solution."),
        ]
        
        task = "Solve this atomic subtask"
        
        # Requires LLM initialization
        # llm = ChatOpenAI(model="gpt-4o", temperature=0)
        # reliable = await red_flagging_workflow(candidates, task, llm)
        # print(f"Reliable candidates: {[c.agent_id for c in reliable]}")

    if __name__ == "__main__":
        asyncio.run(main())
    ```

??? "Integration with Voting"

    Red-flagging integrates seamlessly with voting-based error correction:

    ```python
    from voting_error_correction import VotingErrorCorrection, Candidate

    class EnhancedVotingWithRedFlagging(VotingErrorCorrection):
        """Voting with red-flagging to filter unreliable candidates."""
        
        def __init__(self, *args, red_flag_agent=None, **kwargs):
            super().__init__(*args, **kwargs)
            self.red_flag_agent = red_flag_agent
        
        async def vote_on_solutions(
            self,
            candidates: List[Candidate],
            subtask_description: str
        ) -> VoteResult:
            """Vote on candidates with red-flagging pre-filtering."""
            
            if self.red_flag_agent:
                # Step 1: Red-flag and filter unreliable candidates
                reliable_candidates = await FilteringStrategy.hard_filter(
                    candidates,
                    self.red_flag_agent,
                    subtask_description
                )
                
                # Step 2: Vote on reliable candidates only
                return await super().vote_on_solutions(reliable_candidates, subtask_description)
            else:
                # No red-flagging, use standard voting
                return await super().vote_on_solutions(candidates, subtask_description)
    ```

## Red Flag Patterns

Common red flag patterns to detect:

| Red Flag Type | Indicators | Example |
|--------------|------------|---------|
| **Confusion** | "I'm not sure", "maybe", "perhaps", "I think", contradictory statements | "I'm not sure, but maybe the answer is X, or perhaps Y?" |
| **Circular Reasoning** | Repeating same points, going in circles, no progress | "The solution is X because X is the solution, and X solves it because..." |
| **Contradiction** | Self-contradictory statements | "The value is 5. Actually, it's 10. Wait, it might be 5." |
| **Incoherence** | Illogical statements, non-sequiturs | "The sky is blue, therefore the answer is 42." |
| **Incomplete** | Missing steps, gaps, abrupt conclusions | "Step 1: X. Step 3: Z." (missing Step 2) |

## Key Takeaways

- **Core Concept:** Red-Flagging proactively detects signs of unreliability in agent outputs before they're used, preventing errors from propagating.
- **Key Benefit:** Improves reliability by filtering unreliable outputs, especially critical in voting-based systems where correlated errors break voting.
- **Red Flag Types:** Confusion, circular reasoning, contradictions, incoherence, and incomplete reasoning are common red flags.
- **Filtering Strategies:** Hard filter (exclude), soft filter (weight), or regeneration based on reliability score.
- **Correlation Detection:** Detects when multiple agents produce similarly unreliable outputs, indicating correlated errors that break voting.
- **Best Practice:** Use red-flagging before voting to filter unreliable candidates. Set reliability threshold (e.g., 0.7) and use hard filtering for critical tasks.
- **Common Pitfall:** Over-filtering can remove all candidates. Always have a fallback (e.g., use all candidates if all are filtered).
- **Integration:** Works with **Voting-Based Error Correction** (filters unreliable candidates) and **Extreme Decomposition** (ensures atomic subtask outputs are reliable).

## Related Patterns

This pattern works well with:

- **Voting-Based Error Correction** - Red-flagging filters unreliable candidates before voting, improving voting quality
- **Extreme Decomposition** - Red-flagging ensures atomic subtask outputs are reliable before composition
- **Exception Handling** - Red-flagging is proactive error detection, complementing reactive error handling
- **Reflection** - Red-flagging can trigger reflection to improve outputs

This pattern differs from:

- **Exception Handling** - Red-flagging is proactive (detects before use); exception handling is reactive (handles after errors occur)
- **Reflection** - Red-flagging detects problems; reflection analyzes and improves outputs

??? "References"

    - **MAKER (2025):** Solving a Million-Step LLM Task with Zero Errors - Meyerson et al. - https://arxiv.org/html/2511.09030v1
    - **Red-Flagging:** Recognizing Signs of Unreliability - Section 3.3 of MAKER paper
    - **Correlated Errors:** Understanding how multiple agents can make similar mistakes, breaking voting mechanisms

