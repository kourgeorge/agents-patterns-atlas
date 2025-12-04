# Pattern: Human-in-the-Loop

## Motivation

Apprentices learn under a master's guidance. Surgeons have assistants for critical steps. Editors review writers' work before publication. Humans naturally incorporate oversight, feedback, and collaboration into complex processes. The Human-in-the-Loop pattern brings this to agents: integrating human judgment, feedback, and decision-making into agent workflows for safety, quality, and trust, especially in high-stakes situations.

## Pattern Overview
**What it is:** Human-in-the-Loop (HITL) is a pattern that strategically integrates human oversight, judgment, and intervention into AI agent workflows, creating a symbiotic partnership between human intelligence and AI capabilities.

**When to use:** Use this pattern when deploying AI in domains where errors have significant safety, ethical, or financial consequences, such as healthcare, finance, or autonomous systems. It is essential for tasks involving ambiguity and nuance that LLMs cannot reliably handle.

**Why it matters:** AI systems, including advanced LLMs, often struggle with tasks that require nuanced judgment, ethical reasoning, or a deep understanding of complex, ambiguous contexts. Deploying fully autonomous AI in high-stakes environments carries significant risks, as errors can lead to severe safety, financial, or ethical consequences. HITL ensures that AI operates within ethical boundaries, adheres to safety protocols, and achieves objectives with optimal effectiveness.

The Human-in-the-Loop pattern represents a pivotal strategy in the development and deployment of Agents. It deliberately interweaves the unique strengths of human cognition—such as judgment, creativity, and nuanced understanding—with the computational power and efficiency of AI. This strategic integration is not merely an option but often a necessity, especially as AI systems become increasingly embedded in critical decision-making processes.

HITL acknowledges that even with rapidly advancing AI technologies, human oversight, strategic input, and collaborative interactions remain indispensable. The approach fundamentally revolves around the idea of synergy between artificial and human intelligence. Rather than viewing AI as a replacement for human workers, HITL positions AI as a tool that augments and enhances human capabilities. This augmentation can take various forms, from automating routine tasks to providing data-driven insights that inform human decisions.

HITL encompasses several key aspects: Human Oversight (monitoring AI performance and output), Intervention and Correction (humans rectifying errors or guiding agents), Human Feedback for Learning (collecting feedback to refine models), Decision Augmentation (AI provides analysis, humans make final decisions), Human-Agent Collaboration (cooperative interaction leveraging respective strengths), and Escalation Policies (protocols for when agents should escalate to humans).

### Key Concepts
- **Interruptible Workflow:** The agent workflow can be paused at specific nodes to request human input, approval, or guidance.
- **Human Oversight:** Monitoring AI agent performance and output to ensure adherence to guidelines and prevent undesirable outcomes.
- **Intervention and Correction:** Human operators rectifying errors, supplying missing data, or guiding agents when they encounter problems.
- **Action Handlers:** Different types of human interactions (confirmations, text input, selections) with corresponding handlers that process responses and route workflow accordingly.
- **State Preservation:** Agent state is preserved during workflow pauses, enabling seamless resumption after human response.
- **Configurable Approval Points:** Workflow can be configured to interrupt at specific nodes (after tool calls, before critical actions, etc.) for human approval.
- **Human Feedback for Learning:** Collecting and using human feedback to refine AI models, prominently in reinforcement learning with human feedback.
- **Decision Augmentation:** AI provides analyses and recommendations, humans make final decisions, enhancing decision-making through AI-generated insights.
- **Escalation Policies:** Established protocols dictating when and how agents should escalate tasks to human operators.

### How It Works

HITL works through an **interruptible workflow pattern** that strategically pauses agent execution at configurable approval points:

**1. Workflow Interruption**
When an agent determines human input is needed, it creates a `FollowUpAction` specifying:
- **Action Type:** The type of interaction needed (confirmation, text input, selection, etc.)
- **Action Description:** What the human needs to do or decide
- **Return Point:** Which node to return to after human response

**2. Suggest Human Actions**
The `SuggestHumanActions` node:
- Receives the action request from the agent
- Adds it to the conversation history
- Routes to `WaitForResponse` node

**3. Wait for Response**
The `WaitForResponse` node:
- Uses graph interrupts to pause workflow execution
- Preserves complete agent state (variables, history, context)
- Waits for human response via the interrupt mechanism
- Captures the human's response in `ActionResponse` format

**4. Resume with Response**
After receiving human response:
- State is restored with the human's input
- Action handlers process the response based on `action_id`
- Workflow resumes at the appropriate node (typically the node that requested the interruption)

**5. Action Handlers**
Different action types have corresponding handlers:
- **Confirmation Actions:** Approve/reject decisions (e.g., tool execution, flow approval)
- **Text Input Actions:** Natural language responses, additional information
- **Selection Actions:** Choose from predefined options
- **Custom Actions:** Domain-specific handlers for specialized workflows

**Implementation Components:**

- **SuggestHumanActions Node:** Initiates human interaction, routes to wait node
- **WaitForResponse Node:** Pauses workflow using graph interrupts, preserves state
- **InterruptToolNode:** Special interrupt point after tool calls for approval
- **Action Handlers:** Process human responses and route workflow accordingly

**State Preservation:**
The complete agent state (messages, variables, execution history, context) is preserved during the pause, ensuring seamless resumption. The workflow can resume exactly where it left off, with the human's response incorporated into the state.

**Configurable Approval Points:**
Approval points can be configured at:
- After tool/API calls (via `InterruptToolNode`)
- Before critical actions (via agent decision to escalate)
- At specific workflow nodes (via conditional routing)
- Based on confidence thresholds or policy violations

## Benefits

The interruptible workflow pattern provides several key benefits:

- **Safety and Compliance:** Human approval at critical points ensures compliance with regulations, safety protocols, and ethical guidelines. Critical actions (e.g., financial transactions, medical decisions) can be reviewed before execution.

- **User Control:** Users maintain control over agent behavior, approving or rejecting actions, providing guidance, and making final decisions. This builds trust and ensures alignment with user intent.

- **Error Recovery:** When agents encounter errors or ambiguous situations, human intervention can provide correction, additional context, or alternative approaches, enabling graceful error recovery.

- **Policy Enforcement:** Approval points can enforce organizational policies, ensuring agents don't violate constraints or exceed authority. Policy violations trigger human review automatically.

- **Quality Assurance:** Human review of outputs ensures quality standards are met, especially for high-stakes or public-facing content. Review workflows can catch errors before they impact users.

- **Learning and Adaptation:** Human feedback collected during HITL interactions can be used to improve agent behavior, refine policies, and enhance future autonomous performance.

## When to Use This Pattern

### ✅ Use this pattern when:
- **High-stakes decisions:** Errors have significant safety, ethical, or financial consequences.
- **Ambiguous scenarios:** Tasks involve nuance and ambiguity that LLMs cannot reliably handle.
- **Ethical considerations:** Decisions require ethical reasoning or moral judgment.
- **Quality requirements:** Outputs must meet high quality standards requiring human validation.
- **Learning from feedback:** You want to continuously improve AI models with high-quality human-labeled data.

### ❌ Avoid this pattern when:
- **High-volume, low-stakes tasks:** The task requires scale that human oversight cannot provide.
- **Real-time constraints:** Human intervention adds unacceptable latency for time-sensitive applications.
- **Simple, deterministic tasks:** The task is straightforward enough that AI can handle it autonomously.
- **Cost constraints:** Human oversight is too expensive for the use case.
- **Privacy concerns:** Sensitive information cannot be exposed to human operators.

### Decision Guidelines
Use HITL when the benefits of human judgment and oversight outweigh the costs of reduced scalability and increased latency. Consider: the criticality of decisions (more critical = more need for HITL), the ambiguity of tasks (more ambiguous = more need for HITL), and the availability of human expertise (expertise available = effective HITL). Be aware that HITL has significant caveats: lack of scalability, dependence on skilled operators, and privacy concerns requiring data anonymization. For production systems, implement hybrid approaches combining automation for scale with HITL for accuracy.

## Practical Applications & Use Cases

The Human-in-the-Loop pattern is vital across a wide range of industries and applications, particularly where accuracy, safety, ethics, or nuanced understanding are paramount.

- **Content Moderation:** AI filters content rapidly, but ambiguous or borderline cases are escalated to human moderators for nuanced judgment.
- **Autonomous Driving:** Self-driving cars handle most tasks autonomously but hand over control to human drivers in complex or dangerous situations.
- **Financial Fraud Detection:** AI flags suspicious transactions, but high-risk or ambiguous alerts are sent to human analysts for investigation and final determination.
- **Legal Document Review:** AI scans and categorizes documents, but human legal professionals review findings for accuracy, context, and legal implications.
- **Customer Support:** Chatbots handle routine inquiries, but complex or emotionally charged issues are seamlessly handed over to human support agents.
- **Data Labeling:** Humans accurately label images, text, or audio to provide ground truth for AI training.
- **Generative AI Refinement:** Human editors review and refine AI-generated creative content to ensure it meets brand guidelines and quality standards.

## Implementation

### Core Components

**Interruptible Workflow Pattern:**

```python
from typing import Literal, Optional, List, TypedDict, Any
from enum import Enum
from pydantic import BaseModel, Field
from langgraph.types import Command, interrupt
from langchain_core.messages import AIMessage

class ActionType(str, Enum):
    """Types of human interactions."""
    CONFIRMATION = "confirmation"
    NATURAL_LANGUAGE = "natural_language"
    TEXT_INPUT = "text_input"
    SELECT = "select"
    MULTI_SELECT = "multi_select"

class SelectOption(BaseModel):
    """Option for select actions."""
    value: str
    label: str

class FollowUpAction(BaseModel):
    """Action request for human input."""
    action_id: str
    action_name: str
    description: str
    type: ActionType
    options: Optional[List[SelectOption]] = None
    placeholder: Optional[str] = None
    button_text: Optional[str] = None

class ActionResponse(BaseModel):
    """Human response to action request."""
    action_id: str
    response_type: ActionType
    text_response: Optional[str] = None
    confirmed: Optional[bool] = None
    selected_values: Optional[List[str]] = None

class AgentState(TypedDict, total=False):
    """Agent state with HITL support."""
    messages: List[AIMessage]
    hitl_action: Optional[FollowUpAction]
    hitl_response: Optional[ActionResponse]
    sender: str
    tool_call: Optional[dict]
    next_action: Optional[dict]
    context: Dict[str, Any]

# Usage
action = FollowUpAction(
    action_id="approve_tool",
    action_name="Approve Tool",
    description="Approve execution?",
    type=ActionType.CONFIRMATION,
    button_text="Approve"
)
print(f"Created action: {action.action_name}")
```

**SuggestHumanActions Node:**

```python
from langgraph.types import Command
from langchain_core.messages import AIMessage

class SuggestHumanActions:
    """Node that initiates human interaction."""
    
    @staticmethod
    async def node_handler(state: AgentState) -> Command:
        """Handle suggest human actions node."""
        if not state.get("hitl_action"):
            raise ValueError("hitl_action must be set before SuggestHumanActions")
        
        # Add action to conversation history
        state["messages"].append(AIMessage(
            content=state["hitl_action"].model_dump_json()
        ))
        
        # Route to wait node
        return Command(update=state, goto="WaitForResponse")

# Usage
state: AgentState = {
    "messages": [],
    "hitl_action": FollowUpAction(
        action_id="approve",
        action_name="Approve",
        description="Approve this action?",
        type=ActionType.CONFIRMATION
    ),
    "hitl_response": None,
    "sender": "PlannerAgent",
    "tool_call": None
}
command = await SuggestHumanActions.node_handler(state)
```

**WaitForResponse Node:**

```python
from langgraph.types import Command, interrupt

class WaitForResponse:
    """Node that pauses workflow for human response."""
    
    @staticmethod
    async def node_handler(state: AgentState) -> Command:
        """Handle wait for response node."""
        if not state.get("hitl_action"):
            raise ValueError("hitl_action must be set before WaitForResponse")
        
        # Interrupt workflow - preserves state automatically
        # In real implementation, this pauses and waits for human input
        response_data = interrupt(state["hitl_action"].model_dump())
        
        # Parse human response
        state["hitl_response"] = ActionResponse(**response_data)
        
        # Clear action (response is now in hitl_response)
        prev_sender = state.get("sender", "PlannerAgent")
        state["sender"] = "WaitForResponse"
        
        # Return to previous node that requested interruption
        return Command(update=state, goto=prev_sender)

# Usage (in real workflow, interrupt() would pause and wait)
# state["hitl_action"] = action
# command = await WaitForResponse.node_handler(state)
```

**InterruptToolNode:**

```python
from langchain_core.messages import AIMessage

class InterruptToolNode:
    """Special interrupt point after tool calls."""
    
    @staticmethod
    async def node_handler(state: AgentState) -> AgentState:
        """Handle interrupt tool node."""
        # Tool call was interrupted, restore it
        if state.get("tool_call"):
            msg = AIMessage(content="", tool_calls=[state["tool_call"]])
            state["messages"].append(msg)
            state["tool_call"] = None
        return state

# Usage
state: AgentState = {
    "messages": [],
    "hitl_action": None,
    "hitl_response": None,
    "sender": "ActionAgent",
    "tool_call": {"name": "execute_task", "args": {"task": "process"}}
}
state = await InterruptToolNode.node_handler(state)
```

**Action Handlers:**

```python
from typing import Callable
from langgraph.types import Command

class ActionHandler:
    """Processes human responses and routes workflow."""
    
    def __init__(self):
        self.handlers: dict[str, Callable] = {
            "approve_tool": self._handle_approval,
            "consult_human": self._handle_consultation,
            "save_reuse": self._handle_save_reuse,
        }
    
    def handle(self, state: AgentState, node_name: str) -> Command:
        """Route based on action_id."""
        if not state.get("hitl_response"):
            raise ValueError("hitl_response must be set")
        
        action_id = state["hitl_response"].action_id
        
        if action_id in self.handlers:
            return self.handlers[action_id](state, node_name)
        
        # Default: return to previous node
        return Command(update=state, goto=state.get("sender", "PlannerAgent"))
    
    def _handle_approval(self, state: AgentState, node_name: str) -> Command:
        """Handle tool execution approval."""
        if state["hitl_response"].confirmed:
            # Execute approved tool
            return Command(update=state, goto="ExecuteTool")
        else:
            # Reject, return to planner
            return Command(update=state, goto="PlannerAgent")
    
    def _handle_consultation(self, state: AgentState, node_name: str) -> Command:
        """Handle human consultation response."""
        # Use human's guidance
        guidance = state["hitl_response"].text_response
        # Store guidance in state for use by planner
        return Command(update=state, goto="PlannerAgent")
    
    def _handle_save_reuse(self, state: AgentState, node_name: str) -> Command:
        """Handle save/reuse action."""
        return Command(update=state, goto="ReuseAgent")

# Usage
handler = ActionHandler()
state["hitl_response"] = ActionResponse(
    action_id="approve_tool",
    response_type=ActionType.CONFIRMATION,
    confirmed=True
)
command = handler.handle(state, "PlannerAgent")
```

### Basic Example: Interruptible Workflow

```python
import asyncio
from langgraph.types import Command
from langchain_core.messages import AIMessage

def requires_approval(action: dict) -> bool:
    """Determine if action requires human approval."""
    # Example: require approval for critical actions
    critical_actions = ["delete", "transfer", "purchase"]
    return any(critical in action.get("name", "").lower() for critical in critical_actions)

# Agent determines human approval needed
async def planner_node(state: AgentState) -> Command:
    """Planner node that may request human approval."""
    next_action = state.get("next_action", {})
    
    # Check if tool execution needs approval
    if requires_approval(next_action):
        # Create action request
        state["hitl_action"] = FollowUpAction(
            action_id="approve_tool",
            action_name="Approve Tool Execution",
            description="Approve execution of this tool?",
            type=ActionType.CONFIRMATION,
            button_text="Approve"
        )
        state["sender"] = "PlannerAgent"
        return Command(update=state, goto="SuggestHumanActions")
    
    # Continue autonomously
    return Command(update=state, goto="ExecuteTool")

# SuggestHumanActions node
async def suggest_actions_node(state: AgentState) -> Command:
    """Node that suggests human actions."""
    if not state.get("hitl_action"):
        raise ValueError("hitl_action must be set")
    
    # Add action to history
    state["messages"].append(AIMessage(
        content=state["hitl_action"].model_dump_json()
    ))
    return Command(update=state, goto="WaitForResponse")

# WaitForResponse node - pauses workflow
async def wait_for_response_node(state: AgentState) -> Command:
    """Node that waits for human response."""
    if not state.get("hitl_action"):
        raise ValueError("hitl_action must be set")
    
    # Interrupt preserves state automatically
    # In real implementation, this pauses and waits
    response_data = interrupt(state["hitl_action"].model_dump())
    state["hitl_response"] = ActionResponse(**response_data)
    
    # Return to node that requested interruption
    prev_sender = state.get("sender", "PlannerAgent")
    return Command(update=state, goto=prev_sender)

# Action handler processes response
async def handle_response(state: AgentState) -> Command:
    """Handle human response and route workflow."""
    handler = ActionHandler()
    return handler.handle(state, "PlannerAgent")

# Usage example
async def example_workflow():
    state: AgentState = {
        "messages": [],
        "hitl_action": None,
        "hitl_response": None,
        "sender": "PlannerAgent",
        "tool_call": None,
        "next_action": {"name": "delete_file"}  # Critical action
    }
    
    # Planner determines approval needed
    command = await planner_node(state)
    print(f"Planner routed to: {command.goto}")
    
    # Suggest actions
    if command.goto == "SuggestHumanActions":
        command = await suggest_actions_node(state)
        print(f"Suggested actions, routing to: {command.goto}")

# Run: asyncio.run(example_workflow())
```

**Explanation:**
This demonstrates the interruptible workflow pattern. The planner creates an action request, SuggestHumanActions routes to WaitForResponse, which pauses the workflow. After human response, the handler processes it and routes back to the appropriate node.

### Advanced Example: Multiple Action Types

```python
from typing import Dict, Any, Callable
from langgraph.types import Command

# Confirmation action (approve/reject)
async def request_approval(state: AgentState) -> Command:
    """Request approval for an action."""
    state["hitl_action"] = FollowUpAction(
        action_id="approve_tool",
        action_name="Approve Tool",
        description="Approve execution?",
        type=ActionType.CONFIRMATION,
        button_text="Approve"
    )
    state["sender"] = "PlannerAgent"
    return Command(update=state, goto="SuggestHumanActions")

# Natural language consultation
async def consult_human(state: AgentState) -> Command:
    """Request human consultation."""
    state["hitl_action"] = FollowUpAction(
        action_id="consult_human",
        action_name="Human Consultation",
        description="How should I proceed?",
        type=ActionType.NATURAL_LANGUAGE,
        placeholder="Provide guidance..."
    )
    state["sender"] = "PlannerAgent"
    return Command(update=state, goto="SuggestHumanActions")

# Selection action (choose from options)
async def request_selection(state: AgentState) -> Command:
    """Request selection from options."""
    state["hitl_action"] = FollowUpAction(
        action_id="select_option",
        action_name="Choose Approach",
        description="Which approach should I use?",
        type=ActionType.SELECT,
        options=[
            SelectOption(value="approach_a", label="Approach A"),
            SelectOption(value="approach_b", label="Approach B")
        ]
    )
    state["sender"] = "PlannerAgent"
    return Command(update=state, goto="SuggestHumanActions")

# Action handler with multiple handlers
class AdvancedActionHandler:
    """Advanced handler supporting multiple action types."""
    
    def __init__(self):
        self.handlers: Dict[str, Callable[[AgentState], Command]] = {
            "approve_tool": self._handle_approval,
            "consult_human": self._handle_consultation,
            "select_option": self._handle_selection,
        }
    
    def handle(self, state: AgentState) -> Command:
        """Route based on action_id."""
        if not state.get("hitl_response"):
            raise ValueError("hitl_response must be set")
        
        action_id = state["hitl_response"].action_id
        
        if action_id not in self.handlers:
            # Default: return to sender
            return Command(update=state, goto=state.get("sender", "PlannerAgent"))
        
        return self.handlers[action_id](state)
    
    def _handle_approval(self, state: AgentState) -> Command:
        """Handle approval response."""
        if state["hitl_response"].confirmed:
            return Command(update=state, goto="ExecuteTool")
        return Command(update=state, goto="PlannerAgent")
    
    def _handle_consultation(self, state: AgentState) -> Command:
        """Handle consultation response."""
        # Use human's text response
        guidance = state["hitl_response"].text_response
        
        # Store guidance in state (would need to extend AgentState)
        if "context" not in state:
            state["context"] = {}
        state["context"]["human_guidance"] = guidance
        
        return Command(update=state, goto="PlannerAgent")
    
    def _handle_selection(self, state: AgentState) -> Command:
        """Handle selection response."""
        # Use selected option
        if not state["hitl_response"].selected_values:
            raise ValueError("No selection made")
        
        selected = state["hitl_response"].selected_values[0]
        
        # Store selection in state
        if "context" not in state:
            state["context"] = {}
        state["context"]["selected_approach"] = selected
        
        return Command(update=state, goto="PlannerAgent")

# Usage
handler = AdvancedActionHandler()

# Example: Handle approval response
state: AgentState = {
    "messages": [],
    "hitl_action": None,
    "hitl_response": ActionResponse(
        action_id="approve_tool",
        response_type=ActionType.CONFIRMATION,
        confirmed=True
    ),
    "sender": "PlannerAgent",
    "tool_call": None,
    "context": {}
}
command = handler.handle(state)
print(f"Routed to: {command.goto}")
```

### Example: Interrupt After Tool Call

```python
from langgraph.graph import StateGraph
from langchain_core.messages import AIMessage

def needs_approval(state: AgentState) -> bool:
    """Check if current state needs approval."""
    # Example: require approval for tool calls
    return state.get("tool_call") is not None

# InterruptToolNode - special interrupt point
async def interrupt_tool_node(state: AgentState) -> AgentState:
    """Handle interrupt after tool call."""
    # Tool call was interrupted, restore it
    if state.get("tool_call"):
        msg = AIMessage(content="", tool_calls=[state["tool_call"]])
        state["messages"].append(msg)
        state["tool_call"] = None
    return state

async def action_node(state: AgentState) -> AgentState:
    """Example action node that may create tool calls."""
    # Simulate creating a tool call
    state["tool_call"] = {"name": "execute_task", "args": {"task": "process"}}
    return state

# Configure graph to interrupt after tool calls
def create_graph_with_interrupts():
    """Create graph with interrupt points."""
    graph = StateGraph(AgentState)
    graph.add_node("action_agent", action_node)
    graph.add_node("interrupt_tool", interrupt_tool_node)
    
    # Interrupt after action agent
    graph.add_edge("action_agent", "interrupt_tool")
    graph.add_conditional_edges(
        "interrupt_tool",
        lambda s: "suggest_actions" if needs_approval(s) else "continue"
    )
    return graph

# Usage
# graph = create_graph_with_interrupts()
# compiled = graph.compile()
```

### Workflow Integration

```python
from langgraph.graph import StateGraph, END
from typing import Callable

def requires_approval(state: AgentState) -> bool:
    """Check if approval is required."""
    return state.get("hitl_action") is not None

async def executor_node(state: AgentState) -> AgentState:
    """Example executor node."""
    # Execute action
    return state

async def handle_response_node(state: AgentState) -> AgentState:
    """Handle human response."""
    handler = ActionHandler()
    command = handler.handle(state, "PlannerAgent")
    # In real implementation, would route based on command
    return state

# Complete HITL workflow
def create_hitl_workflow():
    """Create complete HITL workflow graph."""
    graph = StateGraph(AgentState)
    
    # Add HITL nodes
    graph.add_node("suggest_actions", suggest_actions_node)
    graph.add_node("wait_response", wait_for_response_node)
    graph.add_node("interrupt_tool", interrupt_tool_node)
    graph.add_node("handle_response", handle_response_node)
    
    # Regular workflow nodes
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    
    # Conditional routing with HITL
    graph.add_conditional_edges(
        "planner",
        lambda s: "suggest_actions" if requires_approval(s) else "executor"
    )
    
    # HITL flow
    graph.add_edge("suggest_actions", "wait_response")
    graph.add_edge("wait_response", "handle_response")
    graph.add_edge("handle_response", "planner")  # Return to planner after handling
    
    # Interrupt after tool calls
    graph.add_edge("executor", "interrupt_tool")
    graph.add_conditional_edges(
        "interrupt_tool",
        lambda s: "suggest_actions" if requires_approval(s) else "planner"
    )
    
    # Set entry point
    graph.set_entry_point("planner")
    
    return graph

# Usage
# graph = create_hitl_workflow()
# compiled = graph.compile()
# result = await compiled.ainvoke(initial_state)
```

**Key Integration Points:**
- **Configurable Interrupts:** Set approval points at specific nodes
- **State Preservation:** Complete state preserved during pause
- **Action Handlers:** Route workflow based on human response type
- **Resume Logic:** Return to appropriate node after human input

## Key Takeaways

- **Interruptible Workflow Pattern:** HITL uses an interruptible workflow that pauses execution at configurable approval points, preserving complete agent state during the pause for seamless resumption.

- **Core Components:**
  - **SuggestHumanActions:** Initiates human interaction, routes to wait node
  - **WaitForResponse:** Pauses workflow using graph interrupts, preserves state
  - **InterruptToolNode:** Special interrupt point after tool calls for approval
  - **Action Handlers:** Process human responses and route workflow based on action type

- **Action Types:** Support multiple interaction types (confirmation, text input, selection) with corresponding handlers that process responses and route workflow accordingly.

- **State Preservation:** Complete agent state (messages, variables, execution history, context) is preserved during workflow pauses, enabling seamless resumption after human response.

- **Configurable Approval Points:** Approval points can be configured at specific nodes (after tool calls, before critical actions, based on confidence thresholds) to balance automation with human oversight.

- **Best Practice:** Implement clear escalation policies, confidence thresholds, and action handlers for effective HITL. Use different action types based on the type of human input needed.

- **Common Pitfall:** HITL lacks scalability and depends on skilled operators; use hybrid approaches combining automation with selective human oversight at critical decision points.

- **Performance Note:** HITL adds latency and cost but is essential for high-stakes applications requiring human judgment, safety compliance, and error recovery. The interruptible pattern ensures minimal overhead when human input isn't needed.

## Related Patterns

This pattern works well with:
- **Exception Handling** - Critical errors can be escalated to human operators
- **Guardrails and Safety** - HITL provides human oversight for safety-critical decisions
- **Learning and Adaptation** - Human feedback is used to improve AI models

This pattern is often combined with:
- **Goal Setting and Monitoring** - Human oversight ensures goals are met appropriately
- **Evaluation and Monitoring** - Human review is part of evaluation processes

## References

- A Survey of Human-in-the-loop for Machine Learning: https://arxiv.org/abs/2109.02840
- Google ADK Agents: https://google.github.io/adk-docs/agents/
- LangChain Human Approval: https://python.langchain.com/docs/modules/callbacks/human_approval/

