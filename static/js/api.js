/**
 * API Module
 * Maneja toda la comunicación con el backend
 */

/**
 * Calcula la integral enviando una petición al servidor
 */
export async function calculateIntegral(functionValue, lowerLimit, upperLimit) {
    const requestData = {
        function: functionValue,
        lower_limit: lowerLimit,
        upper_limit: upperLimit
    };

    const response = await fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
        throw new Error(data.error || 'Error al calcular la integral');
    }

    return data;
}
