"""
App Package
Inicialización de la aplicación Flask
"""

import os
from flask import Flask

from app.config import config
from app.routes import main_bp


def create_app(config_object=None):
    """
    Factory para crear la aplicación Flask
    
    Args:
        config_object: Objeto de configuración (opcional)
        
    Returns:
        Flask: Instancia de la aplicación
    """
    app = Flask(__name__,
                static_folder='../static',
                template_folder='../templates')
    
    # Cargar configuración
    if config_object is None:
        app.config.from_object(config)
    else:
        app.config.from_object(config_object)
    
    # Asegurar que el directorio de gráficas existe
    os.makedirs(config.PLOTS_DIR, exist_ok=True)
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    
    return app
