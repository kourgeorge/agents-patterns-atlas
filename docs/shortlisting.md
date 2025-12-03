# Pattern: Shortlisting

## Motivation

A librarian faces thousands of books in a catalog and must find the most relevant ones for a researcher's query. They don't read every book—they analyze titles, descriptions, and keywords to create a shortlist of candidates. Similarly, agents often have access to hundreds or thousands of tools, APIs, or functions, but they can't include all of them in their context window. The challenge is: how do you identify the most relevant tools from a large catalog without overwhelming the agent's context or wasting computational resources?

Consider an agent that needs to interact with a large API catalog:
- A digital sales platform with 200+ API endpoints
- An OpenAPI specification with 50+ operations
- A Model Context Protocol (MCP) server with 30+ tools
- A codebase with hundreds of available functions

Including all available tools in every prompt would be expensive, slow, and confusing for the agent. The agent needs a way to intelligently filter and rank tools based on the specific task at hand, identifying not just relevant tools, but also understanding how they can work together in multi-step workflows.

## Pattern Overview

**What it is:** The Shortlisting Pattern enables agents to analyze a large set of available tools, APIs, or functions and select the most relevant subset based on a task description. It uses LLM-based analysis to score and rank candidates, considering direct relevance, parameter matching, and potential for tool chaining in multi-step workflows.

**When to use:** Use this pattern when agents have access to many tools/APIs but need to identify which ones are relevant for a specific task, especially when context window constraints make including all tools impractical.

**Why it matters:** As agentic systems scale, they increasingly interact with large tool catalogs—OpenAPI specifications, MCP servers, codebases with many functions, or multi-agent systems with specialized capabilities. The Shortlisting Pattern reduces context window usage by filtering to relevant tools, improves decision-making by focusing the agent's attention, and enables discovery of tool chains that work together to accomplish complex goals.

Without shortlisting, agents face a fundamental tension: include too many tools and waste tokens while confusing the model, or include too few and risk missing critical capabilities. Shortlisting resolves this by providing an intelligent, task-aware filtering mechanism that identifies not just individual relevant tools, but also understands how tools can be chained together in workflows.

### Key Concepts

- **Relevance Scoring:** LLM-based analysis that evaluates each tool/API against the task description and assigns a relevance score (typically 0.0-1.0), enabling ranking and filtering.
- **Parameter Matching:** Evaluating whether required parameters for a tool can be satisfied—either from direct user input or from the output of other tools in a potential chain.
- **API/Tool Chaining:** Identifying how multiple tools can work together in sequence, where one tool's output provides input parameters for subsequent tools, enabling multi-step workflows.
- **Schema Matching:** Understanding input/output schemas to determine chaining potential—analyzing whether one tool's response structure matches another tool's required parameters.
- **Structured Output:** Returning a ranked list with scores and reasoning for each selected tool, enabling transparency, debugging, and integration with downstream planning agents.

### How It Works

The Shortlisting Pattern operates through a structured process:

1. **Tool Catalog Input:** The agent receives a task description and a catalog of available tools/APIs, each with metadata including name, description, parameters, types, and response schemas.

2. **LLM-Based Analysis:** An LLM analyzes each tool against the task, considering:
   - Direct functional match (does the tool's purpose align with the task?)
   - Parameter availability (can required parameters be sourced from user input or other tools?)
   - Chaining potential (can this tool's output feed into other relevant tools?)
   - Schema compatibility (do response schemas match input requirements for chaining?)

3. **Relevance Scoring:** Each tool receives a relevance score (0.0-1.0) with reasoning explaining why it was selected, how parameters can be satisfied, and its role in potential workflows.

4. **Ranked Shortlist:** The agent returns a ranked list of relevant tools, ordered by relevance score, with detailed reasoning for each selection.

5. **Integration with Planning:** The shortlist feeds into downstream planning or execution agents, which use the filtered, relevant tools to create action sequences.

## When to Use This Pattern

### ✅ Use this pattern when:

- **Large tool/API catalogs:** You have 20+ tools/APIs and including all of them in context is impractical or expensive.
- **Multi-step workflows:** Tasks require chaining multiple tools together, and you need to identify which tools can work in sequence.
- **Context window constraints:** Including all available tools would consume too many tokens or exceed context limits.
- **Dynamic tool discovery:** Tools are discovered at runtime (e.g., from OpenAPI specs, MCP servers) and need filtering before use.
- **Cost optimization:** Reducing the number of tools in context saves on token costs for each agent interaction.
- **Specialized tool selection:** Different tasks require different subsets of tools, and manual filtering is impractical.

### ❌ Avoid this pattern when:

- **Small tool sets:** You have fewer than 10-15 tools, and including all of them is feasible and cost-effective.
- **Simple single-tool tasks:** The task clearly requires one specific tool, and there's no ambiguity.
- **Real-time constraints:** The latency of LLM-based shortlisting (typically 1-3 seconds) is unacceptable for the use case.
- **Fixed tool sets:** The same tools are always used together, making shortlisting unnecessary overhead.
- **Tool availability is dynamic:** Tools appear/disappear frequently, making pre-shortlisting ineffective.

### Decision Guidelines

Use Shortlisting when the benefits of intelligent filtering outweigh the added latency and cost. Consider catalog size: catalogs with 20+ tools benefit significantly from shortlisting. Consider task variability: if different tasks require different tool subsets, shortlisting provides value. Consider context constraints: if including all tools would exceed context limits or be prohibitively expensive, shortlisting is essential. However, if you have a small, fixed set of tools that are always used together, the overhead of shortlisting may not be justified.

## Practical Applications & Use Cases

The Shortlisting Pattern is essential for building scalable agentic systems that interact with large tool ecosystems:

### API Discovery in Large Catalogs

**Scenario:** An agent needs to interact with a digital sales platform that exposes 200+ REST API endpoints through an OpenAPI specification.

**Challenge:** Including all 200+ API definitions in every prompt would consume thousands of tokens and confuse the agent. The agent needs to identify which APIs are relevant for specific tasks like "get the top account by revenue" or "update a customer's contact information."

**Solution:** Shortlisting analyzes the task description against all available APIs, scoring each for relevance. For "get top account by revenue," it might shortlist:
- `get_accounts` (relevance: 0.95) - retrieves account data
- `get_account_by_id` (relevance: 0.85) - can retrieve specific account details
- `get_accounts_tpp` (relevance: 0.80) - alternative account retrieval method

The agent then uses only these shortlisted APIs in subsequent planning and execution, dramatically reducing context usage.

### Tool Selection in Multi-Agent Systems

**Scenario:** An orchestrator agent coordinates multiple specialized worker agents, each with different tool sets. The orchestrator needs to select which workers and tools to use for a given task.

**Challenge:** The orchestrator has access to 50+ tools across 10 different worker agents. It needs to identify which subset of workers and their tools are relevant for the current task.

**Solution:** Shortlisting evaluates tools across all workers, identifying relevant capabilities. The orchestrator then routes the task to workers whose tools were shortlisted, enabling efficient multi-agent coordination.

### Code Generation with Function Selection

**Scenario:** A coding agent has access to a codebase with hundreds of utility functions. When generating code to solve a problem, it needs to identify which functions are relevant.

**Challenge:** Including all function signatures in the prompt would be impractical. The agent needs to identify relevant functions based on the coding task.

**Solution:** Shortlisting analyzes the coding task description and available function signatures, shortlisting relevant functions. The agent then generates code using only the shortlisted functions, improving code quality and reducing context usage.

### MCP Server Tool Discovery

**Scenario:** An agent interacts with multiple Model Context Protocol (MCP) servers, each exposing 10-30 tools. The agent needs to discover and select relevant tools for a task.

**Challenge:** With multiple MCP servers, the total tool count can exceed 100+. The agent needs an efficient way to identify relevant tools without querying all servers for every task.

**Solution:** Shortlisting evaluates tools from all available MCP servers against the task, creating a unified shortlist of relevant tools across servers. This enables efficient tool discovery in distributed tool ecosystems.

## Implementation

### Core Architecture

The Shortlisting Pattern consists of three main components: the Shortlister Agent, the Tool Catalog, and the Output Schema.

#### Shortlister Agent

The core agent that performs the analysis:

```python
from typing import List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, Field

class APIDetails(BaseModel):
    """Details for a shortlisted API/tool."""
    name: str = Field(..., description="Tool/API name")
    relevance_score: float = Field(
        ..., 
        description="Relevance score between 0.0 and 1.0"
    )
    reasoning: str = Field(
        ..., 
        description="Explanation of why this tool is relevant, including parameter sources and chaining potential"
    )

class ShortListerOutput(BaseModel):
    """Output from the shortlisting agent."""
    thoughts: List[str] = Field(
        ..., 
        description="Step-by-step reasoning about the task and available tools"
    )
    result: List[APIDetails] = Field(
        ..., 
        description="Ranked list of relevant tools, ordered by relevance_score (highest first)"
    )

class ShortlisterAgent:
    def __init__(
        self,
        prompt_template: ChatPromptTemplate,
        llm: BaseChatModel,
    ):
        self.llm = llm
        self.prompt_template = prompt_template
    
    async def shortlist(
        self,
        task_description: str,
        available_tools: List[dict],
        app_name: Optional[str] = None,
    ) -> ShortListerOutput:
        """Shortlist relevant tools for a task."""
        # Format tools for analysis
        tools_json = json.dumps(available_tools, indent=2)
        
        # Invoke LLM with structured output
        messages = self.prompt_template.format_messages(
            input=task_description,
            api_shortlister_current_app=app_name or "default",
            api_shortlister_current_app_apis=tools_json,
        )
        
        response = await self.llm.ainvoke(messages)
        
        # Parse structured output
        return ShortListerOutput.model_validate_json(response.content)
```

**Key Design Decisions:**
- **Structured Output:** Using Pydantic models ensures consistent, parseable results
- **Relevance Scoring:** 0.0-1.0 scale enables ranking and threshold filtering
- **Reasoning Field:** Detailed reasoning enables transparency and debugging
- **Thoughts Field:** Step-by-step reasoning helps understand the agent's analysis process

#### Prompt Design

The system prompt is critical for effective shortlisting. It must emphasize:

1. **Parameter Matching:** How to evaluate whether required parameters can be satisfied
2. **API Chaining:** How to identify tools that can work together
3. **Schema Matching:** How to match output schemas to input requirements

```python
SYSTEM_PROMPT = """You are an expert AI assistant responsible for selecting relevant APIs to fulfill a user's request.
Your goal is to analyze a list of available API definitions (provided in JSON format) and a user's query to find relevant APIs.

Based on this analysis, you must identify the APIs that are most relevant to achieve the user's goal. These APIs should be ranked by their `relevance_score` from highest to lowest.

Your primary focus should be on:
1. **Direct User Input:** Parameters explicitly mentioned in the user's query can be used as inputs for an API.
2. **API Output as Input (Chaining):** A crucial aspect of relevance is whether an API's output can provide the necessary input parameters for another API that moves closer to fulfilling the user's overall goal. Use the provided `response_schema` to understand what data each API returns and how it can be used as input for other APIs.
3. **Schema Matching for Chaining:** When evaluating API chaining potential, consider whether the expected output format/schema of one API matches the required input parameters of another API.
4. **Multi-Step Workflows:** Complex user goals often require multiple API calls in sequence. An API that serves as an intermediate step in achieving the final goal should be considered highly relevant.

You need to evaluate each API's relevance based on:
- How directly its described functionality matches the user's query
- The availability of its required input parameters, sourced as described above
- Its potential role in a sequence of API calls to achieve the user's objective
- Its compatibility with other APIs in terms of input/output schema matching for chaining purposes
- Its position in potential multi-step workflows (initial data gathering, intermediate processing, final action)

Return a JSON object with:
- "thoughts": A list of strings representing your step-by-step reasoning
- "result": A list of API details, each with "name", "relevance_score" (0.0-1.0), and "reasoning"
"""
```

#### Integration with Agent Workflow

Shortlisting typically occurs before planning or execution:

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    task_description: str
    available_tools: dict
    shortlisted_tools: Optional[List[APIDetails]]
    plan: Optional[List[str]]
    execution_result: Optional[str]

def shortlist_node(state: AgentState) -> AgentState:
    """Shortlist relevant tools for the task."""
    shortlister = ShortlisterAgent(...)
    result = await shortlister.shortlist(
        task_description=state["task_description"],
        available_tools=state["available_tools"],
    )
    return {
        **state,
        "shortlisted_tools": result.result
    }

def plan_node(state: AgentState) -> AgentState:
    """Create a plan using only shortlisted tools."""
    # Use only shortlisted tools for planning
    relevant_tools = [tool.name for tool in state["shortlisted_tools"]]
    # ... planning logic using relevant_tools ...
    return state

# Build graph
graph = StateGraph(AgentState)
graph.add_node("shortlist", shortlist_node)
graph.add_node("plan", plan_node)
graph.add_edge("shortlist", "plan")
graph.add_edge("plan", END)
```

### Basic Example

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import json

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    temperature=0
)

# Define output schema
class APIDetails(BaseModel):
    name: str
    relevance_score: float = Field(ge=0.0, le=1.0)
    reasoning: str

class ShortListerOutput(BaseModel):
    thoughts: list[str]
    result: list[APIDetails]

# Create prompt
system_prompt = """You are an expert at selecting relevant APIs.
Analyze the available APIs and user query, then return a ranked list of relevant APIs.
Consider parameter matching and API chaining potential."""

user_prompt = """User Intent: {task_description}

Available APIs:
{available_apis}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("user", user_prompt)
])

# Available tools
available_apis = [
    {
        "name": "get_accounts",
        "description": "Retrieve all accounts for the current user's territory",
        "parameters": [],
        "response_schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "revenue": {"type": "number"}
                }
            }
        }
    },
    {
        "name": "get_account_by_id",
        "description": "Get detailed information about a specific account",
        "parameters": [
            {
                "name": "account_id",
                "type": "string",
                "required": True
            }
        ],
        "response_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "revenue": {"type": "number"},
                "contacts": {"type": "array"}
            }
        }
    },
    {
        "name": "update_account",
        "description": "Update account information",
        "parameters": [
            {
                "name": "account_id",
                "type": "string",
                "required": True
            },
            {
                "name": "name",
                "type": "string",
                "required": False
            }
        ],
        "response_schema": {"type": "object"}
    }
]

# Shortlist for a task
task = "Get the top account by revenue"

chain = prompt | llm.with_structured_output(ShortListerOutput)
result = chain.invoke({
    "task_description": task,
    "available_apis": json.dumps(available_apis, indent=2)
})

print("Shortlisted APIs:")
for api in result.result:
    print(f"- {api.name}: {api.relevance_score:.2f}")
    print(f"  Reasoning: {api.reasoning}\n")
```

**Expected Output:**
```
Shortlisted APIs:
- get_accounts: 0.95
  Reasoning: Directly fulfills the task by retrieving all accounts with revenue data. No parameters required, making it immediately usable. Response includes revenue field needed for ranking.

- get_account_by_id: 0.60
  Reasoning: Useful for retrieving detailed information about the top account after identification, but requires account_id parameter that can be sourced from get_accounts output. Good chaining candidate.

- update_account: 0.10
  Reasoning: Low relevance as task is about retrieval, not updates. Could be used in a workflow but not directly relevant to "get top account" goal.
```

### Advanced Example: API Chaining Consideration

This example demonstrates how shortlisting identifies tools that can be chained together:

```python
# More complex scenario with chaining
available_apis = [
    {
        "name": "search_products",
        "description": "Search for products by keyword",
        "parameters": [
            {"name": "keyword", "type": "string", "required": True}
        ],
        "response_schema": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "string"},
                    "name": {"type": "string"},
                    "price": {"type": "number"}
                }
            }
        }
    },
    {
        "name": "get_product_details",
        "description": "Get detailed information about a product",
        "parameters": [
            {"name": "product_id", "type": "string", "required": True}
        ],
        "response_schema": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string"},
                "name": {"type": "string"},
                "price": {"type": "number"},
                "description": {"type": "string"},
                "inventory": {"type": "number"}
            }
        }
    },
    {
        "name": "add_to_cart",
        "description": "Add a product to the shopping cart",
        "parameters": [
            {"name": "product_id", "type": "string", "required": True},
            {"name": "quantity", "type": "integer", "required": True}
        ],
        "response_schema": {"type": "object"}
    }
]

task = "Find products matching 'laptop' and add the cheapest one to my cart"

result = chain.invoke({
    "task_description": task,
    "available_apis": json.dumps(available_apis, indent=2)
})

# The shortlister should identify:
# 1. search_products (high relevance) - finds products by keyword
# 2. get_product_details (medium relevance) - can get price details for comparison
# 3. add_to_cart (high relevance) - required for final action, product_id can come from search_products
```

### Memory-Enhanced Shortlisting

Shortlisting can be improved by learning from past experiences:

```python
class MemoryEnhancedShortlister(ShortlisterAgent):
    def __init__(self, *args, memory_store=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.memory_store = memory_store
    
    async def shortlist(
        self,
        task_description: str,
        available_tools: List[dict],
        **kwargs
    ) -> ShortListerOutput:
        # Retrieve relevant past shortlisting experiences
        memory_tips = None
        if self.memory_store:
            memory_tips = await self.memory_store.retrieve(
                query=task_description,
                namespace="shortlisting",
                limit=3
            )
        
        # Include memory in prompt
        messages = self.prompt_template.format_messages(
            input=task_description,
            available_apis=json.dumps(available_tools, indent=2),
            memory=memory_tips,  # Past experiences
            **kwargs
        )
        
        response = await self.llm.ainvoke(messages)
        result = ShortListerOutput.model_validate_json(response.content)
        
        # Store this shortlisting experience for future use
        if self.memory_store:
            await self.memory_store.store(
                namespace="shortlisting",
                content={
                    "task": task_description,
                    "shortlisted": [api.name for api in result.result],
                    "reasoning": result.thoughts
                }
            )
        
        return result
```

**Benefits:**
- Learns which tools work well together for similar tasks
- Improves relevance scoring over time
- Reduces errors in parameter matching by learning from past chains

### Framework Integration

#### LangGraph Integration

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class ShortlistingState(TypedDict):
    task: str
    all_tools: dict
    shortlisted: Optional[list]
    next_action: Literal["plan", "execute"]

def shortlist_tools(state: ShortlistingState) -> ShortlistingState:
    shortlister = ShortlisterAgent(...)
    result = await shortlister.shortlist(
        task_description=state["task"],
        available_tools=state["all_tools"]
    )
    return {
        **state,
        "shortlisted": result.result,
        "next_action": "plan"
    }

# Build graph
graph = StateGraph(ShortlistingState)
graph.add_node("shortlist", shortlist_tools)
graph.add_conditional_edges(
    "shortlist",
    lambda s: s["next_action"],
    {"plan": "plan_node", "execute": "execute_node"}
)
```

#### Google ADK Integration

```python
from google.adk.agents import Agent
from google.adk.tools import FunctionTool

# Create shortlisting agent
shortlister_agent = Agent(
    name="ToolShortlister",
    model="gemini-2.0-flash-exp",
    description="Selects relevant tools from large catalogs",
    instruction="""Analyze available tools and shortlist the most relevant ones.
    Consider parameter matching and tool chaining potential.""",
    tools=[shortlist_tool]  # Tool that performs shortlisting
)

# Use in workflow
orchestrator = Agent(
    name="Orchestrator",
    model="gemini-2.0-flash-exp",
    sub_agents=[shortlister_agent, planner_agent, executor_agent],
    instruction="""First shortlist relevant tools, then plan, then execute."""
)
```

## Key Takeaways

- **Context Efficiency:** Shortlisting dramatically reduces context window usage by filtering large tool catalogs to relevant subsets, enabling agents to work with 100+ tool ecosystems without overwhelming the context.

- **Parameter Matching is Critical:** Effective shortlisting must evaluate not just functional relevance, but whether required parameters can be satisfied—either from user input or from other tools' outputs in a chain.

- **API Chaining Discovery:** The pattern's greatest value comes from identifying how tools can work together in multi-step workflows, where one tool's output feeds into another's input, enabling complex goal achievement.

- **Structured Output Enables Integration:** Returning ranked lists with scores and reasoning enables downstream agents (planners, executors) to make informed decisions and provides transparency for debugging.

- **Memory Integration Improves Accuracy:** Learning from past shortlisting experiences helps the agent improve over time, recognizing successful tool combinations and parameter patterns.

- **When to Use:** Apply shortlisting for catalogs with 20+ tools, multi-step workflows requiring tool chaining, and scenarios where context window constraints make including all tools impractical.

## Related Patterns

This pattern works well with:

- **Tool Use:** Shortlisting selects which tools to make available to the agent, filtering the tool catalog before tool use occurs.

- **Routing:** Shortlisting can be viewed as a specialized form of routing—selecting which tools to route the task to from a large set of candidates.

- **Planning:** Shortlisting typically precedes planning, as planners need to know which tools are available before creating action sequences. The shortlist informs the planning process.

- **Orchestrator-Worker:** Shortlisting helps orchestrators identify which workers (and their tools) are relevant for a given task, enabling efficient multi-agent coordination.

- **Knowledge Retrieval:** Shortlisting can use semantic search or RAG to find relevant tools from large catalogs, especially when tool descriptions are embedded in vector databases.

This pattern differs from:

- **Tool Use:** Tool Use is about executing tools; Shortlisting is about selecting which tools to consider for use.

- **Routing:** Routing selects between different execution paths or agents; Shortlisting filters a catalog of tools/APIs before use.

- **Planning:** Planning creates action sequences; Shortlisting identifies which tools are available for those sequences.

## References

- LangChain Structured Output: https://python.langchain.com/docs/how_to/structured_output/
- Model Context Protocol (MCP): https://modelcontextprotocol.io/
- OpenAPI Specification: https://swagger.io/specification/
- Google ADK Agents: https://google.github.io/adk-docs/agents/
- Pydantic Models: https://docs.pydantic.dev/

