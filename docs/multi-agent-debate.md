# Pattern: Multi-Agent Debate

## Motivation

In legal systems, adversarial proceedings expose flaws and reveal truth through structured argumentation. 
In scientific discourse, peer review and debate surface errors and refine theories. 
In human reasoning, considering opposing viewpoints prevents confirmation bias and leads to better decisions.
The Multi-Agent Debate pattern applies this principle to LLM systems: multiple agents argue different positions, critique each other's reasoning, and surface errors through structured adversarial discussion.

> **"We don't know how to build one super-human AI. But we can build 10 mediocre ones and let them debate."** — Andrej Karpathy

> **"Debate is a search algorithm embedded in communication."** — Anthropic

This pattern is essential when reasoning quality is critical, when hidden assumptions need exposure, or when a single model's initial approach might be flawed.

> **"Multi-agent is about role specialization, not redundancy."** — Manus Team

## Pattern Overview

**What it is:** A multi-agent architecture where agents engage in structured debate by arguing different positions, critiquing each other's reasoning, and working toward improved solutions. 
Debates can be adversarial (agents take opposing stances) or collaborative (agents explore different approaches), often with optional judge agents overseeing the discussion and determining outcomes.

**When to use:** When reasoning quality is critical, when problems benefit from multiple perspectives, when initial solutions might be incorrect, or when errors need to be caught through adversarial critique. 
Particularly valuable for counter-intuitive problems, complex reasoning tasks, or situations where a single model might fixate on incorrect approaches.

**Why it matters:** Structured debate helps overcome "degeneration-of-thought" issues where a single model fixates on an initial incorrect guess. 
By forcing models to articulate and defend different viewpoints, the system reveals hidden assumptions, exposes logical flaws, and yields more creative, correct solutions. 
Research shows that multi-agent debate significantly improves performance on math word problems and factual QA compared to single-model approaches.

Unlike single-agent reflection or evaluator-optimizer patterns, multi-agent debate introduces adversarial or divergent viewpoints that challenge reasoning from different angles. 
This adversarial process surfaces issues that self-evaluation might miss, leading to more robust solutions.

### Key Concepts

- **Debater Agents:** Agents that argue specific positions, defend viewpoints, and critique opposing arguments. Can take adversarial stances (arguing opposite positions) or explore different approaches (arguing alternative solutions).
- **Judge Agent (Optional):** A neutral agent that monitors the debate, evaluates arguments, and determines the winner or synthesizes a final answer from the discussion. Provides quality control and prevents infinite loops.
- **Adversarial Debate:** Two or more agents take opposing stances and argue against each other, pointing out errors and weaknesses in each other's reasoning.
- **Peer Debate:** Multiple agents explore different approaches on equal footing, all able to critique others and propose alternatives without fixed adversarial roles.
- **Divergent Thinking:** Debate encourages exploration of multiple solution paths, preventing fixation on a single approach and enabling discovery of better alternatives.
- **Error Surfacing:** Through adversarial critique, agents expose logical flaws, incorrect assumptions, or reasoning errors that a single model might miss.

### How It Works

Multi-Agent Debate operates through structured argumentation rounds:

1. **Position Taking:** Debater agents take initial positions—either adversarial (opposing stances) or divergent (different approaches). Each agent presents their solution, reasoning, or argument.
2. **Argumentation Rounds:** Agents engage in multiple rounds of argumentation:
   
    - **Present Arguments:** Each agent defends their position with reasoning and evidence
    - **Critique Opponents:** Agents point out flaws, errors, or weaknesses in others' arguments
    - **Refute Criticisms:** Agents address critiques and refine their positions
    - **Iterate:** Process repeats for multiple rounds

3. **Judgment (Optional):** A judge agent monitors the debate, evaluates arguments, and either:

    - **Declares Winner:** Determines which side made the more convincing case
    - **Synthesizes Answer:** Assembles a final answer from the best arguments across all sides
    - **Provides Feedback:** Offers evaluation to guide further rounds

4. **Convergence:** Debate continues until:

    - **Judge Decision:** Judge determines a winner or synthesizes final answer
    - **Convergence:** Agents reach agreement through discussion
    - **Round Limit:** Maximum debate rounds reached
    - **Quality Threshold:** Solution quality meets criteria

5. **Final Synthesis:** System produces final answer based on debate outcomes, judge decision, or convergence.

## When to Use This Pattern

### ✅ Use when:

- **Reasoning quality critical:** Problems require high-quality reasoning where errors are costly
- **Counter-intuitive problems:** Solutions require challenging initial assumptions or exploring non-obvious approaches
- **Single model fixation risk:** Risk that a single model will fixate on an incorrect initial approach
- **Error detection needed:** Need to surface logical flaws, incorrect assumptions, or reasoning errors
- **Multiple valid approaches:** Problem has multiple valid solution paths that should be explored
- **Complex reasoning tasks:** Tasks requiring multi-step reasoning where errors can compound
- **Hidden assumptions:** Problem likely contains implicit assumptions that need explicit examination

### ❌ Avoid when:

- **Simple problems:** Tasks that don't benefit from adversarial exploration
- **Deterministic solutions:** Problems with clear, unambiguous answers where debate adds little value
- **Low-latency requirements:** Debate rounds introduce significant latency that violates timing constraints
- **Resource constraints:** Computational or cost constraints make multiple agents impractical
- **High agreement expected:** Problems where agents are likely to agree immediately, making debate redundant
- **Subjective preference:** Tasks where preference is purely subjective and debate doesn't improve objective quality

### Decision Guidelines

Use Multi-Agent Debate when the benefits of adversarial exploration, error detection, and divergent thinking outweigh the costs (latency, computational expense, complexity). 
Consider: problem complexity (complex = benefit from debate), reasoning difficulty (difficult = benefit from critique), error tolerance (low tolerance = need adversarial verification), and resource availability (sufficient compute = debate viable). 
For simple problems with reliable single agents, debate may add unnecessary overhead.

## Practical Applications & Use Cases

Multi-Agent Debate excels in scenarios requiring high-quality reasoning, error detection, or exploration of multiple solution paths:

### Mathematical Problem Solving

Debate helps solve counter-intuitive math problems where a single model might fixate on incorrect approaches. Adversarial agents challenge each other's reasoning, exposing flaws and leading to correct solutions.

**Example:** Complex word problems where agents debate different solution approaches, catch calculation errors, and verify reasoning steps through adversarial critique.

### Factual Verification

Multiple agents debate claims, evidence, and sources, cross-verifying information and catching errors or inconsistencies. The adversarial process surfaces issues that single-agent fact-checking might miss.

**Example:** Fact-checking system where agents debate the accuracy of claims, challenge evidence, and reach consensus on verified information.

### Complex Reasoning Tasks

Debate improves performance on tasks requiring multi-step reasoning where errors can compound. Agents catch errors in each other's reasoning chains and propose corrections.

**Example:** Logical reasoning problems where agents debate inference chains, point out logical fallacies, and verify conclusions.

### Code Review and Debugging

Adversarial debate helps identify bugs, logical errors, and design flaws in code. Agents argue different interpretations, challenge assumptions, and surface issues through critique.

**Example:** Code review system where agents debate code correctness, argue about edge cases, and identify potential bugs through adversarial discussion.

### Decision Making

Debate explores different decision options, evaluates trade-offs, and surfaces risks or considerations that might be overlooked. The adversarial process leads to more robust decisions.

**Example:** Strategic decision system where agents debate different options, argue pros and cons, and evaluate risks through structured argumentation.

## Modern Frameworks and Research

### Multi-Agent Debate (MAD) Framework (2024)

The MAD framework introduced by Liang et al. (2024) uses two agent debaters taking opposite stances on a question, arguing in rounds and pointing out each other's errors. A third agent acts as a neutral judge, monitoring the debate and ultimately deciding which side made the more convincing case or assembling a final answer from the discussion.

**Key Features:**

- Adversarial debaters with opposing stances
- Neutral judge agent for quality control
- Structured rounds of argumentation and critique
- Overcomes "degeneration-of-thought" in single models

**Research Results:** The framework helped overcome issues where single models fixate on initial incorrect guesses, leading to more creative and correct solutions on counter-intuitive problems.

### Consensus Through Discussion (Du et al., 2023)

Research by Yilun Du et al. (2023) showed that when multiple LLM instances debated and reconciled their reasoning, performance significantly improved on math word problems and factual QA—reducing errors and hallucinations compared to lone models.

**Key Features:**
- Peer-to-peer discussion without fixed adversarial roles
- Iterative refinement through debate
- Error detection through cross-verification
- Consensus-building through reconciliation

## Challenges: Sycophancy and Groupthink

Recent research highlights challenges in multi-agent debate:

- **Sycophancy:** Agents may agree too readily with each other to preserve harmony, reducing debate effectiveness
- **Groupthink:** Agents may converge prematurely on incorrect answers, reinforcing each other's mistakes
- **Premature Convergence:** Debate may end before all issues are fully explored

Solutions include tuning agent personas to maintain healthy dissent, designing prompts to encourage critical thinking, and using judge agents to prevent premature convergence.

## Implementation

### Prerequisites

```bash
pip install langchain langchain-openai langgraph
```

??? "Basic Example: Adversarial Debate with Judge"

    This example demonstrates the MAD framework with two adversarial debaters and a judge:

    ```python
    from langchain_openai import ChatOpenAI
    from typing import List, Dict, Any
    import json

    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    class DebaterAgent:
        """Agent that debates a specific position."""
        
        def __init__(self, agent_id: str, position: str):
            self.agent_id = agent_id
            self.position = position  # "pro" or "con" or specific stance
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)  # Higher temp for creativity
            self.arguments = []
        
        def present_argument(self, question: str, round_num: int) -> str:
            """Present initial argument for this position."""
            if round_num == 1:
                prompt = f"""You are a debater arguing the {self.position} position.

    Question: {question}

    Present your initial argument supporting your position. Be persuasive and provide strong reasoning."""
            else:
                prompt = f"""You are a debater arguing the {self.position} position.

    Question: {question}

    You've been debating this position. Present your argument for this round, building on previous discussion."""
            
            response = self.llm.invoke(prompt)
            argument = response.content
            self.arguments.append({"round": round_num, "type": "argument", "content": argument})
            return argument
        
        def critique_opponent(self, question: str, opponent_argument: str, round_num: int) -> str:
            """Critique the opponent's argument."""
            previous_args = "\n".join([
                f"Round {arg['round']}: {arg['content'][:200]}..."
                for arg in self.arguments[-2:]
            ])
            
            prompt = f"""You are a debater arguing the {self.position} position.

    Question: {question}

    Your previous arguments:
    {previous_args}

    Your opponent's latest argument:
    {opponent_argument}

    Critique your opponent's argument. Point out:
    - Logical flaws or errors
    - Incorrect assumptions
    - Weak reasoning
    - Missing considerations

    Be specific and constructive."""
            
            response = self.llm.invoke(prompt)
            critique = response.content
            self.arguments.append({"round": round_num, "type": "critique", "content": critique})
            return critique
        
        def refute_criticism(self, question: str, criticism: str, round_num: int) -> str:
            """Refute criticism of your argument."""
            prompt = f"""You are a debater arguing the {self.position} position.

    Question: {question}

    Your opponent criticized your argument:
    {criticism}

    Refute this criticism. Address each point:
    - Explain why the criticism is wrong or irrelevant
    - Provide counter-evidence or reasoning
    - Strengthen your position

    Maintain your stance while addressing valid concerns."""
            
            response = self.llm.invoke(prompt)
            refutation = response.content
            self.arguments.append({"round": round_num, "type": "refutation", "content": refutation})
            return refutation

    class JudgeAgent:
        """Neutral judge that evaluates the debate."""
        
        def __init__(self):
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0)  # Lower temp for objectivity
        
        def evaluate_round(self, question: str, debate_history: List[Dict]) -> Dict:
            """Evaluate a debate round and provide feedback."""
            history_text = "\n\n".join([
                f"{item['agent']} ({item['type']}):\n{item['content']}"
                for item in debate_history
            ])
            
            prompt = f"""You are a neutral judge evaluating a debate.

    Question: {question}

    Debate so far:
    {history_text}

    Evaluate the debate:
    1. Assess the quality of arguments from each side
    2. Identify any logical flaws or errors
    3. Note which side is making stronger points
    4. Provide constructive feedback for both sides

    Return your evaluation."""
            
            response = self.llm.invoke(prompt)
            return {"type": "judge_evaluation", "content": response.content}
        
        def decide_winner(self, question: str, debate_history: List[Dict]) -> Dict:
            """Decide the winner or synthesize final answer."""
            history_text = "\n\n".join([
                f"{item['agent']} ({item['type']}):\n{item['content']}"
                for item in debate_history
            ])
            
            prompt = f"""You are a neutral judge concluding a debate.

    Question: {question}

    Complete debate:
    {history_text}

    Your task:
    1. Evaluate which side made the more convincing case
    2. Identify the best arguments and reasoning from both sides
    3. Synthesize a final answer that incorporates the strongest points

    Provide:
    - Your decision on which position is more convincing (or if it's a tie)
    - Your reasoning
    - A final synthesized answer to the original question

    Return as structured evaluation."""
            
            response = self.llm.invoke(prompt)
            return {"type": "final_decision", "content": response.content}

    def adversarial_debate(question: str, num_rounds: int = 3) -> Dict[str, Any]:
        """Run adversarial debate between two agents with a judge."""
        # Create debaters with opposing positions
        debater_pro = DebaterAgent("debater_pro", "supporting/positive position")
        debater_con = DebaterAgent("debater_con", "opposing/negative position")
        judge = JudgeAgent()
        
        debate_history = []
        
        # Round 1: Initial arguments
        arg_pro = debater_pro.present_argument(question, round_num=1)
        debate_history.append({"agent": "debater_pro", "type": "argument", "content": arg_pro})
        
        arg_con = debater_con.present_argument(question, round_num=1)
        debate_history.append({"agent": "debater_con", "type": "argument", "content": arg_con})
        
        # Subsequent rounds: Critique and refute
        for round_num in range(2, num_rounds + 1):
            # Judge evaluates so far
            judge_eval = judge.evaluate_round(question, debate_history)
            debate_history.append({"agent": "judge", **judge_eval})
            
            # Agents critique each other
            critique_pro = debater_pro.critique_opponent(question, arg_con, round_num)
            debate_history.append({"agent": "debater_pro", "type": "critique", "content": critique_pro})
            
            critique_con = debater_con.critique_opponent(question, arg_pro, round_num)
            debate_history.append({"agent": "debater_con", "type": "critique", "content": critique_con})
            
            # Agents refute criticisms
            refutation_pro = debater_pro.refute_criticism(question, critique_con, round_num)
            debate_history.append({"agent": "debater_pro", "type": "refutation", "content": refutation_pro})
            
            refutation_con = debater_con.refute_criticism(question, critique_pro, round_num)
            debate_history.append({"agent": "debater_con", "type": "refutation", "content": refutation_con})
        
        # Final judgment
        final_decision = judge.decide_winner(question, debate_history)
        debate_history.append({"agent": "judge", **final_decision})
        
        return {
            "question": question,
            "debate_history": debate_history,
            "final_decision": final_decision
        }

    # Usage
    result = adversarial_debate(
        "Should LLM agents have access to external tools, or should they work with reasoning alone?",
        num_rounds=3
    )
    print(result["final_decision"]["content"])
    ```

**Explanation:**
This example demonstrates the MAD framework: two debaters take opposing positions, argue in rounds, critique each other, and refute criticisms. A judge agent monitors the debate and makes a final decision. The adversarial process surfaces errors and leads to more robust solutions.

??? "Advanced Example: Peer Debate Without Judge"

    This example shows a peer-to-peer debate where all agents are equal:

    ```python
    class PeerDebater:
        """Agent that participates in peer debate without fixed roles."""
        
        def __init__(self, agent_id: str, perspective: str):
            self.agent_id = agent_id
            self.perspective = perspective  # Different reasoning approach
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0.8)  # Higher temp for diversity
            self.contributions = []
        
        def contribute(self, question: str, debate_so_far: List[Dict]) -> str:
            """Contribute to the debate from this agent's perspective."""
            if not debate_so_far:
                # First contribution
                prompt = f"""You are an expert with a {self.perspective} reasoning approach.

    Question: {question}

    Provide your initial perspective and solution approach. Be thorough and explain your reasoning."""
            else:
                # Respond to ongoing debate
                debate_text = "\n\n".join([
                    f"{item['agent']}: {item['content']}"
                    for item in debate_so_far[-5:]  # Last 5 contributions
                ])
                
                prompt = f"""You are an expert with a {self.perspective} reasoning approach.

    Question: {question}

    Debate so far:
    {debate_text}

    Contribute to the debate. You can:
    - Agree or disagree with others
    - Point out errors or flaws
    - Propose alternative approaches
    - Challenge assumptions
    - Build on others' ideas

    Maintain your {self.perspective} perspective while engaging constructively."""
            
            response = self.llm.invoke(prompt)
            contribution = response.content
            self.contributions.append(contribution)
            return contribution

    def peer_debate(question: str, num_agents: int = 3, num_rounds: int = 5) -> Dict[str, Any]:
        """Run peer-to-peer debate without judge."""
        perspectives = [
            "analytical and detail-oriented",
            "creative and out-of-the-box",
            "pragmatic and solution-focused"
        ]
        
        agents = [
            PeerDebater(f"agent_{i}", perspectives[i % len(perspectives)])
            for i in range(num_agents)
        ]
        
        debate_history = []
        
        # Multiple rounds of peer discussion
        for round_num in range(num_rounds):
            for agent in agents:
                contribution = agent.contribute(question, debate_history)
                debate_history.append({
                    "agent": agent.agent_id,
                    "round": round_num,
                    "content": contribution
                })
        
        # Synthesize final answer from debate
        debate_text = "\n\n".join([
            f"{item['agent']} (Round {item['round']}):\n{item['content']}"
            for item in debate_history
        ])
        
        synthesis_prompt = f"""Synthesize this peer debate into a final answer.

    Question: {question}

    Debate:
    {debate_text}

    Create a comprehensive answer that:
    - Incorporates the best insights from all perspectives
    - Addresses the key points raised in the debate
    - Represents a synthesis of the discussion

    Provide the final answer."""
        
        final_answer = llm.invoke(synthesis_prompt)
        
        return {
            "question": question,
            "debate_history": debate_history,
            "final_answer": final_answer.content
        }

    # Usage
    result = peer_debate(
        "What is the best approach for handling context window limitations in LLM agents?",
        num_rounds=4
    )
    print(result["final_answer"])
    ```

**Explanation:**
This example demonstrates peer-to-peer debate where all agents are equal, can critique others, and explore different approaches. There's no fixed adversarial structure or judge—agents engage in open discussion and the system synthesizes a final answer from the debate.

## Key Takeaways

- **Core Concept:** Multi-Agent Debate uses structured argumentation between agents to improve reasoning quality, surface errors, and overcome fixation on incorrect approaches.
- **Key Benefits:** Error detection through adversarial critique, improved reasoning by challenging assumptions, divergent thinking that explores multiple solution paths, and more robust solutions than single-agent approaches.
- **Debate Structures:** Adversarial debates (opposing positions), peer debates (equal exploration), and judge-mediated debates (quality control) each serve different purposes.
- **Trade-offs:** Debate improves reasoning quality but introduces latency, computational expense, and complexity. Use when benefits outweigh costs.
- **Best Practice:** Design debate protocols that encourage productive argumentation while preventing infinite loops. Use judges or convergence criteria to determine when debate should conclude.
- **Common Pitfall:** Agents may exhibit sycophancy (agreeing too readily) or groupthink (converging on incorrect answers). Design prompts to maintain healthy dissent and critical thinking.
- **Research Evidence:** Studies show multi-agent debate significantly improves performance on reasoning tasks, math problems, and factual QA compared to single-model approaches.

## Related Patterns

This pattern works well with:

- **Pattern: Swarm/Consensus Architecture** - Debate can be part of consensus-building mechanisms
- **Pattern: Evaluator-Optimizer** - Debate can serve as an evaluation mechanism for generated solutions
- **Pattern: Planner-Checker** - Debate can be used by checker agents to verify plans or solutions
- **Pattern: Reflection** - Single agents can debate with themselves using different personas

??? "References"

    - **Multi-Agent Debate (MAD) Framework:** Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate (Liang et al., 2024) - https://arxiv.org/abs/2305.19118
    - **Consensus Through Debate:** Improving Factuality and Reasoning in Language Models through Multiagent Debate (Du et al., 2023) - https://arxiv.org/abs/2305.14325
    - **Sycophancy Challenges:** Peacemaker or Troublemaker: How Sycophancy Shapes Multi-Agent Debate - https://arxiv.org/html/2509.23055v1
    - **Debate Strategies:** Should we be going MAD? A Look at Multi-Agent Debate Strategies - https://arxiv.org/pdf/2311.17371

