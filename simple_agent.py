from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent

agent = create_agent(
    model="xai:grok-3-mini"
)
result = agent.invoke({"messages" :{"role" : "user", "content" : "Hi how are you" }})

for i, msg in enumerate(result["messages"]):
    msg.pretty_print()