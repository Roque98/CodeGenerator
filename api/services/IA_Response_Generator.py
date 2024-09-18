from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


from models import ChatModelSingleton
from models.code_response import CodeResponseResult, generate_code_response
from services.utils import clean_code_mll_generated
from typing import List, Dict


def generate_code_result(prompt: str, params: Dict[str, str]) -> CodeResponseResult:

    # Model    
    model = ChatOpenAI(model="gpt-4o-mini")

    # Escapar {}
    # prompt = prompt.replace('{', '{{').replace('}', '}}')
    # prompt = prompt.replace('└', '{')
    # prompt = prompt.replace('┘', '}')


    # Definir el template del prompt con los parámetros dinámicos
    promptTemplate = PromptTemplate.from_template(prompt)
    

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = promptTemplate | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke(params)

    # Limpiar el código generado por el modelo 
    cleaned_output = clean_code_mll_generated(output.content)

    # Generar la respuesta en forma to CodeResponseResult
    return generate_code_response(cleaned_output)


