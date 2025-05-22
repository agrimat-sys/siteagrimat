from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, abort
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Use uma chave segura em produção!

USUARIO = "admin"
SENHA = "1234"

# Decorador para verificar login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('usuario_logado'):
            session['proxima_url'] = request.path
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rotas públicas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/perfil-corporativo')
def perfil_corporativo():
    return render_template('perfil_corporativo.html')

@app.route('/setores-atuacao')
def setores_atuacao():
    return render_template('setores_atuacao.html')

@app.route('/composicao-acionaria')
def composicao_acionaria():
    return render_template('composicao_acionaria.html')

@app.route('/estatuto-politicas')
def estatuto_politicas():
    return render_template('estatuto_politicas.html')

@app.route('/codigo-conduta')
def codigo_conduta():
    return render_template('codigo_conduta.html')

@app.route('/sustentabilidade')
def sustentabilidade():
    return render_template('sustentabilidade.html')

@app.route('/contato')  
def contato():
    return render_template('contato.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Login e logout
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == USUARIO and senha == SENHA:
            session['usuario_logado'] = True
            proxima = session.pop('proxima_url', None)
            return redirect(proxima or url_for('dashboard'))
        else:
            return render_template('login.html', erro="Usuário ou senha incorretos.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('login'))

# Rotas protegidas
@app.route('/central-resultado')
@login_required
def central_resultado():
    return render_template('central_resultado.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Configuração de download
@app.route('/download/<nome>')
@login_required
def download(nome):
    nomes_validos = {
        'relatorio2023': 'Agrimat2023 - Relatório Final.pdf',
        'relatorio2024': 'RELATÓRIO AGRIMAT.pdf',
        'apresentacao': 'apresentacao.pdf'
    }

    if nome in nomes_validos:
        try:
            caminho_arquivo = os.path.join('documentos', nomes_validos[nome])
            if os.path.exists(caminho_arquivo):
                return send_from_directory('documentos', nomes_validos[nome], as_attachment=True)
            else:
                abort(404)
        except Exception as e:
            print(f"Erro ao tentar enviar o arquivo: {e}")
            abort(500)
    else:
        abort(404)

if __name__ == '__main__':
    # Cria a pasta de documentos, se não existir
    if not os.path.exists('documentos'):
        os.makedirs('documentos')

    # Render define a porta com a variável de ambiente PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
