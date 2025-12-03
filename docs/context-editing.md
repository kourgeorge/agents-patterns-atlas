# Context Editing: Automatic Context Management

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
pip install anthropic  # For Claude API with context editing
# or
pip install langchain langchain-anthropic
# or
pip install google-adk
```

### Basic Example: Server-Side Tool Result Clearing

This example demonstrates server-side context editing using Claude's API to automatically clear tool results:

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# Enable context editing with tool result clearing
response = client.beta.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Search for recent developments in AI agents"
        }
    ],
    tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search"
        }
    ],
    betas=["context-management-2025-06-27"],
    context_management={
        "edits": [
            {
                "type": "clear_tool_uses_20250919",
                "trigger": {
                    "type": "input_tokens",
                    "value": 30000  # Trigger when context exceeds 30K tokens
                },
                "keep": {
                    "type": "tool_uses",
                    "value": 3  # Keep last 3 tool uses
                }
            }
        ]
    }
)
```

**Explanation:**
This example enables automatic tool result clearing when input tokens exceed 30,000. The API will automatically remove older tool results, keeping only the last 3 tool uses, while preserving conversation structure and allowing the agent to continue normally.

### Advanced Example: Configurable Context Editing

This example demonstrates advanced configuration with multiple editing strategies:

```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

response = client.beta.messages.create(
    model="claude-opus-4-5",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": "Create a comprehensive research report on AI safety"
        }
    ],
    tools=[
        {
            "type": "web_search_20250305",
            "name": "web_search"
        },
        {
            "type": "text_editor_20250728",
            "name": "text_editor",
            "max_characters": 10000
        }
    ],
    betas=["context-management-2025-06-27"],
    context_management={
        "edits": [
            {
                "type": "clear_tool_uses_20250919",
                "trigger": {
                    "type": "input_tokens",
                    "value": 50000
                },
                "keep": {
                    "type": "tool_uses",
                    "value": 5  # Keep last 5 tool uses
                },
                "clear_at_least": {
                    "type": "input_tokens",
                    "value": 10000  # Clear at least 10K tokens each time
                },
                "clear_tool_inputs": True,  # Also clear tool call parameters
                "exclude_tools": ["web_search"]  # Never clear web search results
            },
            {
                "type": "clear_thinking_20251015",
                "trigger": {
                    "type": "input_tokens",
                    "value": 60000
                },
                "keep": {
                    "type": "thinking_turns",
                    "value": 2  # Keep thinking from last 2 assistant turns
                }
            }
        ]
    }
)
```

**Explanation:**
This advanced configuration uses two editing strategies:
1. **Tool Result Clearing:** Triggers at 50K tokens, keeps last 5 tool uses, clears at least 10K tokens, also clears tool inputs, but never clears web search results.
2. **Thinking Block Clearing:** Triggers at 60K tokens, keeps thinking from last 2 assistant turns. This preserves prompt cache efficiency while managing context size.

### Client-Side Compaction Example

This example demonstrates client-side compaction using the Anthropic SDK's tool runner:

```python
from anthropic import Anthropic
from anthropic.lib.tools import ToolRunner

client = Anthropic(api_key="your-api-key")

# Create tool runner with compaction enabled
tool_runner = ToolRunner(
    client=client,
    model="claude-sonnet-4-5",
    compaction_control={
        "enabled": True,
        "context_token_threshold": 100000,  # Trigger at 100K tokens
        "model": "claude-haiku-4-5"  # Use cheaper model for summaries
    }
)

# Long-running agent task
messages = [
    {
        "role": "user",
        "content": "Analyze all files in the codebase and create a comprehensive refactoring plan"
    }
]

# As the agent processes files, context grows
# When threshold is reached, SDK automatically:
# 1. Generates a structured summary
# 2. Replaces conversation history with summary
# 3. Agent continues from summary

result = tool_runner.run(messages=messages)
```

**Explanation:**
The SDK automatically monitors token usage. When it exceeds 100,000 tokens, it generates a structured continuation summary using a cheaper model (Haiku), replaces the full history with the summary, and the agent continues seamlessly from the compressed state.

### Custom Compaction Summary Prompt

This example shows how to customize the summary prompt for domain-specific needs:

```python
from anthropic import Anthropic
from anthropic.lib.tools import ToolRunner

client = Anthropic(api_key="your-api-key")

tool_runner = ToolRunner(
    client=client,
    model="claude-sonnet-4-5",
    compaction_control={
        "enabled": True,
        "context_token_threshold": 100000,
        "summary_prompt": """Summarize the research conducted so far, including:
- Sources consulted and key findings
- Questions answered and remaining unknowns
- Recommended next steps
- Technical constraints discovered

Wrap your summary in <summary></summary> tags."""
    }
)
```

**Explanation:**
Custom summary prompts allow you to tailor compaction summaries to your domain. The prompt should instruct the model to wrap the summary in `<summary></summary>` tags for proper parsing.

### Framework-Specific Examples

#### LangChain: Context Editing Middleware

```python
from langchain_anthropic import ChatAnthropic
from langchain.middleware import ContextEditingMiddleware
from langchain.chains import ConversationChain

llm = ChatAnthropic(
    model="claude-sonnet-4-5",
    anthropic_api_key="your-api-key"
)

# Create context editing middleware
context_editor = ContextEditingMiddleware(
    tool_result_clearing={
        "enabled": True,
        "threshold": 30000,
        "keep_last_n": 3
    },
    thinking_block_clearing={
        "enabled": True,
        "threshold": 50000,
        "keep_turns": 2
    }
)

# Apply middleware to chain
chain = ConversationChain(
    llm=llm,
    middleware=[context_editor],
    verbose=True
)

# Long conversation automatically managed
response = chain.invoke({"input": "Research AI safety"})
# ... many tool calls later ...
response = chain.invoke({"input": "What did we find?"})
# Old tool results automatically cleared
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

#### Custom Context Editor

```python
from typing import List, Dict
import tiktoken

class ContextEditor:
    def __init__(self, max_tokens: int = 100000, keep_recent: int = 20):
        self.max_tokens = max_tokens
        self.keep_recent = keep_recent
        self.encoding = tiktoken.encoding_for_model("gpt-4")
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))
    
    def clear_tool_results(self, messages: List[Dict], threshold: int = 30000) -> List[Dict]:
        """Clear old tool results when threshold exceeded."""
        total_tokens = sum(
            self.count_tokens(str(msg.get("content", "")))
            for msg in messages
        )
        
        if total_tokens < threshold:
            return messages
        
        # Find tool result messages
        tool_results = [
            (i, msg) for i, msg in enumerate(messages)
            if isinstance(msg.get("content"), list) and any(
                item.get("type") == "tool_result"
                for item in msg.get("content", [])
            )
        ]
        
        # Keep recent tool results, clear old ones
        if len(tool_results) > self.keep_recent:
            to_clear = tool_results[:-self.keep_recent]
            
            for idx, msg in to_clear:
                # Replace tool results with placeholder
                if isinstance(messages[idx].get("content"), list):
                    messages[idx]["content"] = [
                        item if item.get("type") != "tool_result"
                        else {"type": "tool_result", "content": "[Tool result cleared]"}
                        for item in messages[idx]["content"]
                    ]
        
        return messages
    
    def edit_context(self, messages: List[Dict]) -> List[Dict]:
        """Apply context editing strategies."""
        # Clear old tool results
        messages = self.clear_tool_results(messages, threshold=self.max_tokens * 0.8)
        
        return messages

# Usage
editor = ContextEditor(max_tokens=100000, keep_recent=20)
edited_messages = editor.edit_context(conversation_messages)
```

**Explanation:**
This custom implementation demonstrates how to build context editing logic that clears old tool results while preserving recent ones, maintaining conversation continuity while managing context size.

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
- Anthropic Context Editing Documentation - https://platform.claude.com/docs/en/build-with-claude/context-editing
- Context Engineering Guide - https://www.promptingguide.ai/guides/context-engineering-guide
- LangChain Context Editing Middleware - https://docs.langchain.com/oss/python/langchain/middleware/built-in#context-editing
- Context Compression Techniques: Managing the Finite Window
- Memory Management: Strategies for Context Windows and External Memory

