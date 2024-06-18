from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    cpf = request.form['cpf']

    # Carregar ou criar o arquivo Excel
    try:
        df = pd.read_excel('data.xlsx')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Name', 'Email', 'CPF'])

    # Criar um DataFrame com os novos dados
    new_data = pd.DataFrame({'Name': [name], 'Email': [email], 'CPF': [cpf]})

    # Concatenar o novo DataFrame com o existente
    df = pd.concat([df, new_data], ignore_index=True)

    # Salvar o DataFrame no arquivo Excel
    df.to_excel('data.xlsx', index=False)

    return redirect(url_for('index'))

@app.route('/view')
def view():
    try:
        df = pd.read_excel('data.xlsx')
    except FileNotFoundError:
        return "No data available"

    return render_template('view.html', tables=[df.to_html(index=False)], titles=[''])

if __name__ == '__main__':
    app.run(debug=True)
