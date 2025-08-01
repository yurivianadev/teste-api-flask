import mysql.connector
import bcrypt
from datetime import datetime, timedelta

import smtplib
from email.message import EmailMessage

def enviar_email_verificacao(destinatario, token):
    msg = EmailMessage()
    msg['Subject'] = 'Verifique seu e-mail'
    msg['From'] = 'Yuri Python'
    msg['To'] = destinatario

    link = f"http://localhost:5000/verificar-email/{token}/{destinatario}"  # ou seu domínio
    msg.set_content(f"Olá! Clique no link para verificar seu e-mail:\n{link}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('yuriviana620@gmail.com', 'gkyjfdaqgzjnzljq')
        smtp.send_message(msg)


def salvar_dados(name, email, password, token, email_verificado):
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='91313826',
            database='cadastro_usuarios',

        )
        cursor = connection.cursor()
           
        command = "INSERT INTO usuarios(name, email, password, email_verificacao_token, email_verificado) VALUES (%s, %s, %s, %s, %s)" 
        value = (name, email, password, token, email_verificado)
        cursor.execute(command, value)
        connection.commit()
        cursor.close()
        connection.close()
        return True


def buscar_usuario_por_email(email):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="91313826",
        database="cadastro_usuarios"
    )
    cursor = connection.cursor()

    sql = "SELECT email FROM usuarios WHERE email = %s"
    cursor.execute(sql, (email,))  # observe a vírgula na tupla

    resultado = cursor.fetchone()  # pega 1 registro, retorna None se não achar
    print(resultado)
    cursor.close()
    connection.close()

    return resultado

'''def excluir_token(email):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="91313826",
        database="cadastro_usuarios"
    )
    cursor = connection.cursor()
    
    query =  "UPDATE usuarios SET token = NULL WHERE email = %s"
    cursor.execute(query, (email,))
    connection.commit()

    cursor.close()
    connection.close()
'''
'''def adicionar_token():'''

def verificar_token(token):
    if not token:
        return "Token inválido.", 400

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="91313826",
        database="cadastro_usuarios"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email_verificacao_token = %s", (token,))
    usuario = cursor.fetchone()
    if usuario == None:
        cursor.close()
        connection.close()    
        return False


    cursor.execute("UPDATE usuarios SET email_verificado = 1 WHERE email_verificacao_token = %s", (token,))
    connection.commit()
    cursor.close()
    connection.close()
    return True



def login_usuario(email, password):
    # Conectar ao banco
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='91313826',
        database='cadastro_usuarios'
    )
    cursor = connection.cursor()

    # Procurar usuário com o email fornecido
    cursor.execute("SELECT password FROM usuarios WHERE email = %s", (email,))
    resultado = cursor.fetchone()
    
    
    if resultado:
        senha_armazenada = resultado[0]
        
        # Comparar senha fornecida com a do banco
        if bcrypt.checkpw(password.encode('utf-8'), senha_armazenada.encode('utf-8')):
            return {"status": "sucesso", "mensagem": "Login realizado com sucesso"}
        else:
            return {"status": "erro", "mensagem": "Senha incorreta"}
    else:
        return {"status": "erro", "mensagem": "Usuário não encontrado"}
    cursor.close()
    connection.close()


def salvar_token_reset_senha(email, token, expiracao):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="91313826",
        database="cadastro_usuarios"
    )
    cursor = connection.cursor()
    cursor.execute("UPDATE usuarios SET reset_senha_token = %s, reset_senha_expiracao = %s WHERE email = %s", (token, expiracao, email))
    connection.commit() 
    cursor.close()
    connection.close()

def verificar_token_reset_senha(token_recebido):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="91313826",
        database="cadastro_usuarios"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT id, reset_senha_expiracao FROM usuarios WHERE reset_senha_token = %s", (token_recebido,))
    resultado = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if not resultado:
        return None  

    usuario_id, expiracao = resultado
    if datetime.utcnow() > expiracao:
        return 'expirado'

    return usuario_id  
    
def enviar_email_reset_senha(destinatario, token):
    msg = EmailMessage()
    msg['Subject'] = 'Verifique seu e-mail'
    msg['From'] = 'Yuri Python'
    msg['To'] = destinatario

    link = f"http://localhost:5000/recuperar-senha/{token}/{destinatario}"  # ou seu domínio
    msg.set_content(f"Olá! Clique no link para redefinir sua senha:\n{link}")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('yuriviana620@gmail.com', 'gkyjfdaqgzjnzljq')
        smtp.send_message(msg)

def update_password(new_password, email):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="91313826",
        database="cadastro_usuarios"
    )
    cursor = connection.cursor()
    cursor.execute("UPDATE usuarios SET password = %s WHERE email = %s", (new_password, email,))
    connection.commit() 
    cursor.close()
    connection.close()    
