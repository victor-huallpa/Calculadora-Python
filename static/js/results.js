/**
 * Results Module
 * Maneja la visualización de resultados
 */

import { DOM } from './dom.js';
import { hideAllResults } from './ui.js';

/**
 * Muestra los resultados de la integral
 */
export function displayResults(data) {
    hideAllResults();
    DOM.resultsSection.classList.remove('hidden');

    // Mostrar función original
    DOM.originalFunctionDiv.innerHTML = `\\[f(x) = ${data.original_function}\\]`;

    // Mostrar integral indefinida
    DOM.indefiniteIntegralDiv.innerHTML = `\\[\\int f(x) \\, dx = ${data.indefinite_integral} + C\\]`;

    // Mostrar integral definida si aplica
    if (data.is_definite && data.definite_integral !== undefined) {
        DOM.definiteResultDiv.classList.remove('hidden');

        const limits = data.limits;
        DOM.definiteIntegralDiv.innerHTML = `\\[\\int_{${limits.lower}}^{${limits.upper}} f(x) \\, dx = ${data.definite_integral_latex || data.definite_integral}\\]`;

        // Mostrar valor numérico
        if (typeof data.definite_integral === 'number') {
            DOM.definiteValueDiv.innerHTML = `<strong>Valor numérico:</strong> ${data.definite_integral.toFixed(6)}`;
        } else {
            DOM.definiteValueDiv.innerHTML = `<strong>Resultado:</strong> ${data.definite_integral}`;
        }
    }

    // Mostrar procedimiento si está disponible
    if (data.procedure && data.procedure.length > 0) {
        displayProcedure(data.procedure);
    }

    // Mostrar gráfica si está disponible
    if (data.plot_url) {
        DOM.plotSection.classList.remove('hidden');
        DOM.plotImage.src = data.plot_url;
        DOM.plotImage.alt = 'Gráfica de la función';
    }

    // Re-renderizar MathJax
    if (window.MathJax) {
        MathJax.typesetPromise([DOM.resultsSection]).catch((err) => {
            console.error('MathJax rendering error:', err);
        });
    }

    // Scroll a resultados
    DOM.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Muestra el procedimiento paso a paso
 */
function displayProcedure(procedure) {
    DOM.procedureSection.classList.remove('hidden');
    DOM.procedureContainer.innerHTML = '';

    procedure.forEach(step => {
        const stepDiv = createStepElement(step);
        DOM.procedureContainer.appendChild(stepDiv);
    });
}

/**
 * Crea un elemento de paso del procedimiento
 */
function createStepElement(step) {
    const stepDiv = document.createElement('div');
    stepDiv.className = 'procedure-step';

    if (step.verification) {
        stepDiv.classList.add('verification');
    }

    // Crear encabezado del paso
    const headerDiv = document.createElement('div');
    headerDiv.className = 'step-header';

    const numberSpan = document.createElement('span');
    numberSpan.className = 'step-number';
    numberSpan.textContent = step.step;

    const descSpan = document.createElement('span');
    descSpan.className = 'step-description';
    descSpan.textContent = step.description;

    headerDiv.appendChild(numberSpan);
    headerDiv.appendChild(descSpan);

    // Agregar badge de verificación si aplica
    if (step.verification) {
        const badge = document.createElement('span');
        badge.className = 'verification-badge';
        badge.textContent = '✓ Verificado';
        headerDiv.appendChild(badge);
    }

    stepDiv.appendChild(headerDiv);

    // Agregar explicación si está disponible
    if (step.explanation) {
        const explanationDiv = document.createElement('div');
        explanationDiv.className = 'step-explanation';
        explanationDiv.textContent = step.explanation;
        stepDiv.appendChild(explanationDiv);
    }

    // Agregar fórmula si está disponible
    if (step.latex) {
        const formulaDiv = document.createElement('div');
        formulaDiv.className = 'step-formula';
        formulaDiv.innerHTML = `\\[${step.latex}\\]`;
        stepDiv.appendChild(formulaDiv);
    }

    return stepDiv;
}
