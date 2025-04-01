import os
from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

os.environ["OPENAI_API_KEY"] = "your api key"

# Initialize Rich console for pretty printing
console = Console()

# Set up the OpenAI model
model = ChatOpenAI(model="gpt-4o", temperature=0.2)

# Example for few-shot learning
FEW_SHOT_EXAMPLE = """
Problem: In a certain game, a player flips a fair coin three times. The player wins $8 if all three flips result in heads and wins $4 if exactly two flips result in heads. Otherwise, the player wins nothing. What is the expected value of this game?

Step-Back Analysis: This is a probability problem involving expected value calculation. Expected value is the sum of all possible outcomes multiplied by their respective probabilities.

Solution: I need to find all possible outcomes, their probabilities, and their payoffs.
- Outcome 1: All heads (HHH) - Probability: (1/2)³ = 1/8 - Payoff: $8
- Outcome 2: Two heads, one tails - Probability: C(3,2) * (1/2)² * (1/2) = 3/8 - Payoff: $4
- Outcome 3: One head, two tails or all tails - Probability: 1 - 1/8 - 3/8 = 4/8 = 1/2 - Payoff: $0

Expected value = (1/8 × $8) + (3/8 × $4) + (1/2 × $0) = $1 + $1.5 + $0 = $2.5 #### $2.50
"""

# Define system messages for different reasoning approaches
SYSTEM_MESSAGE_DIRECT = """
Answer the following problem directly.
Return the answer at the end of the response after a separator ####.
"""

SYSTEM_MESSAGE_STEPBACK = """
To solve this problem:
1. Take a step back and identify what type of problem this is and the key concepts/principles involved.
2. Apply these concepts to solve the specific problem step by step.
Return the answer at the end of the response after a separator ####.
"""

# Create prompt templates
direct_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_MESSAGE_DIRECT),
    HumanMessage(content="{question}")
])

stepback_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_MESSAGE_STEPBACK),
    HumanMessage(content=FEW_SHOT_EXAMPLE),
    HumanMessage(content="{question}")
])

# Create chains
direct_chain = direct_prompt | model
stepback_chain = stepback_prompt | model

def extract_answer(response: str) -> str:
    """Extract the final answer after the #### separator."""
    parts = response.split("####")
    if len(parts) > 1:
        return parts[1].strip()
    return "No answer found"

def compare_approaches(question: str) -> None:
    """Compare Direct vs Step-Back reasoning approaches."""
    console.print(Panel(question, title="Problem", border_style="blue"))
    
    # Get Direct response
    direct_response = direct_chain.invoke({"question": question})
    direct_content = direct_response.content
    direct_tokens = len(direct_content.split())
    direct_answer = extract_answer(direct_content)
    
    # Get Step-Back response
    stepback_response = stepback_chain.invoke({"question": question})
    stepback_content = stepback_response.content
    stepback_tokens = len(stepback_content.split())
    stepback_answer = extract_answer(stepback_content)
    
    # Calculate correctness probability (hypothetical - in reality would need evaluation)
    # This is just for demonstration purposes
    direct_accuracy = "Lower"
    stepback_accuracy = "Higher"
    
    # Display the responses in pretty format
    console.print("\n[bold red]Direct Approach Response:[/bold red]")
    console.print(Panel(direct_content, border_style="red"))
    
    console.print("\n[bold green]Step-Back Approach Response:[/bold green]")
    console.print(Panel(stepback_content, border_style="green"))
    
    # Create comparison table
    table = Table(title="Comparison Results", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="dim")
    table.add_column("Direct Approach", justify="right")
    table.add_column("Step-Back Approach", justify="right")
    
    table.add_row("Word Count", str(direct_tokens), str(stepback_tokens))
    table.add_row("Final Answer", direct_answer, stepback_answer)
    table.add_row("Expected Accuracy", direct_accuracy, stepback_accuracy)
    
    console.print(table)

def multi_step_stepback(question: str) -> Dict[str, Any]:
    """Implement full step-back prompting with separate steps."""
    # Step 1: Identify problem type and principles
    identification_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="Consider the following problem. Before solving it, identify what type of problem this is and what key concepts, principles, or methods are relevant to it."),
        HumanMessage(content=question)
    ])
    
    identification_chain = identification_prompt | model
    identification_response = identification_chain.invoke({})
    problem_analysis = identification_response.content
    
    # Step 2: Solve with the analysis in mind
    solution_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="Solve the following problem step by step, using the provided problem analysis. Return the final answer after a separator ####."),
        HumanMessage(content=f"Problem: {question}\n\nProblem Analysis: {problem_analysis}")
    ])
    
    solution_chain = solution_prompt | model
    solution_response = solution_chain.invoke({})
    solution = solution_response.content
    
    return {
        "problem": question,
        "problem_analysis": problem_analysis,
        "solution": solution,
        "answer": extract_answer(solution)
    }

def display_multi_step_results(results: Dict[str, Any]) -> None:
    """Display the results of multi-step step-back prompting."""
    console.print(Panel(results["problem"], title="Problem", border_style="blue"))
    
    console.print("\n[bold yellow]Step 1: Problem Analysis[/bold yellow]")
    console.print(Panel(results["problem_analysis"], border_style="yellow"))
    
    console.print("\n[bold green]Step 2: Problem Solution[/bold green]")
    console.print(Panel(results["solution"], border_style="green"))
    
    console.print("\n[bold cyan]Final Answer:[/bold cyan]", results["answer"])

if __name__ == "__main__":
    # Run comparison with a test question
    test_question = """
    A charity fundraiser sells raffle tickets for $5 each. There are three prizes: a first prize of $1000, a second prize of $500, and a third prize of $250. If 500 tickets are sold, what is the expected value of buying a single ticket?
    """
    
    # Compare the direct vs step-back approaches
    console.print("[bold]Comparing Direct vs Step-Back Approaches[/bold]", style="blue")
    compare_approaches(test_question)
    
    # Show multi-step step-back prompting
    console.print("\n\n[bold]Multi-Step Step-Back Prompting[/bold]", style="blue")
    results = multi_step_stepback(test_question)
    display_multi_step_results(results)