# Pattern: Evaluator-Optimizer (Critic-Generator)

## Motivation

Writers work with editors who provide objective critique. Scientists submit papers to peer reviewers who identify flaws and suggest improvements. Software developers submit code to reviewers who catch bugs and suggest optimizations. This separation of generation and evaluation roles enables specialized expertise and objective assessment that self-evaluation often cannot achieve.

The Evaluator-Optimizer pattern captures this principle: one agent generates solutions while another specialized agent evaluates and critiques them, creating an iterative improvement loop. This pattern is essential when quality is critical and specialized evaluation expertise is needed—when the skills required for generation differ from those needed for evaluation.

## Pattern Overview

**What it is:** A two-agent iterative loop where one agent (Generator/Optimizer) creates initial solutions and another agent (Evaluator/Critic) provides specialized critique and feedback. The Generator refines solutions based on feedback, creating a continuous improvement cycle until quality criteria are met.

**When to use:** When output quality is critical, iterative refinement is needed, and separate expertise is required for generation versus evaluation. Particularly valuable when evaluation requires specialized knowledge (code review, fact-checking, style analysis) that differs from generation skills.

**Why it matters:** Separating generation and evaluation into specialized agents enables objective critique, specialized expertise, and iterative improvement that single-agent reflection cannot match. The Evaluator brings fresh perspective and domain-specific evaluation skills, while the Generator focuses solely on creation and refinement.

Unlike the Reflection pattern where a single agent evaluates its own work, the Evaluator-Optimizer pattern uses separate specialized agents. This prevents cognitive bias, enables specialized evaluation expertise, and creates a more robust quality improvement process. The Evaluator can be optimized for finding flaws, checking facts, or assessing quality, while the Generator focuses on creation and refinement.

### Key Concepts

- **Generator Agent (Optimizer):** Creates initial solutions, outputs, or content. Focuses on generation, creativity, and implementation. Receives feedback and refines outputs iteratively.

- **Evaluator Agent (Critic):** Provides specialized critique, evaluation, and feedback. Focuses on quality assessment, error detection, and improvement suggestions. Brings objective perspective and domain-specific evaluation expertise.

- **Iterative Refinement Loop:** Continuous cycle of generation → evaluation → refinement → evaluation until quality criteria are met or iteration limit reached.

- **Quality Improvement Through Feedback:** Each iteration incorporates evaluator feedback, systematically improving output quality through targeted refinements.

- **Specialized Expertise:** Generator and Evaluator have distinct roles, prompts, and potentially different models or tools optimized for their specific functions.

- **Convergence Criteria:** Conditions that determine when refinement is complete: quality threshold met, no new issues found, maximum iterations reached, or evaluator approval.

### How It Works

The Evaluator-Optimizer pattern operates through a structured feedback cycle:

1. **Generation Phase:** The Generator agent creates an initial solution, output, or content based on the task requirements. This could be code, text, design, analysis, or any other output type.

2. **Evaluation Phase:** The Evaluator agent receives the Generator's output and evaluates it against specific criteria:
   - **Quality Assessment:** Checks for errors, flaws, or areas for improvement
   - **Criteria Checking:** Verifies adherence to requirements, standards, or constraints
   - **Specialized Analysis:** Applies domain-specific evaluation (code review, fact-checking, style analysis)
   - **Feedback Generation:** Provides structured critique with specific improvement suggestions

3. **Feedback Integration:** The Generator receives the Evaluator's critique and uses it to identify what needs improvement. The feedback is integrated into the refinement process.

4. **Refinement Phase:** The Generator creates a refined version incorporating the Evaluator's feedback. This may involve fixing errors, addressing concerns, or implementing suggestions.

5. **Iteration:** The cycle repeats: refined output → evaluation → further refinement, until convergence criteria are met (quality threshold, no new issues, evaluator approval) or maximum iterations reached.

The key distinction from single-agent reflection is the separation of roles: the Evaluator is optimized for finding problems and providing objective critique, while the Generator focuses on creation and refinement. This specialization enables more effective quality improvement.

## When to Use This Pattern

### ✅ Use when:

- **Quality is paramount:** Output quality is critical and errors are costly (code, legal documents, scientific papers, medical advice)
- **Specialized evaluation needed:** Evaluation requires expertise different from generation (code review, fact-checking, style analysis, compliance checking)
- **Iterative improvement possible:** Output can be refined based on feedback without starting completely over
- **Objective critique valuable:** Benefit from external, objective evaluation rather than self-assessment
- **Multi-criteria evaluation:** Need to evaluate against multiple criteria (correctness, style, performance, compliance)
- **Error correction critical:** Domain requires high accuracy and ability to catch and fix errors systematically

### ❌ Avoid when:

- **Speed is critical:** Real-time or low-latency requirements make iterative refinement impractical
- **Cost constraints:** Budget limitations make multiple LLM calls per task prohibitive
- **Simple tasks:** Task is straightforward enough that single-pass generation produces adequate results
- **Non-refinable outputs:** Output type doesn't benefit from iterative improvement (simple lookups, basic transformations)
- **Context window limits:** Iterative process would exceed context window capacity
- **Single-agent reflection sufficient:** Self-evaluation is adequate and specialized evaluation expertise isn't needed

### Decision Guidelines

Use Evaluator-Optimizer when quality improvement through specialized critique justifies the added cost and latency. Consider: quality requirements (higher quality = more benefit), evaluation complexity (specialized evaluation = need separate agent), error cost (high-stakes = worth iteration cost), and refinability (some outputs improve with iteration, others don't). The pattern is particularly valuable when evaluation requires different expertise than generation (e.g., code generation needs code review expertise, writing needs editing expertise). Be mindful of iteration limits to prevent infinite loops and manage costs.

## Practical Applications & Use Cases

The Evaluator-Optimizer pattern excels in scenarios requiring high-quality outputs with specialized evaluation:

### Code Generation and Review

**Generator:** Coder agent writes code based on requirements.
**Evaluator:** Reviewer agent performs code review, checking for bugs, performance issues, style violations, and best practices.
**Refinement:** Coder fixes issues identified by Reviewer.

**Example:** Software development system where Coder generates implementation, Reviewer performs static analysis and code review, and Coder refines based on feedback in iterative loop.

### Content Creation and Editing

**Generator:** Writer agent creates content (articles, stories, marketing copy).
**Evaluator:** Editor agent evaluates for clarity, style, accuracy, and adherence to guidelines.
**Refinement:** Writer revises based on editorial feedback.

**Example:** Content creation workflow where Writer drafts articles, Editor provides style and clarity feedback, and Writer refines for publication quality.

### Design Optimization

**Generator:** Designer agent creates designs (UI, graphics, layouts).
**Evaluator:** Critic agent evaluates usability, aesthetics, accessibility, and design principles.
**Refinement:** Designer iterates based on critique.

**Example:** UI design system where Designer generates interfaces, Critic evaluates usability and accessibility, and Designer refines based on feedback.

### Scientific Hypothesis Refinement

**Generator:** Researcher agent generates hypotheses or experimental designs.
**Evaluator:** Reviewer agent evaluates scientific rigor, methodology, and feasibility.
**Refinement:** Researcher refines hypotheses based on critique.

**Example:** Scientific research system where Researcher proposes hypotheses, Reviewer evaluates methodology and rigor, and Researcher refines based on scientific critique.

### Legal Document Generation

**Generator:** Legal writer agent drafts contracts or legal documents.
**Evaluator:** Legal reviewer agent checks for compliance, completeness, and legal accuracy.
**Refinement:** Writer revises based on legal review.

**Example:** Legal document system where Writer drafts contracts, Reviewer performs compliance and accuracy check, and Writer refines based on legal feedback.

### Data Analysis and Validation

**Generator:** Analyst agent performs data analysis and generates insights.
**Evaluator:** Validator agent checks statistical validity, methodology, and interpretation accuracy.
**Refinement:** Analyst refines analysis based on validation feedback.

**Example:** Data analysis system where Analyst generates insights, Validator checks statistical methods and interpretations, and Analyst refines based on validation critique.

## Implementation

### Prerequisites

```bash
pip install langchain langchain-openai langgraph
# or
pip install google-adk
```

### Basic Example: Coder-Reviewer Pair

This example demonstrates a code generation system with iterative review:

```python
from langchain_openai import ChatOpenAI
from typing import Dict, Optional
from enum import Enum

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class EvaluationStatus(Enum):
    NEEDS_IMPROVEMENT = "needs_improvement"
    SATISFACTORY = "satisfactory"
    PERFECT = "perfect"

class CodeGenerator:
    """Generator agent that creates code."""
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
    
    def generate(self, requirements: str, feedback: Optional[str] = None) -> str:
        """Generate code based on requirements and optional feedback."""
        if feedback:
            prompt = f"""You are a coding specialist. Generate code based on these requirements.

Requirements: {requirements}

Previous feedback from code reviewer:
{feedback}

Please refine the code addressing the feedback."""
        else:
            prompt = f"""You are a coding specialist. Generate code based on these requirements.

Requirements: {requirements}

Provide complete, working code with comments."""
        
        result = self.llm.invoke(prompt)
        return result.content

class CodeReviewer:
    """Evaluator agent that reviews code."""
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    def evaluate(self, code: str, requirements: str) -> Dict[str, any]:
        """Evaluate code and provide feedback."""
        prompt = f"""You are a senior code reviewer. Evaluate this code against the requirements.

Requirements: {requirements}

Code:
```python
{code}
```

Evaluate the code for:
1. Correctness: Does it meet the requirements?
2. Code quality: Is it clean, readable, and maintainable?
3. Best practices: Does it follow Python conventions?

Return JSON with:
- "status": one of {[s.value for s in EvaluationStatus]}
- "score": float between 0.0 and 1.0
- "feedback": detailed feedback string
- "improvements": list of specific improvement suggestions
"""
        result = self.llm.invoke(prompt)
        # Parse JSON response
        import json
        return json.loads(result.content)

# Evaluator-Optimizer loop
def evaluator_optimizer_loop(requirements: str, max_iterations: int = 5) -> str:
    """Run evaluator-optimizer pattern."""
    generator = CodeGenerator()
    reviewer = CodeReviewer()
    
    code = generator.generate(requirements)
    
    for i in range(max_iterations):
        evaluation = reviewer.evaluate(code, requirements)
        status = evaluation.get("status", EvaluationStatus.NEEDS_IMPROVEMENT.value)
        
        if status == EvaluationStatus.PERFECT.value:
            break
        
        feedback = evaluation.get("feedback", "")
        code = generator.generate(requirements, feedback)
    
    return code

# Example usage
if __name__ == "__main__":
    requirements = "Create a function that calculates the factorial of a number"
    final_code = evaluator_optimizer_loop(requirements)
    print(final_code)
```python
{code}
```

Evaluate the code for:
1. Correctness: Does it meet the requirements?
2. Code quality: Is it clean, readable, and maintainable?
3. Best practices: Does it follow Python best practices?
4. Error handling: Are errors handled appropriately?
5. Performance: Are there performance issues?

Provide:
1. Status: "PERFECT", "SATISFACTORY", or "NEEDS_IMPROVEMENT"
2. Issues found (if any)
3. Specific feedback for improvement

Format your response as:
Status: [STATUS]
Issues: [list of issues]
Feedback: [detailed feedback]"""
        
        result = self.llm.invoke(prompt)
        response = result.content
        
        # Parse response
        status = EvaluationStatus.NEEDS_IMPROVEMENT
        feedback = response
        
        if "Status: PERFECT" in response or "PERFECT" in response.upper():
            status = EvaluationStatus.PERFECT
        elif "Status: SATISFACTORY" in response or "SATISFACTORY" in response.upper():
            status = EvaluationStatus.SATISFACTORY
        
        return {
            "status": status,
            "feedback": feedback,
            "raw_response": response
        }

def evaluator_optimizer_loop(requirements: str, max_iterations: int = 5) -> Dict[str, any]:
    """Run evaluator-optimizer iterative improvement loop."""
    generator = CodeGenerator()
    evaluator = CodeReviewer()
    
    current_code = None
    iteration = 0
    feedback_history = []
    
    while iteration < max_iterations:
        # Generation phase
        if iteration == 0:
            current_code = generator.generate(requirements)
        else:
            last_feedback = feedback_history[-1]["feedback"]
            current_code = generator.generate(requirements, last_feedback)
        
        # Evaluation phase
        evaluation = evaluator.evaluate(current_code, requirements)
        feedback_history.append({
            "iteration": iteration + 1,
            "code": current_code,
            "status": evaluation["status"],
            "feedback": evaluation["feedback"]
        })
        
        # Check convergence
        if evaluation["status"] == EvaluationStatus.PERFECT:
            break
        if evaluation["status"] == EvaluationStatus.SATISFACTORY and iteration >= 2:
            # Allow early exit if satisfactory after a few iterations
            break
        
        iteration += 1
    
    return {
        "final_code": current_code,
        "iterations": iteration + 1,
        "feedback_history": feedback_history,
        "final_status": feedback_history[-1]["status"]
    }

# Usage
result = evaluator_optimizer_loop(
    "Create a Python function that calculates the factorial of a number with error handling",
    max_iterations=5
)

print(f"Iterations: {result['iterations']}")
print(f"Final Status: {result['final_status']}")
print(f"\nFinal Code:\n{result['final_code']}")
```

**Explanation:**
This example demonstrates the evaluator-optimizer pattern: Generator creates code, Evaluator reviews it, Generator refines based on feedback, and the cycle repeats until quality criteria are met. The Evaluator provides specialized code review expertise, while the Generator focuses on implementation.

### Advanced Example: Multi-Criteria Evaluation

This example shows evaluation against multiple criteria:

```python
from typing import List, Dict
from dataclasses import dataclass

@dataclass
class EvaluationCriteria:
    """Criteria for evaluation."""
    name: str
    weight: float
    description: str

class MultiCriteriaEvaluator:
    """Evaluator that assesses against multiple criteria."""
    def __init__(self, criteria: List[EvaluationCriteria]):
        self.criteria = criteria
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    def evaluate(self, output: str, task: str) -> Dict[str, any]:
        """Evaluate output against multiple criteria."""
        criteria_descriptions = "\n".join([
            f"- {c.name} (weight: {c.weight}): {c.description}"
            for c in self.criteria
        ])
        
        prompt = f"""Evaluate this output against multiple criteria.

Task: {task}

Output:
{output}

Criteria:
{criteria_descriptions}

For each criterion, provide:
1. Score (0-10)
2. Justification
3. Specific feedback

Format as:
Criterion: [name]
Score: [0-10]
Justification: [brief explanation]
Feedback: [specific feedback]"""
        
        result = self.llm.invoke(prompt)
        
        # Parse and calculate weighted score
        response = result.content
        scores = {}
        total_weighted_score = 0.0
        total_weight = sum(c.weight for c in self.criteria)
        
        for criterion in self.criteria:
            # Extract score for this criterion (simplified parsing)
            if f"Criterion: {criterion.name}" in response:
                # Find score in response
                lines = response.split('\n')
                for i, line in enumerate(lines):
                    if f"Criterion: {criterion.name}" in line:
                        # Look for score in next few lines
                        for j in range(i+1, min(i+5, len(lines))):
                            if "Score:" in lines[j]:
                                try:
                                    score = float(lines[j].split("Score:")[1].strip())
                                    scores[criterion.name] = score
                                    total_weighted_score += score * criterion.weight
                                    break
                                except:
                                    pass
        
        overall_score = total_weighted_score / total_weight if total_weight > 0 else 0.0
        
        return {
            "overall_score": overall_score,
            "criterion_scores": scores,
            "feedback": response,
            "meets_threshold": overall_score >= 7.0  # Example threshold
        }

# Usage: Content creation with multi-criteria evaluation
criteria = [
    EvaluationCriteria("Clarity", 0.3, "Is the content clear and easy to understand?"),
    EvaluationCriteria("Accuracy", 0.4, "Is the content factually accurate?"),
    EvaluationCriteria("Style", 0.2, "Does the content follow style guidelines?"),
    EvaluationCriteria("Completeness", 0.1, "Does the content cover all required points?")
]

evaluator = MultiCriteriaEvaluator(criteria)

# Generator creates content
generator = CodeGenerator()  # Reusing, but would be ContentGenerator in practice
content = generator.generate("Write an article about AI agents")

# Evaluator evaluates against multiple criteria
evaluation = evaluator.evaluate(content, "Write an article about AI agents")

print(f"Overall Score: {evaluation['overall_score']:.2f}")
print(f"Meets Threshold: {evaluation['meets_threshold']}")
```

**Explanation:**
This example demonstrates multi-criteria evaluation where the Evaluator assesses output against multiple weighted criteria (clarity, accuracy, style, completeness), providing comprehensive feedback that the Generator can use for targeted refinement.

### Framework-Specific Examples

#### LangGraph: Evaluator-Optimizer Loop

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class EvaluatorOptimizerState(TypedDict):
    task: str
    current_output: str
    feedback: Optional[str]
    iteration: int
    status: str
    max_iterations: int

def generator_node(state: EvaluatorOptimizerState) -> EvaluatorOptimizerState:
    """Generator creates or refines output."""
    task = state["task"]
    feedback = state.get("feedback")
    
    if feedback:
        prompt = f"""Generate output for this task, incorporating feedback.

Task: {task}
Previous Feedback: {feedback}

Refine the output addressing the feedback."""
    else:
        prompt = f"""Generate output for this task.

Task: {task}

Provide high-quality output."""
    
    result = llm.invoke(prompt)
    
    return {
        **state,
        "current_output": result.content,
        "iteration": state.get("iteration", 0) + 1
    }

def evaluator_node(state: EvaluatorOptimizerState) -> EvaluatorOptimizerState:
    """Evaluator critiques output."""
    task = state["task"]
    output = state["current_output"]
    
    prompt = f"""You are an evaluator. Critique this output.

Task: {task}

Output:
{output}

Evaluate for quality, correctness, and adherence to requirements.
Provide:
1. Status: "PERFECT", "SATISFACTORY", or "NEEDS_IMPROVEMENT"
2. Issues found
3. Specific feedback for improvement"""
    
    result = llm.invoke(prompt)
    response = result.content
    
    # Determine status
    status = "NEEDS_IMPROVEMENT"
    if "PERFECT" in response.upper():
        status = "PERFECT"
    elif "SATISFACTORY" in response.upper():
        status = "SATISFACTORY"
    
    return {
        **state,
        "status": status,
        "feedback": response
    }

def should_continue(state: EvaluatorOptimizerState) -> str:
    """Determine if iteration should continue."""
    status = state.get("status", "NEEDS_IMPROVEMENT")
    iteration = state.get("iteration", 0)
    max_iterations = state.get("max_iterations", 5)
    
    if status == "PERFECT":
        return "end"
    if status == "SATISFACTORY" and iteration >= 2:
        return "end"
    if iteration >= max_iterations:
        return "end"
    
    return "continue"

# Build graph
graph = StateGraph(EvaluatorOptimizerState)
graph.add_node("generator", generator_node)
graph.add_node("evaluator", evaluator_node)

graph.set_entry_point("generator")
graph.add_edge("generator", "evaluator")
graph.add_conditional_edges(
    "evaluator",
    should_continue,
    {
        "continue": "generator",
        "end": END
    }
)

# Execute
result = graph.invoke({
    "task": "Write a Python function to calculate Fibonacci numbers",
    "max_iterations": 5
})

print(f"Final Status: {result['status']}")
print(f"Iterations: {result['iteration']}")
print(f"\nFinal Output:\n{result['current_output']}")
```

#### Google ADK: Generator-Evaluator Agents

```python
from google.adk.agents import Agent
from google.adk.runners import Runner

# Generator agent
generator = Agent(
    name="Generator",
    model="gemini-2.0-flash",
    instruction="""You are a code generator. Create high-quality code based on requirements.
When you receive feedback, refine your code to address the feedback.""",
    tools=[code_editor_tool]
)

# Evaluator agent
evaluator = Agent(
    name="Evaluator",
    model="gemini-2.0-flash",
    instruction="""You are a code reviewer. Evaluate code for:
- Correctness
- Code quality
- Best practices
- Error handling
- Performance

Provide structured feedback with status (PERFECT, SATISFACTORY, NEEDS_IMPROVEMENT) and specific improvement suggestions.""",
    tools=[static_analysis_tool, test_runner_tool]
)

# Create runner with evaluator-optimizer loop
runner = Runner(
    agents=[generator, evaluator],
    app_name="code_generation_system"
)

# Run iterative improvement
result = runner.run_iterative(
    initial_prompt="Create a Python function to sort a list",
    max_iterations=5,
    convergence_criteria="PERFECT or SATISFACTORY after 2+ iterations"
)
```

## Key Takeaways

- **Core Concept:** Evaluator-Optimizer pattern uses separate specialized agents for generation and evaluation, enabling objective critique and iterative quality improvement.

- **Key Benefits:** Specialized evaluation expertise, objective critique (prevents self-assessment bias), and systematic quality improvement through targeted refinements.

- **Iterative Refinement:** Continuous cycle of generation → evaluation → refinement until quality criteria are met, with convergence based on status (PERFECT, SATISFACTORY) or iteration limits.

- **Trade-offs:** Improves quality significantly but increases latency and cost due to multiple LLM calls. Use when quality improvement justifies overhead.

- **Best Practice:** Optimize Generator and Evaluator with specialized prompts, models, or tools for their specific roles. Use clear convergence criteria to prevent infinite loops.

- **Common Pitfall:** Over-iterating when satisfactory quality is reached. Set appropriate iteration limits and convergence criteria. Not all outputs need perfect scores.

- **Specialization Advantage:** Separate agents enable specialized expertise—Evaluator optimized for finding problems, Generator optimized for creation and refinement.

## Related Patterns

This pattern works well with:
- **Pattern: Reflection** - Single-agent self-evaluation; Evaluator-Optimizer uses separate agents for more objective critique
- **Pattern: Orchestrator-Worker** - Orchestrator can coordinate Generator-Evaluator pairs for complex tasks
- **Pattern: Planning** - Generator can create plans that Evaluator reviews before execution
- **Memory Management** - Store evaluation history and feedback for learning and improvement

This pattern is often combined with:
- **Multi-Agent Architectures** - Evaluator-Optimizer is a fundamental two-agent collaboration pattern
- **Tool Use** - Evaluator may use specialized tools (static analysis, testing, fact-checking)
- **Pattern: Exception Handling** - Handle cases where evaluation fails or convergence isn't reached

??? "References"

- Iterative Refinement: Iterative Refinement for Machine Learning (various)
- Code Review Practices: Best Practices for Code Review (Google, Microsoft)
- Quality Assurance: Software Quality Assurance (IEEE)
- LangGraph Iterative Loops: https://langchain-ai.github.io/langgraph/how-tos/iterative-loops/
- Google ADK Agents: https://google.github.io/adk-docs/agents/
- Multi-Agent Quality Improvement: Research on multi-agent quality assurance systems

