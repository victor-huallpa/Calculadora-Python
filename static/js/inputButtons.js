/**
 * Input Buttons Module
 * Maneja los botones de entrada de símbolos y funciones matemáticas
 */

import { DOM } from './dom.js';
import { insertAtCursor } from './ui.js';

/**
 * Inicializa los botones de símbolos matemáticos
 */
export function initSymbolButtons() {
    const symbolButtons = document.querySelectorAll('.symbol-btn');

    symbolButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const symbol = btn.getAttribute('data-symbol');
            insertAtCursor(DOM.functionInput, symbol);
            DOM.functionInput.focus();
        });
    });
}

/**
 * Inicializa los botones de funciones matemáticas
 */
export function initFunctionButtons() {
    const functionButtons = document.querySelectorAll('.function-btn');

    functionButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const func = btn.getAttribute('data-function');

            // Insertar función con paréntesis y colocar cursor dentro
            const cursorPos = DOM.functionInput.selectionStart;
            const textBefore = DOM.functionInput.value.substring(0, cursorPos);
            const textAfter = DOM.functionInput.value.substring(DOM.functionInput.selectionEnd);

            DOM.functionInput.value = textBefore + func + '()' + textAfter;

            // Colocar cursor dentro de los paréntesis
            const newCursorPos = cursorPos + func.length + 1;
            DOM.functionInput.setSelectionRange(newCursorPos, newCursorPos);
            DOM.functionInput.focus();
        });
    });
}

/**
 * Inicializa todos los botones de entrada
 */
export function initInputButtons() {
    initSymbolButtons();
    initFunctionButtons();
}
