from flask import Flask, jsonify, request
from langchain_openai import ChatOpenAI

from services.coms_codeGenerator import generate_all_code_coms, generate_entidad_coms, generate_model_coms, generate_sps

app = Flask(__name__)

@app.route('/coms/getAll', methods=['POST'])
def get_all_code_coms():
    data = request.json
    script_table = data.get('script_table')

    responses = generate_all_code_coms(script_table)

    # Convertir la lista de instancias a una lista de diccionarios
    responses_dict = [response.dict() for response in responses]
    
    # Devolver la lista de diccionarios como JSON
    return jsonify(responses_dict)

if __name__ == '__main__':
    app.run(debug=True)



# from langchain_openai import ChatOpenAI
# from code_generator import generate_entidad_coms, generate_model_coms, generate_sps
# from flask import Blueprint, jsonify, request
# from models import db, FolderViewArchivos

# api_blueprint = Blueprint('api', __name__)

# @api_blueprint.route('/ConsolaMonitoreo/SPS', methods=['GET'])
# def get_sps():
#     model = ChatOpenAI(model="gpt-4o-mini")

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
#     return jsonify(result_model.to_dict())


# @api_blueprint.route('/archivos', methods=['GET'])
# def get_archivos():
#     archivos = FolderViewArchivos.query.all()
#     return jsonify([archivo.to_dict() for archivo in archivos])

# @api_blueprint.route('/archivo/<int:id>', methods=['GET'])
# def get_archivo(id):
#     archivo = FolderViewArchivos.query.get(id)
#     if archivo is None:
#         return jsonify({'error': 'Archivo no encontrado'}), 404
#     return jsonify(archivo.to_dict())

# @api_blueprint.route('/archivo', methods=['POST'])
# def create_archivo():
#     data = request.json
#     archivo = FolderViewArchivos(**data)
#     db.session.add(archivo)
#     db.session.commit()
#     return jsonify(archivo.to_dict()), 201

# @api_blueprint.route('/archivo/<int:id>', methods=['PUT'])
# def update_archivo(id):
#     archivo = FolderViewArchivos.query.get(id)
#     if archivo is None:
#         return jsonify({'error': 'Archivo no encontrado'}), 404

#     data = request.json
#     for key, value in data.items():
#         setattr(archivo, key, value)
#     db.session.commit()
#     return jsonify(archivo.to_dict())

# @api_blueprint.route('/archivo/<int:id>', methods=['DELETE'])
# def delete_archivo(id):
#     archivo = FolderViewArchivos.query.get(id)
#     if archivo is None:
#         return jsonify({'error': 'Archivo no encontrado'}), 404

#     db.session.delete(archivo)
#     db.session.commit()
#     return jsonify({'message': 'Archivo eliminado'}), 200
