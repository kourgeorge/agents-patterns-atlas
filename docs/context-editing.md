# Pattern: Context Editing

## Motivation

As conversations grow, context accumulates: tool results pile up, thinking blocks expand, and message history lengthens. Without intervention, agents hit token limits, costs escalate, and performance degrades. Just as editors trim manuscripts to focus on essential content, Context Editing automatically manages conversation context as it grows, removing less critical information while preserving what matters most. This pattern enables agents to operate indefinitely within context limits through intelligent, automatic pruning.

## Pattern Overview
**What it is:** Context editing automatically manages conversation context as it grows, removing or compressing less critical content (tool results, thinking blocks, old messages) to stay within token limits and optimize costs.

**When to use:** When building long-running agents that accumulate extensive conversation history, tool results, or thinking blocks that would exceed context window limits or degrade performance over time.

**Why it matters:** Without automatic context management, agents hit hard token limits, incur excessive costs from processing large contexts, and suffer performance degradation. Context editing enables agents to operate indefinitely while maintaining focus on relevant information.

Context editing is a core component of context engineering—the discipline of strategically managing what information appears in the context window to optimize performance, cost, and reasoning quality. Unlike manual context compression techniques, context editing operates automatically, either server-side (before prompts reach the model) or client-side (through SDK compaction), removing or summarizing content based on configurable strategies.

The pattern addresses the fundamental challenge of growing context: as agents execute multi-step tasks, they accumulate tool results, conversation history, and intermediate reasoning that can quickly exhaust available tokens. Context editing provides two complementary approaches:

1. **Server-side editing:** Applied by the API before prompts reach the model, clearing specific content types (tool results, thinking blocks) based on configurable thresholds and retention policies.

2. **Client-side compaction:** SDK-based summarization that replaces entire conversation history with a structured summary when token thresholds are exceeded, enabling agents to continue from a compressed state.

Both approaches maintain conversation continuity while managing context size, ensuring agents can operate effectively over extended interactions without manual intervention.

### Key Concepts
- **Tool Result Clearing:** Automatically removing tool results from conversation history when context exceeds thresholds, replacing them with placeholder text to indicate removal.
- **Thinking Block Clearing:** Managing extended thinking blocks by clearing older thinking content while preserving recent reasoning.
- **Client-Side Compaction:** SDK-based summarization that replaces full conversation history with a structured continuation summary when token limits are approached.
- **Restorable References:** Maintaining lightweight references (file paths, keys) for cleared content that can be retrieved on demand.
- **Context Thresholds:** Configurable token limits that trigger automatic editing operations.
- **Retention Policies:** Rules specifying what content to keep (e.g., last N tool uses, all thinking blocks, recent messages) during editing operations.

### How It Works: Step-by-step Explanation

**Server-Side Editing:**

1. **Monitor Context Size:** Track input token usage as the conversation progresses, comparing against configured thresholds.

2. **Trigger Editing:** When context exceeds the threshold (e.g., 30,000 input tokens), activate the configured editing strategy.

3. **Apply Strategy:** Based on the strategy type:
   - **Tool Result Clearing:** Remove oldest tool results chronologically, replacing with placeholders like "[Tool result cleared]". Optionally clear tool inputs as well.
   - **Thinking Block Clearing:** Remove older thinking blocks while preserving recent ones based on retention policy (e.g., keep last N turns, keep all, or keep none).

4. **Preserve References:** Maintain lightweight references for cleared content (file paths, URLs) that enable retrieval if needed.

5. **Continue Conversation:** The model receives the edited context and continues normally, with cleared content replaced by placeholders.

**Client-Side Compaction:**

1. **Monitor Token Usage:** SDK tracks cumulative token usage across conversation turns.

2. **Detect Threshold:** When token usage exceeds the configured threshold (e.g., 100,000 tokens), trigger compaction.

3. **Generate Summary:** Request the model to generate a structured continuation summary including:
   - Task overview and current state
   - Important discoveries and decisions
   - Next steps and blockers
   - Context to preserve (preferences, commitments)

4. **Replace History:** Replace entire conversation history with the summary message.

5. **Resume Operation:** Agent continues from the summary as if it were the original conversation history.

## When to Use This Pattern

### ✅ Use when:
- Building long-running agents that process many files, conduct extensive research, or execute multi-step tasks.
- Tool-heavy workflows where tool results accumulate quickly and consume significant context.
- Using extended thinking features where thinking blocks grow over time.
- Cost optimization is critical and large contexts are expensive to process repeatedly.
- Agents need to operate indefinitely without hitting hard token limits.
- Conversation history grows beyond optimal context sizes (typically 50K+ tokens).

### ❌ Avoid when:
- Tasks are short-lived or single-turn, making automatic editing unnecessary.
- All context is critical and cannot be safely removed or summarized.
- Real-time retrieval of cleared content is required and latency is unacceptable.
- Using server-side tools extensively (compaction may trigger incorrectly due to cache token counting).
- Tasks require precise recall of early conversation details that would be lost in summarization.

### Decision Guidelines
Context editing is essential for production agents handling long-running tasks. Choose server-side editing for fine-grained control over what gets cleared (tool results, thinking blocks) while preserving conversation structure. Use client-side compaction for more aggressive compression when full history replacement is acceptable. Consider: content type (tool results = server-side clearing, full history = compaction), retrieval needs (cleared content = maintain references, summarized = accept information loss), and cache optimization (preserving thinking blocks = better cache hits). Always configure thresholds conservatively (e.g., 80-90% of max tokens) to prevent hard failures.

## Practical Applications & Use Cases

Context editing is fundamental to building scalable, cost-effective agent systems across diverse applications.

- **Research Agents:** Agents conducting literature reviews automatically clear old search results while preserving recent findings and maintaining references to externalized papers.

- **Code Generation Agents:** Systems processing large codebases clear tool results from file operations, keeping only summaries and file paths for on-demand retrieval.

- **Long-Running Conversations:** Chatbots and assistants automatically manage conversation history, clearing old messages while preserving essential context through summarization.

- **Planning Agents:** Agents with extended thinking clear older thinking blocks while preserving recent reasoning, maintaining cache efficiency for prompt caching.

- **Multi-Agent Systems:** Orchestrator agents clear subagent outputs automatically, storing detailed results externally and keeping only summaries in context.

- **Tool-Heavy Workflows:** Agents using many tools (web search, file operations, API calls) automatically clear old tool results to prevent context bloat.

- **Cost-Sensitive Applications:** Production systems optimize costs by automatically managing context size, reducing token consumption without manual intervention.

## Implementation

### Prerequisites
```bash
pip install langchain langchain-openai langgraph
# or
pip install langchain langchain-google-genai langgraph
# or
pip install google-adk
```

### Basic Example: Context Editing with LangGraph Middleware

```python
from langchain.agents import create_agent
from langchain.agents.middleware import BaseMiddleware
from langchain_core.messages import BaseMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing import List, Dict, Any
import tiktoken

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}"

class ContextEditingMiddleware(BaseMiddleware):
    def __init__(self, token_threshold: int = 30000, keep_last_n: int = 3):
        super().__init__()
        self.token_threshold = token_threshold
        self.keep_last_n = keep_last_n
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, messages: List[BaseMessage]) -> int:
        return sum(
            len(self.encoding.encode(str(msg.content)))
            for msg in messages if hasattr(msg, 'content')
        )
    
    async def on_agent_step_start(self, state: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        if "messages" not in state:
            return state
        
        messages = state["messages"]
        if self.count_tokens(messages) >= self.token_threshold:
            tool_messages = [(i, msg) for i, msg in enumerate(messages) if isinstance(msg, ToolMessage)]
            if len(tool_messages) > self.keep_last_n:
                edited = messages.copy()
                for idx, _ in tool_messages[:-self.keep_last_n]:
                    edited[idx] = ToolMessage(content="[Cleared]", tool_call_id=edited[idx].tool_call_id)
                return {**state, "messages": edited}
        return state

llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_agent(
    model=llm,
    tools=[search_web],
    middleware=[ContextEditingMiddleware(token_threshold=30000, keep_last_n=3)]
)

result = agent.invoke({"messages": [{"role": "user", "content": "Research AI agents"}]})
```

**Explanation:**
This middleware automatically clears old tool results when context exceeds 30,000 tokens, keeping only the last 3. This enables agents to operate indefinitely without hitting token limits.

### Framework-Specific Examples

#### LangGraph: Advanced Context Editing

```python
from langchain.agents import create_agent
from langchain.agents.middleware import BaseMiddleware
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from typing import List, Dict, Any, Optional
import tiktoken

@tool
def web_search(query: str) -> str:
    """Search the web."""
    return f"Results: {query}"

class AdvancedContextEditingMiddleware(BaseMiddleware):
    def __init__(
        self,
        tool_threshold: int = 50000,
        keep_last_n: int = 5,
        exclude_tools: Optional[List[str]] = None
    ):
        super().__init__()
        self.tool_threshold = tool_threshold
        self.keep_last_n = keep_last_n
        self.exclude_tools = exclude_tools or []
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, messages: List[BaseMessage]) -> int:
        return sum(len(self.encoding.encode(str(msg.content))) for msg in messages if hasattr(msg, 'content'))
    
    async def on_agent_step_start(self, state: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        if "messages" not in state:
            return state
        
        messages = state["messages"]
        if self.count_tokens(messages) >= self.tool_threshold:
            tool_messages = [
                (i, msg) for i, msg in enumerate(messages)
                if isinstance(msg, ToolMessage) and msg.name not in self.exclude_tools
            ]
            if len(tool_messages) > self.keep_last_n:
                edited = messages.copy()
                for idx, _ in tool_messages[:-self.keep_last_n]:
                    edited[idx] = ToolMessage(content="[Cleared]", tool_call_id=edited[idx].tool_call_id)
                return {**state, "messages": edited}
        return state

llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_agent(
    model=llm,
    tools=[web_search],
    middleware=[AdvancedContextEditingMiddleware(
        tool_threshold=50000,
        keep_last_n=5,
        exclude_tools=["web_search"]
    )]
)

result = agent.invoke({"messages": [{"role": "user", "content": "Research multiple topics"}]})
```

#### Google ADK: Session State Compression

```python
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

def compress_context(state: dict, max_tokens: int = 80000) -> dict:
    messages = state.get("messages", [])
    if len(messages) > 20:  # Simple heuristic
        state["messages"] = [
            {"role": "system", "content": "[Previous conversation summarized]"}
        ] + messages[-10:]
    return state

session_service = InMemorySessionService()
session_service.add_compression_hook(compress_context)

agent = Agent(
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

#### Google ADK: Session State Compression

```python
from google.adk.sessions import InMemorySessionService
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.middleware import ContextCompressionMiddleware

def compress_context(state: dict, max_tokens: int = 80000) -> dict:
    """Compress session context when it exceeds token limit."""
    # Count tokens in messages
    total_tokens = estimate_tokens(str(state.get("messages", [])))
    
    if total_tokens > max_tokens:
        # Keep recent messages, summarize old ones
        messages = state.get("messages", [])
        recent = messages[-10:]  # Last 10 messages
        old = messages[:-10]
        
        # Summarize old messages
        summary = summarize_messages(old)
        
        # Replace with summary + recent
        state["messages"] = [
            {"role": "system", "content": f"Previous conversation: {summary}"}
        ] + recent
    
    return state

session_service = InMemorySessionService()
session_service.add_compression_hook(compress_context)

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


## Key Takeaways

- **Core Strategy:** Context editing automatically manages conversation context as it grows, removing or compressing less critical content to stay within token limits and optimize costs.

- **Two Approaches:** Server-side editing (API-level clearing of tool results/thinking blocks) provides fine-grained control, while client-side compaction (SDK summarization) offers more aggressive compression.

- **Automatic Operation:** Unlike manual compression, context editing operates automatically based on configurable thresholds, enabling agents to run indefinitely without manual intervention.

- **Preserve References:** When clearing content, maintain lightweight references (file paths, URLs) that enable on-demand retrieval if needed.

- **Cache Optimization:** Preserving thinking blocks and maintaining stable prefixes improves prompt cache efficiency, reducing costs and latency.

- **Common Pitfall:** Aggressive editing that removes critical information or fails to maintain restorable references defeats the purpose. Always configure retention policies appropriately.

- **Best Practice:** Set thresholds conservatively (80-90% of max tokens) and configure retention policies (keep last N tool uses, preserve recent thinking) to prevent information loss while managing context size.

- **Cost Impact:** Effective context editing directly reduces token consumption and API costs by keeping contexts focused and within optimal ranges.

## Related Patterns

This pattern works well with:
- **Context Compression:** Context editing is a specific technique within the broader context compression strategy, focusing on automatic management rather than manual techniques.

- **External Memory (Filesystem as Context):** Cleared tool results can reference externalized content, enabling restorable compression through the filesystem pattern.

- **Memory Management:** Context editing is a key component of comprehensive memory management, complementing external memory and compression techniques.

- **Tool Result Management:** Context editing automatically manages tool results, clearing old ones while preserving recent outputs and references.

This pattern is often combined with:
- **Stable, Append-Only Context:** Context editing maintains conversation structure while clearing content, preserving KV-Cache efficiency.

- **Recitation:** Agents can recite important plans or goals into context after editing operations to maintain focus.

- **Multi-Agent Architectures:** Orchestrators use context editing to manage subagent outputs, keeping summaries while clearing detailed results.

## References

- Context Engineering for AI Agents: The Complete Guide - https://medium.com/@khanzzirfan/context-engineering-for-ai-agents-the-complete-guide-5047f84595c7
- Context Engineering Guide - https://www.promptingguide.ai/guides/context-engineering-guide
- LangGraph Middleware Documentation - https://langchain-ai.github.io/langgraph/how-tos/middleware/
- LangChain Agents Middleware - https://docs.langchain.com/oss/python/langchain/agents/middleware/
- Context Compression Techniques: Managing the Finite Window
- Memory Management: Strategies for Context Windows and External Memory

