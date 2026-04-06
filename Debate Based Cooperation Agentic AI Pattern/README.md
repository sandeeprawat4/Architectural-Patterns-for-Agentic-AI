# Debate-Based Cooperation Agentic AI Pattern

This project demonstrates a **Debate-Based Cooperation Agentic AI architectural pattern** using **CrewAI**, **Gemini LLM**, and **Retrieval-Augmented Generation (RAG)**.

It simulates a **courtroom-style legal debate** where multiple autonomous AI agents argue opposing viewpoints, cite real legal documents (Motor Vehicle Act), and arrive at a reasoned final verdict.

---

## 🧠 Architectural Pattern Overview

Unlike single-agent systems, this pattern models **structured disagreement**:

- Multiple role-driven agents present competing arguments
- Agents respond with rebuttals over multiple rounds
- A supervising agent evaluates arguments using factual legal sources
- Final decisions are delayed until debate saturation

This mirrors real-world legal, policy, and decision-making processes.

---

## ⚖️ Scenario Being Simulated

**Case Summary:**

A minor runs onto the road to save a kitten. A speeding car swerves, crashes, and incurs property damage.

### Core Legal Question

Who is liable?

- The **minor**, for entering the road?
- The **driver**, for overspeeding?
- Or does the **Doctrine of Necessity / Good Samaritan principle** apply?

---

## 🤝 Agents & Their Roles

| Agent | Role | Purpose |
|-----|------|---------|
| Prosecutor | Car Owner | Argues minor caused negligence & damage |
| Defense Attorney | Minor Boy | Argues necessity & driver negligence |
| Judge | Neutral Authority | Evaluates debate & cites Motor Vehicle Act |

---

## 📚 Knowledge Source (RAG)

This project uses **Retrieval-Augmented Generation** to ground decisions in law:

- PDF: **Motor Vehicle Act**
- PDF parsing via `PyPDFLoader`
- Document chunking with `RecursiveCharacterTextSplitter`
- Embeddings using **Gemini Embedding Model**
- Vector search powered by **FAISS**

The Judge agent queries the Act using a custom CrewAI tool.

---

## 🛠 Tech Stack

- Python
- CrewAI
- Google Gemini 2.5 Flash
- LangChain
- FAISS
- Google Generative AI Embeddings
- dotenv / Google Colab

---

## ⚙️ How It Works (Flow)

1. Load Motor Vehicle Act PDF
2. Build FAISS vector store
3. Initialize Prosecutor, Defense, and Judge agents
4. Conduct **multi-round debate** with rebuttals
5. Judge consults the Act using semantic search
6. Judge issues a final verdict citing legal sections

---

## ▶️ Running the Simulation

```bash
pip install crewai langchain-community pypdf faiss-cpu langchain-text-splitters langchain-google-genai python-dotenv
```

Set your API key:

```env
GOOGLE_API_KEY=your_api_key_here
```

Then run:

```bash
python debate_based_cooperation_agentic_ai_pattern.py
```

---

## 📤 Output Example

```
## FINAL COURT VERDICT ##

The court finds that...
(With cited Motor Vehicle Act sections)
```

---

## ✅ Ideal Use Cases

- Legal reasoning simulations
- Policy debate systems
- Ethical decision-making AI
- Compliance & regulatory analysis
- Demonstrating multi-agent coordination

---

## 🚀 Why This Pattern Matters

Debate-Based Cooperation:

- Reduces single-agent bias
- Improves reasoning quality through opposition
- Produces explainable and auditable outcomes
- Scales well for complex decision domains

