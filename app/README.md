# 📁 Estructura Modular de Python Backend

## 🎯 Arquitectura de la Aplicación

La aplicación utiliza el **patrón Application Factory** de Flask con una estructura modular clara.

```
calculadora/
├── app.py                    # Punto de entrada principal
├── app/
│   ├── __init__.py          # Factory de la aplicación
│   ├── config.py            # Configuración centralizada
│   ├── routes/              # Rutas y endpoints
│   │   ├── __init__.py
│   │   └── main.py          # Rutas principales
│   ├── services/            # Lógica de negocio
│   │   ├── __init__.py
│   │   └── integration.py   # Servicio de integración
│   └── utils/               # Utilidades
│       ├── __init__.py
│       ├── parser.py        # Parser de expresiones
│       └── plotter.py       # Generador de gráficas
├── static/                  # Archivos estáticos
├── templates/               # Templates HTML
└── requirements.txt         # Dependencias
```

## 📋 Descripción de Módulos

### 1. **app.py** - Punto de Entrada
**Responsabilidad**: Iniciar la aplicación

**Contenido**:
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Características**:
- Importa la factory
- Crea instancia de la app
- Ejecuta el servidor

---

### 2. **app/__init__.py** - Application Factory
**Responsabilidad**: Crear y configurar la aplicación Flask

**Función principal**:
```python
def create_app(config_object=None):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Crear directorios necesarios
    os.makedirs(config.PLOTS_DIR, exist_ok=True)
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    
    return app
```

**Ventajas del patrón Factory**:
- Facilita testing con diferentes configuraciones
- Permite múltiples instancias de la app
- Configuración centralizada
- Mejor organización del código

---

### 3. **app/config.py** - Configuración
**Responsabilidad**: Centralizar toda la configuración

**Clases**:
- `Config`: Configuración base
- `DevelopmentConfig`: Configuración de desarrollo
- `ProductionConfig`: Configuración de producción

**Configuraciones**:
```python
class Config:
    # Flask
    SECRET_KEY = 'dev-secret-key'
    DEBUG = True
    
    # Paths
    PLOTS_DIR = 'static/plots'
    
    # Matplotlib
    MATPLOTLIB_STYLE = 'seaborn-v0_8-darkgrid'
    FIGURE_SIZE = (10, 6)
    FIGURE_DPI = 100
    
    # Integration
    MAX_PLOT_POINTS = 1000
    PLOT_MARGIN_PERCENT = 0.2
```

**Uso**:
```python
from app.config import config
print(config.PLOTS_DIR)
```

---

### 4. **app/routes/** - Rutas y Endpoints

#### **app/routes/main.py**
**Responsabilidad**: Definir rutas HTTP

**Blueprint**:
```python
main_bp = Blueprint('main', __name__)
```

**Rutas**:
- `GET /`: Página principal
- `POST /calculate`: Calcular integral
- `GET /static/plots/<filename>`: Servir gráficas

**Ejemplo de ruta**:
```python
@main_bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    result = calculate_integral(data['function'])
    return jsonify(result)
```

**Ventajas de Blueprints**:
- Organización modular de rutas
- Fácil de escalar
- Reutilizable en otras apps
- Prefijos de URL opcionales

---

### 5. **app/services/** - Lógica de Negocio

#### **app/services/integration.py**
**Responsabilidad**: Cálculo de integrales y generación de procedimientos

**Funciones principales**:

##### `calculate_integral(func_str, lower_limit, upper_limit)`
Calcula integral indefinida y definida (si aplica)

```python
result = {
    'success': True,
    'original_function': latex(expr),
    'indefinite_integral': latex(result),
    'procedure': [...],
    'is_definite': False
}
```

##### `generate_integration_procedure(expr, x, result)`
Genera pasos detallados del procedimiento

```python
steps = [
    {'step': 1, 'description': '...', 'latex': '...'},
    {'step': 2, 'description': '...', 'explanation': '...'},
    ...
]
```

##### `get_term_integration_steps(term, x, result, number)`
Pasos para integrar un término individual

##### `identify_integration_rule(expr, x)`
Identifica qué regla de integración aplicar

**Reglas identificadas**:
- Constantes
- Polinomios (regla de la potencia)
- Trigonométricas (sin, cos, tan)
- Exponenciales
- Logaritmos
- Funciones racionales
- Productos (integración por partes)

---

### 6. **app/utils/** - Utilidades

#### **app/utils/parser.py**
**Responsabilidad**: Parsear expresiones matemáticas

**Función**:
```python
def parse_function(func_str):
    """Convierte string a expresión SymPy"""
    # Transformaciones
    func_str = func_str.replace('^', '**')
    func_str = func_str.replace('sen', 'sin')
    
    # Parsear
    expr = parse_expr(func_str, transformations=...)
    return expr
```

**Transformaciones**:
- `^` → `**` (potencia)
- `sen` → `sin` (español a inglés)
- `tg` → `tan`
- Multiplicación implícita

---

#### **app/utils/plotter.py**
**Responsabilidad**: Generar gráficas de funciones

**Función principal**:
```python
def plot_function(func_str, lower_limit, upper_limit):
    """Genera gráfica y retorna nombre del archivo"""
    # Parsear función
    expr = parse_function(func_str)
    f = sp.lambdify(x, expr, 'numpy')
    
    # Generar valores
    x_vals = np.linspace(x_min, x_max, 1000)
    y_vals = f(x_vals)
    
    # Crear gráfica
    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals)
    
    # Sombrear área si es definida
    if lower_limit and upper_limit:
        _shade_area(ax, f, lower, upper)
    
    # Guardar
    filename = _save_plot(fig)
    return filename
```

**Funciones auxiliares**:
- `_determine_plot_range()`: Calcula rango de x
- `_calculate_y_values()`: Calcula y filtra valores
- `_shade_area()`: Sombrea área bajo la curva
- `_configure_plot()`: Configura apariencia
- `_save_plot()`: Guarda archivo PNG

---

## 🔄 Flujo de Datos

```
Cliente (JavaScript)
        ↓
    POST /calculate
        ↓
app/routes/main.py
        ↓
app/services/integration.py
    ├── parse_function() (utils/parser.py)
    ├── calculate_integral()
    ├── generate_procedure()
    └── identify_rule()
        ↓
app/utils/plotter.py
    └── plot_function()
        ↓
Respuesta JSON
        ↓
Cliente (results.js)
```

## 🎨 Ventajas de la Modularización

### 1. **Separación de Responsabilidades**
- **Routes**: Solo manejan HTTP
- **Services**: Lógica de negocio
- **Utils**: Funciones auxiliares
- **Config**: Configuración centralizada

### 2. **Testabilidad**
```python
# Test de servicio
from app.services.integration import calculate_integral

def test_integration():
    result = calculate_integral('x^2')
    assert result['success'] == True
```

### 3. **Reutilización**
```python
# Usar parser en otro módulo
from app.utils.parser import parse_function

expr = parse_function('sin(x)')
```

### 4. **Escalabilidad**
Fácil agregar nuevas funcionalidades:
```
app/
├── services/
│   ├── integration.py
│   ├── differentiation.py  # NUEVO
│   └── equation_solver.py  # NUEVO
```

### 5. **Mantenibilidad**
- Código organizado por función
- Fácil localizar bugs
- Cambios aislados

---

## 📦 Dependencias entre Módulos

```
app.py
  └── app/__init__.py (create_app)
        ├── app/config.py
        └── app/routes/main.py
              ├── app/services/integration.py
              │     ├── app/utils/parser.py
              │     └── (SymPy)
              └── app/utils/plotter.py
                    ├── app/utils/parser.py
                    ├── app/config.py
                    └── (Matplotlib, NumPy)
```

## 🚀 Cómo Agregar Nueva Funcionalidad

### Ejemplo: Agregar Derivadas

#### 1. Crear servicio
```python
# app/services/differentiation.py
import sympy as sp
from app.utils.parser import parse_function

def calculate_derivative(func_str, order=1):
    """Calcula la derivada de una función"""
    x = sp.Symbol('x')
    expr = parse_function(func_str)
    
    derivative = expr
    for _ in range(order):
        derivative = sp.diff(derivative, x)
    
    return {
        'success': True,
        'original': sp.latex(expr),
        'derivative': sp.latex(derivative),
        'order': order
    }
```

#### 2. Crear ruta
```python
# app/routes/main.py
@main_bp.route('/differentiate', methods=['POST'])
def differentiate():
    data = request.get_json()
    result = calculate_derivative(data['function'])
    return jsonify(result)
```

#### 3. Actualizar __init__
```python
# app/services/__init__.py
from app.services.integration import calculate_integral
from app.services.differentiation import calculate_derivative

__all__ = ['calculate_integral', 'calculate_derivative']
```

---

## 🔧 Configuración por Entorno

### Desarrollo
```python
# app.py
app = create_app()  # Usa DevelopmentConfig
```

### Producción
```python
# app.py
from app.config import ProductionConfig
app = create_app(ProductionConfig)
```

### Testing
```python
# tests/conftest.py
from app import create_app
from app.config import Config

class TestConfig(Config):
    TESTING = True
    DEBUG = False

@pytest.fixture
def app():
    return create_app(TestConfig)
```

---

## 📝 Convenciones de Código

### Nombres de archivos
- `snake_case.py` para módulos
- Descriptivos y específicos

### Nombres de funciones
- `calculate_*()` para cálculos
- `generate_*()` para generación
- `parse_*()` para parsing
- `plot_*()` para gráficas
- `_private_function()` para funciones internas

### Docstrings
```python
def function_name(param1, param2):
    """
    Descripción breve
    
    Args:
        param1 (type): Descripción
        param2 (type): Descripción
        
    Returns:
        type: Descripción
        
    Raises:
        ErrorType: Cuándo ocurre
    """
    pass
```

### Imports
```python
# Estándar
import os
from datetime import datetime

# Terceros
import sympy as sp
from flask import Flask

# Locales
from app.config import config
from app.utils.parser import parse_function
```

---

## ✅ Checklist para Nuevos Módulos

- [ ] Crear archivo en directorio apropiado
- [ ] Definir responsabilidad clara
- [ ] Documentar con docstrings
- [ ] Agregar a `__init__.py` del paquete
- [ ] Importar solo lo necesario
- [ ] Escribir tests unitarios
- [ ] Actualizar este README
- [ ] Verificar que funciona

---

## 🧪 Testing

### Estructura de tests
```
tests/
├── __init__.py
├── conftest.py
├── test_services/
│   ├── test_integration.py
│   └── test_differentiation.py
├── test_utils/
│   ├── test_parser.py
│   └── test_plotter.py
└── test_routes/
    └── test_main.py
```

### Ejemplo de test
```python
# tests/test_services/test_integration.py
from app.services.integration import calculate_integral

def test_polynomial_integration():
    result = calculate_integral('x^2')
    assert result['success'] == True
    assert 'x^3' in result['indefinite_integral_text']

def test_invalid_function():
    result = calculate_integral('invalid@#$')
    assert result['success'] == False
    assert 'error' in result
```

---

## 📊 Comparación: Antes vs Después

### Antes (Monolítico)
```
app.py (476 líneas)
├── Configuración
├── Parser
├── Cálculo de integrales
├── Generación de procedimientos
├── Plotting
└── Rutas
```

### Después (Modular)
```
app.py (12 líneas)
app/
├── config.py (50 líneas)
├── __init__.py (30 líneas)
├── routes/main.py (80 líneas)
├── services/integration.py (400 líneas)
├── utils/parser.py (40 líneas)
└── utils/plotter.py (150 líneas)
```

**Beneficios**:
- ✅ Código más organizado
- ✅ Fácil de mantener
- ✅ Testeable independientemente
- ✅ Escalable
- ✅ Reutilizable

---

**🎯 Esta estructura modular sigue las mejores prácticas de Flask y hace el backend profesional y mantenible.**
