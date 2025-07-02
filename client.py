from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq


# <----------------------------------->
import os
from dotenv import load_dotenv
load_dotenv('token.env')  # path to your token.env file

langchain_api_key = os.getenv("langchain_api_key")
openai_api_keys = os.getenv("openai_api_key")
tavily_api_key = os.getenv("tavily_api_key")
groq_api_key = os.getenv("groq_api_key")
print("Langchain Key:      ",langchain_api_key[:5] + "..." if langchain_api_key else "key not found")
print("openai_api_key Key: ",openai_api_keys[:5] + "..." if openai_api_keys else "key not found")
print("tavily_api_key Key: ",tavily_api_key[:5] + "..." if tavily_api_key else "key not found")
print("groq_api_key Key:   ",groq_api_key[:5] + "..." if groq_api_key else "key not found")
# <----------------------------------->


import asyncio

async def main():
    client=MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathserver.py"], ## Ensure correct absolute path
                "transport":"stdio",
            
            },
            "weather": {
                "url": "http://localhost:8000/mcp",  # Ensure server is running here
                "transport": "streamable_http",
            }

        }
    )

    import os
    os.environ["GROQ_API_KEY"]=groq_api_key

    tools=await client.get_tools()
    model=ChatGroq(model="qwen-qwq-32b")
    agent=create_react_agent(
        model,tools
    )

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )

    print("Math response:", math_response['messages'][-1].content)

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in California?"}]}
    )
    print("Weather response:", weather_response['messages'][-1].content)

asyncio.run(main())
