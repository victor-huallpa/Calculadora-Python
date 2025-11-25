/**
 * Form Handler Module
 * Maneja el envío del formulario y la lógica principal
 */

import { DOM, State } from './dom.js';
import { validateForm } from './validation.js';
import { showLoading, hideLoading, displayError } from './ui.js';
import { calculateIntegral } from './api.js';
import { displayResults } from './results.js';

/**
 * Maneja el envío del formulario
 */
export async function handleFormSubmit(e) {
    e.preventDefault();

    // Prevenir múltiples envíos
    if (State.isCalculating) {
        return;
    }

    // Validar formulario
    if (!validateForm()) {
        return;
    }

    // Preparar datos
    const functionValue = DOM.functionInput.value.trim();
    const lowerLimit = DOM.lowerLimitInput.value.trim();
    const upperLimit = DOM.upperLimitInput.value.trim();

    // Mostrar carga
    showLoading();

    try {
        // Enviar petición al servidor
        const data = await calculateIntegral(functionValue, lowerLimit, upperLimit);

        // Mostrar resultados
        displayResults(data);

    } catch (error) {
        console.error('Calculation error:', error);
        displayError(error.message || 'Error de conexión con el servidor');
    } finally {
        hideLoading();
    }
}

/**
 * Inicializa el manejador del formulario
 */
export function initFormHandler() {
    DOM.form.addEventListener('submit', handleFormSubmit);
}
