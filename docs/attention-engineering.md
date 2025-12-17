# Pattern: Attention Engineering

## Motivation

When reading a long document, you naturally focus more on the beginning and end—the introduction sets expectations, and the conclusion reinforces key points. Information buried in the middle often gets less attention. Large language models exhibit the same behavior: they show primacy bias (favoring the beginning) and recency bias (favoring the end), while information in the middle can be overlooked—a phenomenon known as the "lost in the middle" problem.

Attention Engineering addresses this by strategically structuring and ordering prompts so that crucial instructions or facts appear in positions where the model is most likely to notice and prioritize them. Just as a skilled presenter emphasizes key points at the start and end of a presentation, Attention Engineering ensures important information receives adequate attention regardless of context length.

> **"Context engineering is the art of filling the window with exactly what the model needs for the next action."** — Andrej Karpathy

## Pattern Overview

### Problem

Research has empirically confirmed that LLMs exhibit a U-shaped attention pattern: models perform best when relevant information is at the start or end of context, and degrade significantly when needed information lies in the middle of lengthy inputs. Without attention engineering, vital requirements buried mid-prompt risk being diluted or ignored, leading to goal drift, missed constraints, and reduced effectiveness. This "lost in the middle" problem becomes particularly acute when building agents that process long contexts, need to ensure critical instructions are followed, or must maintain focus on important information across extended conversations or multi-step tasks.

### Solution

Attention Engineering directly combats this problem by restructuring the prompt landscape. It is a specialized prompt design pattern focused on manipulating where and how information appears in an AI model's context to deliberately steer the model's focus. The pattern exploits the model's inherent attention biases (primacy and recency) by strategically positioning critical information at optimal locations in the prompt.

By strategically positioning information, exploiting recency bias, and using multi-layer reinforcement, we ensure that crucial information isn't relegated to attention dead zones. This pattern has become essential for advanced prompt engineering and context management in 2025, complementing other aspects of context engineering to yield more reliable and focused model responses. The technique involves front-loading essential instructions at the beginning to leverage primacy bias, back-loading critical information at the end to leverage recency bias, and avoiding placing important constraints in the middle of lengthy text.

### Key Concepts

- **Primacy Bias:** The model's tendency to give more weight to information at the beginning of the context, forming strong initial attention weights.
- **Recency Bias:** The model's tendency to prioritize the most recently seen tokens, keeping recent information "fresh" in working memory.
- **Lost in the Middle:** The phenomenon where information in the middle of long contexts receives disproportionately less attention, leading to degraded performance.
- **Strategic Positioning:** Deliberately placing critical information at optimal locations (beginning or end) to leverage attention biases.
- **Attention Scoring:** Assessing and prioritizing information based on importance and attention potential, then organizing content accordingly.
- **Multi-Layer Strategies:** Combining multiple positioning and emphasis techniques to reinforce important information through several "layers" or in different ways.
- **Attention Sorting:** An advanced technique where the model reads context, measures which parts it focuses on, then re-orders context so the most attended pieces move to attention-rich positions.

### How It Works: Step-by-step Explanation

Attention Engineering operates through several complementary techniques:

1. **Identify Critical Information:** Determine which instructions, constraints, or facts are most important for the task. These are candidates for attention engineering.

2. **Assess Context Length:** Evaluate whether the context is long enough that the "lost in the middle" problem could occur. Generally, contexts over 10K tokens benefit from attention engineering.

3. **Apply Strategic Positioning:**
   - **Front-loading:** Place essential instructions or data at the very beginning of the context to leverage primacy bias
   - **Back-loading:** Ensure critical information appears as a final reminder at the end to leverage recency bias
   - **Avoid the middle:** Never hide important constraints in the middle of lengthy text

4. **Exploit Recency Bias:** For long-running conversations or multi-step tasks, continuously update and append key information (like goals or constraints) near the end of context so it stays "fresh" in the model's working memory.

5. **Use Attention Scoring:** Rank pieces of context by relevance and attention potential, then organize content accordingly. High-priority information receives prominent positions or formatting.

6. **Implement Multi-Layer Reinforcement:** Combine positioning strategies—place critical info at both beginning and end, and reiterate it in structured forms throughout the prompt.

7. **Apply Structural Cues:** Use clear sections, headings, or bullet points to guide attention. Each section acts like a mini-prompt where crucial info can be placed at the top.

## Relationship to Other Patterns

### Attention Engineering vs Context Engineering

**Context Engineering** is the broader discipline of managing what information appears in the context window to optimize performance, cost, and reasoning quality. It encompasses:
- Externalization (moving data out)
- Compression (reducing size), including Context Compaction and Summarization to prevent Context Rot
- Automatic management (editing/clearing)
- Attention manipulation (positioning)
- Metadata separation
- Preventing Context Pollution and Context Confusion in multi-agent systems

**Attention Engineering** is a specialized pattern within Context Engineering that focuses specifically on manipulating where information appears to bias model attention. It's the "where" and "how to bias attention" aspect of the broader "what goes in the context window" discipline.

**Relationship:** Attention Engineering is a core technique within Context Engineering. While Context Engineering manages overall context composition, Attention Engineering ensures that the information that remains receives optimal attention.

### Attention Engineering vs Recitation

**Recitation** is a specific implementation of Attention Engineering that exploits recency bias by continuously appending updated plans or goals to the end of context.

**Attention Engineering** is the broader pattern that includes recitation as one technique, along with primacy exploitation, attention scoring, and multi-layer strategies.

**Relationship:** Recitation is an application of Attention Engineering's recency bias exploitation principle. Attention Engineering provides the framework; Recitation demonstrates it in practice.

### Attention Engineering vs Context Editing

**Context Editing** automatically manages context size by removing or compressing content when thresholds are exceeded.

**Attention Engineering** optimizes how remaining content is positioned to maximize attention, regardless of context size.

**How they work together:**
- Use Context Editing to manage context size (remove/compress less critical content)
- Use Attention Engineering to position remaining critical content optimally
- This combination ensures both efficient context usage and maximum attention to important information

## When to Use This Pattern

### ✅ Use when:

- Building agents that process long contexts (typically 10K+ tokens) where the "lost in the middle" problem could occur.
- Critical instructions or constraints must be reliably followed, and you cannot risk them being overlooked.
- Maintaining focus on high-level goals across extended, multi-step tasks.
- Working with complex prompts where important information might get buried.
- You need to ensure the model prioritizes specific facts or requirements over others.
- Building production systems where reliability and consistency are critical.

### ❌ Avoid when:

- Contexts are very short (<5K tokens) where attention distribution is more uniform.
- All information is equally important and there's no need to prioritize.
- The task is simple and single-turn, making attention engineering overhead unnecessary.
- You're working with models that don't exhibit strong primacy/recency biases (though most transformer-based LLMs do).

### Decision Guidelines

Use Attention Engineering whenever context length exceeds 10K tokens or when critical instructions must be reliably followed. The pattern is especially valuable for long-horizon tasks, complex multi-step workflows, and production systems requiring high reliability. Consider the trade-off: attention engineering adds some structural overhead but prevents costly goal drift and missed constraints. For contexts over 20K tokens or tasks with critical requirements, the benefits typically outweigh the costs.

> **"The most powerful design lever in agents today is *context curation*, not more compute."** — Manus Creators


## Practical Applications & Use Cases

Attention Engineering is fundamental to building reliable, focused agent systems across diverse applications.

- **Long-Context Document Processing:** When processing lengthy documents, extract and repeat critical facts at both the beginning and end of the prompt to ensure they're not lost in the middle.

- **Complex Instruction Following:** For agents executing complex workflows, place essential constraints and requirements at the start (primacy) and end (recency) of system instructions.

- **Goal Maintenance in Long Tasks:** Use recitation techniques to continuously append updated goals or plans to the end of context, keeping objectives "fresh" throughout extended execution.

- **Research and Analysis Agents:** When synthesizing information from multiple sources, use attention scoring to prioritize the most relevant sources and position them at attention-rich locations.

- **Code Generation Systems:** Systems like Claude Code use attention engineering to maintain focus on coding objectives by reciting task lists and keeping critical constraints visible.

- **Multi-Agent Orchestration:** Orchestrator agents use attention engineering to ensure worker agents receive critical instructions in prominent positions, preventing misalignment.

- **Constraint-Heavy Applications:** When agents must follow strict rules or safety constraints, attention engineering ensures these requirements are positioned where they'll receive maximum attention.

## Implementation

### Prerequisites
```bash
pip install langchain langchain-openai
# or
pip install google-adk
# or
pip install tiktoken  # For token counting
```

### Basic Example: Strategic Positioning

This example demonstrates front-loading critical instructions and back-loading reminders:

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o")

def build_attention_engineered_prompt(
    critical_instruction: str,
    context_data: str,
    final_reminder: str
) -> str:
    """
    Build a prompt with attention engineering:
    - Critical instruction at the start (primacy)
    - Context in the middle
    - Final reminder at the end (recency)
    """
    prompt = f"""CRITICAL INSTRUCTION (MUST FOLLOW):
{critical_instruction}

---
CONTEXT:
{context_data}
---

FINAL REMINDER (IMPORTANT):
{final_reminder}
"""
    return prompt

# Usage
critical = "Always validate user input before processing. Never execute untrusted code."
context = "User wants to analyze sales data from Q4 2024..."
reminder = "Remember: Validate all input. Do not execute untrusted code."

prompt = build_attention_engineered_prompt(critical, context, reminder)
response = llm.invoke(prompt)
```

**Explanation:**
This example demonstrates the sandwich approach: critical instruction at the start (primacy bias), context in the middle, and final reminder at the end (recency bias). This multi-layer reinforcement ensures the constraint is seen at both attention peaks.

### Advanced Example: Recency Bias Exploitation (Recitation)

This example shows how to continuously update and append critical information to maintain recency:

```python
from typing import List, Dict
from pathlib import Path

class AttentionEngineeredAgent:
    def __init__(self, goals_file: str = "goals.md"):
        self.goals_file = Path(goals_file)
        self.goals = []
        self.conversation_history = []
    
    def update_goals(self, new_goals: List[str]):
        """Update goals and save to persistent file."""
        self.goals = new_goals
        self.goals_file.write_text("\n".join([f"- {g}" for g in self.goals]))
    
    def build_context_with_recitation(self, user_message: str) -> str:
        """
        Build context with recitation: append updated goals to end
        to exploit recency bias.
        """
        # Load conversation history
        history = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in self.conversation_history[-10:]  # Last 10 messages
        ])
        
        # Load current goals (recitation)
        current_goals = self.goals_file.read_text() if self.goals_file.exists() else ""
        
        # Build attention-engineered prompt
        prompt = f"""You are a helpful assistant. Follow these guidelines:
- Be concise and accurate
- Always refer to current goals when making decisions

CONVERSATION HISTORY:
{history}

CURRENT USER MESSAGE:
{user_message}

---
CURRENT GOALS (UPDATED):
{current_goals}

Remember: These goals should guide all your decisions and actions.
"""
        return prompt
    
    def process(self, user_message: str, llm):
        """Process message with attention engineering."""
        prompt = self.build_context_with_recitation(user_message)
        response = llm.invoke(prompt)
        
        # Update history
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": response.content})
        
        return response

# Usage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
agent = AttentionEngineeredAgent()

# Set initial goals
agent.update_goals([
    "Complete research on AI agents",
    "Synthesize findings into report",
    "Ensure all sources are cited"
])

# Process messages - goals are automatically recited at end of each prompt
response1 = agent.process("What should I research first?", llm)
# Goals are appended to end, maintaining recency

# Update goals as tasks complete
agent.update_goals([
    "Complete research on AI agents",  # Done
    "Synthesize findings into report",  # In progress
    "Ensure all sources are cited"
])

response2 = agent.process("I found 5 papers. What next?", llm)
# Updated goals are recited, keeping agent focused
```

**Explanation:**
This example implements recitation by continuously appending updated goals to the end of the context. This exploits recency bias, ensuring goals remain in the model's recent attention span even as conversation history grows.

### Advanced Example: Attention Scoring and Reordering

This example demonstrates attention scoring by measuring which parts of context the model focuses on, then reordering:

```python
from typing import List, Tuple
import tiktoken

class AttentionScorer:
    def __init__(self, model: str = "gpt-4o"):
        self.encoding = tiktoken.encoding_for_model(model)
        self.llm = ChatOpenAI(model=model)
    
    def score_context_chunks(self, chunks: List[str], query: str) -> List[Tuple[str, float]]:
        """
        Score each chunk by having the model assess relevance,
        then return chunks with scores.
        """
        scored_chunks = []
        
        for i, chunk in enumerate(chunks):
            # Ask model to score relevance
            scoring_prompt = f"""Rate the relevance of this text chunk to the query on a scale of 0.0 to 1.0.

Query: {query}

Chunk:
{chunk}

Provide only a number between 0.0 and 1.0:"""
            
            score_response = self.llm.invoke(scoring_prompt)
            try:
                score = float(score_response.content.strip())
            except:
                score = 0.5  # Default if parsing fails
            
            scored_chunks.append((chunk, score))
        
        return scored_chunks
    
    def reorder_by_attention(self, chunks: List[str], query: str) -> str:
        """
        Reorder context chunks so most relevant (high attention) 
        chunks move to the end (recency position).
        """
        # Score all chunks
        scored = self.score_context_chunks(chunks, query)
        
        # Sort by score (highest first)
        scored.sort(key=lambda x: x[1], reverse=True)
        
        # Reorder: put high-scoring chunks at end (recency), 
        # but keep some at start (primacy) too
        high_attention = [chunk for chunk, score in scored if score > 0.7]
        medium_attention = [chunk for chunk, score in scored if 0.4 <= score <= 0.7]
        low_attention = [chunk for chunk, score in scored if score < 0.4]
        
        # Build reordered context: primacy + recency positioning
        reordered = []
        
        # Start with highest attention (primacy)
        if high_attention:
            reordered.append("MOST RELEVANT INFORMATION:")
            reordered.extend(high_attention[:2])  # Top 2 at start
        
        # Middle gets medium and low
        reordered.append("\n---\n")
        reordered.extend(medium_attention)
        reordered.extend(low_attention)
        
        # End with remaining high attention (recency)
        reordered.append("\n---\n")
        reordered.append("KEY INFORMATION (REMEMBER):")
        reordered.extend(high_attention[2:])  # Rest at end
        
        return "\n\n".join(reordered)

# Usage
scorer = AttentionScorer()

chunks = [
    "Sales data shows 20% increase in Q4",
    "Weather was sunny all week",
    "Customer satisfaction scores improved by 15%",
    "The office was painted blue",
    "Revenue targets were exceeded by 5%"
]

query = "What were the key business metrics in Q4?"

# Reorder so most relevant chunks are at attention-rich positions
reordered_context = scorer.reorder_by_attention(chunks, query)

# Use reordered context in final prompt
final_prompt = f"""Analyze this information and answer: {query}

{reordered_context}

Based on the information above, provide your analysis."""
```

**Explanation:**
This advanced example implements attention scoring by having the model assess chunk relevance, then reorders chunks so the most relevant appear at both the beginning (primacy) and end (recency) of the context. This ensures maximum attention to important information.

### Framework-Specific Examples

#### LangChain: Structured Prompt with Attention Engineering

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

llm = ChatOpenAI(model="gpt-4o")

# System message with critical instruction at start (primacy)
system_template = """CRITICAL REQUIREMENTS (READ FIRST):
1. Always validate user input
2. Never execute untrusted code
3. Cite all sources

You are a helpful research assistant. Follow the critical requirements above in all responses.
"""

# Human message template
human_template = """Research Question: {question}

Context:
{context}

---
REMINDER (IMPORTANT):
- Validate all input
- Cite all sources
- Do not execute untrusted code
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", human_template)
])

chain = prompt | llm

# Usage
response = chain.invoke({
    "question": "What are the latest AI agent patterns?",
    "context": "Recent research shows..."
})
```

#### Custom Attention Engineering Middleware

```python
from typing import List, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

class AttentionEngineeringMiddleware:
    """Middleware that applies attention engineering to prompts."""
    
    def __init__(self, critical_instructions: List[str]):
        self.critical_instructions = critical_instructions
    
    def process_messages(self, messages: List[BaseMessage]) -> List[BaseMessage]:
        """Reorder and enhance messages with attention engineering."""
        processed = []
        
        # Extract system messages and critical instructions
        system_parts = []
        other_messages = []
        
        for msg in messages:
            if isinstance(msg, SystemMessage):
                system_parts.append(msg.content)
            else:
                other_messages.append(msg)
        
        # Build attention-engineered system message
        # Primacy: Critical instructions at start
        engineered_system = "CRITICAL INSTRUCTIONS (MUST FOLLOW):\n"
        engineered_system += "\n".join([f"- {inst}" for inst in self.critical_instructions])
        engineered_system += "\n\n---\n\n"
        engineered_system += "\n\n".join(system_parts)
        
        processed.append(SystemMessage(content=engineered_system))
        processed.extend(other_messages)
        
        # Add recency reminder as final human message if needed
        if other_messages and isinstance(other_messages[-1], HumanMessage):
            reminder = "\n\n---\nREMINDER: " + "; ".join(self.critical_instructions[:3])
            other_messages[-1].content += reminder
        
        return processed

# Usage
middleware = AttentionEngineeringMiddleware([
    "Always validate input",
    "Never execute untrusted code",
    "Cite all sources"
])

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Help me analyze this data.")
]

engineered_messages = middleware.process_messages(messages)
```

## Key Takeaways

- **Core Strategy:** Attention Engineering exploits the model's inherent attention biases (primacy and recency) by strategically positioning critical information at optimal locations in the prompt.

- **Primacy and Recency are Key:** Information at the beginning (primacy) and end (recency) of context receives disproportionately more attention than information in the middle. Use this to your advantage.

- **Multi-Layer Reinforcement Works Best:** Combine positioning strategies—place critical info at both beginning and end, and reiterate it in structured forms throughout the prompt.

- **Avoid the Middle:** Never hide important constraints or requirements in the middle of lengthy text. Always surface them at prominent positions.

- **Recency Bias Exploitation:** For long-running tasks, continuously update and append key information (goals, constraints) near the end of context to keep it "fresh" in the model's working memory.

- **Attention Scoring Enables Optimization:** Assess and prioritize information based on importance and attention potential, then organize content accordingly. High-priority information should receive prominent positions.

- **Structural Cues Guide Attention:** Use clear sections, headings, or bullet points to guide attention. Each section acts like a mini-prompt where crucial info can be placed at the top.

- **Common Pitfall:** Assuming all parts of a prompt receive equal attention. Research shows this is false—attention is U-shaped, with peaks at beginning and end.

- **Best Practice:** For contexts over 10K tokens or tasks with critical requirements, always apply attention engineering. The structural overhead is minimal compared to the reliability gains.

## Related Patterns

This pattern works well with:
- **Context Engineering:** Attention Engineering is a core technique within the broader context engineering discipline, focusing specifically on information positioning.

- **Recitation:** Recitation is a specific application of Attention Engineering's recency bias exploitation, continuously appending updated plans to maintain focus.

- **Context Editing:** Use Context Editing to manage context size, then apply Attention Engineering to position remaining critical content optimally.

- **Variables Manager:** Attention Engineering can be applied to position variable summaries at attention-rich locations, ensuring the agent maintains awareness of execution state.

This pattern is often combined with:
- **Strategic Prompting:** Attention Engineering enhances strategic prompting by ensuring critical instructions are positioned where they'll receive maximum attention.

- **Multi-Agent Systems:** Orchestrator agents use attention engineering to ensure worker agents receive critical instructions in prominent positions.

- **Long-Horizon Planning:** Attention Engineering maintains goal visibility throughout extended tasks by exploiting recency bias through recitation.

??? "References"

- Liu, N. F., et al. (2023). "Lost in the Middle: How Language Models Use Long Contexts." *arXiv preprint arXiv:2307.03172*. https://arxiv.org/abs/2307.03172

- Zhou, D., et al. (2023). "Principled Instructions Are All You Need for Questioning LLaMA-1 and LLaMA-2." *arXiv preprint arXiv:2312.16171*. https://arxiv.org/abs/2312.16171

- Lewis, P., et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *Advances in Neural Information Processing Systems*, 33, 9459-9474. https://arxiv.org/abs/2005.11401

- Notion Labs. (2023). "The Prompt Report." https://www.notion.so/prompt-report

- Notion Labs. (2024). "Manuscript: Scaling Agents with Long Context and Attention Engineering." https://blog.sugiv.fyi

- Ding, J., et al. (2023). "LongNet: Scaling Transformers to 1,000,000,000 Tokens." *arXiv preprint arXiv:2307.02486*. https://arxiv.org/abs/2307.02486

- Liu, B., et al. (2023). "Gorilla: Large Language Model Connected with Massive APIs." *arXiv preprint arXiv:2305.15334*. https://arxiv.org/abs/2305.15334

- Context Engineering Guide - https://www.promptingguide.ai/guides/context-engineering-guide

- LangGraph Middleware Documentation - https://langchain-ai.github.io/langgraph/how-tos/middleware/

