# Pattern: Variables Manager

## Introduction

In multi-step agent workflows, intermediate results often need to be referenced across different execution stages. When an agent performs data analysis, API calls, or code execution, it generates values that subsequent steps depend on. The challenge is: how do you track these variables efficiently without overwhelming the LLM's context window with full data dumps?

Consider a data analysis agent that:
1. Fetches user data from an API (returns 10,000 records)
2. Filters the data based on criteria (produces 500 records)
3. Computes statistics on the filtered data
4. Generates a visualization
5. Creates a summary report

At each step, the agent needs to know what variables exist and their characteristics, but including the full 10,000-record dataset in every prompt would be wasteful and expensive. The agent needs metadata about variables without the full values consuming context tokens.

The **Variable Manager Pattern** solves this by maintaining a centralized registry of execution variables with rich metadata while providing context-efficient summaries. Instead of passing full values through context, agents work with variable references and retrieve full values only when needed.

**Core Capabilities:**
- **Metadata-Rich Tracking**: Store variables with type, description, creation time, and item counts
- **Context Efficiency**: Provide summaries that show what exists without exposing full values
- **Singleton Architecture**: Single source of truth across the entire agent execution
- **Observability**: Comprehensive logging for debugging and auditing
- **Lifecycle Management**: Smart cleanup strategies to manage memory efficiently

This pattern is particularly valuable in code execution agents, data analysis workflows, and multi-agent systems where intermediate state must be shared and tracked.

## The Variable Manager Pattern Explained

The Variable Manager Pattern implements a sophisticated variable tracking system that separates variable metadata from variable values. This separation enables agents to maintain awareness of execution state without paying the token cost of including full values in context.

### Key Components

#### Metadata-Rich Tracking

Every variable is stored with comprehensive metadata:

**Type Information**: Automatic type detection (string, list, dict, DataFrame, etc.) allows agents to understand data structure without inspecting content.

**Descriptive Labels**: Human-readable descriptions explain what each variable represents, making it easy for agents to select the right data.

**Creation Timestamps**: Track when variables were created to understand execution flow and identify stale data.

**Item Counts**: For collections (lists, dicts, DataFrames), store the number of items to assess data volume without loading content.

**Value Previews**: Smart truncation shows the first N characters or items, giving agents a glimpse without full exposure.

This metadata enables agents to answer questions like "What variables are available?" or "How large is the dataset?" without retrieving any full values.

#### Context Efficiency: Summaries vs Full Values

The pattern's primary optimization is the distinction between summaries and full values:

**Summaries for Planning**: When agents need to understand available data, they receive lightweight summaries showing variable names, types, descriptions, and counts. This uses minimal tokens.

**Full Values for Execution**: Only when an agent explicitly needs to operate on data does it retrieve the full value. This happens through dedicated tool calls, not context inclusion.

**Last-N Filtering**: Focus summaries on recently created variables, as these are typically most relevant to current execution steps.

Example summary format:
```
# Variables Summary

## customer_data
- Type: DataFrame
- Items: 10000
- Description: Raw customer records from API
- Created: 2024-12-02 10:23:15
- Value Preview: {'id': 1, 'name': 'John', ...} (showing 3 of 10000 items)

## filtered_customers
- Type: DataFrame  
- Items: 500
- Description: Customers in California with orders > 100
- Created: 2024-12-02 10:23:42
- Value Preview: {'id': 45, 'name': 'Alice', ...} (showing 3 of 500 items)
```

This summary uses ~200 tokens versus the ~50,000 tokens the full datasets would consume.

#### Singleton Architecture

The Variable Manager follows the Singleton pattern, ensuring exactly one instance exists across the entire agent execution:

**Global State**: All parts of the agent system reference the same variable registry, eliminating synchronization issues.

**Consistent Naming**: Auto-generated names (`variable_1`, `variable_2`, etc.) never collide because a single counter manages them.

**Shared Access**: Multiple agents or execution threads can coordinate by reading from and writing to the shared registry.

#### Thread Safety

While the basic pattern uses a singleton, production implementations should consider thread safety:

**Atomic Operations**: Variable creation and updates should be atomic to prevent race conditions.

**Lock-Free Reads**: Metadata queries can be lock-free since they're read-only operations.

**Careful Write Ordering**: When agents execute in parallel, ensure variable updates maintain consistency.

### Observability: Logging and Audit Trails

A key feature often overlooked in state management is observability. The Variable Manager Pattern includes comprehensive logging:

**Operation Logs**: Every variable creation, update, and deletion is logged with timestamps and caller information.

**Stack Traces**: Capture where in the code each operation originated, making debugging easier.

**Markdown Format**: Logs are human-readable markdown files, perfect for reviewing execution flows.

**Session Tracking**: Each execution session gets its own log file, allowing historical analysis.

Example log entry:
```markdown
## ➕ Variable Added

- **Time:** 10:23:42.156
- **Caller:** `code_agent.py:execute:127`
- **Details:** **filtered_customers** = `DataFrame` (250000 chars)

### Variable Info
- **Name:** `filtered_customers` (auto-generated)
- **Type:** `DataFrame`
- **Description:** Customers meeting filter criteria
- **Value Preview:**
```python
    id  name          state  orders
0   45  Alice Jones   CA     150
1   67  Bob Smith     CA     200
...
```

### Current State
- **Total Variables:** 5
- **Variable Counter:** 5
- **All Variables:** `customer_data`, `filter_params`, `filtered_customers`, `statistics`, `chart_config`

---
```

This observability is invaluable when debugging complex agent executions.

## Practical Applications & Use Cases

The Variable Manager Pattern excels in scenarios requiring multi-step data transformations and state tracking:

### Data Analysis Workflows

**Scenario**: An agent analyzes sales data through multiple transformation steps.

**Challenge**: Each step produces intermediate datasets. Without variable management, either:
- All datasets stay in context (expensive, hits limits)
- Datasets are lost between steps (requires re-computation)

**Solution**: Variable Manager tracks each transformation result with metadata. The agent sees:
- `raw_sales`: 50,000 records
- `filtered_sales`: 12,000 records  
- `monthly_aggregates`: 36 records
- `trend_analysis`: dict with 5 keys

The agent can plan next steps knowing what data exists and its scale, without loading any full datasets into context.

### API Integration Chains

**Scenario**: An agent orchestrates multiple API calls where responses feed into subsequent requests.

**Challenge**: API responses can be large JSON structures. Passing them through context for later use consumes tokens and obscures the execution flow.

**Solution**: Store each API response as a variable with a description of its purpose. The agent's context contains:
```
## api_response_1
- Type: dict
- Items: 45 keys
- Description: User profile data from /api/users/123
- Value Preview: {'id': 123, 'name': 'John Doe', ...}
```

When the agent needs specific fields for the next API call, it retrieves them with explicit tool calls rather than searching through context.

### Code Execution Agents

**Scenario**: An agent writes and executes Python code to solve data problems.

**Challenge**: Executed code produces variables in the Python namespace. The agent needs to know what variables exist to write subsequent code that references them.

**Solution**: After each code execution, the Variable Manager captures all created variables. The agent sees what's available in the namespace and can write code like:
```python
# Agent knows filtered_data exists from previous execution
summary_stats = filtered_data.describe()
```

This is exactly how the CUGA (Code Understanding and Generation Agent) system operates.

### Multi-Agent Systems

**Scenario**: Multiple specialized agents collaborate on a complex task, each producing intermediate results others need.

**Challenge**: Agents must coordinate without tightly coupling their implementations or maintaining complex message passing.

**Solution**: A shared Variable Manager acts as a communication bus. Agent A stores its results as variables with descriptive names. Agent B queries available variables and retrieves what it needs. The system maintains loose coupling while enabling coordination.

### Debugging and Auditing

**Scenario**: An agent execution fails or produces unexpected results.

**Challenge**: Understanding what happened requires visibility into the execution flow and intermediate states.

**Solution**: The Variable Manager's markdown logs provide a complete audit trail:
- What variables were created and when
- What values they contained (via previews)
- Which code paths created them (via stack traces)
- How the variable landscape evolved over time

This turns debugging from guesswork into systematic analysis.

## Hands-On Code: Variable Manager in CUGA

The CUGA (Code Understanding and Generation Agent) system implements a production-quality Variable Manager. Let's explore its implementation to understand the pattern in practice.

### Core Architecture

The CUGA Variable Manager consists of two main classes: `VariableMetadata` and `VariablesManager`.

#### VariableMetadata Class

This class encapsulates all metadata for a single variable:

```python
class VariableMetadata:
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
    
    def to_dict(self, include_value: bool = True, 
                include_value_preview: bool = False, 
                max_preview_length: int = 5000) -> Dict[str, Any]:
        """Convert metadata to dictionary representation."""
        result = {
            "description": self.description,
            "type": self.type,
            "created_at": self.created_at.isoformat(),
            "count_items": self.count_items,
        }
        if include_value:
            result["value"] = self.value
        if include_value_preview:
            result["value_preview"] = str(self.value)[:max_preview_length]
        return result
```

**Key Design Decisions:**

- **Automatic Type Detection**: No manual type specification needed
- **Flexible Counting**: Works with any iterable type, falls back gracefully
- **Configurable Serialization**: Choose whether to include full values or just previews
- **Timestamp Tracking**: Automatic creation time capture

#### VariablesManager Class (Singleton)

The manager implements the singleton pattern and provides the main API:

```python
class VariablesManager(object):
    _instance = None
    variables: Dict[str, VariableMetadata] = {}
    variable_counter: int = 0
    _creation_order: list = []
    _log_file: Optional[Path] = None
    _session_start: Optional[datetime] = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VariablesManager, cls).__new__(cls)
            if settings.advanced_features.tracker_enabled:
                cls._instance._initialize_logging()
        return cls._instance
```

**Singleton Implementation:**

- **`__new__` Override**: Ensures only one instance exists
- **Class-Level State**: All state is class attributes, shared across instances
- **Lazy Initialization**: Logging is initialized only if enabled in settings
- **Thread-Safe Note**: Basic implementation; production use might add locks

### Adding and Retrieving Variables

The core operations are straightforward yet powerful:

#### Adding Variables

```python
# Automatic naming
vm = VariablesManager()
var_name = vm.add_variable([1, 2, 3, 4, 5], 
                          description="Sample data for analysis")
# Returns: "variable_1"

# Explicit naming
var_name = vm.add_variable({"key": "value"}, 
                          name="config_data",
                          description="Configuration loaded from file")
# Returns: "config_data"

# Update existing variable
vm.add_variable([1, 2, 3, 4, 5, 6], 
               name="variable_1",
               description="Updated sample data")
# Overwrites variable_1
```

**Implementation Details:**

```python
def add_variable(self, value: Any, name: Optional[str] = None, 
                description: Optional[str] = None) -> str:
    """
    Add a new variable with an optional name or auto-generated name and description.
    
    Args:
        value (Any): The value to store
        name (Optional[str]): Optional custom name, if None will auto-generate
        description (Optional[str]): Optional description of the variable
    
    Returns:
        str: The name of the variable that was created
    """
    is_new = True
    original_name = name
    
    if name is None:
        self.variable_counter += 1
        name = f"variable_{self.variable_counter}"
    else:
        # If a custom name is provided and it's a 'variable_X' format,
        # update the counter to avoid future collisions.
        if name.startswith("variable_") and name[9:].isdigit():
            num = int(name[9:])
            if num >= self.variable_counter:
                self.variable_counter = num
        
        # Check if variable already exists
        if name in self.variables:
            is_new = False
    
    self.variables[name] = VariableMetadata(value, description)
    
    # Track creation order
    if name not in self._creation_order:
        self._creation_order.append(name)
    
    # Log the operation (logging code omitted for brevity)
    
    return name
```

**Design Features:**

- **Smart Counter Management**: Prevents collisions between auto-generated and explicit names
- **Update Semantics**: Re-adding with the same name updates the variable
- **Creation Order Tracking**: Maintains chronological order for last-n queries
- **Comprehensive Logging**: Every operation is logged with context

#### Retrieving Variables

```python
# Get the full value
vm = VariablesManager()
data = vm.get_variable("variable_1")
# Returns: [1, 2, 3, 4, 5, 6]

# Get metadata
metadata = vm.get_variable_metadata("variable_1")
# Returns: VariableMetadata object with .value, .type, .description, etc.

# Get all variable names
names = vm.get_variable_names()
# Returns: ['variable_1', 'config_data', 'variable_2', ...]

# Get last N variable names (most recent)
recent = vm.get_last_n_variable_names(3)
# Returns: ['variable_7', 'variable_8', 'variable_9']
```

**Simple, Type-Safe APIs:**

```python
def get_variable(self, name: str) -> Any:
    """Get a variable value by name."""
    metadata = self.variables.get(name)
    return metadata.value if metadata else None

def get_variable_metadata(self, name: str) -> Optional[VariableMetadata]:
    """Get complete metadata for a variable by name."""
    return self.variables.get(name)

def get_last_n_variable_names(self, n: int) -> list[str]:
    """Get the names of the last n created variables."""
    if n <= 0:
        return []
    return self._creation_order[-n:] if len(self._creation_order) >= n else self._creation_order[:]
```

### Summary Generation: The Key Optimization

The most important feature for context efficiency is summary generation:

```python
vm = VariablesManager()

# Get summary of all variables
summary = vm.get_variables_summary()

# Get summary of specific variables
summary = vm.get_variables_summary(
    variable_names=["data_filtered", "statistics", "chart_config"]
)

# Get summary of last N variables (most useful for agents)
summary = vm.get_variables_summary(last_n=5)
```

**Example Output:**

```markdown
# Last 5 Variables Summary

## data_filtered
- Type: list
- Items: 500
- Description: Customer records meeting filter criteria
- Created: 2024-12-02 10:23:42
- Value Preview: [{'id': 45, 'name': 'Alice', 'state': 'CA'}, {'id': 67, 'name': 'Bob', 'state': 'CA'}, ... (+498 more)]

## statistics
- Type: dict
- Items: 6
- Description: Summary statistics computed from filtered data
- Created: 2024-12-02 10:24:15
- Value Preview: {'mean': 156.4, 'median': 150.0, 'std': 45.2, 'min': 100, 'max': 500, 'count': 500}

## chart_config
- Type: dict
- Items: 4
- Description: Configuration for bar chart visualization
- Created: 2024-12-02 10:24:38
- Value Preview: {'type': 'bar', 'x_axis': 'state', 'y_axis': 'order_total', 'title': 'Orders by State'}
```

**Smart Value Preview:**

The preview generation is sophisticated, handling nested structures intelligently:

```python
def _get_value_preview(self, value: Any, max_length: int = 5000) -> str:
    """
    Get a structured preview of the value, truncating nested content when large.
    
    This preserves high-level structure (e.g., dict keys) while shortening
    long strings and large lists/tuples nested within.
    """
    # Try full representation first
    try:
        full_repr = repr(value)
        if len(full_repr) <= max_length:
            return full_repr
    except Exception:
        pass  # Fall back to smart truncation
    
    # Tunable thresholds
    max_string_chars = max(50, min(200, max_length // 4))
    max_list_items = 10
    max_depth = 6
    
    def shorten(val: Any, depth: int = 0, current_length: int = 0) -> str:
        # Try full representation if it might fit
        if depth < max_depth:
            try:
                full_val_repr = repr(val)
                if current_length + len(full_val_repr) <= max_length:
                    return full_val_repr
            except Exception:
                pass
        
        if depth >= max_depth:
            return "..."
        
        # Handle strings
        if isinstance(val, str):
            if len(val) <= max_string_chars:
                return repr(val)
            return repr(val[:max_string_chars] + "...")
        
        # Handle lists/tuples
        if isinstance(val, (list, tuple)):
            open_b, close_b = ("[", "]") if isinstance(val, list) else ("(", ")")
            items = []
            total = len(val)
            
            for index, item in enumerate(val):
                if index >= max_list_items:
                    remaining = total - index
                    items.append(f"... (+{remaining} more)")
                    break
                
                item_repr = shorten(item, depth + 1, current_length)
                items.append(item_repr)
            
            return f"{open_b}{', '.join(items)}{close_b}"
        
        # Handle dicts - preserve all keys
        if isinstance(val, dict):
            if not val:
                return "{}"
            
            parts = []
            for key, nested in val.items():
                key_repr = repr(key)
                nested_repr = shorten(nested, depth + 1, current_length)
                parts.append(f"{key_repr}: {nested_repr}")
            
            return "{" + ", ".join(parts) + "}"
        
        # Fallback
        return repr(val)
    
    preview = shorten(value, 0, 0)
    if len(preview) > max_length:
        return preview[:max_length] + "..."
    return preview
```

**Preview Features:**

- **Structure Preservation**: Shows dict keys even when values are truncated
- **Smart Truncation**: Shortens large collections while indicating how much was omitted
- **Depth Limiting**: Prevents excessive recursion on deeply nested structures
- **Length Control**: Ensures previews never exceed specified token budget

This allows agents to see the "shape" of data without consuming excessive tokens.

### Lifecycle Management

Managing the variable landscape over long executions is crucial:

#### Complete Reset

```python
vm = VariablesManager()
vm.reset()  # Clear all variables, reset counter
```

Useful when starting a completely new task or conversation.

#### Selective Retention

```python
vm = VariablesManager()

# Agent has created 20 variables during analysis
# Keep only the 5 most recent (likely most relevant)
vm.reset_keep_last_n(5)

# Now only the last 5 variables remain
# Counter is adjusted to prevent name collisions with kept variables
```

**Implementation:**

```python
def reset_keep_last_n(self, n: int) -> None:
    """
    Reset the variables manager, keeping only the last 'n' added variables.
    
    Args:
        n (int): The number of last added variables to keep.
    """
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

**Use Case:** In long-running analyses, the agent might accumulate many intermediate variables. Periodically calling `reset_keep_last_n(10)` maintains a sliding window of recent variables, preventing unlimited memory growth while keeping relevant state.

#### Individual Variable Removal

```python
vm = VariablesManager()
success = vm.remove_variable("temporary_data")
# Returns: True if removed, False if not found
```

Useful for explicit cleanup of temporary values no longer needed.

### Observability Features

The CUGA Variable Manager includes production-grade observability:

#### Markdown Logging

When enabled, every operation is logged to a markdown file:

```python
def _initialize_logging(self):
    """Initialize the markdown log file."""
    log_dir = Path("logging/variables_manager")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    self._session_start = datetime.now()
    timestamp = self._session_start.strftime("%Y%m%d_%H%M%S")
    self._log_file = log_dir / f"variables_log_{timestamp}.md"
    
    # Write header
    with open(self._log_file, 'w') as f:
        f.write("# Variables Manager Log\n\n")
        f.write(f"**Session Started:** {self._session_start.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
```

Each session gets its own timestamped log file in `logging/variables_manager/`.

#### Caller Tracking

Every operation captures where it was called from:

```python
def _get_caller_info(self, skip_frames=2) -> str:
    """Get information about the caller function."""
    try:
        stack = inspect.stack()
        if len(stack) > skip_frames:
            frame = stack[skip_frames]
            filename = Path(frame.filename).name
            function = frame.function
            line = frame.lineno
            return f"{filename}:{function}:{line}"
        return "Unknown caller"
    except Exception:
        return "Unknown caller"
```

This tells you exactly which agent or tool created each variable.

#### Operation Logging

```python
def _log_operation(self, operation: str, details: str, extra_info: Optional[str] = None):
    """Log an operation to the markdown file."""
    if not settings.advanced_features.tracker_enabled or not self._log_file:
        return
    
    try:
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        caller = self._get_caller_info(skip_frames=3)
        
        with open(self._log_file, 'a') as f:
            f.write(f"## {operation}\n\n")
            f.write(f"- **Time:** {timestamp}\n")
            f.write(f"- **Caller:** `{caller}`\n")
            f.write(f"- **Details:** {details}\n")
            if extra_info:
                f.write(f"\n{extra_info}\n")
            f.write("\n---\n\n")
    except Exception as e:
        logger.warning(f"Failed to write to variables log: {e}")
```

**Logged Operations:**
- Variable additions (with or without explicit names)
- Variable updates
- Variable removals
- Complete resets
- Partial resets (keep-last-n)

**Example Log Output:**

```markdown
## ➕ Variable Added

- **Time:** 10:23:42.156
- **Caller:** `code_agent.py:execute_code:127`
- **Details:** **variable_3** = `list` (145 chars)

### Variable Info
- **Name:** `variable_3` (auto-generated)
- **Type:** `list`
- **Description:** Filtered customer data
- **Value Preview:**
```python
[{'id': 45, 'name': 'Alice'}, {'id': 67, 'name': 'Bob'}, ... (+498 more)]
```

### Current State
- **Total Variables:** 3
- **Variable Counter:** 3
- **All Variables:** `variable_1`, `variable_2`, `variable_3`

---

## 🔄 PARTIAL RESET

- **Time:** 10:25:10.892
- **Caller:** `plan_controller.py:cleanup_step:89`
- **Details:** Keeping last **5** variables, removing **10** variables

### Variables Kept:
- ✅ `variable_11`: dict
- ✅ `variable_12`: list
- ✅ `variable_13`: dict
- ✅ `variable_14`: str
- ✅ `variable_15`: dict

### Variables Removed:
- ❌ `variable_1`: list
- ❌ `variable_2`: dict
- ❌ `variable_3`: list
...

---
```

This log becomes an invaluable debugging tool, showing exactly how the variable landscape evolved during execution.

## Key Implementation Patterns

Beyond the mechanics, several implementation patterns emerge from production use:

### When to Use Variable Manager vs Direct State Passing

**Use Variable Manager when:**
- Values are large (>1KB) and would consume significant context
- Values are created in one step and used several steps later
- Multiple agents need access to shared state
- You need observability into state evolution
- Values might be reused multiple times across different prompts

**Use Direct State Passing when:**
- Values are small (<100 characters)
- Value is used immediately in the next step
- Value is ephemeral and doesn't need tracking
- Overhead of variable management outweighs benefits

**Example Decision:**

```python
# Small, immediate use - pass directly
next_step_prompt = f"Process this text: {short_text}"

# Large, multi-step use - use Variable Manager
vm = VariablesManager()
var_name = vm.add_variable(large_dataframe, description="Customer analysis data")
next_step_prompt = f"Analyze the data in {var_name}"
```

### Balancing Metadata Richness with Performance

The CUGA implementation captures rich metadata, but you can tune this:

**Minimal Tracking** (fastest):
```python
# Only store value and auto-detected type
metadata = VariableMetadata(value)
```

**Standard Tracking** (recommended):
```python
# Add description for agent context
metadata = VariableMetadata(value, description="Customer data")
```

**Full Tracking** (best observability):
```python
# Include description, enable logging, track caller
# (This is what CUGA does by default)
metadata = VariableMetadata(value, description="Customer data")
# Logging captures caller automatically via stack inspection
```

**Performance Considerations:**
- Stack inspection (for caller tracking) adds ~0.1ms per operation
- Markdown logging adds ~1-5ms per operation
- Metadata serialization for summaries: ~0.01ms per variable
- For most agent workflows (seconds to minutes), this overhead is negligible

### Integration with Agent Tool Systems

The Variable Manager works best when integrated with agent tools:

**Variable Viewer Tool:**
```python
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
```

**Variable Retriever Tool:**
```python
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
```

**Code Execution Integration:**
```python
@tool
def execute_python_code(code: str) -> dict:
    """Execute Python code and capture created variables."""
    vm = VariablesManager()
    
    # Create execution namespace
    namespace = {}
    
    # Execute the code
    exec(code, namespace)
    
    # Capture all created variables
    for name, value in namespace.items():
        if not name.startswith('_'):  # Skip private variables
            vm.add_variable(
                value, 
                name=name,
                description=f"Created by code execution"
            )
    
    # Return summary
    return {
        "status": "success",
        "variables_created": [k for k in namespace.keys() if not k.startswith('_')],
        "summary": vm.get_variables_summary(last_n=5)
    }
```

This integration allows agents to discover, inspect, and use variables naturally through their tool-calling mechanisms.

### Testing Strategies

The CUGA implementation includes comprehensive tests that demonstrate best practices:

**Singleton Testing:**
```python
def test_singleton_pattern():
    """Test that VariablesManager follows singleton pattern."""
    vm1 = VariablesManager()
    vm2 = VariablesManager()
    assert vm1 is vm2, "VariablesManager should be a singleton"
```

**Metadata Tracking:**
```python
def test_add_variable_with_description():
    """Test adding variables with descriptions."""
    vm = VariablesManager()
    vm.reset()
    
    # Test various data types
    var1 = vm.add_variable("Hello World", description="A simple greeting")
    var2 = vm.add_variable([1, 2, 3], description="List of numbers")
    var3 = vm.add_variable({"key": "value"}, name="config", description="Config dict")
    
    # Verify metadata
    meta1 = vm.get_variable_metadata(var1)
    assert meta1.type == "str"
    assert meta1.description == "A simple greeting"
    assert meta1.count_items == 11  # Length of string
```

**Summary Generation:**
```python
def test_last_n_variables_functionality():
    """Test the last_n functionality for variables summary."""
    vm = VariablesManager()
    vm.reset()
    
    # Add multiple variables
    for i in range(7):
        vm.add_variable(f"value_{i}", description=f"Variable {i}")
    
    # Test last_n filtering
    summary = vm.get_variables_summary(last_n=3)
    assert "value_4" in summary
    assert "value_5" in summary
    assert "value_6" in summary
    assert "value_0" not in summary  # Earlier variables excluded
```

**Lifecycle Management:**
```python
def test_reset_keep_last_n():
    """Test selective variable retention."""
    vm = VariablesManager()
    vm.reset()
    
    # Create variables
    vars_added = []
    for i in range(10):
        var_name = vm.add_variable(f"data_{i}", description=f"Dataset {i}")
        vars_added.append(var_name)
    
    assert vm.get_variable_count() == 10
    
    # Keep only last 3
    vm.reset_keep_last_n(3)
    
    assert vm.get_variable_count() == 3
    remaining = vm.get_variable_names()
    assert remaining == vars_added[-3:]
```

These tests ensure the Variable Manager behaves correctly under all conditions and can serve as documentation for users.

## Relationship to Other Patterns

The Variable Manager Pattern complements and differs from related patterns:

### vs. Session State (Memory Management)

**Session State** (Chapter 8) manages conversation-level context:
- Scope: Single conversation thread
- Lifetime: Duration of one session
- Access: Available in LLM context
- Use case: Tracking user preferences, conversation flow

**Variable Manager**:
- Scope: Execution-level (can span sessions)
- Lifetime: Controlled by explicit reset
- Access: Retrieved via tools, summaries in context
- Use case: Tracking computation results, intermediate data

**When to Use Which:**
- User said "I prefer dark mode" → Session State
- Agent computed "filtered_data with 500 records" → Variable Manager
- Multi-turn conversation context → Session State  
- Multi-step computation pipeline → Variable Manager

They can work together: session state tracks conversation context, while Variable Manager tracks execution artifacts.

### vs. External Memory / RAG

**External Memory/RAG** (Chapter 14) provides semantic search over documents:
- Storage: Vector database
- Retrieval: Semantic similarity search
- Content: Documents, knowledge base
- Use case: Finding relevant information from large corpora

**Variable Manager**:
- Storage: In-memory dictionary
- Retrieval: Exact name lookup
- Content: Execution variables, computed results
- Use case: Tracking values created during current execution

**When to Use Which:**
- "Find documents about Python" → External Memory/RAG
- "Get the dataset I filtered 3 steps ago" → Variable Manager
- Long-term knowledge persistence → External Memory
- Session-scoped execution state → Variable Manager

### vs. Persistent Task Lists (Recitation)

**Recitation Pattern** uses persistent files (like `todo.md`) to:
- Track high-level goals and plans
- Ensure agents don't lose sight of objectives
- Provide stable reference across execution

**Variable Manager**:
- Tracks data values, not tasks
- Manages dynamic execution state
- Provides metadata summaries, not task lists

**They Complement Each Other:**
```markdown
# todo.md (Recitation Pattern)
- [x] Fetch customer data
- [x] Filter for California customers
- [ ] Compute summary statistics
- [ ] Generate visualization
```

```python
# Variable Manager tracks the data
vm = VariablesManager()
vm.get_variables_summary(last_n=3)
# Shows: customer_data, ca_customers (ready for statistics computation)
```

The Recitation Pattern tracks *what* to do; Variable Manager tracks *what you have* to do it with.

## Best Practices and Guidelines

### Naming Conventions

**Auto-Generated Names:** Good for temporary values that don't need semantic meaning:
```python
# Agent doesn't need to reference this explicitly
temp_result = vm.add_variable(intermediate_computation())
```

**Semantic Names:** Better for values that will be referenced multiple times:
```python
# Agent will reference this in multiple steps
vm.add_variable(filtered_data, name="california_customers", 
               description="Customers in California with >$100 orders")
```

**Convention:**
- Use `snake_case` for explicit variable names
- Include enough context in the name to be self-documenting
- Keep names under 30 characters when possible

### Description Guidelines

Good descriptions help agents understand variable purpose:

**Too Vague:**
```python
vm.add_variable(data, description="Some data")  # Not helpful
```

**Too Verbose:**
```python
vm.add_variable(data, description="This is the customer data that we retrieved from the API endpoint /api/v2/customers using the filter parameters state=CA and order_total>100 which returned 500 records that we'll use for analysis")  # Too long, summary provides details
```

**Just Right:**
```python
vm.add_variable(data, name="ca_high_value_customers",
               description="CA customers with orders >$100")  # Clear and concise
```

### When to Reset

**Full Reset** (`reset()`):
- Starting a completely new task/conversation
- After completing a major workflow
- When variable accumulation risks memory issues

**Partial Reset** (`reset_keep_last_n()`):
- Midway through long workflows
- When earlier variables are no longer relevant
- To maintain a sliding window of recent state

**No Reset:**
- Variables from current step might be needed soon
- Workflow is short (<10 variables)
- Memory usage is not a concern

### Performance Optimization

**For High-Frequency Operations:**
```python
# Cache the VariablesManager instance
vm = VariablesManager()  # Do this once

# Then use it many times
for item in large_dataset:
    result = process(item)
    vm.add_variable(result)  # Fast: no singleton lookup overhead
```

**For Memory-Constrained Environments:**
```python
# Periodically clean up
if vm.get_variable_count() > 20:
    vm.reset_keep_last_n(10)  # Keep recent, discard old
```

**For Production Systems:**
```python
# Disable logging in performance-critical sections
# (if your implementation supports it)
with vm.logging_disabled():
    for i in range(1000):
        vm.add_variable(f"batch_{i}", heavy_computation())
```

## Summary

The Variable Manager Pattern provides a sophisticated solution for tracking execution state in multi-step agent workflows. By separating variable metadata from variable values, it enables agents to maintain awareness of available data without paying the token cost of including full values in context.

**Core Benefits:**

1. **Context Efficiency**: Agents see what data exists through lightweight summaries, not expensive full values
2. **Observability**: Comprehensive logging provides audit trails for debugging and monitoring
3. **Clean Architecture**: Singleton pattern ensures consistent state across the entire agent system
4. **Flexibility**: Support for both auto-generated and semantic variable names
5. **Lifecycle Control**: Smart reset strategies manage memory over long executions

**When to Apply This Pattern:**

- Code execution agents that create variables in a programming environment
- Data analysis workflows with multiple transformation steps
- API integration chains where responses feed into subsequent calls
- Multi-agent systems requiring shared state coordination
- Any scenario where intermediate results need tracking across execution steps

**Key Takeaway:**

In modern agentic systems with large context windows, it's tempting to simply include everything in context. However, the Variable Manager Pattern demonstrates that thoughtful state management—tracking metadata separately from values—provides superior efficiency, observability, and scalability. The CUGA implementation showcases how a well-designed Variable Manager becomes an essential component of production agent architectures.

As agent systems grow more sophisticated and handle larger datasets, patterns like Variable Manager will become increasingly critical for managing the complexity of long-running, multi-step workflows while maintaining performance and cost efficiency.

