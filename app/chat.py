from langgraph.prebuilt import create_react_agent
# TODO(developer): replace this with another import if needed
from langchain_openai import ChatOpenAI
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_anthropic import ChatAnthropic
from langgraph.checkpoint.memory import MemorySaver
import os
from toolbox_langchain import ToolboxClient
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file in the root directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

# Update the prompt to reflect shipping line searches instead of hotel searches
prompt = """
  You're a helpful shipping line assistant. You handle shipping line searches based on various parameters such as equipment type, country, port, free time, and currency. When the user searches for a shipping line, mention its details such as equipment type, country, port, free time, and currency. Always mention the relevant shipping line details when performing any searches. For any queries, please provide the appropriate shipping line details and never ask for confirmations.
"""

queries = [
    "Find shipping lines that offer 20’ Dry equipment.",
    "Can you search for shipping lines in Germany?",
    "Please show me shipping lines that operate in the Port of Hamburg.",
    "Find shipping lines with a free time of 14 Calendar Days.",
    "Can you search for shipping lines that use USD as their currency?",
]

async def run_application():
    # TODO(developer): replace this with another model if needed
    model = ChatOpenAI(model_name="gpt-4-turbo")
    # model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    
    # Load the tools from the Toolbox server
    client = ToolboxClient("http://127.0.0.1:5000")
    tools = await client.aload_toolset()

    agent = create_react_agent(model, tools, checkpointer=MemorySaver())

    config = {"configurable": {"thread_id": "thread-1"}}
    for query in queries:
        inputs = {"messages": [("user", prompt + query)]}
        response = agent.invoke(inputs, stream_mode="values", config=config)
        print(response["messages"][-1].content)

asyncio.run(run_application())
