#!/usr/bin/env python3
"""
Script para probar el servidor Flask
"""
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def test():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .test-item { margin: 10px 0; padding: 10px; border: 1px solid #ddd; }
            .success { background-color: #d4edda; }
            .error { background-color: #f8d7da; }
        </style>
    </head>
    <body>
        <h1>🧪 Test de Archivos Estáticos</h1>
        <div class="test-item success">
            <i class="fas fa-check"></i> FontAwesome desde CDN funcionando
        </div>
        <div class="test-item">
            <strong>Archivos estáticos:</strong>
            <ul>
                <li><a href="/static/img/kuchau.png" target="_blank">Imagen kuchau.png</a></li>
                <li><a href="/static/img/Logo_J.png" target="_blank">Imagen Logo_J.png</a></li>
                <li><a href="/static/dist/css/adminlte.min.css" target="_blank">AdminLTE CSS</a></li>
                <li><a href="/static/dist/js/adminlte.min.js" target="_blank">AdminLTE JS</a></li>
                <li><a href="/static/plugins/bootstrap/js/bootstrap.bundle.min.js" target="_blank">Bootstrap JS</a></li>
            </ul>
        </div>
        <div class="test-item">
            <strong>Directorio actual:</strong> {current_dir}
        </div>
    </body>
    </html>
    '''.format(current_dir=os.getcwd())

if __name__ == '__main__':
    print("🔧 Iniciando servidor de prueba...")
    print("📍 URL: http://localhost:4000")
    app.run(debug=True, host="0.0.0.0", port=4000)
