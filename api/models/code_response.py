from typing import Any, Dict
from langchain_core.pydantic_v1 import BaseModel,Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

class CodeResponseResult(BaseModel):
    """
    Clase que representa el resultado de una respuesta que contiene código y su ubicación.

    Attributes:
        code (str): Contiene todo el código. Es un string que puede ser `None` por defecto.
        path (str): Nombre del archivo y su ruta en formato "Views|Controllers|sql/Nombre_ruta.extensión". 
                    Es un string que puede ser `None` por defecto.
    """

    code: str = Field(default=None, description="All the code")
    path: str = Field(default=None, description="The name of path with this format (Entities or Models Views or Controllers or sql_scripts)/Name_path.extension. Example: Views/index.cshtml or sql/insert.sql")
    documentation: str = Field(default=None, description=
                               """The name and description of the all instance in the file with this format: 
                                    (Name of method or Name of sp) : Description
                               """)
    extension:str = Field(default=None, description="Extension of the code. Example cshtml, sql.")


def generate_code_response(model: ChatOpenAI, result: str):
    """
    Genera una instancia de `CodeResponseResult` a partir de un resultado utilizando un modelo de lenguaje.

    Esta función toma un resultado de texto, lo procesa utilizando un modelo de lenguaje, y luego
    lo convierte en una instancia de la clase `CodeResponseResult`.

    Args:
        model (ChatOpenAI): El modelo de lenguaje utilizado para generar la respuesta.
        result (str): El resultado que se convertirá en una instancia de `CodeResponseResult`.

    Returns:
        CodeResponseResult: La instancia generada de `CodeResponseResult` que contiene el código y la ruta.
    """
    # Crear un parser para convertir la salida en una instancia de CodeResponseResult
    parser = PydanticOutputParser(pydantic_object=CodeResponseResult)

    # Definir el prompt que se enviará al modelo
    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = prompt | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke({"query": result})

    # Parsear la salida para convertirla en una instancia de CodeResponseResult
    return parser.invoke(output)
