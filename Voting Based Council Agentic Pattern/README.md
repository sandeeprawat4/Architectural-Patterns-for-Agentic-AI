# Voting-Based Council Agentic Pattern for Agile Story Point Estimation

This project demonstrates a **Voting-Based Council Agentic Pattern** using **CrewAI** and **Gemini LLM** to estimate Agile story points collaboratively.

Multiple AI agents, each representing a different engineering role, independently estimate story points for a user story. A **Sprint Leader agent** aggregates these estimates using **role-based weightages** and finalizes a Fibonacci-based story point.

---

## 🧠 Concept Overview

Agile estimation often relies on Planning Poker and team discussions. This project models the same collaborative estimation process using **agentic AI**, enabling:

- Role-specific reasoning
- Parallel and asynchronous estimates
- Weighted voting based on experience
- Deterministic selection from Fibonacci story points

---

## 🏗 Agent Roles & Weightages

| Role | Focus Area | Weight |
|-----|-----------|--------|
| Architect | Design, scalability, technical debt | 5 |
| Senior Engineer | Implementation complexity | 4 |
| Mid Engineer | Patterns, integrations | 3 |
| QA Engineer | Testing and defects | 3 |
| Junior Engineer | Learning curve | 2 |
| Intern | Fundamental complexity | 1 |
| Sprint Leader | Final decision | – |

---

## 📐 Story Point Scale

Only Fibonacci numbers are allowed:

```
[0, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

---

## ⚙️ Workflow

1. A user story is defined (e.g., authentication system).
2. All role agents estimate in parallel.
3. Each estimate includes reasoning and a Fibonacci value.
4. The Sprint Leader applies role weightages.
5. A single final story point is selected.

---

## 🧰 Tech Stack

- Python
- CrewAI
- Gemini 2.5 Flash
- dotenv / Google Colab

---

## 📦 Installation

```bash
pip install -U crewai python-dotenv
```

---

## 🔐 Environment Setup

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

Or set it in Google Colab using `userdata`.

---

## ▶️ Run

```bash
python voting_based_council_agentic_pattern.py
```

---

## 📤 Sample Output

```json
{
  "final_reasoning": "...",
  "final_story_point": 13
}
```

---

## ✅ Use Cases

- Agile estimation automation
- Agentic decision-making demos
- Engineering leadership simulations
- CrewAI pattern examples

---

## 📄 License

MIT License

---

