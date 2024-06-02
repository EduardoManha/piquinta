import os
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template_string

# Carregar o arquivo CSV com o delimitador correto
file_path = 'datasus.csv'
data = pd.read_csv(file_path, delimiter=';')

# Função para contar os valores de SEXOPAC
def count_sexopac_values(df):
    male_count = df[df['SEXOPAC'] == 'M'].shape[0]
    female_count = df[df['SEXOPAC'] == 'F'].shape[0]
    return male_count, female_count

# Contar os valores
male_count, female_count = count_sexopac_values(data)

# Criar o gráfico
def create_bar_chart(male_count, female_count):
    labels = ['Masculino', 'Feminino']
    counts = [male_count, female_count]

    fig, ax = plt.subplots()
    ax.bar(labels, counts, color=['blue', 'pink'])
    ax.set_xlabel('Sexo')
    ax.set_ylabel('Quantidade')
    ax.set_title('Quantidade de Pacientes por Sexo')

    # Criar o diretório static se não existir
    if not os.path.exists('static'):
        os.makedirs('static')

    # Salvar o gráfico em um arquivo
    plt.savefig('static/sexopac_chart.png')

create_bar_chart(male_count, female_count)

# Configurar o Flask para exibir o gráfico
app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <!doctype html>
        <title>Gráfico de Pacientes por Sexo</title>
        <h1>Gráfico de Pacientes por Sexo</h1>
        <img src="/static/sexopac_chart.png" alt="Gráfico de Pacientes por Sexo">
    ''')

if __name__ == '__main__':
    app.run(debug=True)
