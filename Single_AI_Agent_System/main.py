
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
    SystemMessage,
)
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

SYSTEM_PROMPT = """
You are an expert research assistant.
- Search the web when information is current, uncertain, or needs verification.
- Answer straightforward questions directly when appropriate.
- Summarize search results instead of dumping raw results.
- Clearly distinguish verified information from uncertainty.
"""


@tool
def search_web(query: str) -> str:
    """Search the web for current information about a topic."""
    search_tool = TavilySearchResults(max_results=5)
    results = search_tool.invoke({"query": query})
    return str(results)


model = ChatOpenAI()
tools = [search_web]
model_with_tools = model.bind_tools(tools)
tools_by_name = {tool.name: tool for tool in tools}


def ask_agent(question: str, history: list) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *history,
        HumanMessage(content=question),
    ]

    max_iterations = 5

    for _ in range(max_iterations):
        response = model_with_tools.invoke(messages)
        messages.append(response)

        if not response.tool_calls:
            history.extend([
                HumanMessage(content=question),
                response,
            ])
            return response.content or "I couldn't generate a text response."

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            selected_tool = tools_by_name.get(tool_name)

            if selected_tool is None:
                result = f"Unknown tool: {tool_name}"
            else:
                try:
                    result = selected_tool.invoke(tool_call["args"])
                except Exception as e:
                    result = f"Tool execution failed: {e}"

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"],
                )
            )

    return "I couldn't complete the research within the iteration limit."
