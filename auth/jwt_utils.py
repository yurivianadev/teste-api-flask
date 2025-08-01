import jwt
from functools import wraps
from flask import request, jsonify
from config.config import SECRET_KEY


def gerar_token(payload):
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split()[1]

        if not token:
            return jsonify({'message': 'Token ausente!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 401

        # Opcional: passar dados decodificados para a rota
        return f(data, *args, **kwargs)

    return decorated
