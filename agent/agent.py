from langchain.agents import initialize_agent, Tool
from config import get_llm
from agent.tools import analyze_review, get_business_context, generate_response
from agent.memory import get_memory

llm = get_llm()

tools = [
    Tool(name="Analyze Review", func=analyze_review, description="Analyze review"),
    Tool(name="Get Business Context", func=get_business_context, description="Get context"),
    Tool(name="Generate Response", func=generate_response, description="Generate reply"),
]

memory = get_memory()

SYSTEM_PROMPT = """
You are an AI Reputation Manager.

STRICT RULES:
1. ALWAYS call Analyze Review first
2. THEN call Get Business Context
3. THEN you MUST call Generate Response

DO NOT STOP after analysis.
DO NOT give analysis as final answer.

FINAL ANSWER MUST be the customer response ONLY.

Never output analysis in final answer.
Only output the response message to customer.

"""

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    memory=memory,
    verbose=True,
    agent_kwargs={"system_message": SYSTEM_PROMPT}
)