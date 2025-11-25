"""
Flask Integral Calculator Application
Aplicación modular para cálculo de integrales usando SymPy
"""

from app import create_app

# Crear instancia de la aplicación
app = create_app()

if __name__ == '__main__':
    # Ejecutar en modo debug para desarrollo
    app.run(debug=True, host='0.0.0.0', port=5000)
