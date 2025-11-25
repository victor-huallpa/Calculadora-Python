/**
 * DOM Elements Configuration
 * Centraliza todas las referencias a elementos del DOM
 */

export const DOM = {
    // Form elements
    form: document.getElementById('integral-form'),
    functionInput: document.getElementById('function-input'),
    lowerLimitInput: document.getElementById('lower-limit'),
    upperLimitInput: document.getElementById('upper-limit'),
    calculateBtn: document.getElementById('calculate-btn'),

    // Error elements
    functionError: document.getElementById('function-error'),
    limitsError: document.getElementById('limits-error'),

    // Section elements
    resultsSection: document.getElementById('results-section'),
    errorSection: document.getElementById('error-section'),
    loadingOverlay: document.getElementById('loading-overlay'),

    // Result display elements
    originalFunctionDiv: document.getElementById('original-function'),
    indefiniteIntegralDiv: document.getElementById('indefinite-integral'),
    definiteResultDiv: document.getElementById('definite-result'),
    definiteIntegralDiv: document.getElementById('definite-integral'),
    definiteValueDiv: document.getElementById('definite-value'),
    procedureSection: document.getElementById('procedure-section'),
    procedureContainer: document.getElementById('integration-procedure'),
    plotSection: document.getElementById('plot-section'),
    plotImage: document.getElementById('plot-image')
};

/**
 * Application State
 */
export const State = {
    isCalculating: false
};
