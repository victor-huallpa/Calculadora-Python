# 🧮 Calculadora de Integrales

Una aplicación web completa desarrollada con **Flask** y **SymPy** para resolver integrales indefinidas y definidas con visualización gráfica interactiva.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![SymPy](https://img.shields.io/badge/SymPy-1.12-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Características

- 📊 **Cálculo de Integrales**: Resuelve integrales indefinidas y definidas
- 🎨 **Interfaz Moderna**: Diseño premium con efectos glassmorphism y animaciones suaves
- ✅ **Validación en Tiempo Real**: Retroalimentación instantánea sobre la entrada del usuario
- 📐 **Renderizado LaTeX**: Visualización matemática profesional con MathJax
- 📈 **Gráficas Dinámicas**: Visualización de funciones y área bajo la curva
- 🔄 **Pasos de Integración**: Muestra el proceso de cálculo (cuando está disponible)
- 📱 **Diseño Responsivo**: Funciona perfectamente en dispositivos móviles y de escritorio
- 🚀 **Listo para Producción**: Configurado para despliegue en Render/Railway

## 🛠️ Tecnologías

### Backend
- **Flask 3.0**: Framework web ligero y potente
- **SymPy 1.12**: Motor de matemáticas simbólicas
- **Matplotlib 3.8**: Generación de gráficas
- **NumPy 1.26**: Operaciones numéricas
- **Gunicorn 21.2**: Servidor WSGI para producción

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Diseño moderno con variables CSS y glassmorphism
- **JavaScript ES6+**: Lógica interactiva y validación
- **MathJax 3**: Renderizado de fórmulas matemáticas

## 📁 Estructura del Proyecto

```
calculadora/
├── app.py                      # Aplicación Flask principal
├── requirements.txt            # Dependencias de Python
├── Procfile                    # Configuración de despliegue
├── runtime.txt                 # Versión de Python
├── .gitignore                  # Archivos ignorados por Git
├── README.md                   # Este archivo
├── static/
│   ├── css/
│   │   └── style.css          # Estilos personalizados
│   ├── js/
│   │   └── main.js            # Lógica del frontend
│   └── plots/                 # Gráficas generadas (auto-creado)
└── templates/
    └── index.html             # Plantilla principal
```

## 🚀 Instalación y Uso

### Requisitos Previos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Entorno virtual (recomendado)

### Instalación Local

1. **Clonar o descargar el proyecto**

```bash
cd calculadora
```

2. **Crear un entorno virtual**

```bash
python -m venv venv
```

3. **Activar el entorno virtual**

- En Linux/Mac:
```bash
source venv/bin/activate
```

- En Windows:
```bash
venv\Scripts\activate
```

4. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

5. **Ejecutar la aplicación**

```bash
python app.py
```

6. **Abrir en el navegador**

Visita: `http://localhost:5000`

## 📖 Uso de la Aplicación

### Integrales Indefinidas

1. Ingresa una función en el campo "Función f(x)"
2. Deja los límites vacíos
3. Haz clic en "Calcular Integral"
4. Verás la integral indefinida: ∫f(x)dx

**Ejemplo**: `x^2` → `x³/3 + C`

### Integrales Definidas

1. Ingresa una función en el campo "Función f(x)"
2. Especifica el límite inferior y superior
3. Haz clic en "Calcular Integral"
4. Verás la integral definida y el área bajo la curva

**Ejemplo**: `sin(x)` con límites `0` a `pi` → `2`

### Sintaxis Soportada

- **Potencias**: `x^2`, `x^3`
- **Multiplicación**: `2*x`, `x*y` (o implícita: `2x`)
- **Funciones trigonométricas**: `sin(x)`, `cos(x)`, `tan(x)`
- **Exponenciales**: `e^x`, `exp(x)`
- **Logaritmos**: `log(x)`, `ln(x)`
- **Raíces**: `sqrt(x)`
- **Constantes**: `pi`, `e`

## 🌐 Despliegue en Producción

### Opción 1: Render

1. **Crear cuenta en [Render](https://render.com)**

2. **Crear nuevo Web Service**
   - Conecta tu repositorio de GitHub
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Variables de entorno** (opcional)
   - `PYTHON_VERSION`: `3.11.7`

4. **Desplegar**
   - Render detectará automáticamente el `Procfile` y `runtime.txt`

### Opción 2: Railway

1. **Crear cuenta en [Railway](https://railway.app)**

2. **Nuevo Proyecto**
   - Selecciona "Deploy from GitHub repo"
   - Conecta tu repositorio

3. **Configuración automática**
   - Railway detectará automáticamente Flask y Python
   - Usará el `Procfile` para el comando de inicio

4. **Desplegar**
   - El despliegue se iniciará automáticamente

### Opción 3: Servidor Propio (VPS)

```bash
# Instalar dependencias del sistema
sudo apt update
sudo apt install python3.11 python3-pip nginx

# Clonar proyecto
git clone <tu-repositorio>
cd calculadora

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar con gunicorn
gunicorn --bind 0.0.0.0:8000 app:app
```

## 🧪 Ejemplos de Prueba

### Funciones Simples
- `x` → `x²/2 + C`
- `x^2` → `x³/3 + C`
- `x^3` → `x⁴/4 + C`

### Funciones Trigonométricas
- `sin(x)` → `-cos(x) + C`
- `cos(x)` → `sin(x) + C`
- `tan(x)` → `-log(cos(x)) + C`

### Funciones Exponenciales
- `e^x` → `e^x + C`
- `2^x` → `2^x/log(2) + C`

### Funciones Compuestas
- `x*sin(x)` → `sin(x) - x*cos(x) + C`
- `x*e^x` → `(x-1)*e^x + C`

### Integrales Definidas
- `x^2` de `0` a `1` → `1/3`
- `sin(x)` de `0` a `pi` → `2`
- `e^x` de `0` a `1` → `e - 1`

## 🎨 Características del Diseño

- **Tema Oscuro**: Colores vibrantes sobre fondo oscuro
- **Glassmorphism**: Efectos de vidrio esmerilado en las tarjetas
- **Gradientes Animados**: Formas flotantes en el fondo
- **Micro-animaciones**: Transiciones suaves y efectos hover
- **Tipografía Moderna**: Fuente Inter de Google Fonts
- **Responsive**: Adaptado para móviles, tablets y escritorio

## 🔧 Solución de Problemas

### Error: "No se puede parsear la función"

- Verifica la sintaxis de la función
- Usa `*` para multiplicación explícita
- Usa `^` para potencias (se convierte a `**` internamente)

### Error: "Los límites deben ser números válidos"

- Asegúrate de ingresar números en los límites
- El límite inferior debe ser menor que el superior

### La gráfica no se muestra

- Verifica que la función sea válida en el rango especificado
- Algunas funciones pueden tener discontinuidades

### Error de instalación de dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

## 📝 Notas Técnicas

- **Límite de Cálculo**: SymPy puede tardar en funciones muy complejas
- **Precisión Numérica**: Los resultados numéricos tienen 6 decimales
- **Caché de Gráficas**: Las imágenes se guardan en `static/plots/`
- **Seguridad**: La entrada se valida antes de procesarse

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

Desarrollado con ❤️ usando Flask y SymPy

## 🙏 Agradecimientos

- [SymPy](https://www.sympy.org/) - Motor de matemáticas simbólicas
- [Flask](https://flask.palletsprojects.com/) - Framework web
- [MathJax](https://www.mathjax.org/) - Renderizado de LaTeX
- [Matplotlib](https://matplotlib.org/) - Visualización de datos

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!
