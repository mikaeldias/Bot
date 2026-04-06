from typing import Annotated, Literal, TypedDict # define uma estrutura fixa para dicionários
from langgraph.graph import END, START, StateGraph
from rich import print
import operator # serve para contatenar os nós a + b, através da função .add
from dataclasses import dataclass


# 1- Definir o meu estado -> Mantém o meu contexto/Histórico de conversas. Ele entra no input state do grafo 
# e em todo os nodes
@dataclass
class State:
    nodes_path: Annotated[list[str], operator.add] # define o caminho que os nos vão percorrer
    current_number: int = 0

# 2 -> Definir os nodes (Função que recebe o estado)

def node_a(state: State) -> State: # A função node_a recebe a classe State e retorna qualquer coisa que eu quiser
    output_state: State = State(nodes_path= ["A"], current_number=state.current_number)
    print("> node_a", f"{state=}", f"{output_state=}")
    return output_state 

def node_b(state: State) -> State: # A função node_a recebe a classe State e retorna qualquer coisa que eu quiser
    output_state: State = State(nodes_path= ["B"], current_number=state.current_number)
    print("> node_b", f"{state=}", f"{output_state=}")
    return output_state 

def node_c(state: State) -> State: # A função node_a recebe a classe State e retorna qualquer coisa que eu quiser
    output_state: State = State(nodes_path= ["C"], current_number=state.current_number)
    print("> node_c", f"{state=}", f"{output_state=}")
    return output_state 

def the_conditional(state: State) -> Literal['B', 'C']:
    if state.current_number >= 50:
        return 'C'
    return 'B'

# Definir o Bilder do Grafo
builder = StateGraph(State)

builder.add_node('A', node_a)
builder.add_node('B', node_b)
builder.add_node('C', node_c)



# Conectar as edges (ou arestas)
builder.add_edge(START, 'A')
builder.add_conditional_edges('A', the_conditional, ['B', 'C'])
builder.add_edge('B', END )
builder.add_edge('C', END )

# Compilar o Garfo
graph = builder.compile()

# cria imagem do grafo
graph.get_graph().draw_mermaid_png(output_file_path="file.png")



# O resultado de todo o grafo
print()# Pegar o resultado
response = graph.invoke(State(nodes_path=[]))
print(f'{response=}')
print()

# O resultado de todo o grafo
print()# Pegar o resultado
response = graph.invoke(State(nodes_path=[], current_number=51))
print(f'{response=}')
print()