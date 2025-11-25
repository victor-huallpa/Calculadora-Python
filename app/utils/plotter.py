"""
Plot Utilities
Utilidades para generar gráficas de funciones
"""

import matplotlib
matplotlib.use('Agg')  # Backend no interactivo
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import os
from datetime import datetime

from app.config import config
from app.utils.parser import parse_function


# Configurar matplotlib
plt.style.use(config.MATPLOTLIB_STYLE)
matplotlib.rcParams['figure.figsize'] = config.FIGURE_SIZE
matplotlib.rcParams['font.size'] = config.FONT_SIZE


def plot_function(func_str, lower_limit=None, upper_limit=None):
    """
    Genera una gráfica de la función y opcionalmente el área bajo la curva
    
    Args:
        func_str (str): Representación en string de la función
        lower_limit (float, optional): Límite inferior para sombrear área
        upper_limit (float, optional): Límite superior para sombrear área
        
    Returns:
        str: Nombre del archivo de la gráfica generada
        None: Si ocurre un error
    """
    try:
        x = sp.Symbol('x')
        expr = parse_function(func_str)
        
        # Convertir a función numpy
        f = sp.lambdify(x, expr, 'numpy')
        
        # Determinar rango de la gráfica
        x_min, x_max = _determine_plot_range(lower_limit, upper_limit)
        
        # Generar valores de x
        x_vals = np.linspace(x_min, x_max, config.MAX_PLOT_POINTS)
        
        # Calcular valores de y, manejando errores potenciales
        x_vals, y_vals = _calculate_y_values(f, x_vals)
        
        if x_vals is None or y_vals is None:
            return None
        
        # Crear gráfica
        fig, ax = plt.subplots(figsize=config.FIGURE_SIZE)
        
        # Graficar la función
        ax.plot(x_vals, y_vals, 'b-', linewidth=2, label=f'$f(x) = {sp.latex(expr)}$')
        
        # Si es integral definida, sombrear el área
        if lower_limit is not None and upper_limit is not None:
            _shade_area(ax, f, float(lower_limit), float(upper_limit))
        
        # Agregar grid y etiquetas
        _configure_plot(ax)
        
        # Guardar gráfica
        filename = _save_plot(fig)
        
        return filename
        
    except Exception as e:
        print(f"Error plotting: {str(e)}")
        return None


def _determine_plot_range(lower_limit, upper_limit):
    """Determina el rango de la gráfica"""
    if lower_limit is not None and upper_limit is not None:
        lower = float(lower_limit)
        upper = float(upper_limit)
        margin = (upper - lower) * config.PLOT_MARGIN_PERCENT
        return lower - margin, upper + margin
    else:
        return config.DEFAULT_PLOT_RANGE


def _calculate_y_values(f, x_vals):
    """Calcula valores de y filtrando valores inválidos"""
    try:
        y_vals = f(x_vals)
        # Filtrar valores no finitos
        mask = np.isfinite(y_vals)
        return x_vals[mask], y_vals[mask]
    except:
        return None, None


def _shade_area(ax, f, lower, upper):
    """Sombrea el área bajo la curva"""
    try:
        # Generar puntos para sombreado
        x_fill = np.linspace(lower, upper, 500)
        y_fill = f(x_fill)
        
        # Filtrar puntos válidos
        mask_fill = np.isfinite(y_fill)
        x_fill = x_fill[mask_fill]
        y_fill = y_fill[mask_fill]
        
        # Sombrear área
        ax.fill_between(x_fill, 0, y_fill, alpha=0.3, color='cyan',
                       label=f'Área bajo la curva [{lower}, {upper}]')
        
        # Agregar líneas verticales en los límites
        ax.axvline(x=lower, color='r', linestyle='--', alpha=0.5)
        ax.axvline(x=upper, color='r', linestyle='--', alpha=0.5)
    except Exception as e:
        print(f"Error shading area: {str(e)}")


def _configure_plot(ax):
    """Configura la apariencia de la gráfica"""
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='k', linewidth=0.5)
    ax.axvline(x=0, color='k', linewidth=0.5)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.set_title('Gráfica de la Función', fontsize=14, fontweight='bold')
    ax.legend(loc='best')


def _save_plot(fig):
    """Guarda la gráfica y retorna el nombre del archivo"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    filename = f'plot_{timestamp}.png'
    filepath = os.path.join(config.PLOTS_DIR, filename)
    
    plt.tight_layout()
    plt.savefig(filepath, dpi=config.FIGURE_DPI, bbox_inches='tight')
    plt.close()
    
    return filename
