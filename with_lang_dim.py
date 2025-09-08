import pandas as pd
from dotenv import load_dotenv
import os
import json
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_GPT"),
    openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0,
)

df = pd.read_excel("df_ECE.xlsx")
texto_a_corregir = df.iloc[0]["escrito"]

prompt = """
Eres un asistente experto en corrección de textos. Aplica estas reglas al texto:

CATEGORÍAS Y SUBCATEGORÍAS DE ERRORES:

1. ORTOGRAFÍA
   1.1 Ortografía acentual: errores en tildes según normas generales y especiales.
       Ejemplos: esta/está, animos/ánimos
   1.2 Ortografía literal: errores en letras dentro de palabras.
       Omisión: "alchol" → "alcohol"
       Sustitución: "fotocopeo" → "fotocopio"
       Adición: "rrallado" → "rallado"
       Ejemplos adicionales: “apartir” → “a partir”, “através” → “a través”, “porsiacaso” → “por si acaso”
   1.3 Ortografía puntual: errores en signos de puntuación según normas RAE.
       Incluye: coma, punto, punto y coma, signos de exclamación e interrogación

INSTRUCCIONES CRÍTICAS:
- Detecta errores según esta categoría y subcategorías.
- Para CADA error, especifica la subcategoría exacta.
- NO incluyas el texto corregido completo.
- Devuelve SOLAMENTE JSON válido sin formato markdown (sin ```json o similares).
- El JSON debe comenzar inmediatamente con {{ y terminar con }}.

ESTRUCTURA EXACTA REQUERIDA:
{{
  "texto_original_preview": "Primeros 100 caracteres del texto...",
  "errores_detectados": {{
      "ortografia": [
        {{
          "error": "error original",
          "correccion": "corrección propuesta",
          "subcategoria": "acentual/literal/puntual"
        }}
      ], 
  }}
}}

FORMATO DE ERRORES:
IMPORTANTE: Si un error pertenece a otra categoría que no sea la correcta, ignóralo. No pongas subcategorías incorrectas. 
- ORTOGRAFÍA → solo acentual, literal, puntual
- En "texto_original_preview" incluye SOLO los primeros 100 caracteres del texto original.
- NO uses markdown, NO incluyas ```json, devuelve SOLO el JSON.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", prompt),
    ("human", "{input}")
])
store = {}
def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    prompt | llm,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)
session_id = "renata" 
resultado = chain_with_memory.invoke({"input": texto_a_corregir}, {"configurable": {"session_id": session_id}})

respuesta_limpia = resultado.content.strip()
if respuesta_limpia.startswith("```json"):
    respuesta_limpia = respuesta_limpia.replace("```json", "").replace("```", "").strip()

try:
    resultado_json = json.loads(respuesta_limpia)

    categorias_validas = {
        "ortografia": {"acentual", "literal", "puntual"}
    }

    for categoria, subcategorias in resultado_json["errores_detectados"].items():
        resultado_json["errores_detectados"][categoria] = [
            error for error in subcategorias if error["subcategoria"] in categorias_validas[categoria]
            ]
    
    output_path = "resultado_correccion_ui.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultado_json, f, ensure_ascii=False, indent=4)
    
    print(f"Resultado guardado en {output_path}")
    print("Preview del texto:", resultado_json.get("texto_original_preview", ""))
    
    if "errores_detectados" in resultado_json:
        errores = resultado_json["errores_detectados"]
        print("\nEstadísticas de errores:")
        for categoria, lista_errores in errores.items():
            if lista_errores:
                subcategorias = {}
                for error in lista_errores:
                    subcat = error.get("subcategoria", "sin_subcategoria")
                    subcategorias[subcat] = subcategorias.get(subcat, 0) + 1
                
                print(f"{categoria.upper()}: {len(lista_errores)} errores")
                for subcat, count in subcategorias.items():
                    print(f"  - {subcat}: {count}")
    
except json.JSONDecodeError as e:
    print(f"Error al parsear JSON: {e}")
    print("Respuesta cruda recibida:")
    print(respuesta_limpia)
    