/**
 * UI Module
 * Maneja todas las interacciones de interfaz de usuario
 */

import { DOM, State } from './dom.js';

/**
 * Muestra un mensaje de error
 */
export function showError(element, message) {
    element.textContent = message;
    element.classList.add('show');
}

/**
 * Oculta un mensaje de error
 */
export function hideError(element) {
    element.textContent = '';
    element.classList.remove('show');
}

/**
 * Muestra el overlay de carga
 */
export function showLoading() {
    DOM.loadingOverlay.classList.remove('hidden');
    State.isCalculating = true;
    DOM.calculateBtn.disabled = true;
}

/**
 * Oculta el overlay de carga
 */
export function hideLoading() {
    DOM.loadingOverlay.classList.add('hidden');
    State.isCalculating = false;
    DOM.calculateBtn.disabled = false;
}

/**
 * Oculta todas las secciones de resultados
 */
export function hideAllResults() {
    DOM.resultsSection.classList.add('hidden');
    DOM.errorSection.classList.add('hidden');
    DOM.definiteResultDiv.classList.add('hidden');

    if (DOM.procedureSection) {
        DOM.procedureSection.classList.add('hidden');
    }

    DOM.plotSection.classList.add('hidden');
}

/**
 * Muestra un error en la sección de error
 */
export function displayError(message) {
    hideAllResults();
    DOM.errorSection.classList.remove('hidden');
    document.getElementById('error-message').textContent = message;

    // Scroll al error
    DOM.errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Inserta texto en la posición del cursor
 */
export function insertAtCursor(input, text) {
    const start = input.selectionStart;
    const end = input.selectionEnd;
    const value = input.value;

    input.value = value.substring(0, start) + text + value.substring(end);

    // Mover cursor después del texto insertado
    const newPos = start + text.length;
    input.setSelectionRange(newPos, newPos);
}
