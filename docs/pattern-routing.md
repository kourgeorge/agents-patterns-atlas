# Routing

## Motivation

A receptionist listens to each caller and routes them to the right department—sales, support, or billing. A triage nurse assesses patients and directs them to appropriate specialists. We constantly make routing decisions: choosing which tool to use, which person to ask, or which path to take. Routing in agents works the same way: evaluating the situation and directing tasks to the most appropriate handler, tool, or workflow path.

## Pattern Overview
**What it is:** Routing is a mechanism that enables agents to dynamically select between multiple potential actions based on input, state, or conditions, introducing conditional logic into agent workflows.

**When to use:** Use routing when your agent needs to adapt its behavior based on variable inputs, user intent, system state, or the outcome of previous operations, rather than following a fixed sequence.

**Why it matters:** Routing transforms agents from static executors of predetermined sequences into dynamic systems capable of making context-aware decisions. It enables specialization, where different tasks are handled by appropriate sub-agents or tools, improving both accuracy and efficiency.

While sequential processing via prompt chaining is foundational for deterministic, linear workflows, real-world agentic systems often need to arbitrate between multiple potential actions. Routing introduces conditional logic that governs the flow of control to different specialized functions, tools, or sub-processes based on contingent factors such as the state of the environment, user input, or the outcome of a preceding operation.

The core mechanism of routing involves evaluating specific criteria to select from a set of possible subsequent actions. For instance, a customer service agent might first classify an incoming query to determine user intent, then route it to a specialized agent for question-answering, a database retrieval tool for account information, or an escalation procedure for complex issues—rather than defaulting to a single predetermined response pathway.

Routing can be implemented at multiple junctures within an agent's operational cycle: at the outset to classify a primary task, at intermediate points within a processing chain to determine subsequent actions, or during subroutines to select the most appropriate tool from a given set. This flexibility makes routing essential for building adaptive, context-aware agentic systems.

### Key Concepts
- **Dynamic Decision-Making:** Routing enables agents to evaluate conditions and make runtime decisions about execution paths, moving beyond fixed sequences.
- **Intent Classification:** The pattern often begins with classifying user input or system state to determine the appropriate route, enabling specialized handling.
- **Conditional Flow Control:** Routing introduces if-then-else logic into agent workflows, where different conditions lead to different execution paths.
- **Multiple Implementation Methods:** Routing can be achieved through LLM-based analysis, embedding similarity, rule-based logic, or trained ML models, each with different trade-offs.
- **Complexity-Based Routing:** A specialized form of routing that classifies task complexity and routes to appropriate models or tools based on resource constraints, enabling cost-effective optimization by using lightweight models for simple tasks and powerful models for complex ones.

### How It Works
Routing operates through a three-step process: evaluation, decision, and delegation. First, the routing mechanism evaluates the input, state, or condition using one of several methods. LLM-based routing uses the language model to analyze input and output a category or identifier. Embedding-based routing converts input to vectors and compares them to route embeddings using semantic similarity. Rule-based routing uses predefined logic (if-else statements) based on keywords or patterns. ML model-based routing employs a trained classifier to make routing decisions.

Based on this evaluation, the router makes a decision about which route to take. Finally, it delegates the task to the appropriate handler—whether that's a specialized agent, a specific tool, or a different workflow path. The chosen route then receives the original input or a transformed version of it, processes the task, and returns results that may feed back into the routing system for subsequent decisions.

## When to Use This Pattern

### ✅ Use this pattern when:
- **Multiple specialized handlers exist:** You have different agents, tools, or workflows optimized for different types of tasks, and need to direct inputs to the right one.
- **User intent varies significantly:** User queries or inputs can have fundamentally different intents (e.g., booking vs. information vs. support), requiring different processing paths.
- **System state affects behavior:** The agent's behavior should change based on current state, previous outcomes, or environmental conditions.
- **Tool selection is dynamic:** You need to select from multiple available tools based on the task at hand, rather than using a fixed tool sequence.
- **Workflow branching is needed:** Different inputs or conditions require fundamentally different processing workflows, not just parameter variations.
- **Resource optimization is required:** You need to route tasks to different models or tools based on complexity, budget, or performance requirements (e.g., simple queries to fast/cheap models, complex tasks to powerful models).

### ❌ Avoid this pattern when:
- **Sequential processing is sufficient:** If all inputs follow the same processing steps in the same order, prompt chaining is simpler and more appropriate.
- **Routing logic is trivial:** If the routing decision can be made with a simple if-else based on a single, easily extractable feature, consider rule-based routing or even hardcoding the logic.
- **Latency is critical:** Routing adds an extra decision step, which can increase latency. For high-speed, low-latency requirements, consider pre-classification or simpler approaches.

### Decision Guidelines
Choose routing when the benefits of specialization and adaptability outweigh the added complexity. Consider the routing method: LLM-based routing offers flexibility but adds latency and cost; embedding-based routing is fast and semantic but requires pre-computed route embeddings; rule-based routing is deterministic and fast but less flexible; ML model-based routing offers good balance but requires training data. The choice depends on your accuracy requirements, latency constraints, and the complexity of the routing decision.

## Practical Applications & Use Cases

Routing is essential for building adaptive agentic systems that can handle diverse inputs and contexts. Common applications include intent-based request handling, dynamic tool selection, and multi-agent coordination.

- **Customer Service Agents:** Route user queries to specialized handlers for orders, products, support, or general information based on intent classification.
- **Document Processing Pipelines:** Route incoming documents (emails, tickets, forms) to appropriate processing workflows based on content, format, or metadata.
- **Multi-Agent Systems:** Route tasks to specialized agents (researcher, writer, reviewer) based on task type and current workload.
- **AI Coding Assistants:** Route code snippets to different tools based on programming language, intent (debug, explain, translate), or complexity.
- **Content Classification Systems:** Route content to appropriate moderation, analysis, or processing pipelines based on type, topic, or risk level.
- **Resource-Aware Model Routing:** Route requests to different LLM models based on task complexity, budget constraints, or latency requirements. Simple, common questions are routed to fast, cost-efficient models (e.g., Claude Haiku, Gemini Flash), while complex or unusual questions are routed to more capable models (e.g., Claude Sonnet, Gemini Pro). This enables automatic optimization of cost and performance without manual intervention.

## Implementation

### Prerequisites
```bash
pip install langchain langchain-google-genai langgraph
# or
pip install google-adk
```

### Basic Example
```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Define router prompt
router_prompt = ChatPromptTemplate.from_messages([
    ("system", """Analyze the user's request and output ONE word:
    - 'booking' for flight/hotel bookings
    - 'info' for general questions
    - 'support' for technical issues
    Output only: booking, info, or support"""),
    ("user", "{request}")
])

# Define handlers
def booking_handler(request: str) -> str:
    return f"Processing booking: {request}"

def info_handler(request: str) -> str:
    return f"Answering question: {request}"

def support_handler(request: str) -> str:
    return f"Escalating support: {request}"

# Create router chain
router_chain = router_prompt | llm | StrOutputParser()

# Create routing branches
routing_branch = RunnableBranch(
    (lambda x: "booking" in x['decision'].lower(), 
     RunnablePassthrough.assign(output=lambda x: booking_handler(x['request']))),
    (lambda x: "support" in x['decision'].lower(),
     RunnablePassthrough.assign(output=lambda x: support_handler(x['request']))),
    RunnablePassthrough.assign(output=lambda x: info_handler(x['request']))
)

# Combine into agent
agent = {
    "decision": router_chain,
    "request": RunnablePassthrough()
} | routing_branch

# Use
result = agent.invoke({"request": "Book me a flight to Paris"})
print(result['output'])
```

**Explanation:**
This example demonstrates LLM-based routing. The router chain uses an LLM to classify the user's request into one of three categories. The RunnableBranch then routes to the appropriate handler based on the classification. This pattern enables dynamic decision-making while keeping the code structure clear and maintainable.

### Advanced Example
```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch, RunnablePassthrough
from typing import Literal
import json

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Advanced router with structured output and fallback
router_prompt = ChatPromptTemplate.from_messages([
    ("system", """Analyze the request and return JSON with:
    - "route": one of ["booking", "info", "support", "unclear"]
    - "confidence": 0.0-1.0
    - "reasoning": brief explanation
    
    Return ONLY valid JSON."""),
    ("user", "{request}")
])

def parse_route(response: str) -> dict:
    try:
        return json.loads(response)
    except:
        return {"route": "unclear", "confidence": 0.0, "reasoning": "Parse error"}

def route_with_confidence(route_data: dict, request: str) -> dict:
    route = route_data.get("route", "unclear")
    confidence = route_data.get("confidence", 0.0)
    
    # Low confidence threshold
    if confidence < 0.7:
        return {"output": f"Unclear request. Please clarify: {request}", "route": "unclear"}
    
    handlers = {
        "booking": lambda r: f"Booking system: {r}",
        "info": lambda r: f"Information service: {r}",
        "support": lambda r: f"Support ticket created: {r}",
        "unclear": lambda r: f"Need clarification: {r}"
    }
    
    handler = handlers.get(route, handlers["unclear"])
    return {"output": handler(request), "route": route, "confidence": confidence}

# Create advanced routing chain
advanced_router = (
    router_prompt 
    | llm 
    | parse_route
    | (lambda x: route_with_confidence(x, x.get("request", "")))
)

# Usage with error handling
def route_request(request: str) -> str:
    try:
        result = advanced_router.invoke({"request": request})
        return result.get("output", "Error processing request")
    except Exception as e:
        return f"Routing error: {str(e)}"
```

**Explanation:**
This advanced example adds confidence scoring, structured JSON output, and error handling. The router returns not just a route decision but also confidence and reasoning, enabling the system to handle low-confidence cases by asking for clarification. This makes the routing more robust and transparent.

### Complexity-Based Model Routing Example

This example demonstrates routing based on task complexity to optimize resource usage—using fast, cost-efficient models for simple tasks and powerful models for complex ones.

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnablePassthrough

# Initialize different models for different complexity levels
fast_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
powerful_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0)

# Complexity classifier
complexity_prompt = ChatPromptTemplate.from_messages([
    ("system", """Analyze the user's question and classify its complexity:
    - 'simple' for straightforward questions with clear answers (FAQs, definitions, basic facts)
    - 'complex' for questions requiring reasoning, analysis, or multi-step thinking
    
    Consider:
    - Simple: "What is Python?", "How do I install package X?", "What's the weather?"
    - Complex: "Explain the trade-offs between microservices and monoliths", "Debug this error...", "Design a system for..."
    
    Output only: simple or complex"""),
    ("user", "{question}")
])

# Handlers using different models
def handle_simple(question: str) -> str:
    """Use fast, cost-efficient model for simple questions"""
    prompt = ChatPromptTemplate.from_template("Answer this question concisely: {question}")
    chain = prompt | fast_model | StrOutputParser()
    return chain.invoke({"question": question})

def handle_complex(question: str) -> str:
    """Use powerful model for complex questions requiring reasoning"""
    prompt = ChatPromptTemplate.from_template(
        "Think step-by-step and provide a detailed answer: {question}"
    )
    chain = prompt | powerful_model | StrOutputParser()
    return chain.invoke({"question": question})

# Create routing chain
complexity_classifier = complexity_prompt | fast_model | StrOutputParser()

# Route based on complexity
routing_branch = RunnableBranch(
    (lambda x: "simple" in x['complexity'].lower(),
     RunnablePassthrough.assign(
         answer=lambda x: handle_simple(x['question']),
         model_used="fast_model"
     )),
    RunnablePassthrough.assign(
        answer=lambda x: handle_complex(x['question']),
        model_used="powerful_model"
    )
)

# Combine into agent
complexity_router = {
    "complexity": complexity_classifier,
    "question": RunnablePassthrough()
} | routing_branch

# Usage
if __name__ == "__main__":
    # Simple question - will route to fast_model
    result = complexity_router.invoke({
        "question": "What is Python?"
    })
    print(f"Answer: {result['answer']}")
    print(f"Model used: {result['model_used']}\n")
    
    # Complex question - will route to powerful_model
    result = complexity_router.invoke({
        "question": "Explain the architectural trade-offs between event-driven and request-response patterns in distributed systems"
    })
    print(f"Answer: {result['answer']}")
    print(f"Model used: {result['model_used']}")
```

**Explanation:**
This example demonstrates complexity-based routing for resource optimization. The router first classifies the question's complexity using a lightweight model, then routes simple questions to a fast, cost-efficient model and complex questions to a more capable (and expensive) model. This pattern enables automatic cost and performance optimization by matching task complexity to model capability.

### Advanced Complexity Routing with Budget Awareness

This example extends complexity-based routing with budget tracking, enabling graceful degradation when budget constraints are tight.

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
from typing import Dict, Any

# Models with different cost/performance profiles
models = {
    "haiku": ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0),
    "sonnet": ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0),
}

# Budget tracker
class BudgetTracker:
    def __init__(self, budget: float = 100.0):
        self.budget = budget
        self.used = 0.0
        self.costs = {"haiku": 0.25, "sonnet": 1.0}  # per request
    
    def can_afford(self, model: str) -> bool:
        return (self.used + self.costs[model]) <= self.budget
    
    def use(self, model: str):
        if model in self.costs:
            self.used += self.costs[model]
    
    def get_remaining(self) -> float:
        return self.budget - self.used

# Complexity and budget-aware router
router_prompt = ChatPromptTemplate.from_messages([
    ("system", """Analyze the question and return JSON:
    {{
        "complexity": "simple" | "complex",
        "estimated_tokens": number,
        "reasoning": "brief explanation"
    }}
    
    Consider:
    - Simple: clear, factual, single-step questions
    - Complex: requires reasoning, analysis, multi-step thinking, or creative solutions
    
    Return ONLY valid JSON."""),
    ("user", "{question}")
])

def parse_json_response(response: str) -> Dict[str, Any]:
    """Safely parse JSON response from LLM"""
    try:
        # Try to extract JSON from response if it contains markdown code blocks
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            response = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            response = response[start:end].strip()
        return json.loads(response)
    except (json.JSONDecodeError, ValueError):
        # Default to simple if parsing fails
        return {"complexity": "simple", "estimated_tokens": 100, "reasoning": "Parse error"}

def route_with_budget(question: str, budget_tracker: BudgetTracker) -> Dict[str, Any]:
    """Route question based on complexity and available budget"""
    # Classify complexity using the cheaper model
    classifier_chain = router_prompt | models["haiku"] | StrOutputParser()
    response = classifier_chain.invoke({"question": question})
    classification = parse_json_response(response)
    
    complexity = classification.get("complexity", "simple")
    
    # Route based on complexity and budget
    if complexity == "simple":
        model_name = "haiku"
    else:
        # Check if we can afford the powerful model
        if budget_tracker.can_afford("sonnet"):
            model_name = "sonnet"
        else:
            # Fallback to cheaper model if budget is low
            model_name = "haiku"
    
    # Use the selected model
    model = models[model_name]
    answer_prompt = ChatPromptTemplate.from_template(
        "Answer this question: {question}"
    )
    answer_chain = answer_prompt | model | StrOutputParser()
    answer = answer_chain.invoke({"question": question})
    
    # Track usage
    budget_tracker.use(model_name)
    
    return {
        "answer": answer,
        "model_used": model_name,
        "complexity": complexity,
        "budget_remaining": budget_tracker.get_remaining()
    }

# Usage
if __name__ == "__main__":
    tracker = BudgetTracker(budget=10.0)
    
    # Simple question
    result = route_with_budget("What is machine learning?", tracker)
    print(f"Question: What is machine learning?")
    print(f"Model: {result['model_used']}")
    print(f"Complexity: {result['complexity']}")
    print(f"Budget remaining: ${result['budget_remaining']:.2f}\n")
    
    # Complex question
    result = route_with_budget(
        "Design a distributed system architecture for handling 1 million concurrent users with sub-100ms latency",
        tracker
    )
    print(f"Question: Design a distributed system...")
    print(f"Model: {result['model_used']}")
    print(f"Complexity: {result['complexity']}")
    print(f"Budget remaining: ${result['budget_remaining']:.2f}")
```

**Explanation:**
This advanced example adds budget awareness to complexity-based routing. The router classifies complexity and checks available budget before selecting a model. If budget is constrained, it may route complex tasks to cheaper models, enabling graceful degradation while staying within resource limits. The budget tracker monitors usage and prevents overspending.

### Framework-Specific Examples

#### LangGraph
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class RouterState(TypedDict):
    request: str
    route: str
    output: str

def route_node(state: RouterState) -> RouterState:
    # LLM-based routing logic
    route = llm.invoke(f"Route this: {state['request']}").content
    return {**state, "route": route}

def booking_node(state: RouterState) -> RouterState:
    return {**state, "output": f"Booking: {state['request']}"}

def info_node(state: RouterState) -> RouterState:
    return {**state, "output": f"Info: {state['request']}"}

# Build graph
graph = StateGraph(RouterState)
graph.add_node("route", route_node)
graph.add_node("booking", booking_node)
graph.add_node("info", info_node)

graph.add_conditional_edges(
    "route",
    lambda state: state["route"],
    {"booking": "booking", "info": "info"}
)
graph.add_edge("booking", END)
graph.add_edge("info", END)
```

#### Google ADK
```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# Define specialized agents
booking_agent = Agent(
    name="Booker",
    model="gemini-2.0-flash",
    description="Handles all booking requests",
    tools=[booking_tool]
)

info_agent = Agent(
    name="Info",
    model="gemini-2.0-flash", 
    description="Answers general questions",
    tools=[info_tool]
)

# Coordinator with routing
coordinator = Agent(
    name="Coordinator",
    model="gemini-2.0-flash",
    instruction="""Route requests:
    - Booking requests → Booker agent
    - Questions → Info agent""",
    sub_agents=[booking_agent, info_agent]
)
```

## Key Takeaways

- **Core Concept:** Routing enables dynamic, conditional flow control in agent workflows, allowing specialization and adaptability.
- **Best Practice:** Use LLM-based routing for flexibility, embedding-based for speed, rule-based for determinism, or ML-based for balance.
- **Common Pitfall:** Over-routing can add unnecessary complexity; ensure routing decisions are meaningful and improve outcomes.
- **Performance Note:** Routing adds latency (especially LLM-based); consider caching route decisions for repeated similar inputs.
- **Resource Optimization:** Complexity-based routing enables automatic cost and performance optimization by matching task complexity to model capability, significantly reducing costs for simple tasks while maintaining quality for complex ones.

## Related Patterns

This pattern works well with:
- **Multi-Agent** - Routing often directs tasks to specialized agents in multi-agent systems
- **Tool Use** - Routing can select appropriate tools based on task requirements
- **Planning** - Routing decisions can be part of a larger planning process

This pattern is often combined with:
- **Prompt Chaining** - Routes can lead to different prompt chains for different scenarios
- **Reflection** - Routing decisions can be reviewed and corrected through reflection

## References

- LangChain Routing Documentation: https://python.langchain.com/docs/expression_language/how_to/routing
- LangGraph Conditional Edges: https://langchain-ai.github.io/langgraph/how-tos/routing/
- Google ADK Agents: https://github.com/google/generative-ai-python/tree/main/google/adk

