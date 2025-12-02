# Tool Use & Execution

## Motivation

Humans extend their capabilities through tools: a hammer for construction, a calculator for math, a smartphone for communication. Each tool has a clear purpose, specific instructions for use, and predictable results when used correctly. Just as we learn to use tools by understanding their function and boundaries, agents need well-defined tools with clear descriptions, parameters, and constraints. The Tool Use pattern creates this interface between an agent's reasoning and the external world.

## Pattern Overview

**What it is:** Tool Use (also known as Function Calling) is the pattern that enables agents to interact with external systems, APIs, databases, and services. It bridges the gap between an LLM's reasoning capabilities and the external world, allowing agents to perform actions, retrieve real-time data, execute code, and interact with other systems.

**When to use:** Use this pattern whenever an agent needs to break out of the LLM's internal knowledge and interact with the outside world. This is essential for tasks requiring real-time data, accessing private or proprietary information, performing precise calculations, executing code, or triggering actions in other systems.

**Why it matters:** LLMs are powerful text generators, but they are fundamentally disconnected from the outside world. Their knowledge is static, limited to training data, and they lack the ability to perform actions or retrieve real-time information. The Tool Use pattern transforms a language model from a text generator into an agent capable of sensing, reasoning, and acting in the digital or physical world.

The success of tool use relies critically on the quality and robustness of the **Agent-Computer Interface (ACI)**. The ACI is the tightly controlled, isolated execution runtime where the LLM's generated commands are translated into executable, verifiable code. Just as a poor UI confuses a human user, poorly defined, ambiguous, or unreliable tools lead to agent hallucinations, costly loops, and ultimate failure.

### Key Concepts

- **Function Calling:** The technical mechanism where an LLM generates structured output (often JSON) specifying which function to call and with what arguments.
- **Tool Definition:** Clear descriptions of external functions or capabilities, including purpose, parameters, types, and boundaries.
- **Agent-Computer Interface (ACI):** The standardized contract between the generative model (planner) and the code execution environment (executor).
- **Idempotency:** A critical principle where a tool call should produce the same observable side effect regardless of how many times it is executed.
- **Tool Execution:** The orchestration layer that intercepts structured tool calls, executes the actual function, and returns results to the agent.
- **Observation:** The structured result returned from tool execution that the agent uses to inform its next decision.

### How It Works

The Tool Use pattern operates through a structured process:

1. **Tool Definition:** External functions or capabilities are defined and described to the LLM. This description includes the function's purpose, name, parameters, types, and what it cannot do.

2. **LLM Decision:** The LLM receives the user's request and available tool definitions. Based on its understanding, it decides if calling one or more tools is necessary to fulfill the request.

3. **Function Call Generation:** If the LLM decides to use a tool, it generates structured output (often JSON) specifying the tool name and arguments extracted from the user's request.

4. **Tool Execution:** The orchestration layer intercepts this structured output, identifies the requested tool, and executes the actual external function with the provided arguments.

5. **Observation/Result:** The output or result from tool execution is returned to the agent as an observation.

6. **LLM Processing:** The LLM receives the tool's output as context and uses it to formulate a final response or decide on the next step (which might involve calling another tool, reflecting, or providing a final answer).

While "function calling" describes invoking specific, predefined code functions, "tool calling" is a broader concept. A tool can be a traditional function, a complex API endpoint, a database request, or even an instruction directed at another specialized agent. This perspective enables sophisticated systems where agents orchestrate across diverse digital resources and intelligent entities.

## When to Use This Pattern

### ✅ Use this pattern when:

- **Real-time data needed:** Tasks requiring current information not in the LLM's training data (weather, stock prices, news).
- **External system interaction:** Tasks that need to interact with APIs, databases, file systems, or other services.
- **Precise calculations required:** Tasks needing deterministic computations that LLMs cannot perform reliably.
- **Code execution needed:** Tasks requiring running code snippets in a safe environment.
- **Action triggering:** Tasks that need to trigger actions in other systems (send emails, control devices, update databases).
- **Private/proprietary data access:** Tasks requiring access to user-specific or company-specific information not in public training data.
- **Dynamic information retrieval:** Tasks that need to search, query, or retrieve information from external sources.

### ❌ Avoid this pattern when:

- **Pure text generation:** Tasks that only require generating text based on the LLM's training data.
- **No external dependencies:** Tasks that can be completed entirely within the LLM's knowledge and reasoning capabilities.
- **Simple Q&A:** Basic questions that can be answered from the model's training data without external lookup.
- **Cost-sensitive scenarios:** When the overhead of tool calls (latency, API costs) outweighs benefits.
- **Security-critical systems:** When tool execution introduces unacceptable security risks that cannot be mitigated.

### Decision Guidelines

Use Tool Use when the task requires information or capabilities beyond what the LLM can provide from its training data alone. If the task needs real-time data, interaction with external systems, or the ability to perform actions, Tool Use is essential. However, if the task can be completed with the LLM's internal knowledge and reasoning, avoid adding unnecessary complexity.

## Practical Applications & Use Cases

The Tool Use pattern is applicable in virtually any scenario where an agent needs to go beyond generating text to perform an action or retrieve specific, dynamic information:

### 1. Information Retrieval from External Sources
**Use Case:** A weather agent that provides current weather conditions.
- **Tool:** A weather API that takes a location and returns current weather conditions.
- **Agent Flow:** User asks "What's the weather in London?", LLM identifies the need for the weather tool, calls the tool with "London", tool returns data, LLM formats the data into a user-friendly response.

### 2. Interacting with Databases and APIs
**Use Case:** An e-commerce agent that checks inventory and order status.
- **Tools:** API calls to check product inventory, get order status, or process payments.
- **Agent Flow:** User asks "Is product X in stock?", LLM calls the inventory API, tool returns stock count, LLM tells the user the stock status.

### 3. Performing Calculations and Data Analysis
**Use Case:** A financial agent that calculates profits and analyzes stock data.
- **Tools:** A calculator function, a stock market data API, a spreadsheet tool.
- **Agent Flow:** User asks "What's the current price of AAPL and calculate the potential profit if I bought 100 shares at $150?", LLM calls stock API, gets current price, then calls calculator tool, gets result, formats response.

### 4. Sending Communications
**Use Case:** A personal assistant agent that sends emails.
- **Tool:** An email sending API.
- **Agent Flow:** User says "Send an email to John about the meeting tomorrow.", LLM calls an email tool with the recipient, subject, and body extracted from the request.

### 5. Executing Code
**Use Case:** A coding assistant agent that runs and analyzes code.
- **Tool:** A code interpreter.
- **Agent Flow:** User provides a Python snippet and asks "What does this code do?", LLM uses the interpreter tool to run the code and analyze its output.

### 6. Controlling Other Systems or Devices
**Use Case:** A smart home agent that controls IoT devices.
- **Tool:** An API to control smart lights.
- **Agent Flow:** User says "Turn off the living room lights." LLM calls the smart home tool with the command and target device.

## Implementation

### Engineering Best Practices

#### 1. Explicit Tool Definitions & Quality
Tools must have clear, distinct descriptions, strict boundaries, and required parameters. The quality of the tool description directly impacts the model's accuracy. Descriptions must detail:
- **Purpose:** What the tool solves
- **Boundaries:** What it cannot do
- **Parameter Names:** Use descriptive, obvious parameter names that make their purpose clear (e.g., `absolute_filepath` instead of `path`, `user_email_address` instead of `email`)
- **Parameter Types:** Clearly specify types and formats for all parameters
- **Negative examples:** Show the agent when not to use a tool (e.g., "Do not use search_api for real-time stock quotes; use get_stock_price instead")
- **Example Usage:** Include example usage to illustrate how the tool should be called

Use structured data types (like Pydantic schemas in Python or TypeScript interfaces) to enforce type safety and parameter validation. The docstring for the tool should be the single source of truth for the model's understanding.

**Put yourself in the model's shoes:** Is it obvious how to use this tool based on the description and parameters? If you need to think carefully about it, the model will too. A good tool definition often includes example usage, edge cases, input format requirements, and clear boundaries from other tools.

#### 1.5. Tool Format Design: Choosing LLM-Friendly Formats

When designing tools, there are often multiple ways to specify the same action. However, some formats are significantly more difficult for LLMs to generate correctly than others. The format you choose can dramatically impact reliability and error rates.

**Key Principles for Tool Format Selection:**

1. **Give the model enough tokens to "think" before writing itself into a corner**
   - Avoid formats that require precise counts or calculations before generation
   - Example: Writing a diff requires knowing how many lines are changing in the chunk header before the new code is written—this is error-prone for LLMs

2. **Keep formats close to what models see naturally in training data**
   - Formats that appear frequently in the model's training corpus are easier to generate
   - Example: Code in markdown code blocks is more natural than code inside JSON strings

3. **Minimize formatting "overhead"**
   - Avoid formats that require complex escaping, counting, or precise formatting
   - Example: Writing code inside JSON requires extra escaping of newlines and quotes, making it harder for the model
   - Example: Requiring accurate line counts for thousands of lines of code is error-prone

**Practical Examples:**

**❌ Avoid: Diff-based file editing**
```python
# Difficult for LLMs - requires precise line counting
def edit_file(filepath: str, diff: str) -> str:
    """
    Edit a file using a diff format.
    diff format: '@@ -start_line,count +start_line,count @@'
    Example: '@@ -5,3 +5,4 @@\n old line 1\n-old line 2\n+new line 2'
    """
```

**✅ Prefer: Full file replacement or append operations**
```python
# Easier for LLMs - no line counting required
def write_file(filepath: str, content: str) -> str:
    """
    Write content to a file. If file exists, replaces it entirely.
    content: The complete file contents as a string.
    """
```

**❌ Avoid: Code in JSON strings**
```python
# Requires escaping newlines and quotes
def execute_code(code_json: str) -> str:
    """
    Execute code provided as JSON string.
    Example: {"code": "def hello():\n    print('hi')"}
    """
```

**✅ Prefer: Code in markdown or plain text**
```python
# Natural format, no escaping needed
def execute_code(code: str) -> str:
    """
    Execute Python code provided as a string.
    Code should be valid Python syntax.
    """
```

**Poka-Yoke (Error-Proofing) Your Tools:**

Apply the Japanese concept of "poka-yoke" (mistake-proofing) to tool design by making it harder for the model to make mistakes:

- **Use absolute paths instead of relative paths:** After an agent changes directories, relative paths become ambiguous. Requiring absolute paths eliminates this source of error.
- **Use structured types instead of free-form strings:** Instead of accepting a date as "2024-01-15" or "January 15, 2024", require a specific ISO format.
- **Provide clear boundaries:** Explicitly state what the tool cannot do to prevent misuse.
- **Use descriptive parameter names:** Parameter names should make their purpose obvious (e.g., `absolute_filepath` instead of `path`).

**Example from Production:**

When building a coding agent for SWE-bench, Anthropic found that the model made mistakes with tools using relative filepaths after the agent had moved out of the root directory. By changing the tool to always require absolute filepaths, the model used the method flawlessly.

**Rule of Thumb:**

Think about how much effort goes into Human-Computer Interfaces (HCI), and invest similar effort in creating good Agent-Computer Interfaces (ACI). Put yourself in the model's shoes: Is it obvious how to use this tool based on the description and parameters? If you need to think carefully about it, the model will too. A good tool definition often includes example usage, edge cases, input format requirements, and clear boundaries from other tools.

#### 2. Input & Output Validation and Pruning
Add a crucial layer of security and robustness between the LLM and external systems:

- **Pre-Execution Checks:** Verify that parameters generated by the LLM (file paths, database IDs, amounts) are safe, adhere to business logic (non-negative financial values, date ranges), and prevent security risks like path traversal attacks or injection attempts.

- **Post-Execution Sanitization:** Simplify and prune complex, nested JSON or verbose API outputs into concise, token-efficient observations. Use structured querying languages (like JQ or JSONPath) to extract only the most relevant fields, preventing context window bloat.

#### 3. Handling Context Switching
When a tool is called, the orchestrator needs to pause the LLM's reasoning chain, execute the tool, and resume by injecting the observation. This context switch must be seamless. Prepend the observation directly to the history, ensuring it acts as the most recent, high-attention piece of data, mitigating the "Lost in the Middle" problem.

#### 4. Constrained Tool Use & Execution Guardrails
Implement safety mechanisms to prevent harmful, costly, or unproductive behavior:

- **Safety and Recursive Guardrails:** Set strict maximum number of steps in the ReAct loop, use exponential backoff for retries, and proactively block recursive calls (same tool with same input repeatedly).

- **Cost and Rate Monitoring:** Implement runtime counters and alerts for expensive tools, enforce per-session and global rate limits on external APIs.

- **Tool Sandbox Isolation:** Fully sandbox the execution environment, particularly for tools that execute arbitrary code. Use containerization technologies like Docker or gVisor to ensure agent actions are strictly constrained.

#### 5. Tool Result Management (Retrieve-then-Read)
For large tool outputs, use a two-step process:
- **Retrieve:** Get a pointer, list of resource IDs, or brief summary
- **Read:** Selectively pull in only specific, relevant content snippets based on reasoning

This minimizes token consumption by avoiding full dumps of large data into the context.

### Code Examples

#### LangChain Implementation

```python
import os
import asyncio
import nest_asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool as langchain_tool
from langchain.agents import create_tool_calling_agent, AgentExecutor

# Initialize the language model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Define a Tool
@langchain_tool
def search_information(query: str) -> str:
    """
    Provides factual information on a given topic. Use this tool to
    find answers to phrases like 'capital of France' or 'weather in London?'.
    """
    print(f"\n--Tool Called: search_information with query: '{query}' ---")
    
    # Simulate a search tool with predefined results
    simulated_results = {
        "weather in london": "The weather in London is currently cloudy with a temperature of 15°C.",
        "capital of france": "The capital of France is Paris.",
        "population of earth": "The estimated population of Earth is around 8 billion people.",
        "tallest mountain": "Mount Everest is the tallest mountain above sea level.",
        "default": f"Simulated search result for '{query}': No specific information found."
    }
    
    result = simulated_results.get(query.lower(), simulated_results["default"])
    print(f"--- TOOL RESULT: {result} ---")
    return result

tools = [search_information]

# Create a Tool-Calling Agent
agent_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(agent=agent, verbose=True, tools=tools)

async def run_agent_with_tool(query: str):
    """Invokes the agent executor with a query and prints the final response."""
    print(f"\n--Running Agent with Query: '{query}' ---")
    try:
        response = await agent_executor.ainvoke({"input": query})
        print("\n--Final Agent Response ---")
        print(response["output"])
    except Exception as e:
        print(f"\nAn error occurred during agent execution: {e}")

async def main():
    """Runs all agent queries concurrently."""
    tasks = [
        run_agent_with_tool("What is the capital of France?"),
        run_agent_with_tool("What's the weather like in London?"),
        run_agent_with_tool("Tell me something about dogs.")
    ]
    await asyncio.gather(*tasks)

nest_asyncio.apply()
asyncio.run(main())
```

#### CrewAI Implementation

```python
import os
from crewai import Agent, Task, Crew
from crewai.tools import tool
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')

# Define a Tool
@tool("Stock Price Lookup Tool")
def get_stock_price(ticker: str) -> float:
    """
    Fetches the latest simulated stock price for a given stock ticker symbol.
    Returns the price as a float. Raises a ValueError if the ticker is not found.
    """
    logging.info(f"Tool Call: get_stock_price for ticker '{ticker}'")
    
    simulated_prices = {
        "AAPL": 178.15,
        "GOOGL": 1750.30,
        "MSFT": 425.50,
    }
    
    price = simulated_prices.get(ticker.upper())
    if price is not None:
        return price
    else:
        raise ValueError(f"Simulated price for ticker '{ticker.upper()}' not found.")

# Define the Agent
financial_analyst_agent = Agent(
    role='Senior Financial Analyst',
    goal='Analyze stock data using provided tools and report key prices.',
    backstory="You are an experienced financial analyst adept at using data sources to find stock information.",
    verbose=True,
    tools=[get_stock_price],
    allow_delegation=False,
)

# Define the Task
analyze_aapl_task = Task(
    description=(
        "What is the current simulated stock price for Apple (ticker: AAPL)? "
        "Use the 'Stock Price Lookup Tool' to find it. "
        "If the ticker is not found, you must report that you were unable to retrieve the price."
    ),
    expected_output=(
        "A single, clear sentence stating the simulated stock price for AAPL. "
        "For example: 'The simulated stock price for AAPL is $178.15.'"
    ),
    agent=financial_analyst_agent,
)

# Formulate the Crew
financial_crew = Crew(
    agents=[financial_analyst_agent],
    tasks=[analyze_aapl_task],
    verbose=True
)

# Run the Crew
def main():
    """Main function to run the crew."""
    if not os.environ.get("OPENAI_API_KEY"):
        print("ERROR: The OPENAI_API_KEY environment variable is not set.")
        return
    
    print("\n## Starting the Financial Crew...")
    result = financial_crew.kickoff()
    print("\n## Crew execution finished.")
    print("\nFinal Result:\n", result)

if __name__ == "__main__":
    main()
```

#### Google ADK Implementation

```python
import asyncio
from google.adk.agents import Agent as ADKAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types
import nest_asyncio

# Define variables
APP_NAME = "Google Search_agent"
USER_ID = "user1234"
SESSION_ID = "1234"

# Define Agent with access to search tool
root_agent = ADKAgent(
    name="basic_search_agent",
    model="gemini-2.0-flash-exp",
    description="Agent to answer questions using Google Search.",
    instruction="I can answer your questions by searching the internet. Just ask me anything!",
    tools=[google_search]  # Google Search is a pre-built tool
)

# Agent Interaction
async def call_agent(query):
    """Helper function to call the agent with a query."""
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    content = types.Content(role='user', parts=[types.Part(text=query)])
    
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    
    for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)

nest_asyncio.apply()
asyncio.run(call_agent("what's the latest ai news?"))
```

## Key Takeaways

- **Tool Use (Function Calling)** allows agents to interact with external systems and access dynamic information beyond their training data.
- **Agent-Computer Interface (ACI)** is the critical contract between the LLM and execution environment, requiring careful design for reliability and security.
- **Idempotency** is essential: tool calls should produce the same observable side effect regardless of execution count.
- **Tool definitions** must be clear, detailed, and include boundaries and negative examples to guide proper usage.
- **Input/output validation** adds crucial security and robustness layers between the LLM and external systems.
- **Frameworks** like LangChain, CrewAI, and Google ADK provide abstractions that simplify tool integration and execution.
- **Google ADK** includes pre-built tools like Google Search, Code Execution, and Vertex AI Search that can be directly integrated.
- **Tool Use** transforms language models from text generators into agents capable of real-world action and up-to-date information retrieval.

## Related Patterns

- **Planning:** Tool Use often works in conjunction with Planning, where agents create structured plans that include tool calls as steps.
- **Routing:** Routing can determine which tools are available or appropriate based on context or user permissions.
- **Reflection:** Tool results can be evaluated and refined through Reflection patterns.
- **Multi-Agent Architectures:** Different agents can have different tool sets, enabling specialization.
- **Exception Handling:** Robust error handling is critical when tools fail or return unexpected results.
- **Memory Management:** Tool results may need to be stored in external memory systems for later retrieval.

## References

1. LangChain Documentation (Tools): https://python.langchain.com/docs/integrations/tools/
2. Google Agent Developer Kit (ADK) Documentation (Tools): https://google.github.io/adk-docs/tools/
3. OpenAI Function Calling Documentation: https://platform.openai.com/docs/guides/function-calling
4. CrewAI Documentation (Tools): https://docs.crewai.com/concepts/tools
