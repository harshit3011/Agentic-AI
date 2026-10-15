from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool

# prompt_template=ChatPromptTemplate.from_messages([
#     ("system","You are a helpful and a concise geography expert"),
#     ("human","What is the capital of {country}")
# ])

# chain=prompt_template | model
# response=chain.invoke({"country":"India"})

# print(response.content)



@tool
def multiply(a:int, b:int)->int:
    """Multiply two integers and return their product"""
    return a*b


load_dotenv()

model=ChatOpenAI()

model_with_tools = model.bind_tools([multiply])

response=model_with_tools.invoke("What is the product of 12 and 8?")

tool_call=response.tool_calls[0]

tool_result= multiply.invoke(tool_call['args'])
print(tool_result)