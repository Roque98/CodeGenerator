from flask import Flask, jsonify, request
from langchain_openai import ChatOpenAI

from services.IA_Response_Generator import generate_code_result
from services.coms_codeGenerator import generate_controller_coms, generate_entidad_coms, generate_interfaz_coms, generate_model_coms, generate_sps, generate_views_coms

app = Flask(__name__)


@app.route('/generate/code', methods=['POST'])
def generate_code_response_route():
    data = request.json
    promptTemplate = data.get('promptTemplate')
    params = data.get('params', {})  # Recibir los parámetros como un diccionario, con un valor por defecto vacío

    # Validar que el prompt haya sido proporcionado
    if not promptTemplate:
        return jsonify({"error": "Prompt is required"}), 400

    # Ejecutar la función para generar el resultado
    try:
        result = generate_code_result(promptTemplate, params)
        
        # Convertir el resultado a diccionario si es necesario
        response_dict = result.dict() if hasattr(result, 'dict') else result

        # Devolver el resultado como JSON
        return jsonify(response_dict), 200
    except Exception as e:
        # Manejar cualquier error durante la ejecución
        return jsonify({"error": str(e)}), 500


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


