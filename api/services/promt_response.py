from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from models.code_response import CodeResponseResult, generate_code_response
from services.utils import clean_code_mll_generated

def generate_response(prompt: str, params: Dict[str, str]) -> CodeResponseResult:
    
    model = ChatOpenAI(model="gpt-4o-mini")

    # Definir el template del prompt con los parámetros dinámicos
    promptTemplate = PromptTemplate.from_template(prompt)

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = promptTemplate | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke(params)

    resultCode = clean_code_mll_generated(output.content)

    # Parsear la salida para convertirla en una instancia de CodeResponseResult
    return generate_code_response(model, resultCode )