from langchain_core.tools import tool
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate


from models.result import Result

@tool
def multiply(first_int: int, second_int: int) -> int:
    """Multiply two integers together"""
    return first_int * second_int

@tool
def add(first_int: int, second_int: int) -> int:
    "Add two integers."
    return first_int + second_int


@tool
def exponentiate(base: int, exponent: int) -> int:
    "Exponentiate the base to the exponent power."
    return base**exponent

def create_agent_and_executor(llm: ChatOpenAI):

    # Get the prompt to use - can be replaced with any prompt that includes variables "agent_scratchpad" and "input"!
    prompt = hub.pull("hwchase17/openai-tools-agent")
    prompt.pretty_print()
    
    # Tools
    tools = [multiply, add, exponentiate]

    # Construct the tool calling agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    # run agent
    result = agent_executor
    
    # return
    return result

def get_json_result(model: ChatOpenAI, result: str):
    # Set up a parser + inject instructions into the prompt template.
    parser = PydanticOutputParser(pydantic_object=Result)

    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # And a query intended to prompt a language model to populate the data structure.
    prompt_and_model = prompt | model
    output = prompt_and_model.invoke({"query": result})
    return parser.invoke(output)


if __name__ == "__main__":
    # Define llm
    llm = ChatOpenAI(model="gpt-4o-mini")

    print(multiply.name)
    print(multiply.description)
    print(multiply.args)
    
    # result = multiply.invoke({"first_int": 2, "second_int": 5})
    # print(result) # 10

    agent = create_agent_and_executor(llm)

    result = agent.invoke({"input": "Cuanto es 5 mas 5 a la segunda potencia?"})
    # print(result) # {'input': 'Cuanto es 5 mas 5 a la segunda potencia?', 'output': '5 más 5 a la segunda potencia es 30.'}

    result_parser = get_json_result(llm,result)
    print(result_parser.result)