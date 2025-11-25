"""
Configuration Module
Configuración centralizada de la aplicación
"""

import os

class Config:
    """Configuración base de la aplicación"""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # Paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'
    PLOTS_DIR = os.path.join(STATIC_FOLDER, 'plots')
    
    # Matplotlib
    MATPLOTLIB_STYLE = 'seaborn-v0_8-darkgrid'
    FIGURE_SIZE = (10, 6)
    FIGURE_DPI = 100
    FONT_SIZE = 10
    
    # Integration
    MAX_PLOT_POINTS = 1000
    PLOT_MARGIN_PERCENT = 0.2
    DEFAULT_PLOT_RANGE = (-10, 10)


class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True


class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


# Configuración por defecto
config = DevelopmentConfig()
