from ast import operator
from langchain.messages import AIMessage, HumanMessage
from langchain_core.messages import BaseMessage
from typing import Sequence, TypedDict
from typing_extensions import Annotated
from rich import print
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph, add_messages
from langgraph.graph.message import Messages
from langchain.chat_models import init_chat_model
from rich.markdown import Markdown
from langgraph.graph.state import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq


llm = init_chat_model('groq:llama-3.1-8b-instant')



# defino o state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# defino meus nodes
def call_llm(state: AgentState) -> AgentState:
    #llm_result = llm.invoke(state['messages'])
    llm_result = llm.invoke(state['messages']) # resposta fixa para teste
    return {'messages': [llm_result]} 

# crio o stategraph
builder = StateGraph(
    AgentState, context=None, input_schema=AgentState, output_schema=AgentState
)

# add node ao grafo
builder.add_node("call_llm", call_llm)

#fazendo as conexões entre os nodes
builder.add_edge("__start__", "call_llm")
builder.add_edge("call_llm", "__end__")

# compilar
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)
config = RunnableConfig(configurable={"thread_id": 1})

# usar o grafo

if __name__ == "__main__":
    
    while True:
        user_input = input('Digite para falar com o Gemini: ')
        print(Markdown('---'))

        if user_input.lower() in ['q', 'quit']:
            print('Encerrando a conversa. Até mais!')
            print(Markdown('---'))
            break
        human_message = HumanMessage(user_input)
        result = graph.invoke(
         {"messages": [human_message]}
        )
        current_messages = result['messages']
        print(Markdown(str(result['messages'][-1].content)))
        print(Markdown('---'))


