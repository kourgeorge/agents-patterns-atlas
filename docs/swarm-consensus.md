# Pattern: Swarm/Consensus Architecture

## Motivation

Multiple experts discussing a problem can reach better solutions than any individual expert working alone. Through natural language dialogue, debate, and consensus-building, groups of LLM agents can surface insights, catch errors, and converge on high-quality solutions that exceed what a single agent could achieve.

The Swarm/Consensus Architecture pattern enables autonomous LLM agents to coordinate through natural language discussion, debate, voting, or consensus mechanisms, without requiring a central orchestrator. This pattern is essential when multiple perspectives are valuable, when errors need to be caught through cross-verification, or when collective intelligence can improve reasoning quality beyond individual capabilities.

## Pattern Overview

**What it is:** A decentralized multi-agent architecture where autonomous LLM agents coordinate through natural language discussion, debate, voting mechanisms, or shared knowledge bases. Agents make decisions independently based on their reasoning, engage in dialogue with other agents, and reach collective decisions through consensus.

**When to use:** When multiple perspectives improve solution quality, when cross-verification is needed to catch errors, when reasoning benefits from debate and discussion, or when collective intelligence can outperform individual agents. Also valuable when agents have different viewpoints that should be reconciled.

**Why it matters:** Natural language consensus provides error correction (multiple agents catch mistakes), improved reasoning quality (debate surfaces hidden assumptions), diversity of perspectives (different agents explore different approaches), and collective intelligence (group performance exceeds individual capabilities). Research shows that when LLM agents debate and reconcile their reasoning, performance significantly improves on math problems and factual QA.

Unlike orchestrator-worker patterns that rely on central coordination, swarm/consensus architectures distribute decision-making across agents. Agents engage in peer-to-peer communication, enabling collaborative problem-solving, error detection, and collective reasoning that centralized systems cannot achieve.

### Key Concepts

- **Natural Language Discussion:** Agents communicate through natural language dialogue, debate, negotiation, or discussion to share perspectives, critique reasoning, and build consensus.

- **Consensus Mechanisms:** Mechanisms for agents to agree on decisions or solutions through voting, iterative discussion, or convergence to shared understanding. Includes majority voting, weighted aggregation, and iterative refinement until agreement.

- **Peer-to-Peer Coordination:** Agents interact as equals without central authority, enabling open dialogue where any agent can critique others or propose solutions.

- **Collective Intelligence:** Group performance exceeds individual capabilities through collaboration, debate, and synthesis of multiple perspectives.

- **Error Detection and Correction:** Multiple agents cross-verify each other's reasoning, catching errors, hallucinations, or logical flaws that a single agent might miss.

- **Convergence:** Systems converge to stable solutions through iterative discussion, voting rounds, or consensus algorithms. Convergence criteria determine when agents have reached sufficient agreement.

### How It Works

LLM-based swarm/consensus architectures operate through several coordination mechanisms:

1. **Natural Language Discussion:** Agents engage in multi-turn dialogues, sharing perspectives, asking questions, and building on each other's insights. For example, research agents discuss findings, debate interpretations, and converge on shared understanding.

2. **Consensus Mechanisms:** Agents agree on decisions or solutions:
   - **Voting:** Agents vote on options; majority or weighted voting determines outcome
   - **Iterative Discussion:** Agents discuss and refine solutions until convergence
   - **Consensus Through Dialogue:** Agents reach agreement through natural language negotiation and reconciliation

3. **Peer Interactions:** Agents interact directly with each other without central coordinator, enabling open dialogue and equal participation. This enables scalability and reduces coordination overhead.

4. **Error Cross-Verification:** Agents critique each other's reasoning, pointing out errors, logical flaws, or inconsistencies. This collaborative verification improves accuracy.

5. **Convergence:** Systems converge to stable solutions through iterative updates, discussion rounds, or consensus algorithms. Convergence criteria (agreement threshold, stability, timeout) determine when coordination is complete.

## When to Use This Pattern

### ✅ Use when:

- **Multiple perspectives valuable:** Problem benefits from diverse viewpoints and approaches
- **Error detection critical:** Need cross-verification to catch mistakes, hallucinations, or logical errors
- **Reasoning quality important:** Debate and discussion improve solution quality by surfacing hidden assumptions
- **Collective intelligence beneficial:** Group performance can exceed individual capabilities
- **No central authority needed:** Decentralized coordination is sufficient and desirable
- **Natural language negotiation:** Agents need to negotiate, bargain, or build consensus through dialogue
- **Redundant verification:** Critical decisions benefit from multiple independent evaluations

### ❌ Avoid when:

- **Strong coordination required:** Need guaranteed coordination that centralized systems provide
- **Deterministic outcomes needed:** Require predictable, deterministic coordination rather than emergent consensus
- **Low latency critical:** Discussion and consensus introduce latency that violates timing requirements
- **Simple problems:** Tasks that don't benefit from multiple perspectives or debate
- **Resource constraints:** Computational or cost constraints make multiple agents impractical
- **Tight coupling:** Agents have strong dependencies requiring explicit coordination

### Decision Guidelines

Use Swarm/Consensus Architecture when the benefits of multiple perspectives, error detection, and collective intelligence outweigh the costs (coordination overhead, latency, complexity). Consider: problem complexity (complex = benefit from multiple perspectives), error tolerance (low tolerance = need cross-verification), reasoning requirements (difficult reasoning = benefit from debate), and coordination needs (decentralized sufficient = consensus viable). For simple problems with reliable single agents, centralized coordination may be simpler and more efficient.

## Practical Applications & Use Cases

LLM-based swarm/consensus architectures excel in scenarios requiring multiple perspectives, error detection, or collective reasoning:

### Consensus Through Discussion

Multiple LLM agents discuss a question and converge on a joint answer, using debate and agreement as a means of verification. Research by Yilun Du et al. (2023) showed that when models debated and reconciled their reasoning, it significantly enhanced performance on math word problems and factual QA—reducing errors and hallucinations compared to a lone model.

**Example:** "Society of Minds" approach where several instances of an LLM each propose their own solution, then critique and revise in light of others' arguments, aiming to reach a consensus through iterative discussion.

### Peer-to-Peer Research Teams

Research agents independently investigate different aspects of a question, share findings through natural language discussion, debate interpretations, and converge on solutions through consensus. Agents work in parallel, building on each other's discoveries without central coordination.

**Example:** Research system where agents independently investigate different aspects, share findings through discussion, debate the importance of insights, and vote on the most important findings to include in final report.

### Collective Decision-Making

Agents vote or reach consensus on decisions through discussion and negotiation, enabling distributed governance, collaborative evaluation, or group intelligence systems.

**Example:** Multiple agents independently evaluate options, discuss pros and cons through natural language, and reach consensus through iterative voting rounds or discussion until agreement.

### Multi-Agent Fact-Checking

Multiple agents independently verify claims, discuss evidence, and reach consensus on accuracy. This cross-verification catches errors that a single agent might miss.

**Example:** Fact-checking system where agents independently research claims, share evidence, debate credibility, and vote on accuracy through discussion.

### Natural Language Negotiation

Agents engage in multi-turn bargaining, alliance formation, and consensus-building through natural language, as demonstrated by CICERO in Diplomacy. Agents negotiate terms, make promises, and adjust strategies based on responses.

**Example:** Cooperative negotiation system where agents discuss terms, negotiate solutions, build alliances, and reach agreements through natural language dialogue.

## Implementation

### Prerequisites

```bash
pip install langchain langchain-openai langgraph
```

### Basic Example: Consensus Through Discussion

This example demonstrates research agents that coordinate through natural language discussion and reach consensus:

```python
from langchain_openai import ChatOpenAI
from typing import List, Dict, Any
from collections import defaultdict
import json

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class DiscussionAgent:
    """LLM agent that participates in consensus-building discussion."""
    
    def __init__(self, agent_id: str, perspective: str):
        self.agent_id = agent_id
        self.perspective = perspective  # e.g., "technical", "user-focused", "business"
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.opinions = []
    
    def propose_solution(self, query: str) -> str:
        """Agent proposes initial solution from their perspective."""
        prompt = f"""You are an expert agent with a {self.perspective} perspective.

Query: {query}

From your {self.perspective} perspective, propose a solution or answer. Explain your reasoning."""
        
        response = self.llm.invoke(prompt)
        solution = response.content
        self.opinions.append({"type": "proposal", "content": solution})
        return solution
    
    def critique(self, query: str, other_solutions: List[str]) -> str:
        """Agent critiques other agents' solutions."""
        solutions_text = "\n\n".join([f"Solution {i+1}:\n{sol}" for i, sol in enumerate(other_solutions)])
        
        prompt = f"""You are an expert agent with a {self.perspective} perspective.

Query: {query}

Other agents proposed these solutions:
{solutions_text}

Critique these solutions. Point out:
- Strengths and weaknesses
- Potential errors or issues
- Missing considerations
- How they could be improved

Provide your critique."""
        
        response = self.llm.invoke(prompt)
        critique = response.content
        self.opinions.append({"type": "critique", "content": critique})
        return critique
    
    def revise(self, query: str, all_opinions: List[Dict]) -> str:
        """Agent revises their solution based on discussion."""
        opinions_text = "\n\n".join([
            f"{op['agent']} ({op['type']}):\n{op['content']}" 
            for op in all_opinions
        ])
        
        prompt = f"""You are an expert agent with a {self.perspective} perspective.

Query: {query}

Discussion so far:
{opinions_text}

Based on this discussion, revise your solution. Incorporate valid critiques and insights from others."""
        
        response = self.llm.invoke(prompt)
        revised = response.content
        self.opinions.append({"type": "revision", "content": revised})
        return revised
    
    def vote(self, query: str, solutions: List[str]) -> int:
        """Agent votes on best solution (returns index)."""
        solutions_text = "\n\n".join([
            f"Solution {i+1}:\n{sol}" for i, sol in enumerate(solutions)
        ])
        
        prompt = f"""You are an expert agent with a {self.perspective} perspective.

Query: {query}

Solutions to vote on:
{solutions_text}

Which solution is best? Return only the number (1, 2, 3, etc.)"""
        
        response = self.llm.invoke(prompt)
        try:
            vote = int(response.content.strip())
            return min(max(1, vote), len(solutions)) - 1  # Ensure valid index
        except:
            return 0

def consensus_through_discussion(query: str, num_rounds: int = 3) -> Dict[str, Any]:
    """Multiple agents reach consensus through discussion."""
    # Create agents with different perspectives
    perspectives = ["technical", "user-focused", "business"]
    agents = [
        DiscussionAgent(f"agent_{i}", perspectives[i % len(perspectives)])
        for i in range(3)
    ]
    
    # Phase 1: Initial proposals
    solutions = []
    for agent in agents:
        solution = agent.propose_solution(query)
        solutions.append(solution)
    
    discussion_history = []
    
    # Phase 2: Iterative discussion
    for round_num in range(num_rounds):
        # Agents critique others
        critiques = []
        for i, agent in enumerate(agents):
            other_solutions = [sol for j, sol in enumerate(solutions) if j != i]
            critique = agent.critique(query, other_solutions)
            critiques.append({
                "agent": agent.agent_id,
                "type": "critique",
                "content": critique
            })
        
        discussion_history.extend(critiques)
        
        # Agents revise based on critiques
        all_opinions = [
            {"agent": f"agent_{i}", "type": "proposal", "content": sol}
            for i, sol in enumerate(solutions)
        ] + critiques
        
        new_solutions = []
        for i, agent in enumerate(agents):
            revised = agent.revise(query, all_opinions)
            new_solutions.append(revised)
        
        solutions = new_solutions
        discussion_history.extend([
            {"agent": agent.agent_id, "type": "revision", "content": sol}
            for agent, sol in zip(agents, solutions)
        ])
    
    # Phase 3: Voting to reach consensus
    votes = []
    for agent in agents:
        vote = agent.vote(query, solutions)
        votes.append(vote)
    
    # Determine consensus (most voted solution)
    vote_counts = defaultdict(int)
    for vote in votes:
        vote_counts[vote] += 1
    
    consensus_index = max(vote_counts.items(), key=lambda x: x[1])[0]
    consensus_solution = solutions[consensus_index]
    
    # Phase 4: Final synthesis
    synthesis_prompt = f"""Synthesize the discussion into a final consensus answer.

Query: {query}

Final solutions after discussion:
{json.dumps(solutions, indent=2)}

Votes: {dict(vote_counts)}

Create a comprehensive final answer that incorporates the best insights from all perspectives."""
    
    final_result = llm.invoke(synthesis_prompt)
    
    return {
        "query": query,
        "solutions": solutions,
        "votes": votes,
        "consensus_index": consensus_index,
        "consensus_solution": consensus_solution,
        "discussion_history": discussion_history,
        "final_answer": final_result.content
    }

# Usage
result = consensus_through_discussion(
    "What are the best practices for designing multi-agent systems?"
)
print(result["final_answer"])
```

**Explanation:**
This example demonstrates consensus through discussion: agents propose solutions, critique each other, revise based on feedback, and vote on the best solution. The iterative discussion allows agents to surface errors, explore different perspectives, and converge on high-quality solutions.

### Advanced Example: Society of Minds (Peer-to-Peer Discussion)

This example shows a peer-to-peer discussion where all agents are equal and engage in open dialogue:

```python
class PeerDiscussionAgent:
    """Agent that participates in peer-to-peer discussion."""
    
    def __init__(self, agent_id: str, persona: str):
        self.agent_id = agent_id
        self.persona = persona  # Different reasoning styles
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.7)  # Higher temp for diversity
    
    def participate(self, query: str, discussion: List[Dict]) -> str:
        """Agent participates in discussion, responding to others."""
        if not discussion:
            # First contribution
            prompt = f"""You are an expert with a {self.persona} reasoning style.

Query: {query}

Provide your initial thoughts and solution approach."""
        else:
            # Respond to ongoing discussion
            discussion_text = "\n\n".join([
                f"{msg['agent']}: {msg['content']}" 
                for msg in discussion[-5:]  # Last 5 messages
            ])
            
            prompt = f"""You are an expert with a {self.persona} reasoning style.

Query: {query}

Discussion so far:
{discussion_text}

Contribute to the discussion. You can:
- Agree or disagree with others
- Point out errors or issues
- Provide additional insights
- Propose solutions
- Ask clarifying questions

Keep your contribution concise and focused."""
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def check_convergence(self, discussion: List[Dict]) -> bool:
        """Check if agents are converging (simplified)."""
        if len(discussion) < 6:
            return False
        
        # Check if recent messages show agreement patterns
        recent = [msg['content'].lower() for msg in discussion[-3:]]
        agreement_words = ['agree', 'correct', 'yes', 'right', 'consensus', 'same']
        
        agreement_count = sum(1 for msg in recent for word in agreement_words if word in msg)
        return agreement_count >= 2

def society_of_minds(query: str, max_rounds: int = 10) -> Dict[str, Any]:
    """Peer-to-peer discussion among equal agents."""
    personas = [
        "analytical and detail-oriented",
        "creative and out-of-the-box thinking",
        "pragmatic and solution-focused"
    ]
    
    agents = [
        PeerDiscussionAgent(f"agent_{i}", personas[i % len(personas)])
        for i in range(3)
    ]
    
    discussion = []
    convergence_threshold = 3
    convergence_count = 0
    
    for round_num in range(max_rounds):
        # Each agent participates
        for agent in agents:
            contribution = agent.participate(query, discussion)
            discussion.append({
                "agent": agent.agent_id,
                "round": round_num,
                "content": contribution
            })
        
        # Check for convergence
        if any(agent.check_convergence(discussion) for agent in agents):
            convergence_count += 1
            if convergence_count >= convergence_threshold:
                break
        else:
            convergence_count = 0
    
    # Synthesize final answer from discussion
    discussion_text = "\n\n".join([
        f"{msg['agent']} (Round {msg['round']}): {msg['content']}"
        for msg in discussion
    ])
    
    synthesis_prompt = f"""Synthesize this peer discussion into a final consensus answer.

Query: {query}

Discussion:
{discussion_text}

Create a comprehensive answer that incorporates the best insights from all perspectives and represents the group's consensus."""
    
    final_result = llm.invoke(synthesis_prompt)
    
    return {
        "query": query,
        "discussion": discussion,
        "rounds": round_num + 1,
        "final_answer": final_result.content
    }

# Usage
result = society_of_minds(
    "How should LLM agents handle conflicting information from different sources?"
)
print(result["final_answer"])
```

**Explanation:**
This example demonstrates a "Society of Minds" approach where agents engage in peer-to-peer discussion without hierarchy. All agents are equal, can critique others, and contribute freely. The system checks for convergence based on agreement patterns and synthesizes a final answer from the discussion.

### Framework-Specific Examples

#### LangGraph: Consensus Discussion Graph

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class ConsensusState(TypedDict):
    query: str
    solutions: List[str]
    discussion: List[Dict]
    votes: List[int]
    consensus_reached: bool
    final_answer: str

def propose_solutions(state: ConsensusState) -> ConsensusState:
    """Each agent proposes initial solution."""
    query = state["query"]
    solutions = []
    
    for i in range(3):
        prompt = f"""Propose a solution to: {query}
        
Provide your solution and reasoning."""
        response = llm.invoke(prompt)
        solutions.append(response.content)
    
    return {**state, "solutions": solutions}

def discuss_solutions(state: ConsensusState) -> ConsensusState:
    """Agents discuss and critique solutions."""
    query = state["query"]
    solutions = state["solutions"]
    discussion = state.get("discussion", [])
    
    solutions_text = "\n\n".join([
        f"Solution {i+1}:\n{sol}" for i, sol in enumerate(solutions)
    ])
    
    prompt = f"""Query: {query}

Solutions to discuss:
{solutions_text}

Provide a critique discussing strengths, weaknesses, and potential improvements."""
    
    response = llm.invoke(prompt)
    discussion.append({
        "type": "critique",
        "content": response.content
    })
    
    return {**state, "discussion": discussion}

def vote_on_solutions(state: ConsensusState) -> ConsensusState:
    """Agents vote on best solution."""
    query = state["query"]
    solutions = state["solutions"]
    votes = []
    
    solutions_text = "\n\n".join([
        f"Solution {i+1}:\n{sol}" for i, sol in enumerate(solutions)
    ])
    
    for _ in range(3):  # 3 agents voting
        prompt = f"""Query: {query}

Solutions:
{solutions_text}

Vote for the best solution (1, 2, or 3). Return only the number."""
        response = llm.invoke(prompt)
        try:
            vote = int(response.content.strip())
            votes.append(min(max(1, vote), len(solutions)) - 1)
        except:
            votes.append(0)
    
    # Check consensus (all agree or majority)
    vote_counts = {}
    for vote in votes:
        vote_counts[vote] = vote_counts.get(vote, 0) + 1
    
    majority_vote = max(vote_counts.items(), key=lambda x: x[1])[0]
    consensus_reached = vote_counts[majority_vote] >= 2  # Majority
    
    return {
        **state,
        "votes": votes,
        "consensus_reached": consensus_reached
    }

def synthesize_answer(state: ConsensusState) -> ConsensusState:
    """Synthesize final consensus answer."""
    query = state["query"]
    solutions = state["solutions"]
    discussion = state.get("discussion", [])
    votes = state["votes"]
    
    discussion_text = "\n\n".join([
        f"{msg['type']}: {msg['content']}" for msg in discussion
    ])
    
    prompt = f"""Synthesize consensus answer.

Query: {query}

Solutions: {json.dumps(solutions, indent=2)}
Discussion: {discussion_text}
Votes: {votes}

Create final consensus answer."""
    
    response = llm.invoke(prompt)
    
    return {**state, "final_answer": response.content}

def should_continue(state: ConsensusState) -> str:
    """Determine next step."""
    if not state.get("solutions"):
        return "propose"
    elif not state.get("discussion"):
        return "discuss"
    elif not state.get("consensus_reached", False):
        return "vote"
    else:
        return "synthesize"

# Build graph
graph = StateGraph(ConsensusState)
graph.add_node("propose", propose_solutions)
graph.add_node("discuss", discuss_solutions)
graph.add_node("vote", vote_on_solutions)
graph.add_node("synthesize", synthesize_answer)

graph.set_entry_point("propose")
graph.add_conditional_edges("propose", lambda s: "discuss")
graph.add_conditional_edges("discuss", lambda s: "vote")
graph.add_conditional_edges("vote", should_continue)
graph.add_edge("synthesize", END)

# Execute
result = graph.invoke({"query": "Best practices for LLM agent design"})
print(result["final_answer"])
```

## Key Takeaways

- **Core Concept:** Swarm/Consensus Architecture enables decentralized coordination through natural language discussion, debate, and consensus mechanisms, without requiring central orchestrator.

- **Key Benefits:** Error detection through cross-verification, improved reasoning quality through debate, diversity of perspectives, and collective intelligence that exceeds individual capabilities.

- **Coordination Mechanisms:** Natural language discussion (agents engage in dialogue), consensus algorithms (voting, iterative refinement), and peer-to-peer interactions enable collaborative problem-solving.

- **Trade-offs:** Decentralized coordination provides multiple perspectives and error detection but introduces coordination overhead, latency from discussion, and complexity compared to centralized systems.

- **Best Practice:** Design discussion protocols that encourage productive debate while preventing infinite loops. Use convergence criteria to determine when consensus is reached.

- **Common Pitfall:** Agents may converge prematurely or fall into groupthink. Design prompts to maintain healthy dissent and only converge when justified.

- **Collective Intelligence:** Multiple agents discussing and debating can achieve better solutions than any individual agent. Research shows significant improvements in reasoning tasks.

## Related Patterns

This pattern works well with:
- **Pattern: Multi-Agent Debate** - Structured debate frameworks with adversarial agents and judges; debate is a key consensus mechanism
- **Pattern: Orchestrator-Worker** - Hybrid systems combine centralized coordination with decentralized consensus for verification
- **Pattern: Planner-Checker** - Consensus can be used by checker agents to verify plans or execution outcomes
- **Pattern: Parallelization** - Consensus agents naturally execute in parallel, coordinating through discussion
- **Memory Management** - Shared knowledge bases enable agents to build on each other's findings

This pattern is often combined with:
- **Multi-Agent Architectures** - Swarm/Consensus is a fundamental multi-agent coordination pattern
- **Natural Language Negotiation** - Agents negotiate and build consensus through dialogue
- **Tool Use** - Agents use tools to gather information that informs discussion

??? "References"
    - **Consensus Through Discussion:** Improving Factuality and Reasoning in Language Models through Multiagent Debate (Du et al., 2023) - https://arxiv.org/abs/2305.14325
    - **Society of Minds:** Multiple LLM instances discussing and converging on solutions
    - **Natural Language Negotiation:** CICERO - Achieving human-level performance in Diplomacy through negotiation
    - LangGraph Multi-Agent: https://langchain-ai.github.io/langgraph/how-tos/multi-agent/
    - Multi-Agent Collaboration Mechanisms: A Survey of LLMs - https://arxiv.org/html/2501.06322v1
