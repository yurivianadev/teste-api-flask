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
            auth_header = request.headers.get('Authorization')
            print('Authorization Header:', auth_header)  # LOG
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                print('Token extraído:', token)  # LOG
        if not token:
            print('Token ausente')  # LOG
            return jsonify({'message': 'Token ausente!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            print('Token decodificado:', data)  # LOG
        except jwt.ExpiredSignatureError:
            print('Token expirado')
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            print('Token inválido')  # L
            return jsonify({'message': 'Token inválido!'}), 401

        # Opcional: passar dados decodificados para a rota
        return f(data, *args, **kwargs)

    return decorated
