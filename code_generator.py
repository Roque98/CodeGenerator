from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel,Field
from datetime import datetime

class CodeResponseResult(BaseModel):
    """
    Clase que representa el resultado de una respuesta que contiene código y su ubicación.

    Attributes:
        code (str): Contiene todo el código. Es un string que puede ser `None` por defecto.
        path (str): Nombre del archivo y su ruta en formato "Views|Controllers|sql/Nombre_ruta.extensión". 
                    Es un string que puede ser `None` por defecto.
    """

    code: str = Field(default=None, description="All the code")
    path: str = Field(default=None, description="The name of path with this format (Views|Controllers|sql)/Name_path.extension")
    documentation: str = Field(default=None, description="""The name and description of the all instance in the file with this format: 
                                    (Name of method | Name of sp) : Description
                               """)

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

def generate_sps(model: ChatOpenAI, script_table: str) -> str :
    
    promptTemplate = PromptTemplate.from_template(
        """
            Eres un generador de codigo sql para el manejador mmsql. La salida que generes sera guardada en un archivo por lo que no debes generar ningun texto adicional ademas del codigo. No agregues ningun caracter adicional o el compilador sql fallara
            
            Tomando en cuenta la siguiente estructura de tabla 
            
            {script_table} 
            
            Genera el script que cree los siguientes sps
            - [nombreEntidad]_GetAll 
            - [nombreEntidad]_GetById
            - [nombreEntidad]_Add
            - [nombreEntidad]_Delete
            - [nombreEntidad]_Update
            
            Remplaza el texto [nombreEntidad] por un nombre adecuado tomando en cuenta el nombre de la tabla. El nombre de las columnas debe mostrarse explicitamente.

            El sp debe tener el siguiente encabezado para documentar el sp

            -- =============================================
            -- Author:		CHAT GTP
            -- Create date: {date}
            -- Description:	<Description,,>
            -- =============================================
        """
    )

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = promptTemplate | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke({"script_table": script_table, "date": datetime.now()})

    # Parsear la salida para convertirla en una instancia de CodeResponseResult
    return output.content

def clean_mll_generated_sql(text):
    """
    Limpia un texto generado por un modelo de lenguaje (MLL) eliminando los símbolos extra y dejando solo el código SQL.
    
    :param text: El texto generado por el MLL.
    :return: Un string con el código SQL limpio.
    """
    # Reemplazar las secuencias no necesarias
    cleaned_text = text.replace("\\n", "\n")\
        .replace("GO\n", "")\
        .replace("SET NOCOUNT ON;", "")\
        .replace("```", "")\
        .strip()
    
    return cleaned_text

if __name__ == '__main__':

    model =ChatOpenAI(model="gpt-4o-mini")

    script_table = """
        USE [catalogos]
        GO

        CREATE TABLE [dbo].[prtgDevices](
            [idPrtg] [int] NULL,
            [idObj] [int] NULL,
            [device] [varchar](50) NULL,
            [host] [varchar](50) NULL,
            [tags] [varchar](50) NULL
        ) ON [PRIMARY]
        GO
    """

    result = clean_mll_generated_sql(generate_sps(model, script_table))
    resultClass = generate_code_response(model, result)
    print(result)

