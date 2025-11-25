/**
 * Main Application Entry Point
 * Coordina todos los módulos de la aplicación
 */

import { DOM } from './dom.js';
import { initValidation } from './validation.js';
import { initFormHandler } from './formHandler.js';
import { initInputButtons } from './inputButtons.js';
import { initEvents } from './events.js';

/**
 * Inicializa la aplicación
 */
function initApp() {
    // Enfocar en el input de función
    DOM.functionInput.focus();

    // Inicializar todos los módulos
    initValidation();
    initFormHandler();
    initInputButtons();
    initEvents();

    console.log('✅ Calculadora de Integrales inicializada correctamente');
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}
