# Pattern: Exception Handling and Recovery

## Motivation

When a plan fails—a restaurant is closed, a flight is delayed, or a tool breaks—humans adapt. We find alternatives, adjust expectations, and continue toward our goal. We build resilience by having backup plans and learning from mistakes. Exception Handling gives agents this same resilience: gracefully handling failures, recovering from errors, and adapting strategies when things go wrong, just as humans do in everyday life.

## Pattern Overview
**What it is:** Exception Handling and Recovery is a pattern that equips AI agents with the capability to anticipate, detect, manage, and recover from operational failures, ensuring robust and resilient operation in unpredictable environments.

**When to use:** Use this pattern for any AI agent deployed in a dynamic, real-world environment where system failures, tool errors, network issues, or unpredictable inputs are possible and operational reliability is a key requirement.

**Why it matters:** For AI agents to operate reliably in diverse real-world environments, they must be able to manage unforeseen situations, errors, and malfunctions. Just as humans adapt to unexpected obstacles, intelligent agents need robust systems to detect problems, initiate recovery procedures, or at least ensure controlled failure. This essential requirement ensures agents are not only intelligent but also stable and reliable.

AI agents operating in real-world environments inevitably encounter unforeseen situations, errors, and system malfunctions. These disruptions can range from tool failures and network issues to invalid data, threatening the agent's ability to complete its tasks. Without a structured way to manage these problems, agents can be fragile, unreliable, and prone to complete failure when faced with unexpected hurdles. This unreliability makes it difficult to deploy them in critical or complex applications where consistent performance is essential.

The Exception Handling and Recovery pattern provides a standardized solution for building robust and resilient AI agents. It equips them with the capability to anticipate, manage, and recover from operational failures. The pattern involves proactive error detection, such as monitoring tool outputs and API responses, and reactive handling strategies like logging for diagnostics, retrying transient failures, or using fallback mechanisms. For more severe issues, it defines recovery protocols, including reverting to a stable state, self-correction by adjusting its plan, or escalating the problem to a human operator.

This pattern may sometimes be used with reflection. For example, if an initial attempt fails and raises an exception, a reflective process can analyze the failure and reattempt the task with a refined approach, such as an improved prompt, to resolve the error.

### Key Concepts
- **Error Detection:** Meticulously identifying operational issues as they arise, including invalid tool outputs, API errors, timeouts, or incoherent responses. Detection can occur at multiple levels: tool execution, code execution, API responses, and output validation.
- **Error Classification:** Categorizing errors by type (syntax errors, runtime exceptions, connection errors, validation errors) and severity (low, medium, high, critical) to determine appropriate handling strategies.
- **Error Handling:** Response plans including logging, retries with exponential backoff, fallbacks, graceful degradation, and notifications. Different error types require different handling strategies.
- **Retry Logic:** Automatic retry mechanisms for transient errors (connection failures, timeouts) with configurable retry counts and backoff strategies. Retries can be applied at tool execution, API calls, and structured output validation levels.
- **Error Propagation:** Routing errors to appropriate handlers (plan controller for replanning, human-in-the-loop for escalation, error logging for diagnostics) based on error severity and context.
- **Recovery:** Restoring the agent to stable operation through state rollback, diagnosis, self-correction, replanning, or escalation. Recovery strategies adapt based on error type and workflow context.
- **Proactive Preparation:** Anticipating potential issues and developing strategies to mitigate them before they occur, such as session validation before tool execution.
- **Reactive Strategies:** Responding to errors as they occur with appropriate handling mechanisms, including error detection in output content and automatic error routing.

### How It Works

Exception Handling and Recovery operates through a multi-layered process that detects, classifies, handles, and recovers from errors at different stages of agent execution:

**1. Error Detection (Multi-Level)**

**Tool Execution Level:**
- Catch exceptions during tool invocation
- Detect connection errors (e.g., closed sessions, network failures)
- Validate tool outputs before use
- Check for invalid responses or missing data

**Code Execution Level:**
- Catch syntax errors during code generation/execution
- Detect runtime exceptions (TypeError, ValueError, etc.)
- Monitor execution timeouts
- Identify error indicators in output content (e.g., "Error:", "Exception:", "Traceback")

**API Response Level:**
- Check for error status codes in API responses
- Validate response schemas
- Detect exception status in response payloads
- Monitor for timeout or connection errors

**Output Validation Level:**
- Validate structured outputs against schemas
- Detect missing required fields
- Identify format mismatches
- Retry validation failures automatically

**2. Error Classification**

Errors are classified by:
- **Type:** Syntax errors, runtime exceptions, connection errors, validation errors, timeout errors
- **Severity:** Low (recoverable), Medium (requires attention), High (significant impact), Critical (system failure)
- **Transience:** Transient (retryable) vs. Permanent (requires different strategy)

**3. Error Handling Strategies**

**Retry Logic:**
- Automatic retries for transient errors (connection failures, timeouts)
- Exponential backoff between retry attempts
- Configurable retry counts (typically 3 attempts)
- Session reconnection for connection errors

**Fallback Mechanisms:**
- Alternative tool or API when primary fails
- Simplified operations when complex ones fail
- Default values when data retrieval fails

**Error Propagation:**
- Route errors to appropriate handlers based on context
- For sub-tasks: propagate to plan controller for replanning
- For critical errors: escalate to human-in-the-loop
- For validation errors: retry with corrected inputs

**Logging and Diagnostics:**
- Comprehensive error logging with context
- Error tracking in execution history
- State updates with error information
- Diagnostic information for debugging

**4. Recovery Mechanisms**

**State Management:**
- Update execution history with error information
- Preserve partial results when possible
- Mark failed subtasks in plan progress
- Store error messages for context

**Replanning:**
- Return to plan controller with error context
- Allow plan controller to adjust strategy
- Retry with modified approach or different tools
- Skip failed subtasks if alternative path exists

**Self-Correction:**
- Analyze error to identify root cause
- Adjust parameters or approach based on error
- Retry with corrected inputs
- Use alternative methods when available

**Escalation:**
- Escalate critical errors to human operators
- Request human guidance for ambiguous errors
- Provide error context for human review

**5. Error Recovery Flow**

```
Error Detected → Classify Error → Select Strategy → Execute Recovery
     ↓                ↓                ↓                  ↓
  Log Error    Transient?      Retry/Fallback      Success?
     ↓            ↓                ↓                  ↓
  Update State  Permanent?     Replan/Escalate    Continue/Abort
```

**Implementation Patterns:**

- **Try-Except Blocks:** Wrap risky operations (tool calls, code execution, API calls)
- **Error Indicators:** Check output content for error patterns
- **Session Validation:** Validate sessions before operations, reconnect if needed
- **Structured Output Retry:** Automatic retry for validation failures
- **Error Routing:** Route errors to appropriate nodes (plan controller, human-in-the-loop, error handler)

## Error Handling Patterns

### Pattern 1: Try-Except with Retry

Wrap risky operations in try-except blocks with automatic retry for transient errors:

```python
import asyncio
from typing import Callable, Any, TypeVar

T = TypeVar('T')

class TransientError(Exception):
    """Error that can be retried."""
    pass

async def execute_with_retry(
    operation: Callable[[], Any],
    max_retries: int = 3
) -> Any:
    """Execute operation with automatic retry for transient errors."""
    for attempt in range(max_retries):
        try:
            if asyncio.iscoroutinefunction(operation):
                return await operation()
            else:
                return operation()
        except TransientError as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                await asyncio.sleep(wait_time)
                continue
            raise
        except Exception as e:
            # Non-transient errors are re-raised immediately
            raise

# Usage
async def risky_operation():
    # Simulated operation that might fail
    import random
    if random.random() < 0.5:
        raise TransientError("Temporary failure")
    return "Success"

# Example usage
async def main():
    result = await execute_with_retry(risky_operation, max_retries=3)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Pattern 2: Error Detection in Output

Check output content for error indicators, not just exceptions:

```python
def detect_error_in_output(output: str) -> bool:
    """Detect error indicators in output content."""
    if not output:
        return False
    
    error_indicators = [
        'Error:',
        'Exception:',
        'Traceback',
        'Failed to',
        'Error during execution:'
    ]
    return any(indicator in output for indicator in error_indicators)

# Usage
output = "Error: Invalid input parameter"
if detect_error_in_output(output):
    print("Error detected in output")
```

### Pattern 3: Error Propagation for Replanning

Route sub-task errors back to plan controller for adaptive replanning:

```python
from typing import TypedDict, List
from langgraph.types import Command

class SubTaskHistory(TypedDict):
    sub_task: str
    steps: List[str]
    final_answer: str

class AgentState(TypedDict):
    sub_task: str
    stm_all_history: List[SubTaskHistory]

def handle_subtask_error(state: AgentState, error: Exception) -> Command:
    """Handle sub-task errors by returning to plan controller."""
    error_msg = f"Error: {error}"
    
    # Update history with error
    state["stm_all_history"].append(
        SubTaskHistory(
            sub_task=state.get("sub_task", ""),
            steps=[],
            final_answer=error_msg
        )
    )
    
    # Return to planner for replanning
    return Command(update=state, goto="PlanControllerAgent")

# Usage
state: AgentState = {
    "sub_task": "Process data",
    "stm_all_history": [],
    "last_planner_answer": ""
}
try:
    # Some operation that fails
    raise ValueError("Invalid data format")
except Exception as e:
    command = handle_subtask_error(state, e)
    print(f"Command: {command}")
```

### Pattern 4: Session Reconnection

Detect connection errors and attempt reconnection before retrying:

```python
import asyncio
from typing import Any, Dict

class ConnectionError(Exception):
    """Connection-related error."""
    pass

class Tool:
    """Example tool class."""
    def __init__(self, name: str):
        self.name = name
        self.session = None
    
    async def setup(self):
        """Initialize session."""
        self.session = {"connected": True}
    
    async def ainvoke(self, args: Dict[str, Any]) -> Any:
        """Execute tool with args."""
        if not self.session:
            raise ConnectionError("Session not initialized")
        return {"result": "success", "args": args}

async def reconnect_session(tool: Tool):
    """Reconnect tool session."""
    await tool.setup()

async def execute_tool_with_reconnect(
    tool: Tool,
    tool_call: Dict[str, Any]
) -> Any:
    """Execute tool with automatic reconnection on connection errors."""
    try:
        return await tool.ainvoke(tool_call.get("args", {}))
    except ConnectionError:
        print("Connection error detected, reconnecting...")
        await reconnect_session(tool)
        return await tool.ainvoke(tool_call.get("args", {}))  # Retry

# Usage
async def main():
    tool = Tool("example_tool")
    await tool.setup()
    tool.session = None  # Simulate connection loss

    result = await execute_tool_with_reconnect(
        tool,
        {"args": {"param": "value"}}
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Pattern 5: Structured Output Validation with Retry

Automatically retry on validation failures:

```python
from pydantic import BaseModel, ValidationError
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from typing import Any

class OutputSchema(BaseModel):
    """Example output schema."""
    result: str
    confidence: float

def validate_output(output: Any, schema: type[BaseModel]) -> BaseModel:
    """Validate output against schema."""
    try:
        if isinstance(output, dict):
            return schema(**output)
        return output
    except ValidationError as e:
        raise  # Will trigger retry

# Create validated chain with retry
def create_validated_chain(llm, schema: type[BaseModel], prompt_template: ChatPromptTemplate):
    """Create chain with validation and automatic retry."""
    base_chain = prompt_template | llm.with_structured_output(schema)
    
    # Add validation
    validated = base_chain | RunnableLambda(
        lambda output: validate_output(output, schema)
    )
    
    # Add retry on validation failure
    return validated.with_retry(stop_after_attempt=3)

# Usage (requires LLM and prompt_template)
# chain = create_validated_chain(llm, OutputSchema, prompt_template)
# result = await chain.ainvoke({"input": "process this"})
```

## When to Use This Pattern

### ✅ Use this pattern when:
- **Real-world deployment:** The agent operates in environments where perfect conditions cannot be guaranteed.
- **External dependencies:** The agent relies on external services, APIs, or tools that may fail.
- **Critical operations:** Failures could have significant consequences requiring robust error handling.
- **Unpredictable inputs:** The agent receives inputs that may be invalid, malformed, or unexpected.
- **Network operations:** The agent performs network operations subject to connectivity issues or timeouts.

### ❌ Avoid this pattern when:
- **Controlled environments:** The agent operates in highly controlled, predictable environments with guaranteed reliability.
- **Simple, stateless operations:** The agent performs simple operations without external dependencies or state.
- **Prototype/testing:** Early prototypes where error handling adds unnecessary complexity.
- **Deterministic workflows:** Fixed workflows with guaranteed success paths don't need exception handling.

### Decision Guidelines
Use Exception Handling and Recovery when the benefits of robustness and reliability outweigh the implementation complexity. Consider: the criticality of operations (more critical = more need for handling), the reliability of dependencies (less reliable = more need for handling), and the cost of failures (higher cost = more need for handling). Be aware that exception handling adds complexity and overhead, but is essential for production systems. Implement comprehensive error detection, logging, and recovery mechanisms to ensure reliable operation.

## Practical Applications & Use Cases

Exception Handling and Recovery is critical for any agent deployed in a real-world scenario where perfect conditions cannot be guaranteed.

- **Customer Service Chatbots:** Handle database downtime by detecting API errors, informing users, and escalating to human agents.
- **Automated Financial Trading:** Manage "insufficient funds" or "market closed" errors by logging, avoiding repeated invalid trades, and notifying users.
- **Smart Home Automation:** Detect device failures, retry operations, and notify users when manual intervention is needed.
- **Data Processing Agents:** Skip corrupted files, log errors, continue processing, and report skipped files rather than halting entirely.
- **Web Scraping Agents:** Handle CAPTCHAs, changed website structures, or server errors by pausing, using proxies, or reporting failures.
- **Robotics and Manufacturing:** Detect sensor failures, attempt readjustment, retry operations, and alert human operators when persistent.

## Implementation

### Core Components

**Error Detection:**

```python
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ErrorDetector:
    """Detects errors at multiple levels."""
    
    @staticmethod
    def detect_in_output(output: str) -> bool:
        """Detect error indicators in output content."""
        if not output:
            return False
        
        error_indicators = [
            'Error during execution:',
            'Error:',
            'Exception:',
            'Traceback',
            'Failed to'
        ]
        return any(indicator in output for indicator in error_indicators)
    
    @staticmethod
    def detect_in_api_response(response: Dict[str, Any]) -> bool:
        """Detect errors in API responses."""
        return (
            response.get("status") == "exception" or
            "error" in response or
            response.get("status_code", 200) >= 400
        )
    
    @staticmethod
    def detect_connection_error(error: Exception) -> bool:
        """Detect connection-related errors."""
        error_str = str(type(error))
        error_msg = str(error)
        return (
            "ClosedResourceError" in error_str or
            "Connection" in error_msg or
            "ConnectionError" in error_str
        )

# Usage
detector = ErrorDetector()

# Detect errors in output
output = "Error during execution: Invalid syntax"
if detector.detect_in_output(output):
    print("Error detected in output")

# Detect errors in API response
api_response = {"status": "exception", "message": "API error"}
if detector.detect_in_api_response(api_response):
    print("Error detected in API response")

# Detect connection errors
try:
    raise ConnectionError("Connection lost")
except Exception as e:
    if detector.detect_connection_error(e):
        print("Connection error detected")
```

**Retry Logic:**

```python
from typing import Callable, Any, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)

class RetryHandler:
    """Handles retries with exponential backoff."""
    
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries
    
    async def execute_with_retry(
        self,
        operation: Callable[[], Any],
        is_transient: Optional[Callable[[Exception], bool]] = None
    ) -> Any:
        """Execute operation with retry logic."""
        for attempt in range(self.max_retries):
            try:
                if asyncio.iscoroutinefunction(operation):
                    return await operation()
                else:
                    return operation()
            except Exception as e:
                # Check if error is transient
                if is_transient and not is_transient(e):
                    raise  # Don't retry non-transient errors
                
                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Retry {attempt + 1}/{self.max_retries} after {wait_time}s")
                    await asyncio.sleep(wait_time)
                else:
                    raise  # Re-raise after all retries exhausted

# Usage
async def example_operation():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Temporary connection failure")
    return "Success"

def is_transient_error(error: Exception) -> bool:
    """Check if error is transient."""
    return isinstance(error, (ConnectionError, TimeoutError))

async def main():
    handler = RetryHandler(max_retries=3)
    result = await handler.execute_with_retry(example_operation, is_transient_error)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

**Error Recovery:**

```python
from typing import TypedDict, List, Optional
from langgraph.types import Command
import logging

logger = logging.getLogger(__name__)

class SubTaskHistory(TypedDict):
    sub_task: str
    steps: List[str]
    final_answer: str

class AgentState(TypedDict):
    sub_task: Optional[str]
    stm_all_history: List[SubTaskHistory]
    final_answer: Optional[str]

class ErrorRecovery:
    """Routes errors to appropriate recovery mechanisms."""
    
    @staticmethod
    def handle_execution_error(
        state: AgentState,
        error: Exception,
        context: str
    ) -> Command:
        """Handle code execution errors."""
        error_msg = f"Error during execution: {error}"
        logger.error(error_msg)
        
        # Update state with error information
        if state.get("sub_task"):
            # For sub-tasks, return to plan controller for replanning
            state["stm_all_history"].append(
                SubTaskHistory(
                    sub_task=state["sub_task"],
                    steps=[],
                    final_answer=error_msg
                )
            )
            return Command(update=state, goto="PlanControllerAgent")
        else:
            # For main task, set final answer with error
            state["final_answer"] = error_msg
            return Command(update=state, goto="FinalAnswerAgent")
    
    @staticmethod
    def handle_tool_error(
        state: AgentState,
        error: Exception,
        tool_name: str
    ) -> Command:
        """Handle tool execution errors."""
        if ErrorDetector.detect_connection_error(error):
            # Try to reconnect and retry
            logger.info("Connection error detected, attempting reconnection...")
            return Command(update=state, goto="RetryTool")
        else:
            # Log and propagate
            logger.error(f"Tool {tool_name} failed: {error}")
            return Command(update=state, goto="PlanControllerAgent")

# Usage
state: AgentState = {
    "sub_task": "Process data",
    "stm_all_history": [],
    "final_answer": None
}

try:
    # Some operation that fails
    raise ValueError("Invalid data format")
except Exception as e:
    command = ErrorRecovery.handle_execution_error(state, e, "data_processing")
```

**Structured Output Validation with Retry:**

```python
from pydantic import BaseModel, ValidationError
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from typing import Any, Type
import logging

logger = logging.getLogger(__name__)

class ValidatedChain:
    """Chain with automatic retry on validation failures."""
    
    @staticmethod
    def create_validated_chain(
        llm: Any,
        schema: Type[BaseModel],
        prompt_template: ChatPromptTemplate
    ):
        """Create chain with validation and retry."""
        base_chain = prompt_template | llm.with_structured_output(schema)
        
        # Add validation
        validated_chain = base_chain | RunnableLambda(
            lambda output: ValidatedChain._validate_output(output, schema)
        )
        
        # Add retry on validation failure
        return validated_chain.with_retry(stop_after_attempt=3)
    
    @staticmethod
    def _validate_output(output: Any, schema: Type[BaseModel]) -> BaseModel:
        """Validate output against schema."""
        try:
            if isinstance(output, dict):
                return schema(**output)
            elif isinstance(output, schema):
                return output
            else:
                raise ValidationError(f"Invalid output type: {type(output)}")
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise  # Will trigger retry

# Usage example (requires LLM and prompt_template)
# class ResultSchema(BaseModel):
#     result: str
#     confidence: float
# 
# chain = ValidatedChain.create_validated_chain(llm, ResultSchema, prompt_template)
# result = await chain.ainvoke({"input": "process this"})
```

### Basic Example: Tool Execution with Retry

```python
import asyncio
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class Tool:
    """Example tool class."""
    def __init__(self, name: str):
        self.name = name
        self.session = None
    
    async def setup(self):
        """Initialize session."""
        self.session = {"connected": True}
        logger.info(f"Tool {self.name} session initialized")
    
    async def ainvoke(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool with args."""
        if not self.session:
            raise ConnectionError("Session not initialized")
        return {"status": "success", "result": f"Processed {args}"}

async def reconnect_session(tool: Tool):
    """Reconnect tool session."""
    await tool.setup()

async def execute_tool_with_retry(
    tool: Tool,
    tool_call: Dict[str, Any],
    max_retries: int = 3
) -> Optional[Dict[str, Any]]:
    """Execute tool with automatic retry on connection errors."""
    for attempt in range(max_retries):
        try:
            return await tool.ainvoke(tool_call.get("args", {}))
        except Exception as e:
            logger.error(f"Tool execution failed (attempt {attempt + 1}): {e}")
            
            # Check if it's a connection error
            if "ConnectionError" in str(type(e)) or "ClosedResourceError" in str(type(e)):
                if attempt < max_retries - 1:
                    # Reconnect and retry
                    logger.info("Reconnecting session...")
                    await reconnect_session(tool)
                    await asyncio.sleep(1)  # Brief delay before retry
                    continue
            raise  # Re-raise if not retryable or retries exhausted
    
    return None

# Usage
async def main():
    tool = Tool("database_query")
    await tool.setup()
    
    # Simulate connection loss
    tool.session = None
    
    result = await execute_tool_with_retry(
        tool,
        {"args": {"query": "SELECT * FROM users"}},
        max_retries=3
    )
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Example: Error Detection in Output

```python
from typing import Dict, Optional

def detect_execution_error(
    output: str,
    metrics: Optional[Dict[str, Any]] = None
) -> bool:
    """Detect errors in code execution output."""
    # Check metrics for errors
    if metrics and metrics.get('error'):
        return True
    
    # Check output content for error indicators
    if not output:
        return False
    
    error_indicators = [
        'Error during execution:',
        'Error:',
        'Exception:',
        'Traceback',
        'Failed to'
    ]
    return any(indicator in output for indicator in error_indicators)

# Usage
output = "Error during execution: Invalid syntax"
metrics = None

if detect_execution_error(output, metrics):
    print("Error detected in execution output")
    # Route to error recovery
    # return handle_execution_error(state, error_msg)
```

### Example: Error Propagation to Plan Controller

```python
from typing import TypedDict, List
from langgraph.types import Command

class SubTaskHistory(TypedDict):
    sub_task: str
    steps: List[str]
    final_answer: str

class AgentState(TypedDict):
    sub_task: str
    stm_all_history: List[SubTaskHistory]
    last_planner_answer: str

async def handle_subtask_error(
    state: AgentState,
    error: str
) -> Command:
    """Handle errors in sub-tasks by returning to plan controller."""
    # Update history with error
    state["stm_all_history"].append(
        SubTaskHistory(
            sub_task=state.get("sub_task", ""),
            steps=[],
            final_answer=error  # Error message
        )
    )
    
    # Return to plan controller for replanning
    state["last_planner_answer"] = error
    return Command(update=state, goto="PlanControllerAgent")

# Usage
state: AgentState = {
    "sub_task": "Process data",
    "stm_all_history": [],
    "last_planner_answer": ""
}

error_msg = "Error: Invalid data format"
import asyncio


async def main():
    command = await handle_subtask_error(state, error_msg)

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Example: Comprehensive Error Handling

```python
from enum import Enum
from typing import Literal, TypedDict, List
from langgraph.types import Command
import logging

logger = logging.getLogger(__name__)

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SubTaskHistory(TypedDict):
    sub_task: str
    steps: List[str]
    final_answer: str

class AgentState(TypedDict):
    sub_task: str
    stm_all_history: List[SubTaskHistory]
    last_planner_answer: str

class ExceptionHandler:
    """Comprehensive exception handler with multiple recovery strategies."""
    
    def handle_exception(
        self,
        error: Exception,
        context: dict,
        state: AgentState
    ) -> Command:
        """Handle exception with appropriate recovery strategy."""
        # Classify error
        severity = self._assess_severity(error, context)
        strategy = self._determine_strategy(error, severity)
        
        # Log error
        logger.error(f"{severity.value} error: {error} in {context}")
        
        # Execute recovery
        if strategy == "retry":
            return self._retry_with_backoff(context)
        elif strategy == "replan":
            return self._return_to_planner(state, error)
        elif strategy == "escalate":
            return self._escalate_to_human(state, error)
        else:
            return self._log_and_continue(state, error)
    
    def _assess_severity(self, error: Exception, context: dict) -> ErrorSeverity:
        """Assess error severity."""
        error_str = str(error).lower()
        if "critical" in error_str or "fatal" in error_str:
            return ErrorSeverity.CRITICAL
        elif "timeout" in error_str or "connection" in error_str:
            return ErrorSeverity.HIGH
        elif "validation" in error_str:
            return ErrorSeverity.MEDIUM
        return ErrorSeverity.LOW
    
    def _determine_strategy(
        self,
        error: Exception,
        severity: ErrorSeverity
    ) -> Literal["retry", "replan", "escalate", "log"]:
        """Determine recovery strategy."""
        error_str = str(error).lower()
        
        # Retry for transient errors
        if "timeout" in error_str or "connection" in error_str:
            return "retry"
        
        # Replan for execution errors in sub-tasks
        if "execution" in error_str or "syntax" in error_str:
            return "replan"
        
        # Escalate critical errors
        if severity == ErrorSeverity.CRITICAL:
            return "escalate"
        
        return "log"
    
    def _return_to_planner(self, state: AgentState, error: Exception) -> Command:
        """Return to plan controller for replanning."""
        error_msg = f"Error: {error}"
        state["stm_all_history"].append(
            SubTaskHistory(
                sub_task=state.get("sub_task", ""),
                steps=[],
                final_answer=error_msg
            )
        )
        state["last_planner_answer"] = error_msg
        return Command(update=state, goto="PlanControllerAgent")
    
    def _retry_with_backoff(self, context: dict) -> Command:
        """Retry operation with exponential backoff."""
        # Implementation would retry the operation
        return Command(update={}, goto="RetryOperation")
    
    def _escalate_to_human(self, state: AgentState, error: Exception) -> Command:
        """Escalate to human-in-the-loop."""
        return Command(update=state, goto="SuggestHumanActions")
    
    def _log_and_continue(self, state: AgentState, error: Exception) -> Command:
        """Log error and continue execution."""
        logger.warning(f"Non-critical error logged: {error}")
        return Command(update=state, goto="ContinueExecution")

# Usage
handler = ExceptionHandler()
state: AgentState = {
    "sub_task": "Process data",
    "stm_all_history": [],
    "last_planner_answer": ""
}

try:
    # Some operation that fails
    raise ValueError("Execution error: Invalid syntax")
except Exception as e:
    command = handler.handle_exception(e, {"operation": "data_processing"}, state)
```

### Example: Structured Output Validation with Retry

```python
from pydantic import BaseModel, ValidationError
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from typing import Any, Type
import logging

logger = logging.getLogger(__name__)

# Automatic retry on validation failures
def create_validated_chain(
    llm: Any,
    schema: Type[BaseModel],
    prompt_template: ChatPromptTemplate
):
    """Create chain with validation and automatic retry."""
    base_chain = prompt_template | llm.with_structured_output(schema)
    
    # Add validation wrapper
    validated = base_chain | RunnableLambda(
        lambda output: validate_output(output, schema)
    )
    
    # Retry on validation failure (up to 3 times)
    return validated.with_retry(stop_after_attempt=3)

def validate_output(output: Any, schema: Type[BaseModel]) -> BaseModel:
    """Validate output against schema."""
    try:
        if isinstance(output, dict):
            return schema(**output)
        elif isinstance(output, schema):
            return output
        else:
            raise ValidationError(f"Invalid output type: {type(output)}")
    except ValidationError as e:
        logger.error(f"Validation failed: {e}")
        raise  # Triggers retry

# Usage example
# class ResultSchema(BaseModel):
#     result: str
#     confidence: float
# 
# chain = create_validated_chain(llm, ResultSchema, prompt_template)
# result = await chain.ainvoke({"input": "process this"})
```

### Example: API Error Handling

```python
import asyncio
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

async def call_api(app_name: str, api_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """Simulated API call."""
    # Simulate API call that might fail
    import random
    if random.random() < 0.3:
        return {"status": "exception", "message": "API timeout error"}
    return {"status": "success", "data": "result"}

async def retry_api_call(
    app_name: str,
    api_name: str,
    args: Dict[str, Any],
    max_retries: int = 3
) -> Dict[str, Any]:
    """Retry API call with exponential backoff."""
    for attempt in range(max_retries):
        await asyncio.sleep(2 ** attempt)  # Exponential backoff
        response = await call_api(app_name, api_name, args)
        if response.get("status") != "exception":
            return response
    return {"status": "exception", "message": "Max retries exceeded"}

async def call_api_with_error_handling(
    app_name: str,
    api_name: str,
    args: Dict[str, Any]
) -> Dict[str, Any]:
    """Call API with error detection and handling."""
    response = await call_api(app_name, api_name, args)
    
    # Check for error status
    if isinstance(response, dict) and response.get("status") == "exception":
        error_msg = response.get("message", "API error")
        logger.error(f"API error: {error_msg}")
        
        # Determine handling based on error type
        if "timeout" in error_msg.lower():
            # Retry for timeouts
            return await retry_api_call(app_name, api_name, args)
        else:
            # Return error for replanning
            return {"error": error_msg}
    
    return response

# Usage
async def main():
    result = await call_api_with_error_handling(
        "my_app",
        "get_data",
        {"param": "value"}
    )
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Key Takeaways

- **Multi-Level Error Detection:** Errors can be detected at multiple levels: tool execution (connection errors, tool failures), code execution (syntax errors, runtime exceptions), API responses (error status codes), and output validation (schema mismatches). Detection should also check output content for error indicators.

- **Error Classification:** Classify errors by type (syntax, runtime, connection, validation) and severity (low, medium, high, critical) to determine appropriate handling strategies. Transient errors (timeouts, connection failures) should be retried, while permanent errors require different strategies.

- **Retry Logic:** Implement automatic retry mechanisms for transient errors with exponential backoff. Retries can be applied at tool execution, API calls, and structured output validation levels. Session reconnection should be attempted for connection errors before retrying operations.

- **Error Propagation:** Route errors to appropriate handlers based on context. For sub-tasks, propagate errors to plan controller for replanning. For critical errors, escalate to human-in-the-loop. Update execution history with error information for context.

- **Recovery Strategies:** Different errors require different recovery strategies:
  - **Retry:** For transient errors (timeouts, connection failures)
  - **Replan:** For execution errors in sub-tasks (return to plan controller)
  - **Fallback:** Use alternative tools or methods when primary fails
  - **Escalation:** Route critical errors to human operators

- **State Management:** Update execution history with error information, preserve partial results when possible, and mark failed subtasks in plan progress. This enables the plan controller to make informed decisions about replanning.

- **Best Practice:** Implement comprehensive error detection at all levels, automatic retry for transient errors, error propagation to appropriate handlers, and state updates for context preservation. Use structured output validation with automatic retry.

- **Common Pitfall:** Failing to handle exceptions leads to fragile agents that crash on unexpected errors. Not detecting errors in output content can allow errors to propagate undetected. Always implement error handling at tool, code, and validation levels.

- **Performance Note:** Exception handling adds overhead but is essential for reliability. Optimize detection paths and use efficient error classification to minimize performance impact. Retry logic should have reasonable limits to avoid infinite loops.

## Related Patterns

This pattern works well with:
- **Reflection** - Exception handling can trigger reflective analysis to improve future attempts
- **Human-in-the-Loop** - Critical errors can be escalated to human operators
- **Goal Setting and Monitoring** - Exception handling ensures agents can recover and continue toward goals

This pattern is often combined with:
- **Tool Use** - Tool failures require exception handling and recovery
- **Planning** - Exceptions may trigger plan revision and replanning

??? "References"

- Code Complete by Steve McConnell
- Fault Tolerance in Multi-Agent Systems: https://arxiv.org/abs/2412.00534
- Google ADK Agents: https://google.github.io/adk-docs/agents/

