"""
Integration Service
Servicio para cálculo de integrales y generación de procedimientos
"""

import sympy as sp
from app.utils.parser import parse_function


def calculate_integral(func_str, lower_limit=None, upper_limit=None):
    """
    Calcula la integral de una función
    
    Args:
        func_str (str): Representación en string de la función
        lower_limit (str, optional): Límite inferior para integral definida
        upper_limit (str, optional): Límite superior para integral definida
        
    Returns:
        dict: Diccionario con los resultados
    """
    try:
        # Parsear la función
        x = sp.Symbol('x')
        expr = parse_function(func_str)
        
        # Calcular integral indefinida
        indefinite_integral = sp.integrate(expr, x)
        
        result = {
            'success': True,
            'original_function': sp.latex(expr),
            'indefinite_integral': sp.latex(indefinite_integral),
            'indefinite_integral_text': str(indefinite_integral),
        }
        
        # Si se proporcionan límites, calcular integral definida
        if lower_limit is not None and upper_limit is not None:
            definite_result = _calculate_definite_integral(
                expr, x, lower_limit, upper_limit
            )
            result.update(definite_result)
        else:
            result['is_definite'] = False
        
        # Generar procedimiento detallado
        result['procedure'] = generate_integration_procedure(expr, x, indefinite_integral)
        
        return result
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def _calculate_definite_integral(expr, x, lower_limit, upper_limit):
    """Calcula la integral definida"""
    try:
        lower = float(lower_limit)
        upper = float(upper_limit)
        
        # Calcular integral definida
        definite_result = sp.integrate(expr, (x, lower, upper))
        
        # Intentar obtener valor numérico
        try:
            numerical_value = float(definite_result.evalf())
            return {
                'definite_integral': numerical_value,
                'definite_integral_latex': sp.latex(definite_result),
                'limits': {'lower': lower, 'upper': upper},
                'is_definite': True
            }
        except:
            return {
                'definite_integral': str(definite_result),
                'definite_integral_latex': sp.latex(definite_result),
                'limits': {'lower': lower, 'upper': upper},
                'is_definite': True
            }
            
    except Exception as e:
        return {
            'limit_error': f"Error al calcular integral definida: {str(e)}",
            'is_definite': False
        }


def generate_integration_procedure(expr, x, result):
    """
    Genera un procedimiento detallado paso a paso para la integración
    
    Args:
        expr: Expresión original a integrar
        x: Variable de integración
        result: Resultado final de la integración
        
    Returns:
        list: Lista de diccionarios con los pasos
    """
    steps = []
    step_num = 1
    
    try:
        # Paso 1: Mostrar la integral original
        steps.append({
            'step': step_num,
            'description': '📋 Integral a resolver',
            'latex': f'\\int {sp.latex(expr)} \\, dx'
        })
        step_num += 1
        
        # Paso 2: Identificar el tipo de función y regla
        rule_info = identify_integration_rule(expr, x)
        if rule_info:
            steps.append({
                'step': step_num,
                'description': f'📚 Regla a aplicar: {rule_info["rule"]}',
                'explanation': rule_info.get('explanation', '')
            })
            step_num += 1
        
        # Paso 3: Expandir y separar términos si es una suma
        expanded = sp.expand(expr)
        if expanded != expr and expanded.is_Add:
            steps.append({
                'step': step_num,
                'description': '🔄 Expandir la expresión',
                'latex': f'\\int {sp.latex(expanded)} \\, dx'
            })
            step_num += 1
        
        # Paso 4: Separar suma en integrales individuales (linealidad)
        if expanded.is_Add:
            terms = expanded.as_ordered_terms()
            if len(terms) > 1:
                integral_terms = ' + '.join([f'\\int {sp.latex(term)} \\, dx' for term in terms])
                steps.append({
                    'step': step_num,
                    'description': '➕ Aplicar linealidad de la integral (separar suma)',
                    'explanation': '∫(f + g) dx = ∫f dx + ∫g dx',
                    'latex': integral_terms
                })
                step_num += 1
                
                # Paso 5: Integrar cada término individualmente
                for i, term in enumerate(terms, 1):
                    term_integral = sp.integrate(term, x)
                    term_steps = get_term_integration_steps(term, x, term_integral, i)
                    for term_step in term_steps:
                        term_step['step'] = step_num
                        steps.append(term_step)
                        step_num += 1
                
                # Combinar todos los términos integrados
                steps.append({
                    'step': step_num,
                    'description': '🔗 Combinar todos los términos integrados',
                    'latex': sp.latex(result)
                })
                step_num += 1
        else:
            # Integración de un solo término con pasos detallados
            single_steps = get_term_integration_steps(expanded, x, result, 1)
            for single_step in single_steps:
                single_step['step'] = step_num
                steps.append(single_step)
                step_num += 1
        
        # Paso de simplificación si es necesario
        simplified = sp.simplify(result)
        if simplified != result:
            steps.append({
                'step': step_num,
                'description': '✨ Simplificar el resultado',
                'latex': sp.latex(simplified)
            })
            step_num += 1
        
        # Resultado final con constante
        steps.append({
            'step': step_num,
            'description': '🎯 Resultado final (agregar constante de integración)',
            'latex': f'{sp.latex(result)} + C'
        })
        step_num += 1
        
        # Paso de verificación
        derivative = sp.diff(result, x)
        derivative_simplified = sp.simplify(derivative)
        expr_simplified = sp.simplify(expr)
        
        if sp.simplify(derivative_simplified - expr_simplified) == 0:
            steps.append({
                'step': step_num,
                'description': '✅ Verificación (derivar para comprobar)',
                'explanation': 'Si derivamos el resultado, debemos obtener la función original',
                'latex': f'\\frac{{d}}{{dx}}\\left({sp.latex(result)}\\right) = {sp.latex(derivative_simplified)}',
                'verification': True
            })
    
    except Exception as e:
        # Si falla la generación del procedimiento, retornar pasos básicos
        steps = [{
            'step': 1,
            'description': 'Integral calculada',
            'latex': f'\\int {sp.latex(expr)} \\, dx = {sp.latex(result)} + C'
        }]
    
    return steps


def get_term_integration_steps(term, x, term_result, term_number):
    """
    Obtiene pasos detallados de integración para un solo término
    
    Args:
        term: El término a integrar
        x: Variable de integración
        term_result: El resultado de la integración para este término
        term_number: Número de este término en la suma
        
    Returns:
        list: Lista de diccionarios de pasos
    """
    steps = []
    
    try:
        # Identificar qué tipo de término es
        if term.is_constant():
            # Término constante
            steps.append({
                'description': f'📌 Término {term_number}: Integrar constante {sp.latex(term)}',
                'explanation': '∫k dx = kx',
                'latex': f'\\int {sp.latex(term)} \\, dx = {sp.latex(term_result)}'
            })
        
        elif term.is_Mul:
            # Producto: separar coeficiente de parte variable
            coeff, var_part = term.as_coeff_Mul()
            
            if coeff != 1:
                steps.append({
                    'description': f'📌 Término {term_number}: Sacar constante {sp.latex(coeff)}',
                    'explanation': '∫k·f(x) dx = k·∫f(x) dx',
                    'latex': f'{sp.latex(coeff)} \\int {sp.latex(var_part)} \\, dx'
                })
            
            # Verificar si es una potencia de x
            if var_part.is_Pow and var_part.base == x:
                n = var_part.exp
                steps.append({
                    'description': f'📌 Término {term_number}: Aplicar regla de la potencia a {sp.latex(var_part)}',
                    'explanation': f'∫x^{sp.latex(n)} dx = x^{sp.latex(n+1)}/{sp.latex(n+1)}',
                    'latex': f'{sp.latex(coeff)} \\cdot \\frac{{x^{{{sp.latex(n+1)}}}}}{{{sp.latex(n+1)}}} = {sp.latex(term_result)}'
                })
            elif var_part == x:
                steps.append({
                    'description': f'📌 Término {term_number}: Aplicar regla de la potencia a x',
                    'explanation': '∫x dx = x²/2',
                    'latex': f'{sp.latex(coeff)} \\cdot \\frac{{x^2}}{{2}} = {sp.latex(term_result)}'
                })
            else:
                # Otros casos de multiplicación
                steps.append({
                    'description': f'📌 Término {term_number}: Integrar {sp.latex(term)}',
                    'latex': f'\\int {sp.latex(term)} \\, dx = {sp.latex(term_result)}'
                })
        
        elif term.is_Pow and term.base == x:
            # Potencia pura de x
            n = term.exp
            steps.append({
                'description': f'📌 Término {term_number}: Aplicar regla de la potencia',
                'explanation': f'∫x^{sp.latex(n)} dx = x^{sp.latex(n+1)}/{sp.latex(n+1)}',
                'latex': f'\\frac{{x^{{{sp.latex(n+1)}}}}}{{{sp.latex(n+1)}}} = {sp.latex(term_result)}'
            })
        
        elif term == x:
            # Solo x
            steps.append({
                'description': f'📌 Término {term_number}: Integrar x',
                'explanation': '∫x dx = x²/2',
                'latex': f'\\frac{{x^2}}{{2}} = {sp.latex(term_result)}'
            })
        
        elif term.has(sp.sin):
            steps.append({
                'description': f'📌 Término {term_number}: Integrar seno',
                'explanation': '∫sin(x) dx = -cos(x)',
                'latex': f'\\int {sp.latex(term)} \\, dx = {sp.latex(term_result)}'
            })
        
        elif term.has(sp.cos):
            steps.append({
                'description': f'📌 Término {term_number}: Integrar coseno',
                'explanation': '∫cos(x) dx = sin(x)',
                'latex': f'\\int {sp.latex(term)} \\, dx = {sp.latex(term_result)}'
            })
        
        elif term.has(sp.exp):
            steps.append({
                'description': f'📌 Término {term_number}: Integrar exponencial',
                'explanation': '∫e^x dx = e^x',
                'latex': f'\\int {sp.latex(term)} \\, dx = {sp.latex(term_result)}'
            })
        
        else:
            # Caso genérico
            steps.append({
                'description': f'📌 Término {term_number}: Integrar {sp.latex(term)}',
                'latex': f'\\int {sp.latex(term)} \\, dx = {sp.latex(term_result)}'
            })
    
    except Exception as e:
        # Fallback para cualquier error
        steps.append({
            'description': f'📌 Término {term_number}: Integrar',
            'latex': f'\\int {sp.latex(term)} \\, dx = {sp.latex(term_result)}'
        })
    
    return steps


def identify_integration_rule(expr, x):
    """
    Identifica qué regla de integración aplica a la expresión
    
    Args:
        expr: Expresión a analizar
        x: Variable de integración
        
    Returns:
        dict: Diccionario con nombre de regla y explicación
    """
    try:
        # Verificar polinomios básicos
        if expr.is_polynomial(x):
            degree = sp.degree(expr, x)
            if degree == 0:
                return {
                    'rule': 'Integral de una constante',
                    'explanation': '∫k dx = kx + C'
                }
            elif degree == 1:
                return {
                    'rule': 'Integral de función lineal',
                    'explanation': '∫(ax + b) dx = (a/2)x² + bx + C'
                }
            else:
                return {
                    'rule': 'Regla de la potencia',
                    'explanation': '∫xⁿ dx = xⁿ⁺¹/(n+1) + C'
                }
        
        # Verificar funciones trigonométricas
        if expr.has(sp.sin):
            return {
                'rule': 'Integral de seno',
                'explanation': '∫sin(x) dx = -cos(x) + C'
            }
        elif expr.has(sp.cos):
            return {
                'rule': 'Integral de coseno',
                'explanation': '∫cos(x) dx = sin(x) + C'
            }
        elif expr.has(sp.tan):
            return {
                'rule': 'Integral de tangente',
                'explanation': '∫tan(x) dx = -ln|cos(x)| + C'
            }
        
        # Verificar exponencial
        if expr.has(sp.exp):
            return {
                'rule': 'Integral exponencial',
                'explanation': '∫eˣ dx = eˣ + C'
            }
        
        # Verificar logaritmo
        if expr.has(sp.log):
            return {
                'rule': 'Integración por partes',
                'explanation': '∫ln(x) dx = x·ln(x) - x + C'
            }
        
        # Verificar función racional
        if expr.is_rational_function(x):
            return {
                'rule': 'Integral de función racional',
                'explanation': 'Puede requerir fracciones parciales'
            }
        
        # Verificar producto (integración por partes)
        if expr.is_Mul and len(expr.args) >= 2:
            return {
                'rule': 'Integración por partes',
                'explanation': '∫u dv = uv - ∫v du'
            }
        
        return {
            'rule': 'Regla general de integración',
            'explanation': 'Se aplican técnicas estándar de integración'
        }
        
    except:
        return None
