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
- **Error Detection:** Meticulously identifying operational issues as they arise, including invalid tool outputs, API errors, timeouts, or incoherent responses.
- **Error Handling:** Response plans including logging, retries, fallbacks, graceful degradation, and notifications.
- **Recovery:** Restoring the agent to stable operation through state rollback, diagnosis, self-correction, or escalation.
- **Proactive Preparation:** Anticipating potential issues and developing strategies to mitigate them before they occur.
- **Reactive Strategies:** Responding to errors as they occur with appropriate handling mechanisms.

### How It Works
Exception Handling and Recovery operates through a three-stage process: (1) Error Detection—the system identifies operational issues through validation, monitoring, or anomaly detection, (2) Error Handling—once detected, errors are handled through logging, retries, fallbacks, graceful degradation, or notifications, (3) Recovery—the system restores stable operation through state rollback, diagnosis, self-correction, replanning, or escalation to human operators.

Error detection involves validating tool outputs, checking API error codes, monitoring response times, and identifying incoherent responses. Monitoring by other agents or specialized monitoring systems enables proactive anomaly detection. Error handling strategies include logging for debugging, retrying with adjusted parameters for transient errors, using alternative strategies (fallbacks), maintaining partial functionality (graceful degradation), and alerting human operators (notifications). Recovery mechanisms include state rollback to undo error effects, diagnosis to investigate causes, self-correction through plan adjustment, and escalation for complex or severe cases.

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

### Prerequisites
```bash
pip install langchain langchain-openai
# or
pip install google-adk
```

### Basic Example
```python
from langchain_openai import ChatOpenAI
from typing import Dict, Optional
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RobustAgent:
    def __init__(self, max_retries: int = 3):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.max_retries = max_retries
    
    def execute_with_retry(self, tool_call: str, params: Dict) -> Optional[Dict]:
        """Execute tool call with retry logic."""
        for attempt in range(self.max_retries):
            try:
                result = self._execute_tool(tool_call, params)
                if self._validate_result(result):
                    return result
                else:
                    logger.warning(f"Invalid result on attempt {attempt + 1}")
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return self._fallback_operation(tool_call, params)
        return None
    
    def _execute_tool(self, tool_call: str, params: Dict) -> Dict:
        """Execute tool (simulated)."""
        # In production, actual tool execution
        if "error" in params.get("simulate", ""):
            raise Exception("Simulated error")
        return {"status": "success", "data": "result"}
    
    def _validate_result(self, result: Dict) -> bool:
        """Validate tool result."""
        return result.get("status") == "success" and "data" in result
    
    def _fallback_operation(self, tool_call: str, params: Dict) -> Dict:
        """Fallback operation when primary fails."""
        logger.info(f"Using fallback for {tool_call}")
        return {"status": "fallback", "message": "Used alternative method"}

# Usage
agent = RobustAgent()
result = agent.execute_with_retry("database_query", {"query": "SELECT * FROM users"})
```

**Explanation:**
This example demonstrates basic exception handling with retry logic, validation, and fallback mechanisms. The agent retries failed operations with exponential backoff, validates results, and falls back to alternative operations when primary methods fail. This ensures robust operation despite transient failures.

### Advanced Example
```python
from langchain_openai import ChatOpenAI
from typing import Dict, List, Optional, Callable
import json
import logging
from enum import Enum

class ErrorSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ExceptionHandler:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.error_log = []
        self.recovery_strategies = {}
    
    def handle_exception(self, error: Exception, context: Dict) -> Dict:
        """Comprehensive exception handling."""
        # Log error
        error_entry = {
            "error": str(error),
            "type": type(error).__name__,
            "context": context,
            "timestamp": time.time(),
            "severity": self._assess_severity(error, context)
        }
        self.error_log.append(error_entry)
        logger.error(f"Exception: {error_entry}")
        
        # Determine recovery strategy
        strategy = self._determine_recovery_strategy(error, context)
        
        # Execute recovery
        recovery_result = self._execute_recovery(strategy, error, context)
        
        return {
            "error": error_entry,
            "strategy": strategy,
            "recovery": recovery_result
        }
    
    def _assess_severity(self, error: Exception, context: Dict) -> ErrorSeverity:
        """Assess error severity."""
        error_str = str(error).lower()
        if "critical" in error_str or "fatal" in error_str:
            return ErrorSeverity.CRITICAL
        elif "timeout" in error_str or "connection" in error_str:
            return ErrorSeverity.HIGH
        elif "validation" in error_str or "format" in error_str:
            return ErrorSeverity.MEDIUM
        else:
            return ErrorSeverity.LOW
    
    def _determine_recovery_strategy(self, error: Exception, context: Dict) -> str:
        """Determine appropriate recovery strategy."""
        error_type = type(error).__name__
        error_str = str(error).lower()
        
        # Retry for transient errors
        if "timeout" in error_str or "connection" in error_str:
            return "retry"
        
        # Fallback for service errors
        if "service" in error_str or "api" in error_str:
            return "fallback"
        
        # Self-correction for logic errors
        if "validation" in error_str or "invalid" in error_str:
            return "self_correct"
        
        # Escalation for critical errors
        if self._assess_severity(error, context) == ErrorSeverity.CRITICAL:
            return "escalate"
        
        return "log_and_continue"
    
    def _execute_recovery(self, strategy: str, error: Exception, context: Dict) -> Dict:
        """Execute recovery strategy."""
        if strategy == "retry":
            return self._retry_operation(context)
        elif strategy == "fallback":
            return self._fallback_operation(context)
        elif strategy == "self_correct":
            return self._self_correct(context)
        elif strategy == "escalate":
            return self._escalate_to_human(error, context)
        else:
            return {"status": "logged", "action": "continue"}
    
    def _retry_operation(self, context: Dict) -> Dict:
        """Retry failed operation."""
        max_retries = context.get("max_retries", 3)
        for i in range(max_retries):
            try:
                # Retry logic
                return {"status": "retried", "attempt": i + 1}
            except Exception as e:
                if i == max_retries - 1:
                    return {"status": "retry_failed", "error": str(e)}
                time.sleep(2 ** i)
        return {"status": "retry_exhausted"}
    
    def _fallback_operation(self, context: Dict) -> Dict:
        """Use fallback operation."""
        fallback = context.get("fallback")
        if fallback:
            return {"status": "fallback_used", "method": fallback}
        return {"status": "no_fallback_available"}
    
    def _self_correct(self, context: Dict) -> Dict:
        """Self-correct based on error analysis."""
        prompt = f"""Analyze this error and suggest correction:
        Error: {context.get('error')}
        Context: {json.dumps(context)}
        Provide corrected approach."""
        
        response = self.llm.invoke(prompt)
        return {"status": "self_corrected", "correction": response.content}
    
    def _escalate_to_human(self, error: Exception, context: Dict) -> Dict:
        """Escalate to human operator."""
        # In production, send to human queue
        return {
            "status": "escalated",
            "message": f"Critical error escalated: {error}",
            "context": context
        }

# Usage
handler = ExceptionHandler()
try:
    # Operation that might fail
    result = risky_operation()
except Exception as e:
    recovery = handler.handle_exception(e, {"operation": "risky_operation"})
    print(f"Recovery: {recovery}")
```

**Explanation:**
This advanced example implements comprehensive exception handling with severity assessment, strategy determination, and multiple recovery mechanisms. It demonstrates production-ready error handling with logging, retry logic, fallbacks, self-correction, and escalation capabilities.

### Framework-Specific Examples

#### Google ADK Sequential Agent with Fallback
```python
from google.adk.agents import Agent, SequentialAgent

# Primary handler
primary_handler = Agent(
    name="primary_handler",
    model="gemini-2.0-flash",
    instruction="Use get_precise_location_info tool with user's address.",
    tools=[get_precise_location_info]
)

# Fallback handler
fallback_handler = Agent(
    name="fallback_handler",
    model="gemini-2.0-flash",
    instruction="""Check state['primary_location_failed'].
    If True, use get_general_area_info tool.
    If False, do nothing.""",
    tools=[get_general_area_info]
)

# Response agent
response_agent = Agent(
    name="response_agent",
    model="gemini-2.0-flash",
    instruction="Present location info from state['location_result'].",
    tools=[]
)

# Sequential agent with fallback
robust_agent = SequentialAgent(
    name="robust_location_agent",
    sub_agents=[primary_handler, fallback_handler, response_agent]
)
```

#### LangChain with Error Handling
```python
from langchain.agents import AgentExecutor
from langchain_openai import ChatOpenAI

def safe_execute(agent_executor, input_data):
    """Execute agent with error handling."""
    try:
        return agent_executor.invoke(input_data)
    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        # Fallback response
        return {
            "output": "I encountered an error. Let me try an alternative approach.",
            "error": str(e)
        }
```

## Key Takeaways

- **Core Concept:** Exception Handling and Recovery is essential for building robust and reliable agents that can operate effectively in unpredictable environments.
- **Best Practice:** Implement comprehensive error detection, logging, retry logic, fallbacks, and recovery mechanisms for production systems.
- **Common Pitfall:** Failing to handle exceptions leads to fragile agents that crash on unexpected errors; always implement error handling.
- **Performance Note:** Exception handling adds overhead but is essential for reliability; optimize detection and recovery paths for performance.

## Related Patterns

This pattern works well with:
- **Reflection** - Exception handling can trigger reflective analysis to improve future attempts
- **Human-in-the-Loop** - Critical errors can be escalated to human operators
- **Goal Setting and Monitoring** - Exception handling ensures agents can recover and continue toward goals

This pattern is often combined with:
- **Tool Use** - Tool failures require exception handling and recovery
- **Planning** - Exceptions may trigger plan revision and replanning

## References

- Code Complete by Steve McConnell
- Fault Tolerance in Multi-Agent Systems: https://arxiv.org/abs/2412.00534
- Google ADK Agents: https://google.github.io/adk-docs/agents/

