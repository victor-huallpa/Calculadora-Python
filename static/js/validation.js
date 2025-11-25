/**
 * Validation Module
 * Maneja toda la validación de entrada del usuario
 */

import { DOM } from './dom.js';
import { showError, hideError } from './ui.js';

/**
 * Valida la entrada de función en tiempo real
 */
export function validateFunctionInput() {
    const value = DOM.functionInput.value.trim();

    if (!value) {
        showError(DOM.functionError, '');
        return true;
    }

    // Patrones inválidos
    const invalidPatterns = [
        { regex: /[^a-zA-Z0-9+\-*/^().,\s]/g, message: 'Caracteres no válidos detectados' },
        { regex: /\/{2,}/g, message: 'División múltiple no válida' },
        { regex: /\*{3,}/g, message: 'Multiplicación múltiple no válida' },
    ];

    for (const pattern of invalidPatterns) {
        if (pattern.regex.test(value)) {
            showError(DOM.functionError, pattern.message);
            return false;
        }
    }

    hideError(DOM.functionError);
    return true;
}

/**
 * Valida los límites de integración
 */
export function validateLimits() {
    const lower = DOM.lowerLimitInput.value.trim();
    const upper = DOM.upperLimitInput.value.trim();

    // Ambos deben estar vacíos o ambos llenos
    if ((lower && !upper) || (!lower && upper)) {
        showError(DOM.limitsError, 'Debe proporcionar ambos límites o dejar ambos vacíos');
        return false;
    }

    // Si ambos están proporcionados, validar que sean números
    if (lower && upper) {
        const lowerNum = parseFloat(lower);
        const upperNum = parseFloat(upper);

        if (isNaN(lowerNum) || isNaN(upperNum)) {
            showError(DOM.limitsError, 'Los límites deben ser números válidos');
            return false;
        }

        if (lowerNum >= upperNum) {
            showError(DOM.limitsError, 'El límite inferior debe ser menor que el superior');
            return false;
        }
    }

    hideError(DOM.limitsError);
    return true;
}

/**
 * Valida todo el formulario antes de enviar
 */
export function validateForm() {
    const functionValue = DOM.functionInput.value.trim();

    if (!functionValue) {
        showError(DOM.functionError, 'Por favor, ingrese una función');
        DOM.functionInput.focus();
        return false;
    }

    if (!validateLimits()) {
        return false;
    }

    return true;
}

/**
 * Inicializa los event listeners de validación
 */
export function initValidation() {
    DOM.functionInput.addEventListener('input', validateFunctionInput);
    DOM.lowerLimitInput.addEventListener('input', validateLimits);
    DOM.upperLimitInput.addEventListener('input', validateLimits);
}
