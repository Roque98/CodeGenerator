from flask import Blueprint, jsonify, request
from models import db, FolderViewArchivos

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/archivos', methods=['GET'])
def get_archivos():
    archivos = FolderViewArchivos.query.all()
    return jsonify([archivo.to_dict() for archivo in archivos])

@api_blueprint.route('/archivo/<int:id>', methods=['GET'])
def get_archivo(id):
    archivo = FolderViewArchivos.query.get(id)
    if archivo is None:
        return jsonify({'error': 'Archivo no encontrado'}), 404
    return jsonify(archivo.to_dict())

@api_blueprint.route('/archivo', methods=['POST'])
def create_archivo():
    data = request.json
    archivo = FolderViewArchivos(**data)
    db.session.add(archivo)
    db.session.commit()
    return jsonify(archivo.to_dict()), 201

@api_blueprint.route('/archivo/<int:id>', methods=['PUT'])
def update_archivo(id):
    archivo = FolderViewArchivos.query.get(id)
    if archivo is None:
        return jsonify({'error': 'Archivo no encontrado'}), 404

    data = request.json
    for key, value in data.items():
        setattr(archivo, key, value)
    db.session.commit()
    return jsonify(archivo.to_dict())

@api_blueprint.route('/archivo/<int:id>', methods=['DELETE'])
def delete_archivo(id):
    archivo = FolderViewArchivos.query.get(id)
    if archivo is None:
        return jsonify({'error': 'Archivo no encontrado'}), 404

    db.session.delete(archivo)
    db.session.commit()
    return jsonify({'message': 'Archivo eliminado'}), 200
