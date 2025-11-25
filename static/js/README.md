# 📁 Estructura Modular de JavaScript

## 🎯 Organización de Módulos

La aplicación utiliza **ES6 Modules** para una arquitectura modular y escalable.

```
static/js/
├── main.js              # Punto de entrada principal
├── dom.js               # Configuración de elementos DOM
├── validation.js        # Validación de formularios
├── ui.js                # Interacciones de UI
├── api.js               # Comunicación con backend
├── results.js           # Visualización de resultados
├── inputButtons.js      # Botones de entrada matemática
├── formHandler.js       # Manejo de formulario
└── events.js            # Eventos y atajos de teclado
```

## 📋 Descripción de Módulos

### 1. **main.js** - Punto de Entrada
**Responsabilidad**: Coordinar e inicializar todos los módulos

**Funciones**:
- `initApp()`: Inicializa la aplicación completa

**Dependencias**: Todos los demás módulos

---

### 2. **dom.js** - Configuración DOM
**Responsabilidad**: Centralizar referencias a elementos del DOM

**Exports**:
- `DOM`: Objeto con todas las referencias a elementos
- `State`: Estado global de la aplicación

**Elementos gestionados**:
- Formularios y inputs
- Secciones de resultados
- Elementos de error
- Overlays y modales

---

### 3. **validation.js** - Validación
**Responsabilidad**: Validar entrada del usuario

**Funciones exportadas**:
- `validateFunctionInput()`: Valida la función matemática
- `validateLimits()`: Valida los límites de integración
- `validateForm()`: Validación completa del formulario
- `initValidation()`: Inicializa event listeners de validación

**Validaciones**:
- Caracteres inválidos
- Patrones incorrectos
- Límites numéricos
- Coherencia de límites

---

### 4. **ui.js** - Interfaz de Usuario
**Responsabilidad**: Manejar interacciones visuales

**Funciones exportadas**:
- `showError(element, message)`: Muestra mensaje de error
- `hideError(element)`: Oculta mensaje de error
- `showLoading()`: Muestra overlay de carga
- `hideLoading()`: Oculta overlay de carga
- `hideAllResults()`: Oculta todas las secciones de resultados
- `displayError(message)`: Muestra error en sección dedicada
- `insertAtCursor(input, text)`: Inserta texto en posición del cursor

---

### 5. **api.js** - Comunicación Backend
**Responsabilidad**: Gestionar peticiones HTTP al servidor

**Funciones exportadas**:
- `calculateIntegral(functionValue, lowerLimit, upperLimit)`: Calcula integral vía API

**Endpoints**:
- `POST /calculate`: Envía función y límites, recibe resultados

**Manejo de errores**:
- Validación de respuesta
- Parseo de JSON
- Propagación de errores

---

### 6. **results.js** - Visualización de Resultados
**Responsabilidad**: Renderizar resultados de cálculos

**Funciones exportadas**:
- `displayResults(data)`: Muestra todos los resultados
- `displayProcedure(procedure)`: Muestra procedimiento paso a paso (privada)
- `createStepElement(step)`: Crea elemento HTML para un paso (privada)

**Renderiza**:
- Función original
- Integral indefinida
- Integral definida (si aplica)
- Procedimiento detallado
- Gráfica
- MathJax rendering

---

### 7. **inputButtons.js** - Botones de Entrada
**Responsabilidad**: Manejar botones de símbolos y funciones

**Funciones exportadas**:
- `initSymbolButtons()`: Inicializa botones de símbolos (^, *, /, etc.)
- `initFunctionButtons()`: Inicializa botones de funciones (sin, cos, etc.)
- `initInputButtons()`: Inicializa todos los botones

**Funcionalidad**:
- Inserción de símbolos en cursor
- Inserción de funciones con paréntesis
- Auto-posicionamiento de cursor

---

### 8. **formHandler.js** - Manejo de Formulario
**Responsabilidad**: Procesar envío del formulario

**Funciones exportadas**:
- `handleFormSubmit(e)`: Maneja el evento submit
- `initFormHandler()`: Inicializa event listener

**Flujo**:
1. Prevenir envío múltiple
2. Validar formulario
3. Mostrar loading
4. Llamar API
5. Mostrar resultados o error
6. Ocultar loading

---

### 9. **events.js** - Eventos y Atajos
**Responsabilidad**: Manejar eventos globales y atajos de teclado

**Funciones exportadas**:
- `initEnterKeyNavigation()`: Navegación con Enter entre inputs
- `initKeyboardShortcuts()`: Atajos globales (Ctrl+Enter, Escape)
- `initParenthesisAutoComplete()`: Auto-cierre de paréntesis
- `initButtonRipple()`: Efecto ripple en botón
- `initPlotImageErrorHandler()`: Manejo de errores de imagen
- `initEvents()`: Inicializa todos los eventos

**Atajos**:
- `Enter`: Navegar entre campos
- `Ctrl/Cmd + Enter`: Calcular
- `Escape`: Limpiar resultados
- `(`: Auto-completar con `)`

---

## 🔄 Flujo de Datos

```
Usuario ingresa función
        ↓
validation.js → Valida entrada
        ↓
formHandler.js → Procesa formulario
        ↓
ui.js → Muestra loading
        ↓
api.js → Envía a backend
        ↓
Backend procesa (app.py)
        ↓
api.js → Recibe respuesta
        ↓
results.js → Renderiza resultados
        ↓
ui.js → Oculta loading
        ↓
MathJax → Renderiza fórmulas
```

## 🎨 Ventajas de la Modularización

### 1. **Separación de Responsabilidades**
- Cada módulo tiene una función específica
- Fácil de entender y mantener
- Cambios aislados no afectan otros módulos

### 2. **Reutilización de Código**
- Funciones pueden importarse donde se necesiten
- Evita duplicación de código
- Facilita testing unitario

### 3. **Escalabilidad**
- Fácil agregar nuevas funcionalidades
- Nuevos módulos se integran sin modificar existentes
- Estructura clara para crecimiento

### 4. **Mantenibilidad**
- Código organizado y legible
- Fácil localizar y corregir bugs
- Documentación clara de dependencias

### 5. **Testing**
- Módulos pueden testearse independientemente
- Mocking de dependencias simplificado
- Cobertura de código más clara

## 📦 Dependencias entre Módulos

```
main.js
  ├── dom.js (usado por todos)
  ├── validation.js
  │     └── ui.js
  ├── formHandler.js
  │     ├── validation.js
  │     ├── ui.js
  │     ├── api.js
  │     └── results.js
  ├── inputButtons.js
  │     ├── dom.js
  │     └── ui.js
  └── events.js
        ├── dom.js
        └── ui.js

results.js
  ├── dom.js
  └── ui.js

api.js (sin dependencias internas)
```

## 🚀 Cómo Agregar Nueva Funcionalidad

### Ejemplo: Agregar Historial de Cálculos

1. **Crear nuevo módulo** `history.js`:
```javascript
// static/js/history.js
import { DOM } from './dom.js';

export function saveToHistory(calculation) {
    // Lógica para guardar
}

export function displayHistory() {
    // Lógica para mostrar
}

export function initHistory() {
    // Inicializar
}
```

2. **Importar en** `main.js`:
```javascript
import { initHistory } from './history.js';

function initApp() {
    // ... otros inits
    initHistory();
}
```

3. **Usar en otros módulos**:
```javascript
// En formHandler.js
import { saveToHistory } from './history.js';

export async function handleFormSubmit(e) {
    // ... código existente
    saveToHistory(data);
}
```

## 🔧 Debugging

### Ver módulos cargados:
```javascript
// En consola del navegador
console.log(import.meta.url);
```

### Verificar exports:
```javascript
// En cualquier módulo
console.log('Exports:', { DOM, State });
```

### Hot reload en desarrollo:
Los módulos ES6 se recargan automáticamente al guardar cambios.

## 📝 Convenciones de Código

### Nombres de archivos:
- `camelCase.js` para módulos
- Descriptivos y específicos

### Nombres de funciones:
- `init*()` para inicializadores
- `handle*()` para event handlers
- `display*()` para renderizado
- `validate*()` para validaciones

### Exports:
- `export function` para funciones públicas
- Funciones privadas sin export
- `export const` para constantes

### Imports:
- Agrupar por módulo
- Orden alfabético
- Destructuring cuando sea posible

## ✅ Checklist para Nuevos Módulos

- [ ] Crear archivo en `static/js/`
- [ ] Definir responsabilidad clara
- [ ] Documentar con JSDoc
- [ ] Exportar solo lo necesario
- [ ] Importar dependencias
- [ ] Agregar a `main.js` si es necesario
- [ ] Actualizar este README
- [ ] Probar independientemente

---

**🎯 Esta estructura modular hace el código más profesional, mantenible y escalable.**
