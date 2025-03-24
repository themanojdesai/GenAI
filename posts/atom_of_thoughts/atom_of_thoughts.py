import os
import time
from typing import Dict, Any, List, Tuple
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import Progress
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage

# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Initialize Rich console for pretty printing
console = Console()

def setup_model(model_name: str = "gpt-4o", temperature: float = 0) -> ChatOpenAI:
    """Initialize the LLM with the specified parameters."""
    return ChatOpenAI(
        model=model_name,
        temperature=temperature
    )

# Example for few-shot learning (helps establish the pattern)
FEW_SHOT_EXAMPLE = """
Q: Emily had 32 stickers. She gave some to Rachel and then bought 10 more. Now she has 25 stickers. How many stickers did she give to Rachel?

A: 
Atom 1: Calculate Emily's starting stickers
Emily had 32 stickers initially.

Atom 2: Calculate Emily's final stickers
Emily has 25 stickers now.

Atom 3: Calculate stickers Emily bought
Emily bought 10 more stickers.

Atom 4: Find how many stickers Emily gave away
Let x = stickers given to Rachel
Starting + bought - given = final
32 + 10 - x = 25
42 - x = 25
x = 17

Synthesis: Emily gave 17 stickers to Rachel.

#### 17
"""

# System messages for different reasoning approaches
SYSTEM_MESSAGE_COT = """
Think step by step to answer the following question. 
Return the answer at the end of the response after a separator ####.
"""

SYSTEM_MESSAGE_AOT = """
To solve this problem, break it down into the smallest independent "atomic" subproblems.

For each atomic subproblem:
1. Label it as "Atom X: [brief description]"
2. Solve that specific subproblem completely
3. Make sure each atom can be solved independently

After solving all atomic subproblems, provide a synthesis that combines them into a final answer.
Return your final answer after a separator ####.
"""

def create_chains(model: ChatOpenAI):
    """Create both CoT and AoT chains using the same model."""
    # Create prompt templates
    cot_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=SYSTEM_MESSAGE_COT),
        HumanMessage(content=FEW_SHOT_EXAMPLE),
        HumanMessage(content="{question}")
    ])
    
    aot_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=SYSTEM_MESSAGE_AOT),
        HumanMessage(content=FEW_SHOT_EXAMPLE),
        HumanMessage(content="{question}")
    ])
    
    # Create and return chains
    return {
        "cot": cot_prompt | model,
        "aot": aot_prompt | model
    }

def extract_answer(response: str) -> str:
    """Extract the final answer after the #### separator."""
    parts = response.split("####")
    if len(parts) > 1:
        return parts[1].strip()
    return "No answer found"

def extract_atoms(response: str) -> List[Dict[str, str]]:
    """Extract atomic subproblems and their solutions."""
    atoms = []
    lines = response.split("\n")
    current_atom = None
    current_content = []
    
    for line in lines:
        if line.strip().startswith("Atom") and ":" in line:
            # Save previous atom if it exists
            if current_atom:
                atoms.append({
                    "name": current_atom,
                    "content": "\n".join(current_content)
                })
            
            # Start new atom
            current_atom = line.strip()
            current_content = []
        elif line.strip().startswith("Synthesis:"):
            # Save previous atom
            if current_atom:
                atoms.append({
                    "name": current_atom,
                    "content": "\n".join(current_content)
                })
            # Start synthesis
            current_atom = "Synthesis"
            current_content = [line.strip()[10:]]  # Remove "Synthesis:" prefix
        elif current_atom:
            current_content.append(line)
    
    # Add the last atom or synthesis
    if current_atom:
        atoms.append({
            "name": current_atom,
            "content": "\n".join(current_content)
        })
    
    return atoms

def measure_performance(chain, question: str) -> Tuple[str, int, str, float, List[Dict[str, str]]]:
    """
    Measure the performance of a chain.
    
    Returns:
        Tuple containing (response content, word count, extracted answer, time taken, atoms if available)
    """
    start_time = time.time()
    response = chain.invoke({"question": question})
    end_time = time.time()
    
    content = response.content
    words = len(content.split())
    answer = extract_answer(content)
    time_taken = end_time - start_time
    
    # Try to extract atoms if this is an AoT response
    try:
        atoms = extract_atoms(content)
    except:
        atoms = []
    
    return content, words, answer, time_taken, atoms

def compare_chains(question: str, chains: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compare Chain of Thought vs Atom of Thoughts reasoning approaches.
    
    Returns:
        Dictionary with comparison results
    """
    results = {}
    
    # Print the question
    console.print(Panel(question, title="Question", border_style="blue"))
    
    # Get Chain of Thought response
    with console.status("[bold cyan]Running Chain of Thought..."):
        cot_content, cot_words, cot_answer, cot_time, _ = measure_performance(chains["cot"], question)
    
    # Get Atom of Thoughts response
    with console.status("[bold green]Running Atom of Thoughts..."):
        aot_content, aot_words, aot_answer, aot_time, aot_atoms = measure_performance(chains["aot"], question)
    
    # Calculate metrics
    word_difference = ((cot_words - aot_words) / cot_words) * 100 if cot_words > 0 else 0
    time_difference = ((cot_time - aot_time) / cot_time) * 100 if cot_time > 0 else 0
    num_atoms = len(aot_atoms)
    
    # Store results
    results = {
        "cot": {
            "content": cot_content,
            "words": cot_words,
            "answer": cot_answer,
            "time": cot_time
        },
        "aot": {
            "content": aot_content,
            "words": aot_words,
            "answer": aot_answer,
            "time": aot_time,
            "atoms": aot_atoms,
            "num_atoms": num_atoms
        },
        "metrics": {
            "word_difference": word_difference,
            "time_difference": time_difference
        }
    }
    
    # Display the responses in pretty format
    console.print("\n[bold cyan]Chain of Thought Response:[/bold cyan]")
    console.print(Panel(cot_content, border_style="cyan"))
    
    console.print("\n[bold green]Atom of Thoughts Response:[/bold green]")
    console.print(Panel(aot_content, border_style="green"))
    
    # Display individual atoms
    console.print("\n[bold yellow]Atomic Subproblems:[/bold yellow]")
    for atom in aot_atoms:
        if atom["name"] != "Synthesis":
            console.print(Panel(atom["content"], title=atom["name"], border_style="yellow"))
    
    # Display synthesis if available
    synthesis = next((atom for atom in aot_atoms if atom["name"] == "Synthesis"), None)
    if synthesis:
        console.print(Panel(synthesis["content"], title="Synthesis", border_style="magenta"))
    
    # Create comparison table
    table = Table(title="Comparison Results", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="dim")
    table.add_column("Chain of Thought", justify="right")
    table.add_column("Atom of Thoughts", justify="right")
    
    table.add_row("Word Count", str(cot_words), str(aot_words))
    table.add_row("Time (seconds)", f"{cot_time:.2f}", f"{aot_time:.2f}")
    table.add_row("Final Answer", cot_answer, aot_answer)
    table.add_row("Number of Atoms", "-", str(num_atoms))
    
    if word_difference > 0:
        table.add_row("Word Reduction", "-", f"{word_difference:.1f}%")
    else:
        table.add_row("Word Increase", "-", f"{-word_difference:.1f}%")
    
    if time_difference > 0:
        table.add_row("Time Reduction", "-", f"{time_difference:.1f}%")
    else:
        table.add_row("Time Increase", "-", f"{-time_difference:.1f}%")
    
    console.print(table)
    
    return results

def batch_test(questions: List[str]) -> Dict[str, Any]:
    """Run tests on a batch of questions and compile statistics."""
    model = setup_model()
    chains = create_chains(model)
    
    results = []
    
    for i, question in enumerate(questions):
        console.rule(f"[bold]Question {i+1}/{len(questions)}")
        result = compare_chains(question, chains)
        results.append(result)
    
    # Calculate aggregate statistics
    avg_num_atoms = sum(r["aot"]["num_atoms"] for r in results) / len(results)
    avg_word_difference = sum(r["metrics"]["word_difference"] for r in results) / len(results)
    avg_time_difference = sum(r["metrics"]["time_difference"] for r in results) / len(results)
    
    # Count matching answers
    matching_answers = sum(1 for r in results if r["cot"]["answer"] == r["aot"]["answer"])
    
    console.rule("[bold]Aggregate Results")
    aggregate_table = Table(title="Average Performance", show_header=True)
    aggregate_table.add_column("Metric")
    aggregate_table.add_column("Value")
    
    if avg_word_difference > 0:
        aggregate_table.add_row("Average Word Reduction", f"{avg_word_difference:.1f}%")
    else:
        aggregate_table.add_row("Average Word Increase", f"{-avg_word_difference:.1f}%")
        
    if avg_time_difference > 0:
        aggregate_table.add_row("Average Time Reduction", f"{avg_time_difference:.1f}%")
    else:
        aggregate_table.add_row("Average Time Increase", f"{-avg_time_difference:.1f}%")
    
    aggregate_table.add_row("Average Number of Atoms", f"{avg_num_atoms:.1f}")
    aggregate_table.add_row("Answer Match Rate", f"{(matching_answers/len(results))*100:.1f}%")
    aggregate_table.add_row("Questions Tested", str(len(questions)))
    
    console.print(aggregate_table)
    
    return {
        "individual_results": results, 
        "aggregate": {
            "word_difference": avg_word_difference, 
            "time_difference": avg_time_difference,
            "avg_num_atoms": avg_num_atoms,
            "answer_match_rate": (matching_answers/len(results))*100
        }
    }

if __name__ == "__main__":
    # Sample questions to test
    test_questions = [
        """
        Q: A bakery sells muffins for $4 each and cakes for $12 each. 
        If John bought 5 muffins and some cakes, spending $52 in total, 
        how many cakes did he buy?
        """,
        
        """
        Q: You're planning a conference with 120 attendees. The venue charges $2,000 plus $25 per person. 
        Catering costs $45 per person. You need to determine the ticket price to break even while offering a 
        20% discount for the first 30 early-bird registrations. What should the regular ticket price be?
        """
    ]
    
    # Option 1: Run a single comparison
    model = setup_model()
    chains = create_chains(model)
    compare_chains(test_questions[1], chains)
    
    # Option 2: Uncomment to run batch testing
    # batch_results = batch_test(test_questions)