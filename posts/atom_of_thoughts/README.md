# ⚛️ Atom of Thoughts: Breaking Complex Problems Into Simpler Pieces

<div align="center">

[![GitHub stars](https://img.shields.io/github/stars/themanojdesai/GenAI?style=social)](https://github.com/themanojdesai/GenAI/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Twitter Follow](https://img.shields.io/twitter/follow/themanojdesai?style=social)](https://twitter.com/themanojdesai)

</div>

## 🧠 Overview

**Atom of Thoughts (AoT)** is a prompting technique that breaks down complex problems into their smallest independent components ("atoms") and solves each separately before synthesizing a final answer. This implementation demonstrates how AoT compares to traditional Chain of Thought (CoT) reasoning with detailed metrics.

## ✨ Key Features

- 🔄 Side-by-side comparison of CoT and AoT approaches
- 📊 Real-time metrics on effectiveness and accuracy
- 🧮 Automatic extraction and display of atomic subproblems
- 🎨 Beautiful, colorful terminal output using the Rich library
- 🧪 Configurable prompting system that's easy to customize
- 🏗️ Production-ready code structure with proper typing

## 📋 Why Atom of Thoughts?

Traditional Chain of Thought prompting uses a linear, sequential approach to problem-solving. Atom of Thoughts recognizes that many complex problems have independent components that can be isolated and solved separately, often leading to better accuracy on multi-factor problems.

| Approach | Benefits | Drawbacks |
|----------|----------|-----------|
| Chain of Thought | • Well-established<br>• Simple implementation<br>• Good for linear problems | • Can get lost in long chains<br>• Errors cascade through steps<br>• Less flexible |
| Atom of Thoughts | • Error isolation<br>• Modularity<br>• Better for complex problems | • Slightly more complex implementation<br>• Newer technique<br>• May use more tokens |

In testing, AoT shows significant accuracy improvements on multi-factor problems compared to traditional CoT.

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
   python atom_of_thoughts.py
   ```

## 📚 Sample Output

The script produces a beautifully formatted comparison showing:

- Full reasoning process from both approaches
- Extracted atomic subproblems
- Synthesis of the atomic solutions
- Performance metrics
- Final answers

<details>
<summary><b>Click to see sample output</b></summary>

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ Question ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                           ┃
┃     Q: You're planning a conference with 120 attendees. The venue charges $2,000 plus $25 per person.                    ┃
┃     Catering costs $45 per person. You need to determine the ticket price to break even while offering a                 ┃
┃     20% discount for the first 30 early-bird registrations. What should the regular ticket price be?                     ┃
┃                                                                                                                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

Chain of Thought Response:
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ To solve this problem, I'll break it down into steps:                                                                    ┃
┃                                                                                                                           ┃
┃ Step 1: Calculate the total cost for the venue.                                                                           ┃
┃ Base charge: $2,000                                                                                                       ┃
┃ Per-person charge: 120 people × $25 = $3,000                                                                              ┃
┃ Total venue cost: $2,000 + $3,000 = $5,000                                                                                ┃
┃                                                                                                                           ┃
┃ Step 2: Calculate the total cost for catering.                                                                            ┃
┃ Catering cost: 120 people × $45 per person = $5,400