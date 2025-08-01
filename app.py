from flask import Flask
from flask_cors import CORS
from routes.routes import init_routes  # importa as rotas
from config.config import SECRET_KEY

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = SECRET_KEY

init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
