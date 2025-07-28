import mysql.connector
import bcrypt

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
           
        command = "INSERT INTO usuarios(name, email, password, token, email_verificado) VALUES (%s, %s, %s, %s, %s)" 
        value = (name, email, password, token, email_verificado)
        cursor.execute(command, value)
        connection.commit()
        cursor.close()
        connection.close()
        return True


def buscar_usuario_por_email(email):
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="91313826",
        database="cadastro_usuarios"
    )
    cursor = conexao.cursor()

    sql = "SELECT email FROM usuarios WHERE email = %s"
    cursor.execute(sql, (email,))  # observe a vírgula na tupla

    resultado = cursor.fetchone()  # pega 1 registro, retorna None se não achar
    print(resultado)
    cursor.close()
    conexao.close()

    return resultado

'''def excluir_token(email):
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="91313826",
        database="cadastro_usuarios"
    )
    cursor = conexao.cursor()
    
    query =  "UPDATE usuarios SET token = NULL WHERE email = %s"
    cursor.execute(query, (email,))
    conexao.commit()

    cursor.close()
    conexao.close()
'''
'''def adicionar_token():'''

def verificar_token(token):
    if not token:
        return "Token inválido.", 400

    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="91313826",
        database="cadastro_usuarios"
    )
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE token = %s", (token,))
    usuario = cursor.fetchone()
    if usuario == None:
        cursor.close()
        conexao.close()    
        return False


    cursor.execute("UPDATE usuarios SET email_verificado = 1 WHERE token = %s", (token,))
    conexao.commit()
    cursor.close()
    conexao.close()
    return True



def login_usuario(email, password):
    try:
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

    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}

    finally:
        cursor.close()
        connection.close()