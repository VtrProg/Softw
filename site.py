import csv
from datetime import datetime
import os
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Importante para mensagens flash


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/servicos')
def servicos():
    return render_template('servicos.html')


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


# --- ROTA DE CONTATO ATUALIZADA PARA SALVAR EM CSV ---
@app.route('/contato', methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        try:
            # Pega os dados do formulário
            nome = request.form.get('nome')
            telefone = request.form.get('telefone')
            email_cliente = request.form.get('email')
            mensagem = request.form.get('mensagem')
            data_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Define o nome do arquivo e o cabeçalho
            arquivo_csv = 'submissions.csv'
            cabecalho = ['data_envio', 'nome', 'telefone', 'email', 'mensagem']
            dados = [data_envio, nome, telefone, email_cliente, mensagem]

            # Verifica se o arquivo já existe para não reescrever o cabeçalho
            escrever_cabecalho = not os.path.exists(arquivo_csv)

            # Abre o arquivo em modo 'append' (adicionar no final)
            with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if escrever_cabecalho:
                    writer.writerow(cabecalho)  # Escreve o cabeçalho se o arquivo for novo
                writer.writerow(dados)  # Escreve os dados do formulário

            flash('Sua mensagem foi registrada com sucesso!', 'success')

        except Exception as e:
            flash(f'Ocorreu um erro ao registrar sua mensagem: {e}', 'danger')

    return render_template('contato.html')


if __name__ == '__main__':
    app.run(debug=True)