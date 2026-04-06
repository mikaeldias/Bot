from typing import Annotated, TypedDict # define uma estrutura fixa para dicionários
from langgraph.graph import StateGraph
from rich import print
import operator # serve para contatenar os nós a + b, através da função .add

# def reducer(a: list[str], b: list[str]) -> list[str]: # recebe os valores do node a e do b
#    return a + b

# 1- Definir o meu estado -> Mantém o meu contexto/Histórico de conversas. Ele entra no input state do grafo 
# e em todo os nodes
class State(TypedDict):
    nodes_path: Annotated[list[str], operator.add] # define o caminho que os nos vão percorrer

# 2 -> Definir os nodes (Função que recebe o estado)

def node_a(state: State) -> State: # A função node_a recebe a classe State e retorna qualquer coisa que eu quiser
    output_state: State = {'nodes_path': ["A"]}
    print("> node_a", f"{state=}", f"{output_state=}")
    return output_state 

def node_b(state: State) -> State: # A função node_a recebe a classe State e retorna qualquer coisa que eu quiser
    output_state: State = {'nodes_path': ["B"]}
    print("> node_b", f"{state=}", f"{output_state=}")
    return output_state

# Definir o Bilder do Grafo
builder = StateGraph(State)

builder.add_node('A', node_a)
builder.add_node('B', node_b)

# Conectar as edges (ou arestas)
builder.add_edge('__start__', 'A')
builder.add_edge('A', 'B')
builder.add_edge('B', '__end__' )

# Compilar o Garfo
graph = builder.compile()

# cria imagem do grafo
graph.get_graph().draw_mermaid_png(output_file_path="file.png")

# Pegar o resultado
response = graph.invoke({"nodes_path": []})

# O resultado de todo o grafo
print()
print(f'{response=}')
print()