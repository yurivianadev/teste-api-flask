from flask import request, render_template, jsonify
import secrets
import bcrypt
from datetime import datetime, timedelta
from auth.jwt_utils import gerar_token, token_required

from crud.mysqlConnector import (
    salvar_dados,
    login_usuario,
    buscar_usuario_por_email,
    enviar_email_verificacao,
    verificar_token,
    salvar_token_reset_senha,
    verificar_token_reset_senha,
    enviar_email_reset_senha,
    update_password
)

def init_routes(app):
    SECRET_KEY = app.config['SECRET_KEY']
    @app.route('/')
    def form():
        return render_template('index.html')

    @app.route('/receber-dados', methods=['POST'])
    def cadastrar_dados():
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        token = secrets.token_urlsafe(16)

        if password != confirmPassword:
            return jsonify({'ERRO': 'Senhas estão diferentes'})

        hash_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hash_str = hash_bytes.decode('utf-8')

        if buscar_usuario_por_email(email) is None:
            salvar_dados(name, email, hash_str, token, 0)
            enviar_email_verificacao(email, token)
            return 'Conta registrada com sucesso, ative pelo email'

        return "Mensagem: Email já foi cadastrado"

    @app.route('/verificar-email/<token>/<email>')
    def verificar_email(token, email):
        if not verificar_token(token):
            return 'Usuário não encontrado ou token inválido'

        return 'Email cadastrado com sucesso. Faça login <a href="http://127.0.0.1:5500/templates/login.html">aqui</a>'

    @app.route('/login', methods=['POST'])
    def login():
        email = request.form['email']
        password = request.form['password']
        resultado = login_usuario(email, password)
    
        print(resultado)
        if resultado.get('status') == 'sucesso':
            token = gerar_token({'email': email})
            return jsonify({'mensagem': 'Login bem-sucedido', 'token': token})
        else:
            return jsonify({'erro': 'Email ou senha inválidos'}), 401
            
    @app.route('/protected')
    @token_required
    def rota_protegida(dados_token):
        email = dados_token.get('email')
        return jsonify({'mensagem': f'Bem-vindo(a), {email}!'})




    @app.route('/recuperar-senha', methods=['POST'])
    def solicitar_recuperacao_senha():
        email = request.form.get('email')
        usuario = buscar_usuario_por_email(email)
        if not usuario:
            return jsonify({'erro': 'Email não cadastrado'}), 404

        token = secrets.token_urlsafe(20)
        expiracao = datetime.utcnow() + timedelta(hours=1)

        salvar_token_reset_senha(email, token, expiracao)  # função que você cria para salvar token+expiração

        enviar_email_reset_senha(email, token)  # envia link com token no email

        return jsonify({'mensagem': 'Email enviado para recuperação de senha.'})

    @app.route('/recuperar-senha/<token>/<email>', methods=['POST', 'GET'])
    def redefinir_senha_com_token(token, email):
        resultado = verificar_token_reset_senha(token)
        if resultado is None:
            return jsonify({'erro': 'Token inválido'}), 400
        if resultado == 'expirado':
            return jsonify({'erro': 'Token expirado'}), 400

        if request.method == 'POST':
            new_password = request.form.get('new_password')
            confirm_newPassword = request.form.get('confirm_newPassword')

            if not new_password or not confirm_newPassword:
                return jsonify({'erro': 'Preencha todos os campos'}), 400
        
            if new_password != confirm_newPassword:
                return jsonify({'erro': 'Senhas estão diferentes'}), 400
            
            hash_bytes = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            hash_str = hash_bytes.decode('utf-8')
            update_password(hash_str, email)
            return jsonify({'mensagem': 'Senha redefinida com sucesso!'})
        print(token, email)
        return render_template('recoverpassConfirm.html', token=token, email=email)