from flask import Flask, jsonify, request
from langchain_openai import ChatOpenAI

from services.coms_codeGenerator import generate_controller_coms, generate_entidad_coms, generate_interfaz_coms, generate_model_coms, generate_sps, generate_views_coms

app = Flask(__name__)

# @app.route('/coms/getAll', methods=['POST'])
# def get_all_code_coms():
#     data = request.json
#     script_table = data.get('script_table')

#     responses = generate_all_code_coms(script_table)

#     # Convertir la lista de instancias a una lista de diccionarios
#     responses_dict = [response.dict() for response in responses]
    
#     # Devolver la lista de diccionarios como JSON
#     return jsonify(responses_dict)

@app.route('/coms/getEntities', methods=['POST'])
def get_all_entities_coms():
    data = request.json
    script_table = data.get('script_table')

    result_entidad = generate_entidad_coms(script_table)\
    
    responses = [result_entidad]

    # Convertir la lista de instancias a una lista de diccionarios
    responses_dict = [response.dict() for response in responses]
    
    # Devolver la lista de diccionarios como JSON
    return jsonify(responses_dict)

@app.route('/coms/getAllInterfaz', methods=['POST'])
def get_all_interface_coms():
    data = request.json
    entidades = data.get('entidades')

    result_entidad = generate_interfaz_coms(entidades)
    
    responses = [result_entidad]

    # Convertir la lista de instancias a una lista de diccionarios
    responses_dict = [response.dict() for response in responses]
    
    # Devolver la lista de diccionarios como JSON
    return jsonify(responses_dict)

@app.route('/coms/getAllModel', methods=['POST'])
def get_all_models_coms():
    data = request.json
    documentation_sps = data.get('documentation_sps')
    entidades = data.get('entidades')
    interfaz = data.get('interfaz')

    result_entidad = generate_model_coms(documentation_sps, entidades, interfaz)
    
    responses = [result_entidad]

    # Convertir la lista de instancias a una lista de diccionarios
    responses_dict = [response.dict() for response in responses]
    
    # Devolver la lista de diccionarios como JSON
    return jsonify(responses_dict)

@app.route('/coms/getAllController', methods=['POST'])
def get_all_controller_coms():
    data = request.json
    documentation_interfaz = data.get('documentation_interfaz')


    result_entidad = generate_controller_coms(documentation_interfaz)
    
    responses = [result_entidad]

    # Convertir la lista de instancias a una lista de diccionarios
    responses_dict = [response.dict() for response in responses]
    
    # Devolver la lista de diccionarios como JSON
    return jsonify(responses_dict)

@app.route('/coms/getAllViews', methods=['POST'])
def get_all_views_coms():
    data = request.json
    documentation_controller = data.get('documentation_controller')
    entidades = data.get('entidades')

    result_entidad = generate_views_coms(documentation_controller, entidades)
    
    responses = [result_entidad]

    # Convertir la lista de instancias a una lista de diccionarios
    responses_dict = [response.dict() for response in responses]
    
    # Devolver la lista de diccionarios como JSON
    return jsonify(responses_dict)

if __name__ == '__main__':
    app.run(debug=True)


