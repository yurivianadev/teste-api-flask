from flask import Flask, request, render_template, jsonify, redirect, url_for
from flask_cors import CORS  # para permitir requisições do navegador
import bcrypt
from crud.mysqlConnector import salvar_dados, login_usuario, buscar_usuario_por_email, enviar_email_verificacao, verificar_token
import secrets

dados = {}

app = Flask(__name__)
CORS(app)  # libera acesso de qualquer frontend

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

     

    if (password != confirmPassword) :
        return jsonify({'ERRO': 'Senhas estão diferentes'})
    
    hash_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hash_str = hash_bytes.decode('utf-8')


    if buscar_usuario_por_email(email) == None:
        salvar_dados(name, email, hash_str, token, 0)
        enviar_email_verificacao(email, token)
        return 'Conta registrada com sucesso, ative pelo email'
        
    return "Mensagem: Email ja foi cadastrado"


@app.route('/verificar-email/<token>/<email>')
def verificar_email(token, email):
    if verificar_token(token) == False:
        return 'Usuario não encontrado ou token invalido '


    return 'Email cadastrado com sucesso faça login <a href="http://127.0.0.1:5500/templates/login.html">aqui</a>' 



@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    resultado = login_usuario(email, password)
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
