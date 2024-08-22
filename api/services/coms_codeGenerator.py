from langchain_openai import ChatOpenAI
from datetime import datetime
from models.code_response import CodeResponseResult, generate_code_response
from langchain_core.prompts import PromptTemplate

from services.utils import clean_code_mll_generated


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

def generate_entidad_coms(model: ChatOpenAI, script_table: str) -> CodeResponseResult:
    promptTemplate = PromptTemplate.from_template(
        """
            Eres un generador de codigo c#. La salida que generes sera guardada en un archivo por lo que no debes generar ningun texto adicional ademas del codigo. No agregues ningun caracter adicional o el compilador C# fallara
            
            Tomando en cuenta la siguiente documentacion de los tabla
            
            {script_table} 
            
            Genera un archivo que contenga el codigo de las clases dto con el siguiente patron de nombre [operacionCrud][nombreEntidad]Entidad.cs. Donde [operacionCrud] puede ser remplazado por Create, Read, Update, Delete de pendiendo la operacion
            
            Remplaza el texto [nombreEntidad] por un nombre adecuado tomando en cuenta el nombre de la tabla.
        """
    )

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = promptTemplate | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke({"script_table": script_table})

    # Parsear la salida para convertirla en una instancia de CodeResponseResult
    return generate_code_response(model, clean_code_mll_generated(output.content))

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

def generate_all_code_coms(script_table: str) -> [] :

    model = ChatOpenAI(model="gpt-4o-mini")

    result_entidad = generate_entidad_coms(model,script_table)
    result_sps = generate_sps(model,script_table)

    documentation = result_entidad.documentation + result_sps.documentation

    result_model = generate_model_coms(model, documentation)

    responses = [ result_entidad, result_sps, result_model ]

    return responses

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
    

    