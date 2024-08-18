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
    path: str = Field(default=None, description="The name of path with this format (Views or Controllers or sql)/Name_path.extension. Example: Views/index.cshtml or sql/insert.sql")
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

def generate_sps(model: ChatOpenAI, script_table: str) -> CodeResponseResult :
    
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

            El sp _GetAll debe recibir al final como parametros opcionales fechaInicio y fechaFin para poder delimitar por fecha los resultados
        """
    )

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = promptTemplate | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke({"script_table": script_table, "date": datetime.now()})

    # Parsear la salida para convertirla en una instancia de CodeResponseResult
    return generate_code_response(model, clean_code_mll_generated(output.content))

def test_sps(model: ChatOpenAI):
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

    return generate_sps(model, script_table)

def generate_entidad_coms(model: ChatOpenAI, script_table: str) -> CodeResponseResult:
    promptTemplate = PromptTemplate.from_template(
        """
            Eres un generador de codigo c#. La salida que generes sera guardada en un archivo por lo que no debes generar ningun texto adicional ademas del codigo. No agregues ningun caracter adicional o el compilador C# fallara
            
            Tomando en cuenta la siguiente documentacion de los tabla
            
            {script_table} 
            
            Genera un archivo que contenga el codigo de la clase para guardar los datos de la tabla llamado [nombreEntidad]Entidad.cs
            
            Remplaza el texto [nombreEntidad] por un nombre adecuado tomando en cuenta el nombre de la tabla.
        """
    )

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = promptTemplate | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke({"script_table": script_table})

    # Parsear la salida para convertirla en una instancia de CodeResponseResult
    return generate_code_response(model, clean_code_mll_generated(output.content))

def test_entidad(model: ChatOpenAI):
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

    result = clean_code_mll_generated(generate_entidad_coms(model, script_table))
    print(result)
    return generate_code_response(model, result)

def generate_model_coms(model: ChatOpenAI, documentation: str) -> CodeResponseResult:
    framgento_codigo = """
        namespace Consola_Monitoreo.Models
        {
            public class BaseDatosModel : Model
            {
                public BaseDatosModel() : base()
                {

                }

                public List<AlertaTablespace> GetAll(DateTime fechaInicio, DateTime fechaFin)
                {
                    return ejecutaStoredProcedure<AlertaTablespace>("ConsolaMonitoreo.dbo.BDOracle_ConsultaAlertasTablespace", new Dictionary<string, object>()
                    {
                        {"@fechaInicio", fechaInicio },
                        {"@fechaFin", fechaFin }
                    });
                }

            }
        }
    """
    
    promptTemplate = PromptTemplate.from_template(
        """
            Eres un generador de codigo c#. La salida que generes sera guardada en un archivo por lo que no debes generar ningun texto adicional ademas del codigo. No agregues ningun caracter adicional o el compilador C# fallara
            
            Tomando en cuenta la siguiente documentacion de los sp y la clase entidad
            
            {documentation} 
            
            Genera un archivo que contenga el codigo de la clase para model llamado [nombreEntidad]Model.cs

            Esto tomando como referencia la siguiente clase para que sigas el mismo estilo de codigo.

            {framgento_codigo}
            
            Asegurante de implementar todos los metodos para todos los sps. Documenta las funciones c#
            

            Remplaza el texto [nombreEntidad] por un nombre adecuado tomando en cuenta el nombre de la tabla.
        """
    )

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = promptTemplate | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke({"documentation": documentation, "framgento_codigo": framgento_codigo})

    # Parsear la salida para convertirla en una instancia de CodeResponseResult
    return generate_code_response(model, clean_code_mll_generated(output.content))


def clean_code_mll_generated(code):
    """
    Limpia un texto generado por un modelo de lenguaje (MLL) eliminando los símbolos extra y dejando solo el código de programacion.
    
    :param text: El texto generado por el MLL.
    :return: Un string con el código SQL limpio.
    """
    # Reemplazar las secuencias no necesarias
    code_text = code.replace("\\n", "\n")\
        .replace("GO\n", "")\
        .replace("SET NOCOUNT ON;", "")\
        .replace("```", "")\
        .strip() 
    
    return code_text

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

    result_entidad = generate_entidad_coms(model,script_table)
    result_sps = generate_sps(model,script_table)

    documentation = result_entidad.documentation + result_sps.documentation

    result_model = generate_model_coms(model, documentation)
    print(result_model)
    

    