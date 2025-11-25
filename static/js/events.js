/**
 * Events Module
 * Maneja eventos adicionales y atajos de teclado
 */

import { DOM, State } from './dom.js';
import { hideAllResults } from './ui.js';

/**
 * Inicializa soporte de tecla Enter para navegación entre inputs
 */
export function initEnterKeyNavigation() {
    const inputs = [DOM.functionInput, DOM.lowerLimitInput, DOM.upperLimitInput];

    inputs.forEach((input, index) => {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (index < inputs.length - 1) {
                    inputs[index + 1].focus();
                } else {
                    DOM.form.dispatchEvent(new Event('submit'));
                }
            }
        });
    });
}

/**
 * Inicializa atajos de teclado globales
 */
export function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + Enter para enviar
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (!State.isCalculating) {
                DOM.form.dispatchEvent(new Event('submit'));
            }
        }

        // Escape para limpiar resultados
        if (e.key === 'Escape') {
            hideAllResults();
        }
    });
}

/**
 * Inicializa auto-completado de paréntesis
 */
export function initParenthesisAutoComplete() {
    DOM.functionInput.addEventListener('keydown', (e) => {
        if (e.key === '(' && !e.shiftKey) {
            const start = DOM.functionInput.selectionStart;
            const end = DOM.functionInput.selectionEnd;
            const value = DOM.functionInput.value;

            // Verificar si debemos auto-cerrar paréntesis
            const textAfter = value.substring(end);
            if (!textAfter.startsWith(')')) {
                e.preventDefault();
                const newValue = value.substring(0, start) + '()' + textAfter;
                DOM.functionInput.value = newValue;
                DOM.functionInput.setSelectionRange(start + 1, start + 1);
            }
        }
    });
}

/**
 * Inicializa efecto ripple en botón de calcular
 */
export function initButtonRipple() {
    DOM.calculateBtn.addEventListener('click', (e) => {
        const ripple = document.createElement('span');
        const rect = DOM.calculateBtn.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');

        DOM.calculateBtn.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    });
}

/**
 * Inicializa manejo de errores de carga de imagen
 */
export function initPlotImageErrorHandler() {
    DOM.plotImage.addEventListener('error', () => {
        DOM.plotSection.classList.add('hidden');
        console.error('Failed to load plot image');
    });
}

/**
 * Inicializa todos los event listeners
 */
export function initEvents() {
    initEnterKeyNavigation();
    initKeyboardShortcuts();
    initParenthesisAutoComplete();
    initButtonRipple();
    initPlotImageErrorHandler();
}
