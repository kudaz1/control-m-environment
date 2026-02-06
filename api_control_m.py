from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
import logging

app = Flask(__name__)
CORS(app)  # Permitir CORS para que Jira pueda llamar a la API

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def replace_environment(json_data, target_environment):
    """
    Reemplaza todas las referencias de ambiente en el JSON manteniendo el orden original.
    
    Args:
        json_data: String JSON o diccionario con la configuración
        target_environment: El ambiente objetivo (Q5, Q7, Q8)
    
    Returns:
        JSON modificado con el ambiente correcto manteniendo el orden original
    """
    # Convertir a string si es necesario
    if isinstance(json_data, dict):
        # Usar sort_keys=False para mantener el orden original
        json_str = json.dumps(json_data, indent=4, ensure_ascii=False, sort_keys=False)
    else:
        json_str = str(json_data)
    
    # Definir los ambientes
    environments = ['Q5A', 'Q7A', 'Q8A']
    target_env = target_environment.upper()
    
    # Asegurar que tiene la 'A' al final
    if not target_env.endswith('A'):
        target_env = target_env + 'A'
    
    logger.info(f"Reemplazando todos los ambientes por: {target_env}")
    
    # Reemplazar todos los otros ambientes por el objetivo
    for env in environments:
        if env != target_env:
            # Reemplazo case-sensitive
            json_str = json_str.replace(env, target_env)
            # También reemplazo sin la 'A' por si acaso
            json_str = json_str.replace(env[:-1], target_env[:-1])
    
    # Convertir de vuelta a diccionario manteniendo el orden usando OrderedDict
    try:
        import collections
        result = json.loads(json_str, object_pairs_hook=collections.OrderedDict)
        return result
    except json.JSONDecodeError as e:
        logger.error(f"Error al parsear JSON: {e}")
        return json_str


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que la API está funcionando"""
    return jsonify({
        'status': 'ok',
        'message': 'API Control-M está funcionando correctamente'
    }), 200


@app.route('/api/replace-environment', methods=['POST'])
def replace_environment_endpoint():
    """
    Endpoint principal para reemplazar el ambiente en el JSON.
    
    Espera un JSON con:
    {
        "environment": "Q5",  // El ambiente objetivo
        "json_data": {...}    // El JSON de Control-M a modificar
    }
    """
    try:
        # Obtener datos del request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No se recibieron datos'
            }), 400
        
        # Validar que vengan los campos requeridos
        if 'environment' not in data:
            return jsonify({
                'error': 'Falta el campo "environment"'
            }), 400
        
        if 'json_data' not in data:
            return jsonify({
                'error': 'Falta el campo "json_data"'
            }), 400
        
        environment = data['environment']
        json_data = data['json_data']
        
        # Validar que el ambiente sea válido (solo Q5, Q7, Q8)
        valid_environments = ['Q5', 'Q7', 'Q8']
        if environment.upper() not in valid_environments:
            return jsonify({
                'error': 'Ambiente inválido. Debe ser uno de: Q5, Q7, Q8'
            }), 400
        
        logger.info(f"Procesando request para ambiente: {environment}")
        
        # Realizar el reemplazo
        modified_json = replace_environment(json_data, environment)
        
        # Crear respuesta manteniendo el orden
        response_data = {
            'success': True,
            'environment': environment.upper() if not environment.upper().endswith('A') else environment.upper(),
            'modified_json': modified_json
        }
        
        # Usar json.dumps con sort_keys=False para mantener orden
        from flask import Response
        response_json = json.dumps(response_data, indent=2, ensure_ascii=False, sort_keys=False)
        return Response(response_json, mimetype='application/json'), 200
        
    except Exception as e:
        logger.error(f"Error procesando request: {str(e)}")
        return jsonify({
            'error': f'Error interno del servidor: {str(e)}'
        }), 500


@app.route('/api/replace-environment-from-jira', methods=['POST'])
def replace_environment_from_jira():
    """
    Endpoint optimizado para recibir datos directamente desde Jira Automation.
    
    Espera un JSON con la estructura que Jira envía:
    {
        "issue": {
            "fields": {
                "customfield_xxxxx": "Q5"  // Campo personalizado con el ambiente
            }
        },
        "json_data": {...}  // El JSON a modificar
    }
    
    O simplemente:
    {
        "environment": "Q5",
        "json_data": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
        
        # Intentar extraer el ambiente de diferentes formas
        environment = None
        
        # Opción 1: Campo directo
        if 'environment' in data:
            environment = data['environment']
        
        # Opción 2: Desde estructura de Jira
        elif 'issue' in data and 'fields' in data['issue']:
            fields = data['issue']['fields']
            # Buscar cualquier campo que contenga Q5, Q7 o Q8
            for key, value in fields.items():
                if isinstance(value, str) and value.upper() in ['Q5', 'Q7', 'Q8', 'Q5A', 'Q7A', 'Q8A']:
                    environment = value
                    break
        
        if not environment:
            return jsonify({'error': 'No se pudo extraer el ambiente del request'}), 400
        
        # Validar que el ambiente sea uno de los permitidos (solo Q5, Q7, Q8)
        valid_environments = ['Q5', 'Q7', 'Q8']
        if environment.upper() not in valid_environments:
            return jsonify({
                'error': 'Ambiente inválido. Debe ser uno de: Q5, Q7, Q8'
            }), 400
        
        # Obtener el JSON a modificar
        json_data = data.get('json_data')
        
        if not json_data:
            return jsonify({'error': 'Falta el campo "json_data"'}), 400
        
        logger.info(f"Request desde Jira - Ambiente: {environment}")
        
        # Realizar el reemplazo
        modified_json = replace_environment(json_data, environment)
        
        # Crear respuesta manteniendo el orden
        response_data = {
            'success': True,
            'environment': environment.upper(),
            'modified_json': modified_json,
            'message': f'JSON modificado exitosamente para ambiente {environment.upper()}'
        }
        
        # Usar json.dumps con sort_keys=False para mantener orden
        from flask import Response
        response_json = json.dumps(response_data, indent=2, ensure_ascii=False, sort_keys=False)
        return Response(response_json, mimetype='application/json'), 200
        
    except Exception as e:
        logger.error(f"Error procesando request desde Jira: {str(e)}")
        return jsonify({
            'error': f'Error: {str(e)}'
        }), 500


if __name__ == '__main__':
    # Ejecutar la API
    # En producción, usar un servidor WSGI como gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)


