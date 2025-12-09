# Pattern: Filesystem as Context

## Motivation

Humans don't store everything in working memory. We use notebooks, calendars, reference books, and digital files as external memory. When needed, we retrieve relevant information. We can't remember every detail, but we know where to find it. The Filesystem as Context pattern gives agents this capability: treating persistent storage as unlimited memory, retrieving information just-in-time rather than trying to keep everything in the limited context window.


> **"Memory is not storage; it is context selection over time."** — LangChain

## Pattern Overview
**What it is:** A mechanism to treat an external persistent memory (like a filesystem or database) as an unlimited extension of the agent's working memory.

**When to use:** When the agent needs to handle large data or unstructured observations (like web pages or PDF text) that would exceed context length limits. Also used for long-horizon tasks that require persistent, restorable information retention.

**Why it matters:** It helps mitigate the fundamental constraint of the LLM's finite context window. It reduces token costs and latency by allowing the agent to retrieve only the relevant information when needed.

The Filesystem as Context pattern addresses one of the most fundamental constraints in LLM-based agent systems: the finite context window. As agents process complex tasks, they encounter large data sources—web search results, PDF documents, codebases, or extensive research findings—that would quickly exhaust the available context tokens. Simply truncating or summarizing this data risks losing critical information, while including everything inflates costs and can degrade performance due to attention dilution.

This pattern treats external storage (filesystem, databases, or other persistent stores) as an unlimited extension of the agent's working memory. Instead of keeping all data in the immediate context, the agent offloads large content to external storage and retains only lightweight references (file paths, URLs, or database keys). When specific information is needed, the agent performs targeted retrieval, pulling only the relevant portions back into context.

The pattern is particularly powerful because it enables restorable compression: the agent can drop large content from context while maintaining the ability to retrieve it precisely when needed. This creates a "just-in-time" information architecture where context remains focused and efficient, while the agent retains access to an unlimited knowledge base.

### Key Concepts
- **Externalized Memory:** Large data stored outside the context window in persistent storage (filesystem, database, etc.).
- **Scratchpad Memory Pattern:** Using temporary files or workspaces as intermediate storage for agent computations and observations.
- **Restorable Compression:** Dropping large content from context while retaining a reference (path, URL, key) that allows precise retrieval later.
- **Just-in-Time Retrieval:** Selectively reading only relevant portions of stored data when needed, rather than loading everything upfront.
- **Context Engineering:** Strategic management of what information appears in the context window to optimize performance and cost.

### How It Works: Step-by-step Explanation

1. **Offload Large Data:** The agent writes intermediate results, notes, or large data (such as a 10K token web search result) to an external persistent file (a scratch file) instead of keeping it in the immediate conversation context.

2. **Retain Reference:** The compression strategy is always *restorable*—the agent drops the large content but retains a lightweight reference, such as the file path or URL, so it can be reloaded on demand.

3. **Just-in-Time Retrieval:** When necessary for a subsequent step, the agent selectively reads only the relevant portions of the stored data. This can be done using dedicated tools like `grep` or `read_file` to pull in only what is needed.

4. **Inject Context:** The small, relevant snippets are injected into the agent's next prompt, ensuring the context is focused and concise, thereby preventing the context window from being flooded.

## Relationship to Context Compression

Filesystem as Context is the **primary externalization technique** within the broader Context Compression strategy. Understanding this relationship helps clarify how it fits into comprehensive context management.

### Filesystem as Context as Externalization Component

**Filesystem as Context** is the **externalization component** of Context Compression. It's the most powerful compression strategy because:
- It enables unlimited storage beyond context limits
- It provides restorable compression (maintains references for retrieval)
- It supports just-in-time retrieval of only relevant portions
- It's the first step in a layered compression approach

**Note:** This pattern is the externalization component of Context Compression. The typical workflow is: first externalize large data (Filesystem as Context), then compress what remains in context (summarization/pruning via Context Compression).

### How It Works with Context Compression

**Layered Compression Strategy:**
1. **First:** Externalize large data using Filesystem as Context (offload to persistent storage)
2. **Then:** Compress what remains in context using Context Compression techniques (summarization, pruning)
3. **Result:** Maximum compression with unlimited external storage

**Example:** An agent processing research papers might:
- Use Filesystem as Context to write paper contents to files, keeping only file paths in context
- Use Context Compression to summarize conversation history
- Retrieve specific sections on-demand using targeted tools

### How It Works with Context Editing

**Automatic Management with External Storage:**
- Externalize large tool results first using Filesystem as Context
- Let Context Editing automatically clear old tool result references when context grows
- Maintain references to externalized files for restorable compression

**Example:** An agent with many tool calls might:
- Write large tool results to files using Filesystem as Context
- Keep only file paths in context
- Let Context Editing automatically clear old tool result references
- Retrieve specific results on-demand using file paths

This combination provides automatic context management while maintaining restorable compression through external storage references.

## When to Use This Pattern

### ✅ Use when:
- Building long-horizon agents that must sustain goals without losing information.
- Dealing with large inputs (web search, PDFs) that would exceed context limits.
- Implementing complex systems where large amounts of necessary context must be available on demand (e.g., codebases or documentation).
- The agent needs to process multiple large documents or datasets that cannot fit simultaneously in context.
- Working with dynamic data that changes over time and needs to be stored and retrieved across sessions.

### ❌ Avoid when:
- The task is single-turn or simple, as the overhead of file management is unnecessary.
- The application requires only a small, static set of knowledge accessible via standard RAG techniques.
- All necessary information fits comfortably within the context window without performance degradation.
- The retrieval overhead (file I/O, database queries) would introduce unacceptable latency for real-time applications.

### Decision Guidelines
This pattern is a crucial context engineering strategy, particularly for multi-step agentic systems, as it makes the retrieved context as small a subset of the needed information as possible. The filesystem effectively acts as a single, flexible interface for the agent to store, retrieve, and update an infinite amount of context. Consider: the size of your data (large = external memory), the retrieval pattern (targeted = filesystem tools, semantic = RAG), and the persistence requirement (session = temporary files, cross-session = persistent storage). Always ensure references are maintained so data remains restorable.

## Practical Applications & Use Cases

The Filesystem as Context pattern is essential for agents that work with large datasets, complex codebases, or extensive research materials.

- **Manus AI:** Uses the filesystem as "structured, externalized memory" to store and retrieve information across agent steps.

- **Planning Persistence:** The agent writes its long-horizon plan (e.g., a `todo.md` file) to the filesystem, allowing it to recite this plan back into the context later to remind itself of its objectives. Anthropic's research agent saves its plan to memory before spawning subagents.

- **Subagent Collaboration:** Subagents write their research findings and knowledge directly to the filesystem, and only pass lightweight references to the main coordinator, minimizing token overhead and avoiding the "game of telephone."

- **Code Agents:** Agent systems, such as those in Deep Agents, are equipped with filesystem tools like `read_file`, `write_file`, `ls`, and `edit_file` to navigate and manipulate codebases that exceed context limits.

- **Skill Management:** Instructions and skills can be stored as files, which the agent can dynamically read as needed, rather than stuffing all instructions into the system prompt.

- **Research Agents:** Agents conducting literature reviews or web research offload search results and articles to files, then retrieve specific sections when synthesizing findings.

- **Document Processing:** Agents processing large PDFs or documents save extracted content to files, then query specific sections when answering questions.

## Implementation

### Prerequisites
```bash
pip install langchain langchain-openai
# or
pip install google-adk
# or
pip install deepagents
```

### Basic Example: Offloading and Retrieval

This example demonstrates the scratchpad memory pattern, where a large web search observation is offloaded to a file, and only relevant parts are retrieved later:

```python
from pathlib import Path
from typing import Dict, List
import json

class ExternalMemoryAgent:
    def __init__(self, workspace_dir: str = "./workspace"):
        self.workspace = Path(workspace_dir)
        self.workspace.mkdir(exist_ok=True)
        self.memory_index = {}  # Maps keys to file paths
    
    def offload_to_memory(self, content: str, key: str, metadata: Dict = None) -> str:
        """Offload large content to external memory and return reference."""
        filepath = self.workspace / f"{key}.txt"
        filepath.write_text(content)
        
        # Store metadata for retrieval
        self.memory_index[key] = {
            "path": str(filepath),
            "metadata": metadata or {},
            "size": len(content)
        }
        
        # Return lightweight reference
        return f"Content stored in memory: {key} ({len(content)} chars). Use retrieve_memory('{key}') to access."
    
    def retrieve_memory(self, key: str, query: str = None, max_lines: int = 50) -> str:
        """Retrieve from external memory, optionally with targeted search."""
        if key not in self.memory_index:
            return f"Memory key '{key}' not found."
        
        filepath = Path(self.memory_index[key]["path"])
        if not filepath.exists():
            return f"Memory file for '{key}' not found."
        
        content = filepath.read_text()
        
        # If query provided, search for relevant lines
        if query:
            lines = content.split('\n')
            relevant_lines = [
                line for line in lines 
                if query.lower() in line.lower()
            ][:max_lines]
            return '\n'.join(relevant_lines)
        
        # Return first portion if no query
        return content[:2000]  # First 2000 chars
    
    def list_memory(self) -> List[str]:
        """List all available memory keys."""
        return list(self.memory_index.keys())

# Usage
agent = ExternalMemoryAgent()

# Offload large web search result
large_result = "..." # 10K token web search result
reference = agent.offload_to_memory(
    large_result, 
    key="web_search_agentic_patterns",
    metadata={"source": "web_search", "query": "agentic AI design patterns"}
)

# Later, retrieve only relevant parts
relevant = agent.retrieve_memory(
    "web_search_agentic_patterns",
    query="recitation pattern",
    max_lines=20
)
# Inject 'relevant' into next prompt instead of full 10K token result
```

**Explanation:**
This example demonstrates the core pattern: offloading large content to external storage, maintaining a reference, and performing targeted retrieval. The agent can store unlimited data externally while keeping context focused and efficient.

### Advanced Example: Filesystem Tools with Targeted Reading

```python
from pathlib import Path
from typing import Optional, List
import re

class FilesystemMemoryTools:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.workspace.mkdir(exist_ok=True)
    
    def write_file(self, filepath: str, content: str) -> str:
        """Write content to file in workspace."""
        full_path = self.workspace / filepath
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        return f"Written {len(content)} characters to {filepath}"
    
    def read_file(self, filepath: str, start_line: int = 1, end_line: Optional[int] = None) -> str:
        """Read file with optional line range for targeted retrieval."""
        full_path = self.workspace / filepath
        if not full_path.exists():
            return f"File {filepath} not found."
        
        lines = full_path.read_text().split('\n')
        
        # Adjust for 0-based indexing
        start_idx = max(0, start_line - 1)
        end_idx = end_line if end_line else len(lines)
        
        selected_lines = lines[start_idx:end_idx]
        return '\n'.join(selected_lines)
    
    def grep_file(self, filepath: str, pattern: str, max_matches: int = 10) -> str:
        """Search file for pattern and return matching lines with context."""
        full_path = self.workspace / filepath
        if not full_path.exists():
            return f"File {filepath} not found."
        
        content = full_path.read_text()
        lines = content.split('\n')
        
        matches = []
        for i, line in enumerate(lines):
            if re.search(pattern, line, re.IGNORECASE):
                # Include line number and context
                context_start = max(0, i - 1)
                context_end = min(len(lines), i + 2)
                context = '\n'.join(lines[context_start:context_end])
                matches.append(f"Line {i+1}:\n{context}")
                if len(matches) >= max_matches:
                    break
        
        return '\n'.join(matches) if matches else f"No matches found for pattern: {pattern}"
    
    def list_files(self, directory: str = ".") -> str:
        """List files in directory."""
        dir_path = self.workspace / directory
        if not dir_path.exists():
            return f"Directory {directory} not found."
        
        files = [f.name for f in dir_path.iterdir() if f.is_file()]
        dirs = [f.name + "/" for f in dir_path.iterdir() if f.is_dir()]
        return '\n'.join(sorted(dirs + files))

# Usage with agent
workspace = Path("./agent_workspace")
fs_tools = FilesystemMemoryTools(workspace)

# Agent offloads large PDF text
pdf_content = "..." # Large extracted PDF text
fs_tools.write_file("research_paper.pdf.txt", pdf_content)

# Later, agent searches for specific information
relevant_section = fs_tools.grep_file(
    "research_paper.pdf.txt",
    pattern="recitation|external memory",
    max_matches=5
)

# Agent uses only the relevant section in context
```

**Explanation:**
This advanced example provides filesystem tools with targeted reading capabilities. The `read_file` tool supports line ranges, and `grep_file` enables semantic search within stored files. This allows agents to retrieve precisely what they need without loading entire files into context.

### Framework-Specific Examples

#### Deep Agents: Built-in Filesystem Tools
```python
# Deep Agents includes built-in filesystem tools with detailed specifications

def read_file_tool(filepath: str, start_line: int = 1, num_lines: int = 2000) -> str:
    """
    Read a file from the workspace.
    
    Args:
        filepath: Path to file relative to workspace
        start_line: Line number to start reading from (1-indexed)
        num_lines: Maximum number of lines to read (default: 2000)
    
    Returns:
        File content within specified line range
    """
    # Implementation reads up to 2000 lines by default
    # but allows specifying line offsets and limits
    pass

def write_file_tool(filepath: str, content: str) -> str:
    """Write content to file in workspace."""
    pass

def list_files_tool(directory: str = ".") -> str:
    """List files and directories in workspace."""
    pass

# Agent uses these tools to manage external memory
# Large observations are written to files, then read selectively
```

#### LangGraph: Filesystem State Management
```python
from langgraph.graph import StateGraph
from typing import TypedDict, Annotated
import operator
from pathlib import Path

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    scratchpad_files: dict  # Maps keys to file paths
    workspace: str

def offload_to_scratchpad(state: AgentState, content: str, key: str) -> AgentState:
    """Offload content to scratchpad file."""
    workspace = Path(state["workspace"])
    workspace.mkdir(exist_ok=True)
    
    filepath = workspace / f"{key}.txt"
    filepath.write_text(content)
    
    state["scratchpad_files"][key] = str(filepath)
    return state

def retrieve_from_scratchpad(state: AgentState, key: str, query: str = None) -> AgentState:
    """Retrieve from scratchpad with optional filtering."""
    if key not in state["scratchpad_files"]:
        return state
    
    filepath = Path(state["scratchpad_files"][key])
    content = filepath.read_text()
    
    # If query, filter content
    if query:
        lines = [line for line in content.split('\n') if query.lower() in line.lower()]
        content = '\n'.join(lines[:50])  # Top 50 matches
    
    # Inject into messages
    state["messages"].append({
        "role": "system",
        "content": f"Retrieved from {key}:\n\n{content[:2000]}"
    })
    
    return state

# Graph with external memory management
workflow = StateGraph(AgentState)
workflow.add_node("offload", offload_to_scratchpad)
workflow.add_node("retrieve", retrieve_from_scratchpad)
# ... rest of workflow
```

#### Google ADK: External Storage Integration
```python
from google.adk.agents import LlmAgent
from google.adk.tools import Tool
from pathlib import Path

def read_file_tool(filepath: str, start_line: int = 1, end_line: int = None) -> str:
    """Read file with line range support."""
    path = Path(filepath)
    if not path.exists():
        return f"File {filepath} not found."
    
    lines = path.read_text().split('\n')
    start_idx = max(0, start_line - 1)
    end_idx = end_line if end_line else len(lines)
    
    return '\n'.join(lines[start_idx:end_idx])

def write_file_tool(filepath: str, content: str) -> str:
    """Write content to file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return f"Written {len(content)} characters to {filepath}"

# Agent with filesystem tools
agent = LlmAgent(
    name="ExternalMemoryAgent",
    model="gemini-2.0-flash",
    instruction="""You have access to filesystem tools for managing external memory.
    
    When you receive large data (web search results, documents, etc.):
    1. Use write_file to save it to external storage
    2. Keep only a reference in your response
    3. Use read_file with line ranges to retrieve specific parts when needed
    
    This keeps your context focused and efficient.""",
    tools=[read_file_tool, write_file_tool]
)
```

## Key Takeaways

- **Core Function:** External memory provides persistent, unlimited storage, preventing context window limits from being hit by offloading large data.

- **Efficiency Principle:** Retrieval should be focused (Just-in-Time Retrieval), ensuring the agent injects only necessary snippets into the prompt to reduce token costs and latency.

- **Persistence Requirement:** The agent must maintain a reference (like a file path or URL) to ensure the dropped information remains restorable.

- **Context Quality:** Context engineering, which includes leveraging external memory, is essential because an agent's ability to reason is entirely dependent on the quality of its context.

- **Best Practice:** Design tools with targeted retrieval capabilities (line ranges, search functions) to enable precise information extraction without loading entire files.

- **Common Pitfall:** Failing to maintain references to offloaded data makes it irretrievable, defeating the purpose of external memory. Always ensure references are preserved in agent state or context.

## Related Patterns

This pattern works well with:
- **Context Compression:** Filesystem as Context is the primary externalization technique within Context Compression. **Combination workflow:** First externalize large data (Filesystem as Context), then compress what remains in context (Context Compression summarization/pruning).

- **Context Editing:** Externalize large tool results first using Filesystem as Context, then let Context Editing automatically clear old tool result references. The cleared references point to externalized files, maintaining restorable compression.

- **Persistent Task List (Recitation):** The persistent plan is often stored in the external filesystem (`todo.md`) to enable its continuous recitation into the context.

- **Stable, Append-Only Context:** Offloading large data helps maintain a stable context prefix, which is crucial for maximizing KV-cache reuse and reducing cost.

- **Memory Management:** Filesystem as Context is a key component of comprehensive memory management strategies, specifically for implementing long-term memory (persistent storage). It complements context window management (Context Compression/Editing) and other memory techniques.

This pattern is often combined with:
- **Tool Result Management (Retrieve-then-Read):** This structure is implemented by using filesystem tools that allow targeted reading (e.g., specifying a line range) after the initial large data has been stored.

- **Knowledge Retrieval (RAG):** Filesystem as Context stores documents for targeted retrieval, while RAG provides semantic search capabilities over the stored content. Use Filesystem as Context for exact file/line access, RAG for semantic search.

- **Multi-Agent Architectures:** Subagents write findings to shared external memory, and the orchestrator retrieves only relevant portions when synthesizing results.

??? "References"

- Agentic AI System Design Patterns
- Context Engineering for AI Agents: Lessons from Building Manus
- Deep Agents: Filesystem Tools Documentation
- LangGraph State Management: https://langchain-ai.github.io/langgraph/
- Google ADK Tools: https://google.github.io/adk-docs/tools/
- How agents can use filesystems for context engineering

