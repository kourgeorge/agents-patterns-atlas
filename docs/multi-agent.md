# Multi-Agent Architectures

## Introduction

As LLM-based agentic systems tackle increasingly complex problems, a single agent often reaches its limits. 
Context window constraints, lack of specialization, and the complexity of multifaceted objectives can cause even sophisticated agents to fail. 
Multi-agent architectures address these limitations by enabling specialized LLM agents to collaborate, each focusing on their domain of expertise and leveraging natural language communication.
This chapter provides an overview of modern LLM-based multi-agent architectures, exploring when and why to use multiple agents, the benefits they provide, and the organizational patterns that enable effective collaboration. 
For detailed implementation patterns, see the specific pattern modules referenced throughout this chapter.

> "Agentic systems represent a new paradigm that breaks traditional barriers. More than tools, agents act as collaborators, assisting humans in dynamic environments and automating decision-making." - Aatrbin

## The Case for Multi-Agent Systems

Multi-agent architectures represent a paradigm shift from pursuing a single, all-powerful super-agent toward sophisticated, collaborative systems of specialized LLM agents.

The collective strength lies in division of labor, natural language negotiation, and synergy created through coordinated effort.

> **"Multi-agent is about role specialization, not redundancy."** — Manus Team

**Why Multiple Agents? An Intuitive Perspective?** 
When first encountering multi-agent systems, a natural question arises: "Why do I need multiple agents? It's just the same LLM that I'm prompting over and over, or just one computer. Why do I need multiple agents?"
This question reflects a common misconception. Even though you may be using a single LLM or a single computer, the way you structure and coordinate work can dramatically impact both the quality of outputs and the ease of development.

Just as a single computer can run multiple processes or threads, even though it's one CPU, developers decompose work into multiple processes and multi-threaded programs. This decomposition makes it easier to write code, manage complexity, and achieve better performance. Similarly, in multi-agent systems, even though you're using the same underlying LLM, decomposing complex tasks into multiple specialized agents makes the system easier to design, debug, and optimize.

For complex tasks, instead of thinking "what's the one person I might hire to do something," consider "would it make sense to hire people with three or four different roles to do this overall task for me?" This mental framework helps decompose complex work into sub-tasks and build for those individual sub-tasks one at a time. Just as human teams benefit from specialization (a researcher, a designer, and a writer working together), multi-agent systems benefit from role-based specialization where each agent focuses on their domain of expertise.
In practice, many developers find that having this mental framework—thinking about hiring a team rather than a single person—helps give another way to take a complex thing and decompose it into sub-tasks. You can focus on building one specialized agent at a time (e.g., the best graphic designer agent you can), while collaborators build other agents (e.g., research agents and writer agents), then string them all together into a cohesive multi-agent system.

This approach also enables agent reuse: having built a graphic designer for marketing brochures, you might build a more general graphic designer that can help with marketing brochures, social media posts, and web page illustrations. By thinking in terms of roles and teams, you create reusable, composable agents that can be combined in different ways for different tasks.

### Why Single LLM Agents Fail?

Even highly capable LLM agents face fundamental limitations:

- **Context Window Constraints:** Complex tasks require more information than fits in a single context window, forcing difficult trade-offs between breadth and depth
- **Lack of Specialization:** Generalist agents cannot match the performance of specialized agents with domain-specific prompts, tools, and knowledge
- **Sequential Bottlenecks:** Tasks that could be parallelized are forced into sequential execution, dramatically increasing latency
- **Reasoning Degeneration:** Single agents may fixate on initial incorrect approaches, lacking mechanisms to explore alternative solutions
- **Tool Use Limitations:** Single agents struggle to orchestrate complex multi-tool workflows requiring global optimization

### The Multi-Agent Advantage

Modern LLM-based multi-agent systems address these limitations through:

- **Role-Based Specialization:** Each agent can be optimized for specific roles (researcher, writer, coder, reviewer, planner) with domain-specific prompts, tools, and Standard Operating Procedures (SOPs). Systems like ChatDev and MetaGPT demonstrate that role-based specialization produces higher quality outputs than filtering everything through a general coordinator.
- **Parallel Execution:** Multiple agents can work simultaneously on independent tasks, dramatically reducing execution time. Parallel execution of specialized agents can reduce research time by up to 90% for complex queries that require exploring multiple directions simultaneously.
- **Context Window Distribution:** Multi-agent systems effectively scale context capacity for tasks that exceed single-agent limits. By distributing work across agents with separate context windows, systems add capacity for parallel reasoning and reduce context compression losses.
- **Debate and Verification:** Multiple agents can engage in natural language debate, discussion, or critique, catching errors that a single agent might miss. This collaborative verification improves accuracy and reduces hallucinations.

> **"Coordination is emergent when communication channels are well-designed."** — Google DeepMind
- **Dynamic Orchestration:** Modern systems like AgentVerse enable dynamic adjustment of team composition, spawning specialist agents as needed and releasing them when tasks complete, optimizing resource usage.


## Concrete Examples: Building Multi-Agent Teams

To understand how multi-agent systems work in practice, let's examine concrete examples where complex tasks are naturally decomposed into sub-tasks that different people with different skills can carry out. These examples illustrate how to think about building agent teams by identifying the roles needed and the tools each role requires.

??? "Example 1: Creating Marketing Assets"

    Consider the task of creating marketing assets, such as a marketing brochure for sunglasses. This task naturally breaks down into roles that require different expertise:

    **Researcher Agent:**

    - **Role:** Analyze market trends and research competitors
    - **Task:** Look at trends on sunglasses and what competitors are offering
    - **Required Tools:** Web search capabilities to conduct online research
    - **Output:** Research report summarizing current sunglasses trends and competitive offerings

    **Graphic Designer Agent:**

    - **Role:** Create visualizations and artwork
    - **Task:** Render charts or nice-looking graphics of sunglasses
    - **Required Tools:**

            - Image generation APIs (e.g., DALL-E, Midjourney)
            - Image manipulation APIs
            - Code execution capabilities for generating charts and data visualizations

    - **Output:** Visual assets including charts, graphics, and artwork options

    **Writer Agent:**

    - **Role:** Transform research into report text and marketing copy
    - **Task:** Take the research and graphic assets and put it all together into a nice-looking brochure
    - **Required Tools:** Text generation (inherent LLM capability, no additional tools needed)
    - **Output:** Final marketing brochure with integrated research and visuals

    **How They Work Together:** The researcher conducts market analysis, the graphic designer creates visual assets based on the research findings, and the writer synthesizes everything into the final marketing brochure.

??? "Example 2: Writing a Research Article"

    For writing a research article, you might need a team with complementary skills:

    **Researcher Agent:**

    - **Role:** Conduct online research and gather information
    - **Task:** Do online research on the topic
    - **Required Tools:** Web search, academic database access, web scraping
    - **Output:** Research findings and source materials

    **Statistician Agent:**

    - **Role:** Calculate statistics and perform data analysis
    - **Task:** Analyze data and compute statistical measures
    - **Required Tools:** Code execution for statistical calculations, data analysis libraries
    - **Output:** Statistical analysis and results

    **Lead Writer Agent:**

    - **Role:** Draft the article content
    - **Task:** Write the research article based on research and statistics
    - **Required Tools:** Text generation, potentially citation management
    - **Output:** Draft article with research and statistics integrated

    **Editor Agent:**

    - **Role:** Review and polish the content
    - **Task:** Review the draft for quality, clarity, and accuracy
    - **Required Tools:** Text analysis, potentially fact-checking tools
    - **Output:** Polished, final research report

    **How They Work Together:** The researcher gathers information, the statistician analyzes data, the lead writer drafts the article, and the editor reviews and refines it into a polished final report.

??? "Example 3: Preparing a Legal Case"

    Real law firms often use teams with different roles, which translates well to multi-agent systems:

    **Associate Agent:**
    - **Role:** Legal research and case analysis
    - **Task:** Research case law, statutes, and legal precedents
    - **Required Tools:** Legal database access, document search, case law retrieval
    - **Output:** Legal research findings and case analysis

    **Paralegal Agent:**
    - **Role:** Document preparation and case management
    - **Task:** Organize documents, prepare filings, manage case materials
    - **Required Tools:** Document management systems, file organization tools
    - **Output:** Organized case files and prepared documents

    **Investigator Agent:**
    - **Role:** Fact-finding and evidence gathering
    - **Task:** Investigate facts, gather evidence, interview relevant parties
    - **Required Tools:** Web search, public records access, information retrieval systems
    - **Output:** Investigation findings and evidence summaries

    **How They Work Together:** The investigator gathers facts and evidence, the associate researches relevant law, the paralegal organizes everything into case files, and together they prepare a comprehensive legal case.

### Key Insights from These Examples

These examples demonstrate several important principles:

1. **Natural Decomposition:** Complex tasks often naturally decompose into sub-tasks that require different skills, making them ideal candidates for multi-agent systems.
2. **Tool Specialization:** Each agent role requires specific tools. A researcher needs web search, a graphic designer needs image generation, a statistician needs code execution. This tool specialization is a key aspect of role-based specialization.
3. **Clear Role Boundaries:** Each agent has a well-defined role with clear responsibilities, preventing overlap and ensuring complete coverage of the task.
4. **Sequential and Parallel Workflows:** Some agents work sequentially (researcher → writer), while others can work in parallel (multiple researchers exploring different aspects simultaneously).
5. **Reusability:** Once built, agents like a graphic designer or researcher can be reused across different projects and combined in different ways.

## Building Individual Agents

Once you've identified the roles needed for your multi-agent system, the next step is to build each individual agent. 
The way you build individual agents is by prompting an LLM to play the role of a researcher, graphic designer, writer, or whatever role that agent is part of.
Each agent is built by:

1. **Defining the role:** Clearly specify what role the agent should play (e.g., research agent, graphic designer, writer).
2. **Providing role-specific instructions:** Give the agent expert-level instructions for their domain. Specialized prompts tuned for each agent's role, potentially encoding SOPs.
3. **Assigning tools:** Provide the agent with the tools they need to perform their role.
4. **Setting clear objectives:** Define what the agent should accomplish and what output is expected. Well-defined responsibilities to avoid duplication and gaps.
5. **Reusability:** Design agents to be reusable. A well-built graphic designer agent should be able to work on marketing brochures, social media posts, and web page illustrations.

??? "Example: Building a Research Agent"

    ```python
    #For a research agent that analyzes market trends and competitors, you might create a prompt like:

    research_agent_prompt = """You are a research agent, expert at analyzing market trends and competitors.

    Your role:
    - Conduct online research to analyze market trends
    - Research competitor offerings and strategies
    - Summarize findings in a clear, structured format

    Available tools:
    - web_search(query): Search the web for information
    - web_scraper(url): Extract content from web pages

    Task: Carry out online research to analyze market trends for the sunglasses product and give a summary as well of what competitors are doing.

    Provide your research findings as a structured report with:
    1. Current market trends
    2. Competitor analysis
    3. Key insights and recommendations"""
    ```

??? "Example: Building a Graphic Designer Agent"

    ```python
    # For a graphic designer agent that creates visualizations and artwork:
    graphic_designer_prompt = """You are a graphic designer agent, expert at creating visualizations and artwork.

    Your role:
    - Create data visualizations and charts
    - Generate artwork and graphics
    - Design visual assets for marketing materials

    Available tools:
    - generate_image(prompt): Generate images using image generation API
    - create_chart(data, chart_type): Create charts and data visualizations
    - manipulate_image(image, operation): Edit and manipulate images

    Task: Based on the research data provided, create a few data visualizations and artwork options that can be used in marketing materials.

    Provide:
    1. Data visualizations (charts, graphs)
    2. Artwork options
    3. Design recommendations"""
    ```

??? "Example: Building a Writer Agent"

    ```python
    #For a writer agent that synthesizes research and graphics into final content:
    writer_agent_prompt = """You are a writing specialist agent, expert at creating clear, well-structured content.

    Your role:
    - Transform research findings into written content
    - Integrate visual assets with written text
    - Create marketing copy and reports

    Available tools:
    - Text generation (inherent LLM capability)

    Task: Take the research findings and graphic assets provided, and write the final marketing brochure that integrates everything into a cohesive, compelling document.

    Provide:
    1. Marketing brochure text
    2. Integration of research insights
    3. References to visual assets
    4. Clear, engaging copy"""
    ```


## Building the Team

Once you've built individual agents, you can combine them into a multi-agent system. 
The advantage of building agents one at a time is that you can focus on making each agent excellent at their specific role. 
You can spend time building the best graphic designer agent you can, while collaborators build research agents and writer agents, then string them all together into a cohesive system.
This modular approach also enables agent reuse: having built a graphic designer for marketing brochures, you might build a more general graphic designer that can help with marketing brochures, social media posts, and web page illustrations. By thinking in terms of roles and building specialized agents, you create reusable, composable components that can be combined in different ways for different tasks.

Modern LLM-based multi-agent systems employ several organizational patterns, each suited to different problem types:

### Orchestrator-Worker Pattern

A central orchestrator (lead agent/coordinator) breaks high-level goals into sub-tasks and delegates them to specialized worker agents. The orchestrator analyzes queries, develops strategies, dynamically creates specialized subagents with clear objectives, coordinates parallel execution, and synthesizes results.

**The Manager as Fourth Agent:** One useful way to think about the orchestrator-worker pattern is that the orchestrator is effectively a "fourth agent" that coordinates the other agents. For example, in a marketing team, you might have a researcher, graphic designer, and writer as worker agents, plus a marketing manager agent that coordinates their work. The manager agent sets direction and delegates tasks to the specialized workers, creating a collection of four agents where one agent manages the others.

This pattern is detailed in the **Pattern: Orchestrator-Worker (Coordinator)** module.

**Linear Workflow Example:**

A simple way to have agents work together is to use a linear workflow where agents take actions one at a time. For example, to create a summer marketing campaign for sunglasses:

1. **Research Agent** receives the prompt: "Create a summer marketing campaign for sunglasses". The research agent conducts research and writes a report: "Here are the current sunglasses trends and competitive offerings"
2. **Graphic Designer Agent** receives the research report. The graphic designer looks at the data the research has found and creates a few data visualizations and artwork options
3. **Writer Agent** receives both the research report and graphic output. The writer takes the research and the graphic output and writes the final marketing brochure

This linear plan has the advantage that when designing a researcher, graphic designer, or writer, you can focus on one thing at a time. 
You can spend time building the best graphic designer agent you can, while collaborators build research agents and writer agents, then string them all together into this multi-agent system.

**Hierarchical Workflow Example:**

As an alternative to a linear plan, you can have agents interact in more complex ways. Instead of giving an LLM a set of tools to call, you can give an LLM the option to call on different agents to ask them to help complete different tasks.
For example, you might write a prompt like: "You're a marketing manager. You have the following team of agents to work with: [description of agents]. Return a step-by-step plan to carry out the user's request."

The LLM (acting as marketing manager) may create a plan:

- Step 1: Ask the researcher to research current sunglasses trends, then report back
- Step 2: Ask the graphic designer to create the images, then report back
- Step 3: Ask the writer to create the report, then report back
- Step 4: Review and reflect on the report one final time

In executing this plan, you would then take step one, carry out research, pass that to the graphic designer, pass it to the writer, and then do one final reflection step.
This becomes a collection of four agents: a marketing manager agent coordinating the work of the researcher, graphic designer, and writer agents. The manager agent receives results from workers and coordinates the overall workflow, rather than workers passing results directly to each other.

**Examples:**

- **ChatDev (2023):** Simulates a software development team with LLM-based agents filling roles like software designer, coder, and tester. Agents communicate in natural language to clarify requirements, generate code, and debug, using a structured chat chain.
- **MetaGPT (2024):** Encodes Standard Operating Procedures (SOPs) into prompts for distinct job roles (architect, programmer, reviewer), ensuring each agent has expert-level domain knowledge and can verify each other's results.
- **AutoGen (2024):** Provides flexible communication patterns among LLM agents, with one agent assigned as a "project manager" that breaks queries into pieces, delegates to specialist agents, then integrates outputs.

### Dynamic Agent Spawning Pattern

An advanced evolution of the Orchestrator-Worker pattern where the orchestrator agent dynamically creates specialized worker agents at runtime, rather than selecting from a predefined set. The orchestrator analyzes each subtask, determines what specialized capabilities are needed, and generates new agents (as code, prompts, or configurations) tailored to each specific task.

**Key Distinction:** Unlike static agent selection where agents are predefined with fixed roles, dynamic spawning creates agents on-demand with task-specific specializations. This enables maximum flexibility and adaptation to unpredictable task requirements.

**How It Works:**
1. Orchestrator receives a high-level goal and decomposes it into subtasks
2. For each subtask, orchestrator analyzes what specialized agent is needed
3. Orchestrator checks if existing agents can handle the subtask
4. If not, orchestrator generates a new specialized agent with:
   - Tailored prompts optimized for the specific subtask
   - Appropriate tools and capabilities
   - Clear objectives and expected outputs
5. Orchestrator assembles spawned agents into a multi-agent system
6. Agents execute their specialized tasks
7. Orchestrator synthesizes results

**Examples:**
- **Anthropic's Multi-Agent Research System:** LeadResearcher agent spawns specialized Web Search subagents, each configured for specific research aspects (academic papers, industry news, technical docs), working in parallel
- **Emergence.ai Orchestrator:** Starting from a single task, automatically decomposes it, checks existing agents, generates new specialized agents (as code) for each step, and continuously creates new agents to tackle an expanding set of problems
- **EvoMAC:** Parent agent dynamically creates child agents to handle specific subtasks during runtime, with iterative refinement capabilities

**When to Use:**
- Tasks with unpredictable requirements where agent roles cannot be predetermined
- Complex, evolving problems requiring different specializations as understanding deepens
- Enterprise automation where requirements vary significantly across use cases
- When task-specific optimization justifies the overhead of agent generation

**Trade-offs:**
- ✅ Maximum flexibility and task-specific optimization
- ✅ Adaptive problem-solving that evolves with requirements
- ✅ Resource efficiency (agents created only when needed)
- ❌ Increased complexity and system unpredictability
- ❌ Higher latency and cost (agent generation overhead)
- ❌ Reduced reproducibility compared to static agents

This pattern is detailed in the **Pattern: Dynamic Agent Spawning** module.

### Evaluator-Optimizer Pattern

An iterative loop where one agent generates solutions and another critiques them, enabling quality improvement through specialized feedback. 
The generator creates initial outputs, the evaluator provides critique, and the generator refines based on feedback in a continuous improvement cycle.
This pattern is detailed in the **Pattern: Evaluator-Optimizer** module. 
It is similar to the **Pattern: Reflection** but involves separate specialized agents rather than a single agent reflecting on itself, enabling domain-specific expertise in both generation and evaluation.
**Example:** A coding system where a Coder agent writes code, a Reviewer agent critiques it with specialized code review expertise, and the Coder refines based on feedback in an iterative loop.

### Planner-Checker Pattern

A triad of agents where a Plan Agent produces a precise multi-step plan, a Tool/Executor Agent carries out the plan using external tools, and a Reflect/Checker Agent evaluates outcomes and correctness. This decouples planning from execution and verification, enabling global optimization of action sequences.
This pattern is detailed in the **Pattern: Planner-Checker** module.

**Examples:**

- **CoReaAgents (2025):** Defines Plan Agent, Tool Agent, and Reflect Agent working together for complex reasoning tasks
- **Plan-and-Execute (2025):** Introduces a dedicated planning model that outputs a global directed acyclic graph (DAG) of sub-tasks, with an executor model following the optimized plan
- **HuggingGPT (2023):** Uses a ChatGPT-based controller to analyze requests, plan subtask sequences, delegate to appropriate AI models, and synthesize results

### Multi-Agent Debate Pattern

Multiple agents engage in structured debate, discussion, or negotiation to improve reasoning quality or reach consensus. 
Agents may argue different viewpoints, critique each other's reasoning, or engage in cooperative negotiation, with optional judge agents overseeing the discussion.
This pattern is detailed in the **Pattern: Multi-Agent Debate** module.

**Examples:**

- **Multi-Agent Debate (MAD) Framework:** Two agent debaters take opposite stances and argue in rounds, with a third agent as a neutral judge monitoring and deciding
- **Society of Minds:** Multiple LLM instances discuss questions and converge on joint answers through debate and agreement
- **CICERO (2022):** Achieved human-level performance in Diplomacy through strategic planning combined with natural language negotiation and alliance-forming dialogue

### Swarm/Consensus Architectures

Autonomous agents coordinate through natural language discussion, voting mechanisms, or consensus algorithms rather than centralized control. 
Agents interact through shared state, debate, or voting to reach collective decisions.
This pattern is detailed in the **Pattern: Swarm/Consensus Architecture** module.

**Example:** Multiple research agents that independently explore a problem space, share findings through natural language discussion, and converge on solutions through consensus voting or iterative agreement.

### Agent-as-Tool Pattern

Instead of anthropomorphizing agents as organizational entities (Manager, Designer, Coder) that chat with each other, the Agent-as-Tool pattern treats agents as deterministic, tool-like functions. 
This approach flattens complexity, improves modularity, and reduces token overhead.
Don't over-anthropomorphize agents. 
You don't need an "Org Chart" of agents that maintain persistent conversations. 
Instead, treat agents as tools that the main agent invokes through structured function calls.

For the main model, "Deep Research" or "Plan Task" should be a simple tool call. 
The main agent invokes `call_planner(goal="...")`, the harness spins up a temporary sub-agent loop, executes the task, and returns a structured result. 
This allows the main agent to treat sub-agents exactly like deterministic code functions.

**Benefits:**

- **Flattened Complexity:** Agents become composable functions rather than persistent organizational entities
- **Modularity:** Sub-agents can be easily swapped, modified, or versioned
- **Token Efficiency:** Structured outputs reduce token overhead compared to conversational approaches
- **Deterministic Interfaces:** Clear input/output contracts enable predictable behavior
- **Cache Optimization:** Deterministic tool-like calls enable better caching strategies

**When to Use:**

Use Agent-as-Tool for:

- Discrete tasks with clear inputs and outputs
- Tasks that can be completed independently
- Operations that benefit from structured schemas
- Scenarios where conversational overhead is unnecessary

Prefer conversational multi-agent patterns when:

- Agents need to negotiate or debate
- Tasks require iterative refinement through dialogue
- Complex coordination requires natural language communication

## Communication Patterns: A Key Design Decision

One of the key design decisions you'll need to make when building multi-agent systems is: **what is the communication pattern between your different agents?** 
This is an area of active research, and there are multiple patterns emerging. T
he communication pattern you choose determines how agents interact, coordinate, and share information.
Designing communication patterns for multi-agent systems is similar to designing organizational charts for human teams—it's complex, but critical for effective collaboration. 
The pattern you choose impacts system predictability, coordination overhead, and the types of problems your system can handle.

While agents can use any type of structured or non structured modality for communication, what makes them unique is there ability to coordinate through natural language, enabling rich communication, negotiation, debate, and consensus-building. 
This natural language interface allows agents to clarify requirements, critique reasoning, negotiate solutions, and build consensus in ways that classical agent systems cannot.

Agents must communicate, share state, and coordinate their actions toward common goals. 
This requires:

- Clear communication protocols (natural language dialogues, structured messages)
- Shared state management (knowledge bases, blackboards, external memory)
- Task delegation mechanisms (orchestrator routing, dynamic spawning)
- Result synthesis strategies (integration, consensus, voting)


### Linear Communication Pattern

In a linear communication pattern, agents communicate sequentially in a chain, where one agent's output becomes the next agent's input. 
This is one of the two most common communication patterns used today.

**How It Works:**

- Agent A completes their work and passes output to Agent B
- Agent B processes the input and passes output to Agent C
- The chain continues until the final agent produces the end result

**Example: Marketing Team with Linear Plan**

For creating a summer marketing campaign for sunglasses:

1. **Research Agent** receives the prompt: "Create a summer marketing campaign for sunglasses"
2. Research Agent writes a report: "Here are the current sunglasses trends and competitive offerings"
3. **Graphic Designer Agent** receives the research report and creates data visualizations and artwork options
4. **Writer Agent** receives both the research and graphic output, then writes the final marketing brochure

**When to Use:**

- Tasks have clear sequential dependencies
- Each agent's output is needed as input for the next agent
- Simple, predictable workflows
- Low coordination overhead needed

**Trade-offs:**

- ✅ Simple to implement and understand
- ✅ Low coordination overhead
- ✅ Predictable execution flow
- ❌ Cannot parallelize dependent steps
- ❌ Sequential bottlenecks can slow down execution
- ❌ Less flexible for dynamic task requirements


### Hierarchical Communication Pattern

In a hierarchical communication pattern, a manager agent coordinates the work of multiple team member agents. The manager receives the high-level goal, creates a plan, delegates tasks to specialized agents, receives their results, and synthesizes the final output. 
This is the second of the two most common communication patterns.

**How It Works:**

- A manager agent (orchestrator) receives the user's request
- The manager creates a step-by-step plan
- The manager delegates each step to appropriate worker agents
- Worker agents report back to the manager
- The manager synthesizes all results into the final output

**Example: Marketing Manager Coordinating Team**

Instead of a linear flow, you might have:

1. **Marketing Manager Agent** receives: "Create a summer marketing campaign for sunglasses"
2. Manager creates a plan:
   
        - Step 1: Ask researcher to research current sunglasses trends
        - Step 2: Ask graphic designer to create images
        - Step 3: Ask writer to create report
        - Step 4: Review and improve the report

3. Manager delegates to **Researcher Agent**, receives research report
4. Manager delegates to **Graphic Designer Agent**, receives graphic assets
5. Manager delegates to **Writer Agent**, receives draft brochure
6. Manager reviews and synthesizes final output

**Implementation Note:** In practice, it's simpler to have workers report back to the manager rather than passing results directly between workers. The manager acts as the central coordinator.

**When to Use:**

- Tasks require dynamic planning and coordination
- Multiple agents can work in parallel on independent subtasks
- Central oversight and quality control is needed
- Task decomposition is unpredictable and requires runtime decisions

**Trade-offs:**

- ✅ Enables parallel execution of independent tasks
- ✅ Central coordination allows for dynamic planning
- ✅ Manager can review and improve outputs
- ✅ More flexible than linear patterns
- ❌ Higher coordination overhead
- ❌ Manager becomes a potential bottleneck
- ❌ More complex to implement

**Framing Note:** The manager agent is effectively a "fourth agent" that coordinates the other three (researcher, graphic designer, writer). This mental model helps understand hierarchical systems as collections of agents where one agent manages the others.

### Deeper Hierarchy Pattern

A deeper hierarchy extends the hierarchical pattern by allowing worker agents to themselves have sub-agents. This creates nested multi-agent structures.

**How It Works:**

- Manager agent coordinates worker agents
- Some worker agents themselves coordinate sub-agents
- Creates a tree-like organizational structure

**Example: Marketing Team with Sub-Agents**

- **Marketing Manager** coordinates:

    - **Researcher Agent** (which has sub-agents):

        - Web Researcher Agent
        - Fact Checker Agent

    - **Graphic Designer Agent** (works independently)
    - **Writer Agent** (which has sub-agents):

        - Initial Style Writer Agent
        - Citation Checker Agent

**When to Use:**

- Very complex tasks requiring multiple levels of specialization
- Tasks where some subtasks themselves need decomposition
- Large-scale systems with many specialized roles

**Trade-offs:**

- ✅ Handles very complex, multi-level tasks
- ✅ Enables fine-grained specialization
- ✅ Can model complex organizational structures
- ❌ Much more complex than one-level hierarchy
- ❌ Higher coordination overhead
- ❌ Harder to debug and maintain
- ❌ Used less frequently today due to complexity

### All-to-All Communication Pattern

In an all-to-all communication pattern, any agent can communicate with any other agent at any time. There is no predefined structure or hierarchy—agents collaborate in a decentralized, crowd-like manner.

**How It Works:**
- All agents are aware of all other agents
- Any agent can send a message to any other agent at any time
- When an agent sends a message, it gets added to the receiver agent's context
- The receiver agent processes the message and can respond or take action
- Agents declare when they're done with their task
- The system concludes when all agents are done or when a designated agent (e.g., the writer) concludes the task is complete

**Example: Marketing Team with All-to-All Communication**

All four agents (researcher, graphic designer, writer, and potentially a manager) can:
- Send messages to each other
- Request information from each other
- Provide feedback to each other
- Collaborate dynamically without predefined structure

**Implementation Approach:**

1. Prompt all agents to tell them about the other agents they can call on
2. When one agent sends a message to another, add it to the receiver's context
3. The receiver agent processes the message and decides when to respond
4. Agents collaborate until each declares they're done
5. System concludes when consensus is reached or a designated agent signals completion

**When to Use:**

- Tasks benefit from open collaboration and negotiation
- Unpredictable problem-solving where structure emerges dynamically
- Applications that can tolerate some unpredictability
- Experimental or research scenarios

**Trade-offs:**

- ✅ Maximum flexibility and emergent behavior
- ✅ Agents can negotiate and collaborate freely
- ✅ No predefined structure constraints
- ❌ Results are harder to predict
- ❌ Can be chaotic and unpredictable
- ❌ Difficult to debug and control
- ❌ May not converge or may produce inconsistent results
- ❌ Used less frequently in production systems

**Note:** In practice, all-to-all communication patterns produce results that are harder to predict. 
Some applications don't need high control—you can run it and see what you get. 
If the marketing brochure isn't good, maybe that's okay—you just run it again and see if you get a different result. 
For applications where you're willing to tolerate some chaos and unpredictability, some developers do use this communication pattern.

### Choosing a Communication Pattern

The communication pattern you choose depends on your requirements:

- **Use Linear** when: Tasks have clear sequential dependencies, you want simplicity and predictability
- **Use Hierarchical** when: Tasks need dynamic planning, parallel execution is possible, central coordination is beneficial
- **Use Deeper Hierarchy** when: Tasks are very complex and require multiple levels of decomposition
- **Use All-to-All** when: Maximum flexibility is needed, unpredictability is acceptable, experimental scenarios

Most production systems today use **Linear** or **Hierarchical** patterns, as they provide the best balance of flexibility, predictability, and control. Many modern multi-agent frameworks make implementing these communication patterns relatively straightforward.

## Integration with Other Capabilities

Multi-agent systems integrate with other agent capabilities:

- **Pattern: Routing** - Orchestrators use routing to delegate tasks to appropriate workers
- **Pattern: Parallelization** - Multiple agents can work concurrently on independent tasks
- **Pattern: Planning** - Orchestrators create plans that guide multi-agent workflows
- **Pattern: Planner-Checker** - Separates planning, execution, and verification across agents
- **Pattern: Multi-Agent Debate** - Agents engage in structured debate to improve reasoning
- **Memory Management** - Shared state and context enable agent coordination
- **Pattern: Tool Use** - Each agent may have specialized tools for their domain
- **Pattern: Exception Handling** - Robust error handling is critical when multiple agents interact

## Key Insights

1. **Multi-agent systems are not always better:** They add significant complexity and cost (15× more tokens). Use them when the benefits of specialization and parallelization justify the overhead.
2. **Role-based specialization is key:** Specialized agents with domain-specific prompts, tools, and SOPs outperform generalist agents filtering everything through a coordinator.
3. **Parallelization drives performance:** The ability to execute multiple agents in parallel can reduce execution time by up to 90% for suitable tasks.
4. **Context isolation enables scale:** Each agent's separate context window adds capacity for parallel reasoning, essential for complex tasks.
5. **Natural language enables rich coordination:** LLM agents can engage in debate, negotiation, and consensus-building through natural language, enabling coordination patterns impossible in classical systems
6. **Collaborative verification improves quality:** Multiple agents debating, critiquing, or cross-verifying can catch errors that a single agent might miss.
7. **Dynamic orchestration optimizes resources:** Modern frameworks enable dynamic team composition, spawning specialists as needed and releasing them when tasks complete.
8. **Avoid Context Pollution:** "Share memory by communicating, don't communicate by sharing memory." Minimize context sharing between agents, preferring structured communication over full context duplication to prevent KV-cache invalidation and reduce costs.
9. **Agent-as-Tool reduces complexity:** Treat agents as deterministic functions rather than organizational entities. This flattens complexity, improves modularity, and reduces token overhead compared to persistent conversational approaches.

## Next Steps

This chapter provided an overview of modern LLM-based multi-agent architectures, key patterns, real-world frameworks, and design considerations. For detailed implementation guidance, see:

- **Pattern: Orchestrator-Worker** - Detailed implementation of the orchestrator-worker pattern with modern examples
- **Pattern: Dynamic Agent Spawning** - Runtime creation of specialized worker agents tailored to specific tasks
- **Pattern: Self-Improving Agents** - Recursive self-improvement through self-exploration, evaluation, and iterative refinement
- **Pattern: Planner-Checker** - Separation of planning, execution, and verification across specialized agents
- **Pattern: Multi-Agent Debate** - Structured debate and discussion frameworks for improved reasoning
- **Pattern: Swarm/Consensus Architecture** - Decentralized coordination through discussion and consensus
- **Pattern: Evaluator-Optimizer** - Iterative improvement through specialized critique and refinement
- **Pattern: Reflection** - Single-agent self-evaluation and improvement
- **Pattern: Parallelization** - Techniques for parallel agent execution

??? "References"

    - Context Engineering for AI Agents: Part 2 - https://www.philschmid.de/context-engineering-part-2
    - Context Engineering for AI Agents: Lessons from Building Manus
    - Manus AI Agent Harness learnings from Peak Ji
