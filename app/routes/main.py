"""
Main Routes
Rutas principales de la aplicación
"""

from flask import Blueprint, render_template, request, jsonify, send_from_directory
import os

from app.config import config
from app.services.integration import calculate_integral
from app.utils.plotter import plot_function

# Crear blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Renderiza la página principal"""
    return render_template('index.html')


@main_bp.route('/calculate', methods=['POST'])
def calculate():
    """
    API endpoint para calcular integrales
    
    JSON esperado:
        {
            "function": "x^2",
            "lower_limit": "0" (opcional),
            "upper_limit": "1" (opcional)
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'function' not in data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó ninguna función'
            }), 400
        
        func_str = data['function'].strip()
        lower_limit = data.get('lower_limit', '').strip()
        upper_limit = data.get('upper_limit', '').strip()
        
        # Validar función
        if not func_str:
            return jsonify({
                'success': False,
                'error': 'La función no puede estar vacía'
            }), 400
        
        # Convertir límites a None si están vacíos
        lower = lower_limit if lower_limit else None
        upper = upper_limit if upper_limit else None
        
        # Validar límites
        if (lower is None) != (upper is None):
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar ambos límites o ninguno'
            }), 400
        
        # Calcular integral
        result = calculate_integral(func_str, lower, upper)
        
        if not result['success']:
            return jsonify(result), 400
        
        # Generar gráfica
        plot_filename = plot_function(func_str, lower, upper)
        if plot_filename:
            result['plot_url'] = f'/static/plots/{plot_filename}'
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error del servidor: {str(e)}'
        }), 500


@main_bp.route('/static/plots/<filename>')
def serve_plot(filename):
    """Sirve imágenes de gráficas"""
    return send_from_directory(config.PLOTS_DIR, filename)
