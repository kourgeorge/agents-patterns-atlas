# Pattern: Swarm/Consensus Architecture

## Motivation

A flock of birds coordinates without a leader, each bird following simple local rules that produce elegant group behavior. Ant colonies solve complex problems through indirect communication—ants leave pheromone trails that guide others. These biological systems demonstrate that sophisticated coordination can emerge from decentralized, local interactions rather than centralized control.

The Swarm/Consensus Architecture pattern captures this principle: autonomous agents coordinate through local interactions, consensus mechanisms, or emergent behavior, without requiring a central orchestrator. This pattern is essential when centralized coordination is impractical, undesirable, or impossible—whether due to fault tolerance requirements, network partitions, scalability needs, or the desire for emergent behaviors that exceed what centralized planning can achieve.

## Pattern Overview

**What it is:** A decentralized multi-agent architecture where autonomous agents coordinate through local interactions, consensus algorithms, voting mechanisms, or indirect communication (stigmergy). Agents make decisions independently based on local information and shared state, with global coordination emerging from these local interactions.

**When to use:** When centralized coordination is impractical or undesirable—fault tolerance is critical, network partitions are common, systems must scale to many agents, or emergent behaviors are desired. Also valuable when agents have partial information and must reach collective decisions.

**Why it matters:** Decentralized coordination provides fault tolerance (no single point of failure), scalability (coordination overhead doesn't grow linearly with agent count), and enables emergent behaviors that centralized systems cannot achieve. It mirrors biological systems that solve complex problems through simple local rules.

Unlike orchestrator-worker patterns that rely on central coordination, swarm/consensus architectures distribute decision-making across agents. This creates systems that are more resilient to failures, can scale to large numbers of agents, and can exhibit emergent intelligence that exceeds the sum of individual agent capabilities.

### Key Concepts

- **Stigmergy:** Indirect communication through shared environment modification. Agents leave markers (pheromones, state updates) that influence others' behavior, enabling coordination without direct communication.

- **Consensus Algorithms:** Mechanisms for agents to agree on shared state or decisions despite failures or network partitions. Includes voting, averaging, and Byzantine fault-tolerant consensus.

- **Emergent Coordination:** Complex global behaviors that emerge from simple local rules. Agents follow local rules, producing sophisticated group behaviors without explicit global planning.

- **Local vs. Global Optimization:** Agents optimize locally (their immediate context) while contributing to global objectives. The system balances individual agent goals with collective outcomes.

- **Decentralized Decision-Making:** Agents make decisions independently based on local information, shared state, and communication with neighbors, rather than receiving directives from a central coordinator.

- **Fault Tolerance:** System continues operating despite agent failures, network partitions, or malicious agents, achieved through redundancy and consensus mechanisms.

### How It Works

Swarm/Consensus architectures operate through several coordination mechanisms:

1. **Shared State (Stigmergy):** Agents read and modify shared state (blackboard, knowledge base, environment). Changes influence other agents' behavior, creating indirect coordination. For example, research agents deposit findings in a shared knowledge base; other agents read and build upon these findings.

2. **Consensus Mechanisms:** Agents must agree on decisions or shared state:
   - **Voting:** Agents vote on options; majority or weighted voting determines outcome
   - **Averaging Consensus:** Agents iteratively average values with neighbors, converging to global average
   - **Byzantine Consensus:** Reach agreement despite faulty or malicious agents using algorithms like PBFT or Raft

3. **Local Interactions:** Agents interact primarily with neighbors or local subset, rather than all agents. This enables scalability and reduces communication overhead.

4. **Emergent Behavior:** Agents follow simple local rules (e.g., "follow strongest pheromone trail," "align with neighbors," "vote based on local information"). Complex global behaviors emerge from these interactions.

5. **Convergence:** Systems converge to stable states through iterative updates, voting rounds, or consensus algorithms. Convergence criteria determine when coordination is complete.

## When to Use This Pattern

### ✅ Use when:

- **Fault tolerance is critical:** System must continue operating despite agent failures or network partitions
- **Scalability requirements:** Need to coordinate large numbers of agents where centralized coordination becomes bottleneck
- **Network partitions expected:** Agents operate in unreliable networks where centralized coordination may fail
- **Emergent behaviors desired:** Want behaviors that emerge from local interactions rather than explicit planning
- **Partial information:** Agents have partial, local information and must reach collective decisions
- **Decentralized infrastructure:** System architecture is inherently decentralized (edge computing, IoT, distributed systems)
- **No single point of control:** Political, organizational, or technical constraints prevent central coordination

### ❌ Avoid when:

- **Strong consistency required:** Need guaranteed consistency that centralized coordination provides
- **Deterministic outcomes needed:** Require predictable, deterministic coordination rather than emergent behaviors
- **Low coordination overhead:** Centralized coordination is feasible and more efficient
- **Small agent count:** Few agents where coordination overhead of consensus exceeds benefits
- **Tight coupling:** Agents have strong dependencies requiring explicit coordination
- **Real-time constraints:** Consensus algorithms introduce latency that violates timing requirements

### Decision Guidelines

Use Swarm/Consensus Architecture when the benefits of decentralization (fault tolerance, scalability, emergent behaviors) outweigh the costs (coordination overhead, eventual consistency, complexity). Consider: agent count (more agents = more benefit), failure rates (high failures = need fault tolerance), network reliability (unreliable = decentralized better), and consistency requirements (eventual consistency acceptable = consensus viable). For small systems with reliable networks, centralized coordination may be simpler and more efficient.

## Practical Applications & Use Cases

Swarm/Consensus architectures excel in scenarios requiring fault tolerance, scalability, or emergent coordination:

### Distributed Research Agents

Multiple research agents independently explore problem spaces, deposit findings in shared knowledge base, and converge on solutions through consensus voting. Agents work in parallel, building on each other's discoveries without central coordination.

**Example:** Research system where agents independently investigate different aspects of a question, share findings through a shared knowledge base, and vote on the most important insights to include in final report.

### Swarm Robotics

Robots coordinate through local interactions and shared state, enabling collective behaviors like formation control, distributed sensing, and collaborative manipulation.

**Example:** Drone swarm for search and rescue where drones share location and findings, use consensus to decide search areas, and coordinate coverage without central control.

### Distributed Optimization

Agents collaboratively solve optimization problems through local interactions, using swarm intelligence algorithms like ant colony optimization or particle swarm optimization.

**Example:** Vehicle routing where agents (representing routes) adjust based on pheromone trails (shared state indicating route quality), converging on optimal solutions through local updates.

### Collective Decision-Making

Agents vote or reach consensus on decisions, enabling distributed governance, collaborative filtering, or group intelligence systems.

**Example:** Distributed voting system where agents independently evaluate options, share opinions, and reach consensus through iterative voting rounds.

### Distributed Sensing Networks

Sensor networks where agents coordinate to cover areas, detect events, or aggregate data through local interactions and consensus.

**Example:** Environmental monitoring network where sensors share readings, use consensus to detect anomalies, and coordinate coverage without central server.

## Implementation

### Prerequisites

```bash
pip install langchain langchain-openai langgraph
# For consensus algorithms
pip install pydantic
# For simulation/testing
pip install mesa  # Agent-based modeling
```

### Basic Example: Consensus-Based Research Agents

This example demonstrates research agents that coordinate through shared knowledge base and consensus voting:

```python
from langchain_openai import ChatOpenAI
from typing import List, Dict, Any
from collections import defaultdict
import json

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class SharedKnowledgeBase:
    """Shared state for stigmergy-based coordination."""
    def __init__(self):
        self.findings = []
        self.votes = defaultdict(list)  # topic -> [votes]
    
    def add_finding(self, agent_id: str, topic: str, finding: str):
        """Agent deposits finding in shared knowledge base."""
        self.findings.append({
            "agent_id": agent_id,
            "topic": topic,
            "finding": finding
        })
    
    def get_findings(self, topic: str = None) -> List[Dict]:
        """Retrieve findings, optionally filtered by topic."""
        if topic:
            return [f for f in self.findings if f["topic"] == topic]
        return self.findings
    
    def vote(self, agent_id: str, topic: str, importance: int):
        """Agent votes on topic importance (1-10)."""
        self.votes[topic].append({
            "agent_id": agent_id,
            "importance": importance
        })
    
    def get_consensus(self, topic: str) -> float:
        """Calculate average importance (consensus) for topic."""
        if topic not in self.votes or not self.votes[topic]:
            return 0.0
        votes = [v["importance"] for v in self.votes[topic]]
        return sum(votes) / len(votes)

class ResearchAgent:
    """Autonomous research agent that coordinates through shared state."""
    def __init__(self, agent_id: str, specialization: str, knowledge_base: SharedKnowledgeBase):
        self.agent_id = agent_id
        self.specialization = specialization
        self.kb = knowledge_base
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    def research(self, query: str) -> str:
        """Agent conducts research on assigned aspect."""
        # Read existing findings from shared knowledge base
        existing_findings = self.kb.get_findings()
        context = "\n".join([f"{f['topic']}: {f['finding']}" for f in existing_findings[-5:]])
        
        prompt = f"""You are a research agent specializing in {self.specialization}.

Query: {query}

Existing findings from other agents:
{context}

Conduct research on your specialized aspect. Provide key findings."""
        
        result = self.llm.invoke(prompt)
        finding = result.content
        
        # Deposit finding in shared knowledge base (stigmergy)
        self.kb.add_finding(self.agent_id, self.specialization, finding)
        
        return finding
    
    def vote_on_importance(self, topics: List[str]):
        """Agent votes on topic importance based on local evaluation."""
        for topic in topics:
            # Agent evaluates importance locally
            prompt = f"""Evaluate the importance of this research topic: {topic}

Rate importance from 1-10 based on:
- Relevance to query
- Quality of findings
- Uniqueness of contribution

Return only a number 1-10."""
            
            result = self.llm.invoke(prompt)
            try:
                importance = int(result.content.strip())
                self.kb.vote(self.agent_id, topic, importance)
            except:
                pass

def swarm_research(query: str, num_agents: int = 3) -> Dict[str, Any]:
    """Swarm of research agents coordinate to answer query."""
    # Initialize shared knowledge base
    kb = SharedKnowledgeBase()
    
    # Create specialized agents
    specializations = ["technical analysis", "market trends", "user impact"]
    agents = [
        ResearchAgent(f"agent_{i}", specializations[i % len(specializations)], kb)
        for i in range(num_agents)
    ]
    
    # Phase 1: Agents research in parallel (stigmergy)
    findings = []
    for agent in agents:
        finding = agent.research(query)
        findings.append(finding)
    
    # Phase 2: Agents vote on importance (consensus)
    topics = list(set([f["topic"] for f in kb.get_findings()]))
    for agent in agents:
        agent.vote_on_importance(topics)
    
    # Phase 3: Calculate consensus
    consensus_scores = {topic: kb.get_consensus(topic) for topic in topics}
    
    # Phase 4: Synthesize based on consensus
    top_topics = sorted(consensus_scores.items(), key=lambda x: x[1], reverse=True)[:3]
    
    synthesis_prompt = f"""Synthesize research findings into final answer.

Query: {query}

Top findings (by consensus):
{json.dumps([{"topic": t, "finding": kb.get_findings(t)[0]["finding"]} for t, _ in top_topics], indent=2)}

Provide comprehensive answer."""
    
    final_result = llm.invoke(synthesis_prompt)
    
    return {
        "query": query,
        "findings": findings,
        "consensus_scores": consensus_scores,
        "final_answer": final_result.content
    }

# Usage
result = swarm_research("What are the latest trends in AI agent architectures?")
print(result["final_answer"])
```

**Explanation:**
This example demonstrates swarm coordination: agents research independently, deposit findings in shared knowledge base (stigmergy), vote on importance (consensus), and system synthesizes based on consensus scores. No central orchestrator coordinates agents; coordination emerges from shared state and voting.

### Advanced Example: Byzantine Fault-Tolerant Consensus

This example shows consensus with fault tolerance:

```python
from typing import List, Dict, Optional
from enum import Enum
import random

class AgentState(Enum):
    NORMAL = "normal"
    FAULTY = "faulty"  # May send incorrect messages
    BYZANTINE = "byzantine"  # May send malicious messages

class ConsensusAgent:
    """Agent participating in Byzantine fault-tolerant consensus."""
    def __init__(self, agent_id: str, state: AgentState = AgentState.NORMAL):
        self.agent_id = agent_id
        self.state = state
        self.proposed_value = None
        self.received_proposals = {}
        self.decided_value = None
    
    def propose(self, value: Any) -> Any:
        """Agent proposes value for consensus."""
        if self.state == AgentState.NORMAL:
            self.proposed_value = value
            return value
        elif self.state == AgentState.FAULTY:
            # Faulty agent proposes random value
            self.proposed_value = random.choice(["A", "B", "C"])
            return self.proposed_value
        elif self.state == AgentState.BYZANTINE:
            # Byzantine agent proposes malicious value
            self.proposed_value = "MALICIOUS"
            return self.proposed_value
    
    def receive_proposal(self, from_agent: str, value: Any):
        """Receive proposal from another agent."""
        if self.state == AgentState.NORMAL:
            self.received_proposals[from_agent] = value
    
    def decide(self, all_proposals: Dict[str, Any], f: int) -> Optional[Any]:
        """Reach consensus using simple majority, tolerating f faulty agents."""
        if self.state != AgentState.NORMAL:
            return None
        
        # Count votes for each value
        vote_counts = {}
        for agent_id, value in all_proposals.items():
            if value not in vote_counts:
                vote_counts[value] = 0
            vote_counts[value] += 1
        
        # Find value with majority (need > f votes to tolerate f faults)
        for value, count in vote_counts.items():
            if count > f:
                self.decided_value = value
                return value
        
        return None  # No consensus reached

def byzantine_consensus(agents: List[ConsensusAgent], f: int) -> Optional[Any]:
    """Run Byzantine fault-tolerant consensus."""
    # Phase 1: Agents propose values
    proposals = {}
    for agent in agents:
        proposal = agent.propose("A")  # All propose "A" normally
        proposals[agent.agent_id] = proposal
    
    # Phase 2: Agents receive all proposals
    for agent in agents:
        for other_id, value in proposals.items():
            if other_id != agent.agent_id:
                agent.receive_proposal(other_id, value)
    
    # Phase 3: Agents decide
    decisions = {}
    for agent in agents:
        decision = agent.decide(proposals, f)
        if decision:
            decisions[agent.agent_id] = decision
    
    # Check if consensus reached (all normal agents agree)
    normal_decisions = [d for aid, d in decisions.items() 
                       if agents[[a.agent_id for a in agents].index(aid)].state == AgentState.NORMAL]
    
    if len(set(normal_decisions)) == 1:
        return normal_decisions[0]
    
    return None

# Usage: 5 agents, tolerate 1 Byzantine fault
agents = [
    ConsensusAgent("agent_0", AgentState.NORMAL),
    ConsensusAgent("agent_1", AgentState.NORMAL),
    ConsensusAgent("agent_2", AgentState.NORMAL),
    ConsensusAgent("agent_3", AgentState.NORMAL),
    ConsensusAgent("agent_4", AgentState.BYZANTINE),  # One Byzantine agent
]

consensus_value = byzantine_consensus(agents, f=1)
print(f"Consensus reached: {consensus_value}")
```

**Explanation:**
This example demonstrates Byzantine fault-tolerant consensus where agents must agree on a value despite some agents being faulty or malicious. The algorithm tolerates f faulty agents in a system of 3f+1 agents, ensuring normal agents reach consensus even when Byzantine agents try to disrupt it.

### Framework-Specific Examples

#### LangGraph: Swarm Coordination

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class SwarmState(TypedDict):
    query: str
    shared_knowledge: List[Dict]
    agent_findings: Dict[str, str]
    votes: Dict[str, List[int]]
    consensus: Dict[str, float]
    final_output: str

def agent_research(state: SwarmState) -> SwarmState:
    """Agent conducts research and updates shared knowledge."""
    agent_id = "agent_1"
    query = state["query"]
    shared_knowledge = state.get("shared_knowledge", [])
    
    # Read shared knowledge (stigmergy)
    context = "\n".join([f"{k['topic']}: {k['finding']}" for k in shared_knowledge[-3:]])
    
    prompt = f"""Research this query: {query}

Existing knowledge:
{context}

Provide key findings."""
    
    result = llm.invoke(prompt)
    finding = result.content
    
    # Update shared knowledge
    new_knowledge = shared_knowledge + [{"agent": agent_id, "finding": finding}]
    agent_findings = state.get("agent_findings", {})
    agent_findings[agent_id] = finding
    
    return {
        **state,
        "shared_knowledge": new_knowledge,
        "agent_findings": agent_findings
    }

def agent_vote(state: SwarmState) -> SwarmState:
    """Agent votes on findings importance."""
    agent_id = "agent_1"
    findings = state.get("agent_findings", {})
    votes = state.get("votes", {})
    
    # Vote on each finding
    for finding_id, finding in findings.items():
        prompt = f"""Rate importance of this finding (1-10): {finding[:100]}..."""
        result = llm.invoke(prompt)
        try:
            vote = int(result.content.strip())
            if finding_id not in votes:
                votes[finding_id] = []
            votes[finding_id].append(vote)
        except:
            pass
    
    return {**state, "votes": votes}

def calculate_consensus(state: SwarmState) -> SwarmState:
    """Calculate consensus scores from votes."""
    votes = state.get("votes", {})
    consensus = {}
    
    for finding_id, vote_list in votes.items():
        if vote_list:
            consensus[finding_id] = sum(vote_list) / len(vote_list)
    
    return {**state, "consensus": consensus}

# Build graph
graph = StateGraph(SwarmState)
graph.add_node("research", agent_research)
graph.add_node("vote", agent_vote)
graph.add_node("consensus", calculate_consensus)

graph.set_entry_point("research")
graph.add_edge("research", "vote")
graph.add_edge("vote", "consensus")
graph.add_edge("consensus", END)

# Execute
result = graph.invoke({"query": "Latest AI trends"})
```

## Key Takeaways

- **Core Concept:** Swarm/Consensus Architecture enables decentralized coordination through local interactions, shared state, and consensus mechanisms, without requiring central orchestrator.

- **Key Benefits:** Fault tolerance (no single point of failure), scalability (coordination doesn't bottleneck), and emergent behaviors that exceed centralized planning capabilities.

- **Coordination Mechanisms:** Stigmergy (indirect communication through shared state), consensus algorithms (voting, averaging, Byzantine fault tolerance), and local interactions enable global coordination.

- **Trade-offs:** Decentralized coordination provides fault tolerance and scalability but introduces coordination overhead, eventual consistency, and complexity compared to centralized systems.

- **Best Practice:** Design simple local rules that produce desired global behaviors. Use consensus algorithms appropriate for failure model (crash failures vs. Byzantine failures).

- **Common Pitfall:** Over-engineering consensus when simpler mechanisms suffice. Not all systems need Byzantine fault tolerance; simple voting may be sufficient.

- **Emergent Intelligence:** Complex behaviors emerge from simple local rules. Design for emergence rather than trying to explicitly program all coordination.

## Related Patterns

This pattern works well with:
- **Pattern: Orchestrator-Worker** - Hybrid systems combine centralized coordination for high-level planning with decentralized execution
- **Pattern: Parallelization** - Swarm agents naturally execute in parallel, coordinating through shared state
- **Memory Management** - Shared knowledge bases and state management enable stigmergy-based coordination
- **Pattern: Reflection** - Agents can reflect on shared state and adjust behavior based on collective outcomes

This pattern is often combined with:
- **Multi-Agent Architectures** - Swarm/Consensus is a fundamental multi-agent coordination pattern
- **Tool Use** - Agents use tools to interact with shared environment, enabling stigmergy
- **Planning** - Agents can plan locally while contributing to global objectives

## References

- Swarm Intelligence: From Natural to Artificial Systems (Bonabeau, Dorigo, Theraulaz)
- Byzantine Fault Tolerance: Practical Byzantine Fault Tolerance (Castro & Liskov)
- Consensus Algorithms: Raft Consensus Algorithm (Ongaro & Ousterhout)
- Stigmergy: The Stigmergic Approach to Swarm Intelligence (Parunak)
- Multi-Agent Systems: An Introduction to Multiagent Systems (Wooldridge)
- LangGraph Multi-Agent: https://langchain-ai.github.io/langgraph/how-tos/multi-agent/
- Mesa Agent-Based Modeling: https://mesa.readthedocs.io/

