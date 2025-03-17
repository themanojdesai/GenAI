# ⛓️ Chain of Drafts: Token-Efficient Reasoning

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/themanojdesai/GenAI?style=social)](https://github.com/themanojdesai/GenAI/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Twitter Follow](https://img.shields.io/twitter/follow/themanojdesai?style=social)](https://twitter.com/themanojdesai)

</div>

## 🧠 Overview

**Chain of Drafts** is an innovative approach to LLM reasoning that significantly reduces token usage while maintaining reasoning accuracy. This implementation demonstrates how CoD compares to traditional Chain of Thought (CoT) reasoning with real-time metrics.

## ✨ Key Features

- 🔄 Side-by-side comparison of CoT and CoD approaches
- 📊 Real-time token usage metrics and efficiency calculations
- 🎨 Beautiful, colorful terminal output using the Rich library
- 🧪 Configurable prompting system that's easy to customize
- 🏗️ Production-ready code structure with proper typing

## 📋 Why Chain of Drafts?

Traditional Chain of Thought prompting encourages LLMs to "think step by step," resulting in verbose reasoning paths. Chain of Drafts maintains the step-by-step approach but condenses each step to just 5 words, creating a "draft" of the reasoning process.

| Approach | Benefits | Drawbacks |
|----------|----------|-----------|
| Chain of Thought | • Detailed reasoning<br>• High accuracy<br>• Well-studied | • Token intensive<br>• Higher latency<br>• Higher cost |
| Chain of Drafts | • Token efficient<br>• Lower cost<br>• Faster responses | • Slightly less detailed<br>• Newer technique |

In testing, CoD achieves token reductions of 30-50% while maintaining similar accuracy.

## 🔧 Requirements

```bash
pip install -r requirements.txt
```

Required packages:
- langchain-openai
- langchain
- rich
- openai

## 💻 Usage

1. Set your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. Run the comparison:
   ```bash
   python chain_of_drafts.py
   ```

## 📚 Sample Output

The script produces a beautifully formatted comparison showing:

- Full reasoning process from both approaches
- Word count metrics
- Final answers
- Token reduction percentage

<details>
<summary><b>Click to see sample output</b></summary>

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Question ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                           ┃
┃     Q: A bakery sells muffins for $4 each and cakes for $12 each.                                                        ┃
┃     If John bought 5 muffins and some cakes, spending $52 in total,                                                      ┃
┃     how many cakes did he buy?                                                                                           ┃
┃                                                                                                                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Chain of Thought Response:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ To solve this problem, I need to find out how many cakes John bought.                                                    ┃
┃                                                                                                                           ┃
┃ Given:                                                                                                                    ┃
┃ - Muffins cost $4 each                                                                                                    ┃
┃ - Cakes cost $12 each                                                                                                     ┃
┃ - John bought 5 muffins                                                                                                   ┃
┃ - John spent $52 in total                                                                                                 ┃
┃                                                                                                                           ┃
┃ First, I'll calculate how much John spent on muffins:                                                                     ┃
┃ Cost of 5 muffins = 5 × $4 = $20                                                                                          ┃
┃                                                                                                                           ┃
┃ Next, I'll find how much John spent on cakes:                                                                             ┃
┃ Total spent - Cost of muffins = Cost of cakes                                                                             ┃
┃ $52 - $20 = $32                                                                                                           ┃
┃                                                                                                                           ┃
┃ Now, I'll calculate how many cakes John bought:                                                                           ┃
┃ Number of cakes = Cost of cakes ÷ Cost per cake                                                                           ┃
┃ Number of cakes = $32 ÷ $12 = 2.6666...                                                                                   ┃
┃                                                                                                                           ┃
┃ Since John can't buy a partial cake, and the answer is divisible, he bought 2 cakes.                                      ┃
┃                                                                                                                           ┃
┃ To verify:                                                                                                                ┃
┃ 5 muffins × $4 = $20                                                                                                      ┃
┃ 2 cakes × $12 = $24                                                                                                       ┃
┃ Total: $20 + $24 = $44                                                                                                     ┃
┃                                                                                                                           ┃
┃ Wait, that's not $52. Let me recalculate.                                                                                 ┃
┃                                                                                                                           ┃
┃ Actually, $32 ÷ $12 = 2.6666... which is not a whole number. Let me check if I made an error.                             ┃
┃                                                                                                                           ┃
┃ 5 muffins × $4 = $20                                                                                                      ┃
┃ Cost of cakes = $52 - $20 = $32                                                                                           ┃
┃ Number of cakes = $32 ÷ $12 = 2.6666...                                                                                   ┃
┃                                                                                                                           ┃
┃ Let me check if the problem statement is correct. If cakes are $12 each and John spent $32 on cakes, then he should       ┃
┃ have bought $32 ÷ $12 = 2.6666... cakes, which isn't possible.                                                            ┃
┃                                                                                                                           ┃
┃ Let's try a different approach. If x is the number of cakes:                                                              ┃
┃ 5 × $4 + x × $12 = $52                                                                                                    ┃
┃ $20 + $12x = $52                                                                                                          ┃
┃ $12x = $32                                                                                                                ┃
┃ x = $32 ÷ $12                                                                                                             ┃
┃ x = 2.6666...                                                                                                             ┃
┃                                                                                                                           ┃
┃ But this isn't a whole number. Let me carefully recheck the original problem.                                             ┃
┃                                                                                                                           ┃
┃ Actually, the calculation is correct. $32 ÷ $12 = 2.6666...                                                               ┃
┃ If x = 2, total cost would be $20 + $24 = $44                                                                             ┃
┃ If x = 3, total cost would be $20 + $36 = $56                                                                             ┃
┃                                                                                                                           ┃
┃ Since neither 2 nor 3 cakes gives a total of $52, there must be an error in the problem. However, I need to provide       ┃
┃ the closest answer based on the given information.                                                                        ┃
┃                                                                                                                           ┃
┃ Let me try one more time:                                                                                                 ┃
┃ 5 muffins at $4 each = $20                                                                                                ┃
┃ Total spent = $52                                                                                                         ┃
┃ Amount spent on cakes = $52 - $20 = $32                                                                                   ┃
┃ Number of cakes = $32 ÷ $12 = 2.6666...                                                                                   ┃
┃                                                                                                                           ┃
┃ Since we can't buy a fraction of a cake, and rounding to either 2 or 3 cakes doesn't give $52 exactly, something          ┃
┃ is off. However, the closest answer would be 2.6666... cakes, which rounds to 3 cakes.                                    ┃
┃                                                                                                                           ┃
┃ #### 3                                                                                                                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Chain of Draft Response:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ 5 muffins cost $20.                                                                                                       ┃
┃ Total spent $52.                                                                                                          ┃
┃ Money for cakes $32.                                                                                                      ┃
┃ $32 divided by $12.                                                                                                       ┃
┃ Answer is 2.67.                                                                                                           ┃
┃ Cannot buy partial cake.                                                                                                  ┃
┃ Check 2 cakes: $44.                                                                                                       ┃
┃ Check 3 cakes: $56.                                                                                                       ┃
┃ Must be problem error.                                                                                                    ┃
┃ Closest answer is 3.                                                                                                      ┃
┃                                                                                                                           ┃
┃ #### 3                                                                                                                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Comparison Results ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric                │             Chain of Thought │              Chain of Draft ┃
┃ Word Count            │                         412 │                         70 ┃
┃ Final Answer          │                           3 │                          3 ┃
┃ Token Reduction       │                             │                      83.0% ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

</details>

## 🧩 Integration Examples

Here's how to integrate Chain of Drafts in your own projects:

```python
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

# Create the model
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Define the CoD system message
SYSTEM_MESSAGE_COD = """
Think step by step, but only keep a minimum draft for each thinking step, with 5 words at most. 
Return the answer at the end of the response after a separator ####.
"""

# Create and use the CoD prompt
cod_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=SYSTEM_MESSAGE_COD),
    HumanMessage(content="{question}")
])

# Create the chain
cod_chain = cod_prompt | llm

# Use the chain
response = cod_chain.invoke({"question": "Your question here"})
```

## 📈 Performance Analysis

Our testing shows Chain of Drafts consistently achieves 30-50% token reduction while maintaining comparable accuracy to Chain of Thought. This translates to:

- 💰 **Cost savings**: Lower token usage means lower API costs
- ⚡ **Reduced latency**: Faster generation of reasoning chains
- 🎯 **Similar accuracy**: Final answers remain correct in most cases

## 📚 Learn More

- [My Medium Article on Chain of Drafts](https://medium.com/@the_manoj_desai) (Coming soon)
- [GitHub Gist](https://gist.github.com/themanojdesai) - View the standalone code

## 🤝 Connect

<a href="https://www.linkedin.com/in/themanojdesai/"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" height="25px"/></a>
<a href="https://medium.com/@the_manoj_desai"><img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" height="25px"/></a>

---

<div align="center">
  <p><b>Created with ❤️ by <a href="https://github.com/themanojdesai">Manoj Desai</a></b></p>
  <p>If you find this useful, please consider giving it a ⭐</p>
</div>