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
model = ChatOpenAI(model="gpt-4o", temperature=0)

# Example for few-shot learning
FEW_SHOT_EXAMPLE = """
Q: Emily had 32 stickers. She gave some to Rachel and then bought 10 more. Now she has 25 stickers. How many stickers did she give to Rachel?
A: 32 - x + 10 = 25; 42 - x = 25; x = 17. #### 17
"""

# Define system messages for different reasoning approaches
SYSTEM_MESSAGE_COT = """
Think step by step to answer the following question. 
Return the answer at the end of the response after a separator ####.
"""

SYSTEM_MESSAGE_COD = """
Think step by step, but only keep a minimum draft for each thinking step, with 5 words at most. 
Return the answer at the end of the response after a separator ####.
"""

# Create prompt templates
cot_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_MESSAGE_COT),
    HumanMessage(content=FEW_SHOT_EXAMPLE),
    HumanMessage(content="{question}")
])

cod_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_MESSAGE_COD),
    HumanMessage(content=FEW_SHOT_EXAMPLE),
    HumanMessage(content="{question}")
])

# Create chains
cot_chain = cot_prompt | model
cod_chain = cod_prompt | model

def extract_answer(response: str) -> str:
    """Extract the final answer after the #### separator."""
    parts = response.split("####")
    if len(parts) > 1:
        return parts[1].strip()
    return "No answer found"

def compare_chains(question: str) -> None:
    """Compare Chain of Thought vs Chain of Draft reasoning approaches."""
    console.print(Panel(question, title="Question", border_style="blue"))
    
    # Get Chain of Thought response
    cot_response = cot_chain.invoke({"question": question})
    cot_content = cot_response.content
    cot_tokens = len(cot_content.split())
    cot_answer = extract_answer(cot_content)
    
    # Get Chain of Draft response
    cod_response = cod_chain.invoke({"question": question})
    cod_content = cod_response.content
    cod_tokens = len(cod_content.split())
    cod_answer = extract_answer(cod_content)
    
    # Calculate token reduction
    reduction = ((cot_tokens - cod_tokens) / cot_tokens) * 100
    
    # Display the responses in pretty format
    console.print("\n[bold cyan]Chain of Thought Response:[/bold cyan]")
    console.print(Panel(cot_content, border_style="cyan"))
    
    console.print("\n[bold green]Chain of Draft Response:[/bold green]")
    console.print(Panel(cod_content, border_style="green"))
    
    # Create comparison table
    table = Table(title="Comparison Results", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="dim")
    table.add_column("Chain of Thought", justify="right")
    table.add_column("Chain of Draft", justify="right")
    
    table.add_row("Word Count", str(cot_tokens), str(cod_tokens))
    table.add_row("Final Answer", cot_answer, cod_answer)
    table.add_row("Token Reduction", "", f"{reduction:.1f}%")
    
    console.print(table)

if __name__ == "__main__":
    # Run comparison with a test question
    test_question = """
    Q: A bakery sells muffins for $4 each and cakes for $12 each. 
    If John bought 5 muffins and some cakes, spending $52 in total, 
    how many cakes did he buy?
    """
    
    compare_chains(test_question)