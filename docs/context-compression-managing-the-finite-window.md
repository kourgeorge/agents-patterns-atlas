# Context Compression: Managing the Finite Window

## Motivation

When summarizing a long meeting, you extract key decisions and action items, not every word spoken. When reading a research paper, you focus on the abstract and conclusions. Humans naturally compress information, keeping essential details while discarding the rest. Context Compression applies this principle: fitting necessary information into the finite context window through summarization, pruning, and selective retrieval, just as we distill complex information into manageable insights.

## Pattern Overview
**What it is:** Context compression encompasses techniques used to fit the necessary information for a task into the Large Language Model's (LLM) finite context window, thereby sustaining performance and reducing costs.

**When to use:** When building agents that process large amounts of information, maintain long conversation histories, or work with extensive datasets that would exceed context window limits or degrade performance.

**Why it matters:** The finite context window is a fundamental constraint of LLM-based agents. Without effective compression strategies, agents hit hard limits, suffer performance degradation, and incur excessive costs. Context compression enables agents to work with unlimited information while maintaining efficiency and performance.

The context window represents the maximum number of tokens an LLM can process in a single interaction. This finite boundary creates a fundamental challenge: agents must balance the need for comprehensive information against the constraints of token limits, processing costs, and performance degradation. As agents tackle complex, multi-step tasks, they accumulate conversation history, tool results, and intermediate reasoning that can quickly exhaust available context.

Context compression is not a single technique but a comprehensive strategy combining multiple approaches. The most powerful method is externalizing memory—offloading large or long-term information to persistent storage. For information that must remain in context, techniques like summarization, truncation, and attention manipulation ensure the agent maintains focus on what matters most.

Effective context compression is essential for production agent systems. It directly impacts cost (fewer tokens = lower API costs), latency (shorter contexts = faster processing), and performance (focused contexts = better reasoning). Without compression, agents cannot scale to handle real-world complexity.

### Key Concepts
- **Finite Context Window:** The maximum number of tokens an LLM can process at once, creating a hard limit on information capacity.
- **Externalized Memory:** Offloading large data to persistent storage (filesystem, database) to extend working memory beyond context limits.
- **Restorable Compression:** Dropping content from context while maintaining references (paths, URLs) for on-demand retrieval.
- **Contextual Pruning:** Removing or summarizing less relevant information to preserve space for critical content.
- **Summarization:** Condensing conversation history or documents into compact representations that preserve essential information.
- **Chunking:** Breaking large documents into smaller, manageable pieces for processing and retrieval.
- **Attention Manipulation:** Strategically positioning important information (like plans) to bias model attention.
- **Lost-in-the-Middle Problem:** Performance degradation when critical information appears in the middle of very long contexts.

### How It Works: Step-by-step Explanation

Context compression operates through multiple complementary strategies:

1. **Externalize Large Data:** The primary compression strategy is to offload large or long-term information to external persistent storage. The agent writes intermediate results, tool outputs, or large observations to files or databases, keeping only lightweight references in context.

2. **Maintain Restorable References:** Compression must be restorable. The agent drops large content from the prompt but retains references (file paths, URLs, database keys) that enable precise retrieval when needed.

3. **Just-in-Time Retrieval:** When specific information is required, the agent retrieves only relevant snippets using targeted tools (grep, line-range reads, semantic search) rather than loading entire files.

4. **Summarize Context History:** For information that must remain in context, older conversation segments are summarized into compact blocks, preserving essential information while freeing space for active reasoning.

5. **Prune and Prioritize:** Less critical information is truncated or removed, ensuring the most relevant content remains accessible within context limits.

6. **Manipulate Attention:** Important information (like high-level plans) is strategically positioned (e.g., at the end of context) to leverage recency bias and maintain focus.

## When to Use This Pattern

### ✅ Use when:
- Building agents that process large documents, datasets, or extensive research materials.
- Maintaining long conversation histories across multiple turns.
- Working with unstructured data (web pages, PDFs) that exceeds context limits.
- Implementing multi-step agents that accumulate intermediate results and reasoning.
- Cost and latency optimization are critical requirements.
- Performance degradation is observed with long contexts.

### ❌ Avoid when:
- All necessary information fits comfortably within context limits without performance issues.
- The task is simple and single-turn, making compression overhead unnecessary.
- Real-time retrieval latency from external storage is unacceptable.
- The compression strategy would lose critical information that cannot be restored.

### Decision Guidelines
Context compression is essential for any production agent system handling real-world complexity. The strategy should be layered: externalize large data first (most effective), then summarize/prune what remains in context, and finally use attention manipulation for critical information. Consider: data size (large = externalize), access pattern (frequent = keep in context, rare = externalize), and criticality (essential = keep recent, supplementary = summarize or externalize). Always maintain restorable references for externalized data.

## Practical Applications & Use Cases

Context compression is fundamental to building scalable, efficient agent systems across diverse applications.

- **Research Agents:** Agents conducting literature reviews offload search results and papers to external storage, retrieving specific sections when synthesizing findings.

- **Code Generation Agents:** Systems like Claude Code use external memory to store codebase context, reading specific files and functions on demand rather than loading entire repositories.

- **Long-Running Conversations:** Chatbots and assistants compress old conversation history through summarization, maintaining recent context while preserving essential context from earlier exchanges.

- **Document Processing:** Agents processing large PDFs or documents save extracted content externally, then query specific sections when answering questions.

- **Multi-Agent Systems:** Orchestrator agents compress subagent outputs, storing detailed results externally and keeping only summaries and references in context.

- **RAG Systems:** Knowledge bases are chunked and indexed, with agents retrieving only relevant chunks rather than entire documents.

- **Planning Agents:** Agents maintain persistent plans externally (todo.md) and recite them into context, ensuring goals remain visible without consuming context space.

## Implementation

### Prerequisites
```bash
pip install langchain langchain-openai
# or
pip install google-adk
# or
pip install tiktoken  # For token counting
```

### Basic Example: Context Compression Manager

This example demonstrates a comprehensive context compression system combining externalization, summarization, and pruning:

```python
from typing import List, Dict
from pathlib import Path
import tiktoken

class ContextCompressionManager:
    def __init__(self, workspace_dir: str = "./workspace", max_tokens: int = 100000):
        self.workspace = Path(workspace_dir)
        self.workspace.mkdir(exist_ok=True)
        self.max_tokens = max_tokens
        self.encoding = tiktoken.encoding_for_model("gpt-4")
        self.context_history = []
        self.external_memory = {}
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))
    
    def externalize(self, content: str, key: str) -> str:
        """Offload large content to external storage."""
        filepath = self.workspace / f"{key}.txt"
        filepath.write_text(content)
        self.external_memory[key] = str(filepath)
        
        # Return lightweight reference
        size = len(content)
        return f"[External Memory: {key} ({size} chars stored)]"
    
    def should_compress(self) -> bool:
        """Check if context needs compression."""
        total_tokens = sum(self.count_tokens(msg["content"]) for msg in self.context_history)
        return total_tokens > self.max_tokens * 0.9
    
    def summarize_old_messages(self, messages: List[Dict], llm) -> str:
        """Summarize old conversation messages."""
        if not messages:
            return ""
        
        # Prepare messages for summarization
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content'][:500]}"  # Truncate for summary
            for msg in messages
        ])
        
        summary_prompt = f"""Summarize this conversation history concisely, 
        preserving key decisions, user preferences, and important context:
        
        {conversation_text}
        
        Summary:"""
        
        summary = llm.invoke(summary_prompt).content
        return summary
    
    def compress_context(self, llm) -> List[Dict]:
        """Compress context when approaching limits."""
        if not self.should_compress():
            return self.context_history
        
        # Keep recent messages (last 10)
        recent_messages = self.context_history[-10:]
        old_messages = self.context_history[:-10]
        
        # Summarize old messages
        if old_messages:
            summary = self.summarize_old_messages(old_messages, llm)
            summary_message = {
                "role": "system",
                "content": f"Previous conversation summary: {summary}"
            }
            # Replace old messages with summary
            self.context_history = [summary_message] + recent_messages
        
        return self.context_history
    
    def add_message(self, role: str, content: str, llm=None):
        """Add message with automatic compression."""
        # Check if content is too large
        if self.count_tokens(content) > 5000:
            # Externalize large content
            key = f"message_{len(self.context_history)}"
            reference = self.externalize(content, key)
            self.context_history.append({
                "role": role,
                "content": f"{reference}\n\n[Content stored externally. Use retrieve_external('{key}') to access.]"
            })
        else:
            self.context_history.append({"role": role, "content": content})
        
        # Compress if needed
        if llm and self.should_compress():
            self.compress_context(llm)
    
    def retrieve_external(self, key: str, query: str = None) -> str:
        """Retrieve from external memory with optional filtering."""
        if key not in self.external_memory:
            return f"Key '{key}' not found in external memory."
        
        filepath = Path(self.external_memory[key])
        content = filepath.read_text()
        
        # If query provided, filter content
        if query:
            lines = [line for line in content.split('\n') if query.lower() in line.lower()]
            return '\n'.join(lines[:50])  # Top 50 matches
        
        return content[:2000]  # Return first portion

# Usage
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
compressor = ContextCompressionManager(max_tokens=100000)

# Add messages (large content automatically externalized)
compressor.add_message("user", "Large web search result...", llm)
compressor.add_message("assistant", "Processing...", llm)

# Context automatically compressed when approaching limits
compressed_context = compressor.compress_context(llm)
```

**Explanation:**
This example demonstrates a comprehensive compression manager that automatically externalizes large content, summarizes old messages, and maintains context within token limits. It combines multiple compression strategies in a unified system.

### Advanced Example: Intelligent Context Pruning

```python
from typing import List, Dict, Tuple
import re
from collections import defaultdict

class IntelligentContextPruner:
    def __init__(self, max_tokens: int = 100000, keep_recent: int = 20):
        self.max_tokens = max_tokens
        self.keep_recent = keep_recent
        self.encoding = tiktoken.encoding_for_model("gpt-4")
        self.importance_scores = {}
    
    def calculate_importance(self, message: Dict, context: List[Dict]) -> float:
        """Calculate importance score for a message."""
        score = 0.0
        content = message.get("content", "")
        
        # Recent messages are more important
        position = context.index(message) if message in context else len(context)
        recency_score = 1.0 / (position + 1)
        score += recency_score * 0.3
        
        # System messages are important
        if message.get("role") == "system":
            score += 0.4
        
        # Messages with tool results might be important
        if "tool" in content.lower() or "result" in content.lower():
            score += 0.2
        
        # Messages with user queries are important
        if message.get("role") == "user":
            score += 0.3
        
        # Check for key indicators
        key_phrases = ["error", "important", "critical", "decision", "plan"]
        if any(phrase in content.lower() for phrase in key_phrases):
            score += 0.2
        
        return score
    
    def prune_context(self, context: List[Dict], target_tokens: int) -> List[Dict]:
        """Intelligently prune context to fit within token budget."""
        # Calculate importance for each message
        importance_scores = {
            i: self.calculate_importance(msg, context)
            for i, msg in enumerate(context)
        }
        
        # Always keep most recent messages
        recent_indices = set(range(max(0, len(context) - self.keep_recent), len(context)))
        
        # Sort by importance (descending)
        sorted_indices = sorted(
            importance_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Select messages to keep
        kept_indices = set(recent_indices)
        current_tokens = sum(
            self.count_tokens(context[i]["content"])
            for i in recent_indices
        )
        
        for idx, score in sorted_indices:
            if idx in kept_indices:
                continue
            
            msg_tokens = self.count_tokens(context[idx]["content"])
            if current_tokens + msg_tokens <= target_tokens:
                kept_indices.add(idx)
                current_tokens += msg_tokens
            else:
                break
        
        # Reconstruct context in original order
        pruned_context = [
            context[i] for i in sorted(kept_indices)
            if i < len(context)
        ]
        
        return pruned_context
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))
    
    def compress_with_summarization(self, context: List[Dict], llm, max_summary_tokens: int = 1000) -> List[Dict]:
        """Compress by summarizing less important messages."""
        # Identify messages to summarize (not in recent set)
        recent_count = min(self.keep_recent, len(context))
        to_summarize = context[:-recent_count] if recent_count < len(context) else []
        to_keep = context[-recent_count:] if recent_count < len(context) else context
        
        if not to_summarize:
            return context
        
        # Create summary of old messages
        summary_text = "\n".join([
            f"{msg['role']}: {msg['content'][:200]}"
            for msg in to_summarize
        ])
        
        summary_prompt = f"""Create a concise summary of this conversation history, 
        preserving key information, decisions, and context:
        
        {summary_text}
        
        Summary (max {max_summary_tokens} tokens):"""
        
        summary = llm.invoke(summary_prompt).content
        
        # Combine summary with recent messages
        compressed = [
            {"role": "system", "content": f"Previous conversation summary: {summary}"}
        ] + to_keep
        
        return compressed

# Usage
pruner = IntelligentContextPruner(max_tokens=100000, keep_recent=20)

# Prune context intelligently
compressed = pruner.prune_context(long_context, target_tokens=80000)

# Or use summarization
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")
compressed = pruner.compress_with_summarization(long_context, llm)
```

**Explanation:**
This advanced example implements intelligent context pruning that considers message importance, recency, and content type. It prioritizes critical information while removing less important messages, and can also use summarization for more aggressive compression.

### Framework-Specific Examples

#### LangChain: Conversation Summary Memory
```python
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain

llm = ChatOpenAI(model="gpt-4o")

# Summary memory automatically compresses old messages
memory = ConversationSummaryMemory(
    llm=llm,
    max_token_limit=1000,  # Target summary size
    return_messages=True
)

chain = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Long conversation automatically compressed
response1 = chain.predict(input="Tell me about AI agents")
# ... many turns later ...
response10 = chain.predict(input="What did we discuss earlier?")
# Old messages are summarized, recent ones preserved
```

#### Google ADK: Session State with Compression
```python
from google.adk.sessions import InMemorySessionService
from google.adk.agents import LlmAgent
from google.adk.runners import Runner

def compress_session_state(state: dict, max_size: int = 10000) -> dict:
    """Compress session state when it exceeds size limit."""
    state_str = str(state)
    if len(state_str) > max_size:
        # Summarize or externalize large state
        # Keep only essential keys
        essential_keys = ["user_id", "current_task", "recent_messages"]
        compressed = {k: state[k] for k in essential_keys if k in state}
        # Externalize rest
        # ... externalization logic ...
        return compressed
    return state

session_service = InMemorySessionService()
session_service.add_compression_hook(compress_session_state)

agent = LlmAgent(
    name="CompressedAgent",
    model="gemini-2.0-flash",
    instruction="Work efficiently within context limits."
)

runner = Runner(
    agent=agent,
    app_name="compressed_app",
    session_service=session_service
)
```

#### Custom Chunking for RAG
```python
from typing import List
import tiktoken

class DocumentChunker:
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.encoding = tiktoken.encoding_for_model("gpt-4")
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        tokens = self.encoding.encode(text)
        chunks = []
        
        for i in range(0, len(tokens), self.chunk_size - self.overlap):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)
        
        return chunks
    
    def chunk_by_sentences(self, text: str) -> List[str]:
        """Chunk by sentences for better semantic coherence."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = []
        current_size = 0
        
        for sentence in sentences:
            sent_tokens = len(self.encoding.encode(sentence))
            if current_size + sent_tokens > self.chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_size = sent_tokens
            else:
                current_chunk.append(sentence)
                current_size += sent_tokens
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

# Usage
chunker = DocumentChunker(chunk_size=1000, overlap=200)
chunks = chunker.chunk_by_sentences(large_document)

# Store chunks in vector database
# Retrieve only relevant chunks for context
```

## Key Takeaways

- **Core Strategy:** Context compression is essential for managing the finite context window through externalization, summarization, pruning, and attention manipulation.

- **Primary Method:** Externalizing memory (offloading to filesystem/database) is the most powerful compression technique, enabling unlimited information storage with restorable references.

- **Layered Approach:** Combine multiple strategies: externalize large data first, then summarize/prune what remains, and use attention manipulation for critical information.

- **Restorable Compression:** Always maintain references (paths, URLs, keys) when externalizing data to enable precise retrieval when needed.

- **Performance Impact:** Effective compression directly improves cost, latency, and reasoning quality by keeping contexts focused and within optimal token ranges.

- **Common Pitfall:** Aggressive compression that loses critical information or fails to maintain restorable references defeats the purpose. Always preserve essential context and references.

- **Best Practice:** Monitor context token usage and implement automatic compression when approaching limits (e.g., 90% of max tokens) to prevent hard failures.

## Related Patterns

This pattern works well with:
- **Leverage External Memory (Filesystem as Context):** Externalization is the primary compression strategy, offloading large data to persistent storage.

- **Persistent Task List (Recitation):** Attention manipulation through recitation keeps important plans visible without consuming context space.

- **Memory Management:** Context compression is a key component of comprehensive memory management, complementing context window optimization and external memory systems.

- **Knowledge Retrieval (RAG):** Chunking enables RAG systems to retrieve only relevant document sections rather than entire documents.

This pattern is often combined with:
- **Stable, Append-Only Context:** Compression helps maintain stable context prefixes for KV-Cache optimization.

- **Tool Result Management:** Large tool results are externalized, with only summaries or references kept in context.

- **Multi-Agent Architectures:** Orchestrators compress subagent outputs, storing details externally and keeping summaries in context.

## References

- Agentic AI System Design Patterns
- Context Engineering for AI Agents: Lessons from Building Manus
- LangChain Memory Management: https://python.langchain.com/docs/modules/memory/
- Google ADK Sessions: https://google.github.io/adk-docs/sessions/
- Context Compression Techniques: https://arxiv.org/abs/2309.00071
- Lost in the Middle: How Language Models Use Long Contexts: https://arxiv.org/abs/2307.03172

