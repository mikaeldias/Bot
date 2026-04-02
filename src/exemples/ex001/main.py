# uv run --env-file=".env" src/exemples/ex001/main.py -> Roda esse arquivo 

from langchain.chat_models import init_chat_model 
from rich import print # facilita a vizualição da saída da resposta do agente 
from langchain_core.messages import HumanMessage, SystemMessage # SystemMessage, serve para passar para a LLM de como ela deve se comportar


llm = init_chat_model('google_genai:gemini-2.5-flash') #Iniciando a llm (ja configurada com chave da api)

system_message = SystemMessage("Você é um guia de estudos que ajuda estudantes a aprenderem novos tópicos. \n\n"
    "Seu trabalho é guiar as ideias do estudante para que ele consiga entender o "
    "tópico escolhido sem receber respostas prontas da sua parte. \n\n"
    "Evite conversar sobre assuntos paralelos ao tópico escolhido. Se o estudante "
    "não fornecer um tópico inicialmente, seu primeiro trabalho será solicitar um "
    "tópico até que o estudante o informe. \n\n"
    "Você pode ser amigável, descolado e tratar o estudante como adolescente. Queremos "
    "evitar a fadiga de um estudo rígido e mantê-lo engajado no que estiver "
    "estudando. \n\n"
    "As próximas mensagens serão de um estudante. ") # definindo como o LLM deve se comportar.

human_message = HumanMessage('Olá meu nome é Mikael, tudo bem?') # mensagem humano
messages = [system_message, human_message] # mensagem do sistema
response = llm.invoke(messages) #chamando o chat_model iniciado
print(f'{"AI":-^80}')
print(response.content) # .content apresenta somente o texto do llm

# adciona a resposta do modelo em menssages
messages.append(response)
while True:
    print(f'{"Human":-^80}')
    user_input = input('Digite sua mensagem: ')
    human_message = HumanMessage(user_input)

    if user_input.lower() in ['exit', 'quit', 'bye']:
        break

    messages.append(human_message)

    # manda as messagens com o histórico de volta para o modelo
    response= llm.invoke(messages)
    print(f'{"AI":-^80}')
    print(response.content)
    print()

    # add mensagem do agente 
    messages.append(response)
