# Pattern: Variables Manager

## Motivation

In multi-step agent workflows, intermediate results often need to be referenced across different execution stages. When an agent performs data analysis, API calls, or code execution, it generates values that subsequent steps depend on. The challenge is: how do you track these variables efficiently without overwhelming the LLM's context window with full data dumps?

Consider a data analysis agent that:

1. Fetches user data from an API (returns 10,000 records)
2. Filters the data based on criteria (produces 500 records)
3. Computes statistics on the filtered data
4. Generates a visualization
5. Creates a summary report

At each step, the agent needs to know what variables exist and their characteristics, but including the full 10,000-record dataset in every prompt would be wasteful and expensive. 
The agent needs metadata about variables without the full values consuming context tokens.

## Pattern Overview

### Problem

In multi-step agent workflows, intermediate results often need to be referenced across different execution stages. 
When an agent performs data analysis, API calls, or code execution, it generates values that subsequent steps depend on. LLMs have finite context windows, and including large intermediate values in every prompt is expensive and wasteful. 
At each step, the agent needs to know what variables exist and their characteristics, but including full data dumps (like 10,000-record datasets) in every prompt would be wasteful and expensive. Agents need metadata about variables without the full values consuming context tokens.

### Solution

The Variables Manager Pattern maintains a centralized registry of execution variables with rich metadata while providing context-efficient summaries. 
Instead of passing full values through context, agents work with variable references and retrieve full values only when needed. 
This pattern enables agents to maintain awareness of execution state through lightweight metadata summaries, retrieving full values only when explicitly needed.

This separation of metadata from values dramatically improves context efficiency while maintaining full observability. 
The pattern is particularly valuable when agents create intermediate values that need to be tracked across multiple execution steps, especially when those values are large and would consume significant context tokens if included directly. 
By providing summaries that show what exists without exposing full values, using minimal tokens, the pattern enables efficient state management across complex multi-step workflows.

### Key Concepts

- **Metadata-Rich Tracking**: Store variables with type, description, creation time, and item counts without requiring full values in context
- **Context Efficiency**: Provide summaries that show what exists without exposing full values, using minimal tokens
- **Singleton Architecture**: Single source of truth across the entire agent execution, ensuring consistent state
- **Observability**: Comprehensive logging for debugging and auditing execution flows
- **Lifecycle Management**: Smart cleanup strategies to manage memory efficiently over long executions

### How It Works

The Variables Manager Pattern operates through a structured process:

1. **Variable Registration**: When an agent creates a value (from code execution, API calls, or data processing), it registers the variable with the manager, providing an optional name and description.
2. **Metadata Extraction**: The manager automatically extracts metadata: type detection, item counts for collections, creation timestamps, and generates value previews.
3. **Summary Generation**: When agents need to understand available data, they receive lightweight summaries showing variable names, types, descriptions, and counts—not full values.
4. **On-Demand Retrieval**: Only when an agent explicitly needs to operate on data does it retrieve the full value through dedicated tool calls.
5. **Lifecycle Management**: The manager provides reset strategies (full reset, keep-last-n) to manage memory over long executions.

## When to Use This Pattern

### ✅ Use this pattern when:

- **Large intermediate values**: Values are large (>1KB) and would consume significant context tokens
- **Multi-step workflows**: Values are created in one step and used several steps later
- **Code execution agents**: Agents that write and execute code, creating variables in a programming environment
- **Multi-agent coordination**: Multiple agents need access to shared state
- **Observability required**: You need visibility into state evolution for debugging
- **Repeated value access**: Values might be reused multiple times across different prompts

### ❌ Avoid this pattern when:

- **Small, immediate values**: Values are small (<100 characters) and used immediately in the next step
- **Ephemeral data**: Values are temporary and don't need tracking
- **Simple workflows**: Overhead of variable management outweighs benefits
- **Single-step operations**: Values are created and consumed in the same operation

### Decision Guidelines

Use Variable Manager when the benefits of context efficiency and observability justify the added complexity. 
Consider value size: large values (>1KB) benefit from metadata-only summaries. 
Consider workflow length: multi-step workflows where values persist across steps benefit from tracking. 
Consider reuse: values accessed multiple times benefit from centralized management. 
However, if values are small, immediate, and ephemeral, direct state passing is simpler.

## Practical Applications & Use Cases

The Variable Manager Pattern excels in scenarios requiring multi-step data transformations and state tracking:

### Data Analysis Workflows

**Scenario**: An agent analyzes sales data through multiple transformation steps.

**Challenge**: Each step produces intermediate datasets. Without variable management, either all datasets stay in context (expensive, hits limits) or datasets are lost between steps (requires re-computation).

**Solution**: Variable Manager tracks each transformation result with metadata. The agent sees:

- `raw_sales`: 50,000 records
- `filtered_sales`: 12,000 records  
- `monthly_aggregates`: 36 records
- `trend_analysis`: dict with 5 keys

The agent can plan next steps knowing what data exists and its scale, without loading any full datasets into context.

### Code Execution Agents

**Scenario**: An agent writes and executes Python code to solve data problems.

**Challenge**: Executed code produces variables in the Python namespace. The agent needs to know what variables exist to write subsequent code that references them.

**Solution**: After each code execution, the Variable Manager captures all created variables. The agent sees what's available in the namespace and can write code like:
```python
# Agent knows filtered_data exists from previous execution
summary_stats = filtered_data.describe()
```

### API Integration Chains

**Scenario**: An agent orchestrates multiple API calls where responses feed into subsequent requests.

**Challenge**: API responses can be large JSON structures. Passing them through context for later use consumes tokens and obscures the execution flow.

**Solution**: Store each API response as a variable with a description of its purpose. The agent's context contains metadata summaries, and full values are retrieved only when needed for the next API call.

### Multi-Agent Systems

**Scenario**: Multiple specialized agents collaborate on a complex task, each producing intermediate results others need.

**Challenge**: Agents must coordinate without tightly coupling their implementations or maintaining complex message passing.

**Solution**: A shared Variable Manager acts as a communication bus. Agent A stores its results as variables with descriptive names. Agent B queries available variables and retrieves what it needs. The system maintains loose coupling while enabling coordination.

## Implementation

??? "Basic Example"

    The Variable Manager consists of two main components: `VariableMetadata` and `VariablesManager`. Here's the complete, self-contained implementation:

    ```python
    from datetime import datetime
    from typing import Any, Dict, List, Optional


    class VariableMetadata:
        """Encapsulates all metadata for a single variable."""
        
        def __init__(self, value: Any, description: Optional[str] = None, 
                    created_at: Optional[datetime] = None):
            self.value = value
            self.description = description or ""
            self.type = type(value).__name__
            self.created_at = created_at if created_at is not None else datetime.now()
            self.count_items = self._calculate_count(value)
        
        def _calculate_count(self, value: Any) -> int:
            """Calculate the count of items in the value based on its type."""
            if isinstance(value, (list, tuple, set)):
                return len(value)
            elif isinstance(value, dict):
                return len(value)
            elif isinstance(value, str):
                return len(value)
            elif hasattr(value, '__len__'):
                try:
                    return len(value)
                except Exception:
                    return 1
            else:
                return 1


    class VariablesManager(object):
        """Singleton manager for tracking execution variables with metadata."""
        
        _instance = None
        variables: Dict[str, VariableMetadata] = {}
        variable_counter: int = 0
        _creation_order: list = []
        
        def __new__(cls, *args, **kwargs):
            """Singleton pattern: ensure only one instance exists."""
            if not cls._instance:
                cls._instance = super(VariablesManager, cls).__new__(cls)
            return cls._instance
        
        def add_variable(self, value: Any, name: Optional[str] = None, 
                        description: Optional[str] = None) -> str:
            """Add a new variable with an optional name or auto-generated name."""
            if name is None:
                self.variable_counter += 1
                name = f"variable_{self.variable_counter}"
            
            self.variables[name] = VariableMetadata(value, description)
            
            # Track creation order
            if name not in self._creation_order:
                self._creation_order.append(name)
            
            return name
        
        def get_variable(self, name: str) -> Any:
            """Get a variable value by name."""
            metadata = self.variables.get(name)
            return metadata.value if metadata else None
        
        def get_variable_metadata(self, name: str) -> Optional[VariableMetadata]:
            """Get complete metadata for a variable by name."""
            return self.variables.get(name)
        
        def get_variable_names(self) -> List[str]:
            """Get all variable names."""
            return list(self.variables.keys())
        
        def get_last_n_variable_names(self, n: int) -> List[str]:
            """Get the names of the last n created variables."""
            if n <= 0:
                return []
            return self._creation_order[-n:] if len(self._creation_order) >= n else self._creation_order[:]
        
        def get_variables_summary(self, variable_names: Optional[List[str]] = None, 
                                last_n: Optional[int] = None) -> str:
            """Generate a markdown summary of variables."""
            if last_n:
                variable_names = self.get_last_n_variable_names(last_n)
            elif variable_names is None:
                variable_names = list(self.variables.keys())
            
            if last_n:
                summary_lines = [f"# Last {last_n} Variables Summary\n"]
            else:
                summary_lines = [f"# Variables Summary\n"]
            
            for name in variable_names:
                if name not in self.variables:
                    continue
                
                metadata = self.variables[name]
                preview = self._get_value_preview(metadata.value, max_length=5000)
                
                summary_lines.append(f"## {name}")
                summary_lines.append(f"- Type: {metadata.type}")
                summary_lines.append(f"- Items: {metadata.count_items}")
                summary_lines.append(f"- Description: {metadata.description}")
                summary_lines.append(f"- Created: {metadata.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                summary_lines.append(f"- Value Preview: {preview}\n")
            
            return "\n".join(summary_lines)
        
        def _get_value_preview(self, value: Any, max_length: int = 5000) -> str:
            """Get a structured preview of the value, truncating when large."""
            try:
                full_repr = repr(value)
                if len(full_repr) <= max_length:
                    return full_repr
            except Exception:
                pass
            
            # Smart truncation for large values
            if isinstance(value, (list, tuple)):
                if len(value) <= 10:
                    return repr(value)
                preview = repr(value[:10])
                return preview[:-1] + f", ... (+{len(value) - 10} more)]"
            
            if isinstance(value, dict):
                if len(value) <= 5:
                    return repr(value)
                items = list(value.items())[:5]
                preview = "{" + ", ".join(f"{k!r}: {v!r}" for k, v in items) + ", ...}"
                return preview
            
            # For strings and other types
            str_repr = str(value)
            if len(str_repr) <= max_length:
                return str_repr
            return str_repr[:max_length] + "..."
        
        def reset(self) -> None:
            """Reset the variables manager, clearing all variables."""
            self.variables = {}
            self.variable_counter = 0
            self._creation_order = []
        
        def reset_keep_last_n(self, n: int) -> None:
            """Reset the variables manager, keeping only the last 'n' added variables."""
            if n <= 0:
                self.reset()
                return
            
            variables_to_keep = {}
            original_creation_order = []
            max_variable_counter = 0
            
            # Identify the last 'n' variables
            names_to_keep = self._creation_order[-n:]
            
            for name in names_to_keep:
                if name in self.variables:
                    variables_to_keep[name] = self.variables[name]
                    original_creation_order.append(name)
                    # Update counter to avoid collisions
                    if name.startswith("variable_") and name[9:].isdigit():
                        max_variable_counter = max(max_variable_counter, int(name[9:]))
            
            # Perform the reset
            self.variables = {}
            self.variable_counter = 0
            self._creation_order = []
            
            # Re-add the kept variables
            for name in original_creation_order:
                metadata = variables_to_keep[name]
                self.variables[name] = VariableMetadata(
                    metadata.value, 
                    description=metadata.description, 
                    created_at=metadata.created_at
                )
                self._creation_order.append(name)
            
            # Set counter to prevent collisions
            self.variable_counter = max_variable_counter
    ```

**Key Design Decisions:**
- **Automatic Type Detection**: No manual type specification needed
- **Flexible Counting**: Works with any iterable type, falls back gracefully
- **Timestamp Tracking**: Automatic creation time capture
- **Singleton Architecture**: Single source of truth across the entire agent execution
- **Smart Counter Management**: Prevents collisions between auto-generated and explicit names
- **Update Semantics**: Re-adding with the same name updates the variable
- **Creation Order Tracking**: Maintains chronological order for last-n queries

### Usage Examples

??? "Adding Variables"

    ```python
    from variables_manager import VariablesManager

    vm = VariablesManager()

    # Automatic naming
    var_name = vm.add_variable([1, 2, 3, 4, 5], 
                            description="Sample data for analysis")
    print(var_name)  # Returns: "variable_1"

    # Explicit naming
    var_name = vm.add_variable({"key": "value"}, 
                            name="config_data",
                            description="Configuration loaded from file")
    print(var_name)  # Returns: "config_data"

    # Update existing variable
    vm.add_variable([1, 2, 3, 4, 5, 6], 
                name="variable_1",
                description="Updated sample data")
    # Overwrites variable_1
    ```

??? "Retrieving Variables"

    ```python
    from variables_manager import VariablesManager

    vm = VariablesManager()

    # Get the full value
    data = vm.get_variable("variable_1")
    print(data)  # Returns: [1, 2, 3, 4, 5, 6]

    # Get metadata
    metadata = vm.get_variable_metadata("variable_1")
    print(f"Type: {metadata.type}, Items: {metadata.count_items}")

    # Get all variable names
    names = vm.get_variable_names()
    print(names)  # Returns: ['variable_1', 'config_data', 'variable_2', ...]

    # Get last N variable names (most recent)
    recent = vm.get_last_n_variable_names(3)
    print(recent)  # Returns: ['variable_7', 'variable_8', 'variable_9']
    ```

??? "Summary Generation"

    The most important feature for context efficiency is summary generation:

    ```python
    from variables_manager import VariablesManager

    vm = VariablesManager()

    # Add some example variables
    vm.add_variable(
        [{'id': i, 'name': f'User{i}', 'state': 'CA'} for i in range(500)],
        name="data_filtered",
        description="Customer records meeting filter criteria"
    )

    vm.add_variable(
        {'mean': 156.4, 'median': 150.0, 'std': 12.3, 'min': 100, 'max': 200, 'count': 500},
        name="statistics",
        description="Summary statistics computed from filtered data"
    )

    # Get summary of all variables
    summary = vm.get_variables_summary()
    print(summary)

    # Get summary of specific variables
    summary = vm.get_variables_summary(
        variable_names=["data_filtered", "statistics"]
    )
    print(summary)

    # Get summary of last N variables (most useful for agents)
    summary = vm.get_variables_summary(last_n=5)
    print(summary)
    ```

**Example Output:**

```markdown
# Last 5 Variables Summary

## data_filtered
- Type: list
- Items: 500
- Description: Customer records meeting filter criteria
- Created: 2024-12-02 10:23:42
- Value Preview: [{'id': 0, 'name': 'User0', 'state': 'CA'}, ... (+490 more)]

## statistics
- Type: dict
- Items: 6
- Description: Summary statistics computed from filtered data
- Created: 2024-12-02 10:24:15
- Value Preview: {'mean': 156.4, 'median': 150.0, ...}
```

This allows agents to see the "shape" of data without consuming excessive tokens.

??? "Lifecycle Management"

    Managing the variable landscape over long executions is crucial:

    ```python
    from variables_manager import VariablesManager

    vm = VariablesManager()

    # Complete reset - useful when starting a completely new task
    vm.reset()  # Clear all variables, reset counter

    # Selective retention - keep only the most recent variables
    # Agent has created 20 variables during analysis
    # Keep only the 5 most recent (likely most relevant)
    vm.reset_keep_last_n(5)

    # Now only the last 5 variables remain
    ```

**Use Case:** In long-running analyses, the agent might accumulate many intermediate variables. Periodically calling `reset_keep_last_n(10)` maintains a sliding window of recent variables, preventing unlimited memory growth while keeping relevant state.

### Integration with Agent Tool Systems

The Variable Manager works best when integrated with agent tools. Here are complete, self-contained examples:

??? "LangChain Integration"

    ```python
    from typing import Optional, Any
    from langchain.tools import tool
    from variables_manager import VariablesManager


    @tool
    def list_available_variables(last_n: Optional[int] = None) -> str:
        """
        Get a summary of available variables with metadata.
        
        Args:
            last_n: If provided, only show the last N variables created
        
        Returns:
            Markdown-formatted summary of variables
        """
        vm = VariablesManager()
        return vm.get_variables_summary(last_n=last_n)


    @tool
    def get_variable_value(variable_name: str) -> Any:
        """
        Retrieve the full value of a variable by name.
        
        Args:
            variable_name: The name of the variable to retrieve
        
        Returns:
            The variable's value, or None if not found
        """
        vm = VariablesManager()
        return vm.get_variable(variable_name)


    @tool
    def execute_python_code(code: str) -> dict:
        """
        Execute Python code and capture created variables.
        
        Args:
            code: Python code to execute
        
        Returns:
            Dictionary with status, created variables, and summary
        """
        vm = VariablesManager()
        
        # Create execution namespace
        namespace = {}
        
        # Execute the code
        try:
            exec(code, namespace)
            status = "success"
        except Exception as e:
            status = f"error: {str(e)}"
        
        # Capture all created variables
        variables_created = []
        for name, value in namespace.items():
            if not name.startswith('_') and name not in ['__builtins__', '__name__', '__doc__']:
                vm.add_variable(
                    value, 
                    name=name,
                    description=f"Created by code execution"
                )
                variables_created.append(name)
        
        # Return summary
        return {
            "status": status,
            "variables_created": variables_created,
            "summary": vm.get_variables_summary(last_n=5)
        }


    # Example usage with an agent
    from langchain.agents import initialize_agent, AgentType
    from langchain.llms import OpenAI

    # tools = [list_available_variables, get_variable_value, execute_python_code]
    # agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    ```

??? "Custom Tool Framework Integration"

    ```python
    from typing import Optional, Any, Dict
    from variables_manager import VariablesManager


    class VariableManagerTools:
        """Wrapper class for variable manager tools in custom frameworks."""
        
        def __init__(self):
            self.vm = VariablesManager()
        
        def list_variables(self, last_n: Optional[int] = None) -> str:
            """Get a summary of available variables."""
            return self.vm.get_variables_summary(last_n=last_n)
        
        def get_variable(self, name: str) -> Any:
            """Get a variable value by name."""
            return self.vm.get_variable(name)
        
        def execute_code(self, code: str) -> Dict[str, Any]:
            """Execute Python code and capture variables."""
            namespace = {}
            try:
                exec(code, namespace)
                status = "success"
            except Exception as e:
                status = f"error: {str(e)}"
            
            variables_created = []
            for name, value in namespace.items():
                if not name.startswith('_') and name not in ['__builtins__', '__name__', '__doc__']:
                    self.vm.add_variable(value, name=name, description="Created by code execution")
                    variables_created.append(name)
            
            return {
                "status": status,
                "variables_created": variables_created,
                "summary": self.vm.get_variables_summary(last_n=5)
            }


    # Usage example
    tools = VariableManagerTools()

    # Agent can call:
    summary = tools.list_variables(last_n=5)
    value = tools.get_variable("data_filtered")
    result = tools.execute_code("x = [1, 2, 3, 4, 5]\ny = sum(x)")
    ```

This integration allows agents to discover, inspect, and use variables naturally through their tool-calling mechanisms.

## Key Takeaways

- **Context Efficiency**: The Variable Manager Pattern separates metadata from values, enabling agents to maintain awareness of execution state through lightweight summaries rather than expensive full-value inclusion.
- **Singleton Architecture**: A single instance ensures consistent state across the entire agent execution, preventing synchronization issues.
- **On-Demand Retrieval**: Full values are retrieved only when explicitly needed, not included in every prompt.
- **Lifecycle Management**: Smart reset strategies (full reset, keep-last-n) manage memory efficiently over long executions.
- **Tool Integration**: Variable Manager works best when integrated with agent tools, allowing natural discovery and retrieval through tool calls.
- **When to Use**: Apply this pattern for multi-step workflows with large intermediate values, code execution agents, and multi-agent systems requiring shared state.

## Related Patterns

This pattern works well with:

- **Code Execution Agents** - Variable Manager is essential for tracking variables created during code execution
- **Multi-Agent Systems** - Shared Variable Manager enables loose coupling and coordination between agents
- **Memory Management** - Variable Manager complements session state and external memory by managing execution-level state
- **Tool Use** - Variable Manager integrates naturally with agent tools for discovery and retrieval

This pattern differs from:

- **Session State (Memory Management)** - Session state manages conversation-level context; Variable Manager tracks execution-level computation results
- **Filesystem as Context / RAG** - Filesystem as Context provides semantic search over documents; Variable Manager provides exact-name lookup for execution variables
- **Persistent Task Lists (Recitation)** - Recitation tracks tasks; Variable Manager tracks data values

??? "References"

    - LangChain State Management: https://python.langchain.com/docs/modules/memory/
    - LangGraph State Management: https://langchain-ai.github.io/langgraph/concepts/low_level/#state-management
    - Google ADK State Management: https://google.github.io/adk-docs/state/
