import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'chave_secreta_super_segura_para_o_senai'

DB_NAME = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL DEFAULT 'A Fazer',
            prioridade TEXT NOT NULL DEFAULT 'Média',
            data_entrega TEXT,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

if not os.path.exists(DB_NAME):
    init_db()

# ==========================================
# ROTAS DE AUTENTICAÇÃO E SESSÃO
# ==========================================

@app.route('/')
def index():
    if 'usuario_id' in session:
        conn = get_db_connection()
        tarefas = conn.execute('SELECT * FROM tarefas WHERE usuario_id = ? ORDER BY data_entrega ASC', (session['usuario_id'],)).fetchall()
        conn.close()
        return render_template('dashboard.html', tarefas=tarefas)
    return render_template('login.html')

@app.route('/tela-cadastro')
def tela_cadastro():
    if 'usuario_id' in session:
        return redirect(url_for('index'))
    return render_template('cadastro.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')

    if not nome or not email or not senha:
        flash("Todos os campos devem ser preenchidos!")
        return redirect(url_for('tela_cadastro'))

    senha_hash = generate_password_hash(senha)

    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', 
                     (nome, email, senha_hash))
        conn.commit()
        flash("Conta criada com sucesso! Faça seu login.")
        return redirect(url_for('index'))
    except sqlite3.IntegrityError:
        flash("Este e-mail já está cadastrado!")
        return redirect(url_for('tela_cadastro'))
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    senha = request.form.get('senha')

    conn = get_db_connection()
    usuario = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()
    conn.close()

    if usuario and check_password_hash(usuario['senha'], senha):
        session['usuario_id'] = usuario['id']
        session['usuario_nome'] = usuario['nome']
        return redirect(url_for('index'))
    else:
        flash("E-mail ou senha incorretos!")
        return redirect(url_for('index'))

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar_senha():
    if 'usuario_id' in session:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        nova_senha = request.form.get('nova_senha')

        if not email or not nova_senha:
            flash("Preencha todos os campos para recuperar!")
            return redirect(url_for('recuperar_senha'))

        conn = get_db_connection()
        usuario = conn.execute('SELECT * FROM usuarios WHERE email = ?', (email,)).fetchone()

        if usuario:
            nova_senha_hash = generate_password_hash(nova_senha)
            conn.execute('UPDATE usuarios SET senha = ? WHERE email = ?', (nova_senha_hash, email))
            conn.commit()
            conn.close()
            flash("Senha redefinida com sucesso! Acesse sua conta.")
            return redirect(url_for('index'))
        else:
            conn.close()
            flash("E-mail não encontrado no sistema!")
            return redirect(url_for('recuperar_senha'))

    return render_template('recuperar.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ==========================================
# ROTAS DO CRUD DE TAREFAS
# ==========================================

@app.route('/nova-tarefa')
def nova_tarefa():
    """Exibe a tela isolada para o formulário de cadastro de tarefa."""
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
    return render_template('nova_tarefa.html')

@app.route('/tarefa/criar', methods=['POST'])
def criar_tarefa():
    if 'usuario_id' not in session:
        return redirect(url_for('index'))
        
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    prioridade = request.form.get('prioridade')
    data_entrega = request.form.get('data_entrega')

    if not titulo:
        flash("O título da tarefa é obrigatório!")
        return redirect(url_for('nova_tarefa'))

    conn = get_db_connection()
    conn.execute('INSERT INTO tarefas (titulo, descricao, prioridade, data_entrega, usuario_id) VALUES (?, ?, ?, ?, ?)',
                 (titulo, descricao, prioridade, data_entrega, session['usuario_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('index')) # Retorna automaticamente para o painel com as tarefas cadastradas

@app.route('/tarefa/status/<int:id>/<string:novo_status>')
def alterar_status(id, novo_status):
    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    conn.execute('UPDATE tarefas SET status = ? WHERE id = ? AND usuario_id = ?', 
                 (novo_status, id, session['usuario_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/tarefa/editar/<int:id>', methods=['GET', 'POST'])
def editar_tarefa(id):
    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    tarefa = conn.execute('SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?', (id, session['usuario_id'])).fetchone()

    if not tarefa:
        conn.close()
        return redirect(url_for('index'))

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        status = request.form.get('status')
        prioridade = request.form.get('prioridade')
        data_entrega = request.form.get('data_entrega')

        if not titulo:
            flash("O título não pode ficar vazio!")
            return redirect(request.url)

        conn.execute('''
            UPDATE tarefas 
            SET titulo = ?, descricao = ?, status = ?, prioridade = ?, data_entrega = ? 
            WHERE id = ? AND usuario_id = ?
        ''', (titulo, descricao, status, prioridade, data_entrega, id, session['usuario_id']))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('editar.html', tarefa=tarefa)

@app.route('/tarefa/deletar/<int:id>')
def deletar_tarefa(id):
    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    conn = get_db_connection()
    conn.execute('DELETE FROM tarefas WHERE id = ? AND usuario_id = ?', (id, session['usuario_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)