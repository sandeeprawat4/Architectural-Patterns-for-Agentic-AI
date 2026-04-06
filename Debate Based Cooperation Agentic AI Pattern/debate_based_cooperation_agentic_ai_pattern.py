!pip install crewai
import os
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from google.colab import userdata
!pip install -q langchain-community pypdf faiss-cpu langchain-text-splitters langchain-google-genai

# Load environment variables
load_dotenv()

# Set the API key
os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")

# Initialize the LLM
gemini_llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=userdata.get("GOOGLE_API_KEY")
)

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from crewai.tools import BaseTool
from google.colab import userdata

# Load the PDF document
loader = PyPDFLoader("/content/Motor_vehicle_act.pdf")
docs = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(docs)

# Initialize Google Generative AI Embeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=userdata.get("GOOGLE_API_KEY"))

# Create a FAISS vector store from the document chunks
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever()

# Define a custom CrewAI tool class
class MVASearchTool(BaseTool):
    name: str = "Motor Vehicle Act Search"
    description: str = "Useful for looking up relevant sections of the Motor Vehicle Act. Input should be a search query."

    def _run(self, query: str) -> str:
        results = retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in results])

mva_tool = MVASearchTool()

print("FAISS vector store created and CrewAI-compatible 'mva_tool' is ready.")

# Define the Prosecutor Agent representing the Car Owner
prosecutor = Agent(
    role="Prosecutor for the Complainant",
    goal="Argue that the minor's sudden movement onto the road caused the accident and property damage, regardless of the intent to save a kitten.",
    backstory="You represent a car owner whose vehicle was damaged after swerving to avoid a pedestrian. You argue that the road is for vehicles and the minor's presence caused an unsafe situation leading to financial loss.",
    llm=gemini_llm,
    verbose=True
)

# Define the Defendant Agent representing the Minor Boy
defendant = Agent(
    role="Defense Attorney for the Minor",
    goal="Argue that the boy acted out of necessity to save a life (the kitten) and that the car's speeding was the primary factor in the loss of control.",
    backstory="You are defending a young boy who acted heroically. You aim to show that 'Doctrine of Necessity' applies and that the driver's inability to stop safely indicates a violation of speed limits by the complainant.",
    llm=gemini_llm,
    verbose=True
)

# Define the Judge Agent
judge = Agent(
    role="Judge",
    goal="Evaluate the liability in the accident. Determine if the minor's actions constitute negligence or if the driver's speed contributed to the incident, citing the Motor Vehicle Act.",
    backstory="You are a fair judge. You must weigh the 'Good Samaritan' principles and necessity of saving a life against the laws governing road safety and property damage as per the MVA.",
    tools=[mva_tool],
    llm=gemini_llm,
    verbose=True
)

# Enhanced Tasks for an extended multi-round debate
prosecution_task = Task(
    description="Present the car owner's case. Once the defense responds, you MUST provide a specific rebuttal addressing their claims about the 'Doctrine of Necessity' and the driver's speed. Continue the debate for at least 3 exchanges.",
    agent=prosecutor,
    expected_output="A series of legal arguments and specific rebuttals to the defense's points, focusing on the minor's liability."
)

defense_task = Task(
    description="Defend the minor. Counter the prosecution's claims. When the prosecutor rebuts, you MUST respond again, focusing on the 'Good Samaritan' aspect and the driver's negligence. Maintain the debate for at least 3 exchanges.",
    agent=defendant,
    expected_output="A series of defensive arguments and counter-rebuttals emphasizing necessity and driver error."
)

verdict_task = Task(
    description="Monitor the entire multi-round debate. Only after both sides have exhausted their legal points and the manager signals the end, use the Motor Vehicle Act Search tool to find relevant sections and deliver the final judgment.",
    agent=judge,
    expected_output="A definitive final verdict citing specific MVA sections, delivered only after a thorough debate."
)

# Re-initialize the hierarchical crew with stricter debate requirements
court_crew = Crew(
    agents=[prosecutor, defendant, judge],
    tasks=[prosecution_task, defense_task, verdict_task],
    process=Process.hierarchical,
    manager_llm=gemini_llm,
    verbose=True
)

# Execute the extended simulation
result = court_crew.kickoff()

print('\n\n########################')
print('## FINAL COURT VERDICT ##')
print('########################\n')
print(result.raw)
