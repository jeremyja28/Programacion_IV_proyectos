from flask import Flask, send_file, render_template, request
from routes import register_blueprints

app = Flask(__name__)
# Registramos los blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=4000)
