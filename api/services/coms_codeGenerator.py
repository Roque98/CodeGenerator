from langchain_openai import ChatOpenAI
from datetime import datetime
# from models.code_response import CodeResponseResult, generate_code_response
from langchain_core.prompts import PromptTemplate

from models import ChatModelSingleton
from models.code_response import CodeResponseResult, generate_code_response
from services.utils import clean_code_mll_generated


def generate_sps(script_table: str) -> CodeResponseResult :
    
    model = ChatModelSingleton()

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

            Cambia <Description,,> por una documentacion adecuada.
        """
    )

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = promptTemplate | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke({"script_table": script_table, "date": datetime.now()})

    # Parsear la salida para convertirla en una instancia de CodeResponseResult
    return generate_code_response(model, clean_code_mll_generated(output.content))

def generate_entidad_coms( script_table: str) -> CodeResponseResult:
    
    model = ChatModelSingleton()

    promptTemplate = PromptTemplate.from_template(
        """
            Eres un generador de codigo c#. La salida que generes sera guardada en un archivo por lo que no debes generar ningun texto adicional ademas del codigo. No agregues ningun caracter adicional o el compilador C# fallara
            
            Tomando en cuenta la siguiente documentacion de los tabla
            
            {script_table} 
            
            Genera un archivo que contenga el codigo para guardar el resultado de la tabla llamado [nombreEntidad]Entidad.cs
            
            Si existe una referencia a otra tabla genera una propiedad adicional para guardar la referencia a la tabla entidad

            Remplaza el texto [nombreEntidad] por un nombre adecuado tomando en cuenta el nombre de la tabla.
        """
    )

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = promptTemplate | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke({"script_table": script_table})

    # Parsear la salida para convertirla en una instancia de CodeResponseResult
    return generate_code_response(model, clean_code_mll_generated(output.content))

def generate_interfaz_coms( codigo_entidad: str) -> CodeResponseResult:
    
    model = ChatModelSingleton()

    fragmento_codigo = """
            using FolderView.Dapper.Entidades;

            namespace FolderView.Dapper.Interfaces
            {
                public interface IArchivoRepository
                {
                    Task<List<ArchivoEntidad>> GetAll(int directorioId);
                    Task<ArchivoEntidad> GetByIdDirectorio(int directorioId);
                }
            }

    """

    lista_interfaces = """
            Task<List<TipoProyectoEntidad>> CreateTipoProyectoAsync(TipoProyectoEntidad dto);
            Task<TipoProyectoEntidad> GetTipoProyectoByIdAsync(int id);
            Task<List<TipoProyectoEntidad>> GetAllTipoProyecto();
            Task<List<TipoProyectoEntidad>> UpdateTipoProyectoAsync(TipoProyectoEntidad dto);
            Task<bool> TipoProyectoEntidad(int id);

            Solo en caso de que exista alguna dependecia generar este metodo
            Task<List<TipoProyectoEntidad>> GetAllTipoProyectoById[EntidadRelacionadaPadre]Async(int id);  ( Remplaza [EntidadRelacionadaPadre] por el nombre de la entidad referenciada. Genera tantos como sea posible)

    """

    promptTemplate = PromptTemplate.from_template(
        """
            Eres un generador de codigo c#. La salida que generes sera guardada en un archivo por lo que no debes generar ningun texto adicional ademas del codigo. No agregues ningun caracter adicional o el compilador C# fallara
            
            
            Tomando en cuenta la siguiente clase entidad 

            {codigo_entidad}
            
            Toma como referencia el siguiente codigo del la clase IArchivoRepository respetando los imports y el namespace genera la interfaz [NombreEntidad]Repository

            {fragmento_codigo}
            
            Lista las funciones en las que basarse que debe contener la interfaz

            {lista_interfaces}
            
        """
    )

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = promptTemplate | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke({"codigo_entidad": codigo_entidad, "lista_interfaces": lista_interfaces,"fragmento_codigo" : fragmento_codigo})

    # Parsear la salida para convertirla en una instancia de CodeResponseResult
    return generate_code_response(model, clean_code_mll_generated(output.content))

def generate_model_coms(entidades: str, interfaz: str) -> CodeResponseResult:
    
    model = ChatModelSingleton()

    framgento_codigo = """
        using Dapper;
        using FolderView.Dapper.Entidades;
        using FolderView.Dapper.Interfaces;
        using System.Data;

        namespace FolderView.Dapper.Repositorios
        {{
            public class ArchivoRepositorio : IArchivoRepository
            {{
                private readonly DapperContext _context;
                public ArchivoRepositorio(DapperContext context)
                {{
                    _context = context;
                }}
                public async Task<List<ArchivoEntidad>> GetByDirectorioIdAsync(int directorioId)
                {{
                    var query = $"consolaMonitoreo..[FolderView_Archivo_GetAllByParentDirectoryId]";
                    var connection = _context.CreateConnection();
                    var param = new {{ directorioId }};
                    var resultado = await connection.QueryAsync<ArchivoEntidad>(query,
                                                                                        param,
                                                                                        commandType: CommandType.StoredProcedure);
                    return resultado.ToList();
                }}
            }}
        }}
    """
    
    promptTemplate = PromptTemplate.from_template(
        """
            Eres un generador de codigo c#. La salida que generes sera guardada en un archivo por lo que no debes generar ningun texto adicional ademas del codigo. No agregues ningun caracter adicional o el compilador C# fallara
            
            Tomando en cuenta la siguiente entidad 

            {entidades}

            Genera un archivo que contenga el codigo de la clase para model llamado [NombreEntidad]Model.cs

            Que implemente la siguente interfaz

            {interfaz}
            
            Esto tomando como referencia la siguiente clase para que sigas el mismo estilo de codigo.

            {framgento_codigo}
                        
            En caso de tener propiedades referentes a otras clases, asegurate de poblarlas llamando los getAll de las entidades correspondientes.
        """
    )

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = promptTemplate | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke({"framgento_codigo": framgento_codigo, "entidades": entidades, "interfaz": interfaz})

    # Parsear la salida para convertirla en una instancia de CodeResponseResult
    return generate_code_response(model, clean_code_mll_generated(output.content))

def generate_controller_coms(documentation_interfaz: str) -> CodeResponseResult:
    
    model = ChatModelSingleton()

    framgento_codigo = """
        using FolderView.Dapper.Entidades;
        using FolderView.Dapper.Interfaces;
        using Microsoft.AspNetCore.Mvc;
        using Newtonsoft.Json;
        using System.Collections.Generic;
        using System.Threading.Tasks;

        namespace FolderView.Controllers
        {
            public class TipoProyectoController : Controller
            {
                private readonly ITipoProyectoRepository _TipoProyectoRepositorio;

                public TipoProyectoController(ITipoProyectoRepository TipoProyectoRepositorio)
                {
                    _TipoProyectoRepositorio = TipoProyectoRepositorio;
                }

                [HttpGet("")]
                public async Task<IActionResult> tipoproyecto()
                {
                    return View();
                }

                [HttpGet("api/tipoproyecto/{id}")]
                public async Task<IActionResult> GetTipoProyectoById(int id)
                {
                    var result = await _TipoProyectoRepositorio.GetTipoProyectoByIdAsync(id);
                    return Ok(result);
                }

                [HttpGet("api/tipoproyecto")]
                public async Task<IActionResult> GetAllTipoProyecto()
                {
                    var result = await _TipoProyectoRepositorio.GetAllTipoProyectoAsync();
                    return Ok(result);
                }
            }
        }
    """
    
    promptTemplate = PromptTemplate.from_template(
        """
            Eres un generador de codigo c#. La salida que generes sera guardada en un archivo por lo que no debes generar ningun texto adicional ademas del codigo. No agregues ningun caracter adicional o el compilador C# fallara
            
            Tomando en cuenta la siguiente documentacion de el archivo interfaz
            
            {documentation_interfaz} 
            

            Genera un archivo que contenga el codigo de la clase para controller llamado [NombreEntidad]Controller.cs donde NombreEntidad es el nombre del objeto con el que se esta trabajando

            
            Esto tomando como referencia la siguiente clase para que sigas el mismo estilo de codigo.

            {framgento_codigo}
                        
            Asegurate de implementar un endpoint para cada metodo y un metodo para llamar la vista index. 

            Como consideracion adicional por cada elemento result asegura de poblar sus propiedades usando los otros metodos creados
        """
    )

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = promptTemplate | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke({"framgento_codigo": framgento_codigo, "documentation_interfaz": documentation_interfaz})

    # Parsear la salida para convertirla en una instancia de CodeResponseResult
    return generate_code_response(model, clean_code_mll_generated(output.content))

def generate_views_coms(documentation_controller: str, documentacion_entidad:str) -> CodeResponseResult:
    
    model = ChatModelSingleton()

    fragmento_codigo = """
        @{
    ViewData["Title"] = "Tipo Proyecto";

}

<div class="content-wrapper">
    <section class="content-header">
        <h1>
            Tipo Proyecto
            <small>CRUD</small>
        </h1>
    </section>

    <section class="content">
        <div class="box">
            <div class="box-header with-border">
                <h3 class="box-title">Lista de Tipo Proyectos</h3>
                <button id="btnAdd" class="btn btn-primary pull-right">Agregar Tipo Proyecto</button>
            </div>
            <div class="box-body">
                <table id="tipoProyectoTable" class="table table-bordered table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                    </tbody>
                </table>
            </div>
        </div>
    </section>
</div>

<!-- Modal para agregar/editar Tipo Proyecto -->
<div class="modal fade" id="tipoProyectoModal" tabindex="-1" role="dialog" aria-labelledby="tipoProyectoModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="tipoProyectoModalLabel">Agregar Tipo Proyecto</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <form id="tipoProyectoForm">
                    <input type="hidden" id="tipoProyectoId" />
                    <div class="form-group">
                        <label for="nombre">Nombre</label>
                        <input type="text" class="form-control" id="nombre" placeholder="Ingrese el nombre" required />
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>
                <button type="button" id="btnSave" class="btn btn-primary">Guardar</button>
            </div>
        </div>
    </div>
</div>


    <script>
            $(document).ready(function () {
                loadTipoProyectos();

                $('#btnAdd').click(function () {
                    $('#tipoProyectoModalLabel').text('Agregar Tipo Proyecto');
                    $('#tipoProyectoForm')[0].reset();
                    $('#tipoProyectoId').val('');
                    $('#tipoProyectoModal').modal('show');

            });

            $('#btnSave').click(function () {
                    const id = $('#tipoProyectoId').val();
                    const nombre = $('#nombre').val();
                    const url = id ? `/api/tipoproyecto` : `/api/tipoproyecto`;
                    const method = id ? 'PUT' : 'POST';

                    $.ajax({
                        url: url,
                        type: method,
                        contentType: 'application/json',
                        data: JSON.stringify({ id: id, nombre: nombre }),
                    success: function (result) {
                            $('#tipoProyectoModal').modal('hide');
                            loadTipoProyectos();

                    },
                    error: function (err) {
                            console.error(err);

                    }
                });
            });
        });

        function loadTipoProyectos() {
                $.ajax({
                    url: '/api/tipoproyectos',
                    type: 'GET',
                    success: function (data) {
                        const tableBody = $('#tipoProyectoTable tbody');
                        tableBody.empty();
                        data.forEach(function (tipoProyecto) {
                            tableBody.append(`
                                <tr>
                                    <td>${tipoProyecto.id}</td>
                                    <td>${tipoProyecto.nombre}</td>
                                    <td>
                                        <button class="btn btn-warning btnEdit" data-id="${tipoProyecto.id}">Editar</button>
                                        <button class="btn btn-danger btnDelete" data-id="${tipoProyecto.id}">Eliminar</button>
                                    </td>
                                </tr>
                            `);
                    });

                    $('.btnEdit').click(function () {
                            const id = $(this).data('id');
                            editTipoProyecto(id);

                    });

                    $('.btnDelete').click(function () {
                            const id = $(this).data('id');
                            deleteTipoProyecto(id);

                    });
                }
            });
        }

        function editTipoProyecto(id) {
                $.ajax({
                    url: `/api/tipoproyecto/${id}`,
                    type: 'GET',
                    success: function (data) {
                        $('#tipoProyectoModalLabel').text('Editar Tipo Proyecto');
                        $('#tipoProyectoId').val(data.id);
                        $('#nombre').val(data.nombre);
                        $('#tipoProyectoModal').modal('show');

                }
            });
        }

        function deleteTipoProyecto(id) {
                if (confirm('¿Está seguro de que desea eliminar este tipo de proyecto?')) {
                    $.ajax({
                        url: `/api/tipoproyecto/${id}`,
                        type: 'DELETE',
                        success: function () {
                            loadTipoProyectos();

                    },
                    error: function (err) {
                            console.error(err);

                    }
                });
            }
        }
    </script>

    """

    promptTemplate = PromptTemplate.from_template(
        """
            Eres un generador de cshtml. La salida que generes sera guardada en un archivo por lo que no debes generar ningun texto adicional ademas del codigo. No agregues ningun caracter adicional o el compilador C# fallara
            
            Tomando en cuenta la siguiente documentacion del siguiente archivo controller
            
            {documentation_controller} 

            Tomando en cuenta que estoy usando el template adminlte 2.

            Genera las views necesarias para crear un crud de la entidades. Para funcionar debe llamar a travez de ajax las funciones del controller

            Con sidera que estos son las entidades

            {documentacion_entidad}

            Sigue el siguiente fragmento de codigo como ejemplo.

            {fragmento_codigo}

            Pero ademas agrega validacion y decora los inputs con un error y mensaje al no cumplirse las validaciones.

        """
    )

    # Combinar el prompt con el modelo de lenguaje
    prompt_and_model = promptTemplate | model

    # Ejecutar el modelo con la consulta y obtener la salida
    output = prompt_and_model.invoke({"documentation_controller": documentation_controller, "fragmento_codigo": fragmento_codigo, "documentacion_entidad": documentacion_entidad})

    # Parsear la salida para convertirla en una instancia de CodeResponseResult
    return generate_code_response(model, clean_code_mll_generated(output.content))


# def generate_all_code_coms(script_table: str) -> [] :

#     model = ChatOpenAI(model="gpt-4o-mini")

#     result_entidad = generate_entidad_coms(model,script_table)
#     result_sps = generate_sps(model,script_table)

#     documentation = result_entidad.documentation + result_sps.documentation

#     result_model = generate_model_coms(model, documentation)

#     responses = [ result_entidad, result_sps, result_model ]

#     return responses

# if __name__ == '__main__':
#     model =ChatOpenAI(model="gpt-4o-mini")

#     script_table = """
#         USE [catalogos]
#         GO

#         CREATE TABLE [dbo].[prtgDevices](
#             [idPrtg] [int] NULL,
#             [idObj] [int] NULL,
#             [device] [varchar](50) NULL,
#             [host] [varchar](50) NULL,
#             [tags] [varchar](50) NULL
#         ) ON [PRIMARY]
#         GO
#     """

#     result_entidad = generate_entidad_coms(model,script_table)
#     result_sps = generate_sps(model,script_table)

#     documentation = result_entidad.documentation + result_sps.documentation

#     result_model = generate_model_coms(model, documentation)
#     print(result_model)
    

    