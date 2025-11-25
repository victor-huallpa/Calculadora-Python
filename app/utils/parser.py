"""
Parser Utilities
Utilidades para parsear expresiones matemáticas
"""

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application


def parse_function(func_str):
    """
    Parsea una función matemática desde string a expresión SymPy
    
    Args:
        func_str (str): Representación en string de la función
        
    Returns:
        sp.Expr: Expresión de SymPy
        
    Raises:
        ValueError: Si la función no puede ser parseada
    """
    try:
        # Definir transformaciones para el parsing
        transformations = standard_transformations + (implicit_multiplication_application,)
        
        # Reemplazar patrones comunes
        func_str = func_str.replace('^', '**')
        func_str = func_str.replace('sen', 'sin')  # Español a inglés
        func_str = func_str.replace('tg', 'tan')
        
        # Parsear la expresión
        expr = parse_expr(func_str, transformations=transformations)
        return expr
        
    except Exception as e:
        raise ValueError(f"Error al parsear la función: {str(e)}")
