from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_community.tools.tavily_search import TavilySearchResults

@tool
def search_web(query:str)->str:
    """Search the web for current information about a topic."""
    search_tool= TavilySearchResults(max_results=5)
    results=search_tool.invoke(query)
    return str(results)


load_dotenv()

model = ChatOpenAI()
tools = [search_web]
model_with_tools = model.bind_tools(tools)

question = input("Ask me a question: ")
messages=[HumanMessage(content=question)]

tools_by_name = {tool.name: tool for tool in tools}

while True:
    response = model_with_tools.invoke(messages)
    messages.append(response)

    if not response.tool_calls:
        print(response.content)
        break

    for tool_call in response.tool_calls:
        selected_tool = tools_by_name[tool_call["name"]]
        tool_result = selected_tool.invoke(tool_call["args"])

        print("Tool executed successfully.")
        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"],
            )
        )
