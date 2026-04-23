# Smart Traffic Management System (Dual-LLM Swarm Architecture)

## Overview
This project demonstrates a **Smart Traffic Management System** built using a **dual LLM swarm architectural pattern**. It leverages **LangGraph** for agent orchestration and **Google Gemini models** for differentiated reasoning tasks.

The system simulates how modern smart cities can process:
- Unstructured traffic reports
- On-ground patrol sensor input
- Traffic violations and penalty enforcement

using **multiple cooperating AI agents**.

---

## Architecture: Dual LLM Swarm Pattern

The system uses **two specialized LLMs**:

| Agent Role | Model | Responsibility |
|----------|------|----------------|
| Observer Agent | Gemini 2.5 Flash | Fast extraction from unstructured text & sensor data |
| Penalty/Manager Agent | Gemini 2.5 Pro | Higher-reasoning tasks such as violation assessment, severity and enforcement |

All agents communicate through a **shared state graph** implemented using LangGraph.

---

## Project Structure

```text
traffic_management_system.py   # Main multi-agent orchestration code
README.md                      # Project documentation
```

---

## Key Components

### 1. TrafficSystemState
A strongly-typed shared state that flows through the agent graph.

```python
class TrafficSystemState(TypedDict):
    unstructured_input: str
    raw_sensor_data: Dict
    refined_data: Dict
    penalty_status: str
    notifications_sent: List[str]
    management_action: str
    on_ground_image_ref: str
```

---

### 2. Agent Nodes

- **Input Processor Node**
  - Normalizes text and sensor inputs
- **Management Orchestrator Node**
  - Decides operational response (warnings, towing, monitoring)
- **Penalty Compliance Node**
  - Issues penalties and sends notifications

---

### 3. LangGraph Orchestration

```text
processor -> manager -> penalty -> END
```

A single unified graph handles *both* patrol sensor data and citizen reports.

---

## Simulated Scenarios

- Illegal parking detection
- Median bypass violations
- High congestion narrative reports
- Smart patrol vehicle sightings

---

## How to Run

```bash
pip install langchain-google-genai langgraph pandas
python traffic_management_system.py
```

Ensure your Google Gemini API key is set via environment variables.

---

## Why Dual LLM Swarm?

✅ Separation of concerns
✅ Cost-efficient inference
✅ Better reasoning accuracy
✅ Scalable city-wide deployments

---

## Future Enhancements

- Real-time camera feeds
- Computer vision integration
- Dynamic traffic light control
- Reinforcement learning for congestion optimization

---
