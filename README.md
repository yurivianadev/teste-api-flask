# Projeto API de Registro, Login e Verificação de E-mail com Flask

## Descrição

API simples desenvolvida com Flask para realizar cadastro de usuários, envio de e-mail de verificação e login seguro.  
As senhas são armazenadas com hash usando bcrypt e o banco de dados utilizado é MySQL.  
O fluxo inclui o envio automático de um token por e-mail para ativar a conta.

---

## Tecnologias Utilizadas

- Python 3.x
- Flask
- MySQL
- bcrypt
- smtplib (para envio de e-mails via SMTP)
- HTML e CSS (front-end básico)
- flask-cors (para permitir chamadas CORS no backend)

## Como Rodar o Projeto Localmente

1. **Clone o repositório**:
```bash
git clone <url-do-repo>
cd projeto-api

2. Crie e ative um ambiente virtual:
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

3.Instale as dependências:
pip install flask bcrypt mysql-connector-python flask-cors

4.Configure seu banco MySQL:
Crie o banco cadastro_usuarios.
Crie a tabela usuarios com o seguinte comando SQL:


CREATE TABLE usuarios (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    token VARCHAR(64) DEFAULT NULL,
    email_verificado TINYINT(1) DEFAULT 0
);

5.Atualize o arquivo crud/mysqlConnector.py com as credenciais corretas do banco e do SMTP para envio de e-mails.


6.Execute a aplicação:
python3 app.py

7.Acesse em seu navegador:
http://localhost:5000/ para acessar o formulário de cadastro.
http://localhost:5000/login para acessar o formulário de login.


Endpoints da API: 

| Endpoint                           | Método | Descrição                                                                           |
| ---------------------------------- | ------ | ----------------------------------------------------------------------------------- |
| `/`                                | GET    | Renderiza formulário de cadastro (index.html)                                       |
| `/receber-dados`                   | POST   | Recebe dados do formulário de cadastro, salva usuário e envia e-mail de verificação |
| `/verificar-email/<token>/<email>` | GET    | Verifica o token enviado por e-mail e ativa o usuário                               |
| `/login`                           | POST   | Recebe dados do login e autentica usuário                                           |


Fluxo de Cadastro e Verificação:
O usuário preenche os dados no formulário de cadastro.
A senha é hashada com bcrypt.
Um token seguro é gerado e salvo no banco junto com os dados do usuário.
Um e-mail de verificação contendo o link com o token é enviado para o usuário.
O usuário clica no link do e-mail para ativar a conta.
Após ativação, o usuário pode fazer login normalmente.

Segurança
As senhas nunca são armazenadas em texto puro, apenas o hash gerado pelo bcrypt.
O token de verificação é um valor aleatório e único gerado por secrets.token_urlsafe.
O envio de e-mail utiliza SMTP com login seguro (senha de app recomendada).


Melhorias Futuras:
Implementar proteção CSRF nos formulários.
Validar entrada de dados no backend com mais rigor.
Adicionar paginação, sistema de recuperação de senha.
Substituir o uso direto de credenciais no código por variáveis de ambiente.
Implementar autenticação JWT para proteger rotas.

Contato:
Para dúvidas ou sugestões, entre em contato:
Yuri Ferreira — yuriferreira620@gmail.com