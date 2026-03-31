

!pip install -U crewai

import os
from crewai import Agent, Task, Crew, Process, LLM
from google.colab import userdata
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set the OpenAI API key
os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")
llm = LLM(
    model="gemini/gemini-2.5-flash",
)


FIBONACCI_STORY_POINTS = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55]
ROLE_WEIGHTAGES = {
    "Architect": 5,
    "Senior Engineer": 4,
    "Mid Engineer": 3,
    "QA": 3,
    "Junior Engineer": 2,
    "Intern": 1
}

# Define Agents with the Gemini LLM
leader = Agent(
    role="Sprint Leader",
    goal="Facilitate story point discussion and conclude the final story point based on weighted team input.",
    backstory=f"""You are an experienced Agile Sprint Leader.
                 Gather input from everyone, apply role weightages, and pick a single Fibonacci story point: {FIBONACCI_STORY_POINTS}.""",
    verbose=True,
    llm=llm
)

architect = Agent(
    role="Software Architect",
    goal="Estimate points focusing on system design and scalability.",
    backstory="You are a seasoned Architect. Your estimates consider long-term technical debt and infrastructure.",
    verbose=True,
    llm=llm
)

senior_engineer = Agent(
    role="Senior Software Engineer",
    goal="Estimate points based on implementation complexity and roadblocks.",
    backstory="You are a hands-on Senior Engineer focused on practical execution and best practices.",
    verbose=True,
    llm=llm
)

mid_engineer = Agent(
    role="Mid-Level Software Engineer",
    goal="Estimate points focusing on common patterns and module interactions.",
    backstory="You understand typical development cycles and execution patterns.",
    verbose=True,
    llm=llm
)

junior_engineer = Agent(
    role="Junior Software Engineer",
    goal="Estimate points considering learning curve and basic implementation.",
    backstory="You are eager to learn and your estimates reflect the effort for someone newer to the codebase.",
    verbose=True,
    llm=llm
)

intern = Agent(
    role="Software Engineering Intern",
    goal="Estimate points based on fundamental concepts.",
    backstory="You are just starting out. Your estimates reflect basic complexity perception.",
    verbose=True,
    llm=llm
)

qa = Agent(
    role="Quality Assurance Engineer",
    goal="Estimate points focusing on testing effort and potential bugs.",
    backstory="You are meticulous about quality and robust acceptance criteria.",
    verbose=True,
    llm=llm
)

# Define Tasks with Async Execution for parallel processing
define_task_description = Task(
    description=(
        "The team needs to estimate story points for the following task: "
        "Implement a user authentication system with email/password login, Google OAuth, and password reset functionality. "
        "This includes backend API development, database schema changes, and frontend integration."
        f"The chosen Fibonacci story points are: {FIBONACCI_STORY_POINTS}."
    ),
    agent=None,
    expected_output="A clear and concise description of the task."
)

architect_estimate_task = Task(
    description="Estimate the story points for the task: '{task_description}'. Focus on architecture and scalability.",
    agent=architect,
    expected_output="A JSON string with 'reasoning' and 'estimate'.",
    async_execution=True
)

senior_engineer_estimate_task = Task(
    description="Estimate the story points for the task: '{task_description}'. Focus on implementation and roadblocks.",
    agent=senior_engineer,
    expected_output="A JSON string with 'reasoning' and 'estimate'.",
    async_execution=True
)

mid_engineer_estimate_task = Task(
    description="Estimate the story points for the task: '{task_description}'. Focus on common patterns and testing.",
    agent=mid_engineer,
    expected_output="A JSON string with 'reasoning' and 'estimate'.",
    async_execution=True
)

junior_engineer_estimate_task = Task(
    description="Estimate the story points for the task: '{task_description}'. Focus on learning curve and basic steps.",
    agent=junior_engineer,
    expected_output="A JSON string with 'reasoning' and 'estimate'.",
    async_execution=True
)

intern_estimate_task = Task(
    description="Estimate the story points for the task: '{task_description}'. Focus on fundamental concepts.",
    agent=intern,
    expected_output="A JSON string with 'reasoning' and 'estimate'.",
    async_execution=True
)

qa_estimate_task = Task(
    description="Estimate the story points for the task: '{task_description}'. Focus on testing effort and bugs.",
    agent=qa,
    expected_output="A JSON string with 'reasoning' and 'estimate'.",
    async_execution=True
)

role_weightages_escaped = str(ROLE_WEIGHTAGES).replace('{', '{{').replace('}', '}}')

leader_decision_task = Task(
    description=(
        "Synthesize the story point estimations for '{task_description}'. "
        f"Apply these weightages: {role_weightages_escaped}. "
        f"Pick a final point from {FIBONACCI_STORY_POINTS}."
    ),
    agent=leader,
    context=[architect_estimate_task, senior_engineer_estimate_task, mid_engineer_estimate_task, junior_engineer_estimate_task, intern_estimate_task, qa_estimate_task],
    expected_output="A JSON string with 'final_reasoning' and 'final_story_point'."
)

# Assemble and Run the Crew
crew = Crew(
    agents=[leader, architect, senior_engineer, mid_engineer, junior_engineer, intern, qa],
    tasks=[architect_estimate_task, senior_engineer_estimate_task, mid_engineer_estimate_task, junior_engineer_estimate_task, intern_estimate_task, qa_estimate_task, leader_decision_task],
    process=Process.sequential,
    verbose=True
)

results = crew.kickoff(inputs={'task_description': define_task_description.description})
print("\n### Final Story Point Discussion Result ###")
print(results)
