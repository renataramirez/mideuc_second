import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

load_dotenv()

# Configurar el LLM con Azure
llm = AzureChatOpenAI(
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT"),
    model="gpt-4",  # opcional, depende de tu deployment
    openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0.7,
)

# Agregar memoria conversacional
memory = ConversationBufferMemory(return_messages=True)
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Simular una conversación
print(conversation.invoke("Hola, soy Renata."))
print(conversation.invoke("¿Recuerdas cómo me llamo?"))
print(conversation.invoke("¿Puedes darme un consejo de estudio?"))
