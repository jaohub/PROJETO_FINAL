from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'chave_secreta_super_segura_para_o_senai'

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Tabela de Usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    
    # 2. Tabela de Projetos/Módulos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projetos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_projeto TEXT NOT NULL,
            descricao TEXT,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')
    
    # 3. Tabela de Tarefas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT DEFAULT 'A Fazer',
            prioridade TEXT DEFAULT 'Média',
            data_entrega TEXT,
            projeto_id INTEGER NOT NULL,
            FOREIGN KEY (projeto_id) REFERENCES projetos(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

# --- ROTAS DE AUTENTICAÇÃO ---

@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect(url_for('lista_projetos'))
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        if not nome or not email or not senha:
            flash('Preencha todos os campos!', 'danger')
            return redirect(url_for('cadastro'))
            
        senha_hash = generate_password_hash(senha)
        
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha_hash))
            conn.commit()
            conn.close()
            flash('Cadastro realizado com sucesso! Faça o login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Este e-mail já está cadastrado no sistema!', 'danger')
            return redirect(url_for('cadastro'))
            
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[3], senha):
            session['usuario_id'] = user[0]
            session['usuario_nome'] = user[1]
            return redirect(url_for('lista_projetos'))
        else:
            flash('E-mail ou senha incorretos!', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- ROTAS DE PROJETOS / MÓDULOS ---

@app.route('/projetos', methods=['GET', 'POST'])
def lista_projetos():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    usuario_id = session['usuario_id']
    
    if request.method == 'POST':
        nome = request.form.get('nome_projeto')
        descricao = request.form.get('descricao')
        if nome:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO projetos (nome_projeto, descricao, usuario_id) VALUES (?, ?, ?)', 
                           (nome, descricao, usuario_id))
            conn.commit()
            conn.close()
            return redirect(url_for('lista_projetos'))
            
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projetos WHERE usuario_id = ?', (usuario_id,))
    meus_projetos = cursor.fetchall()
    conn.close()
    
    mostrar_criador_direto = True if not meus_projetos else False
    
    if request.args.get('novo') == '1':
        mostrar_criador_direto = True

    return render_template('projetos.html', projetos=meus_projetos, mostrar_criador=mostrar_criador_direto)

@app.route('/projeto/<int:projeto_id>/excluir', methods=['POST'])
def excluir_projeto(projeto_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute('DELETE FROM projetos WHERE id = ? AND usuario_id = ?', (projeto_id, session['usuario_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('lista_projetos'))

# --- ROTAS DE TAREFAS ---

@app.route('/projeto/<int:projeto_id>')
def dashboard_projeto(projeto_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM projetos WHERE id = ? AND usuario_id = ?', (projeto_id, session['usuario_id']))
    projeto = cursor.fetchone()
    
    if not projeto:
        conn.close()
        return "Acesso negado ou módulo não encontrado.", 403
        
    cursor.execute('SELECT * FROM tarefas WHERE projeto_id = ? ORDER BY data_entrega ASC', (projeto_id,))
    tarefas = cursor.fetchall()
    
    cursor.execute('SELECT id, nome_projeto FROM projetos WHERE usuario_id = ?', (session['usuario_id'],))
    barra_lateral = cursor.fetchall()
    conn.close()
    
    return render_template('dashboard.html', projeto=projeto, tarefas=tarefas, barra_lateral=barra_lateral)

@app.route('/projeto/<int:projeto_id>/nova-tarefa', methods=['GET', 'POST'])
def nova_tarefa(projeto_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projetos WHERE id = ? AND usuario_id = ?', (projeto_id, session['usuario_id']))
    projeto = cursor.fetchone()
    
    if not projeto:
        conn.close()
        return "Operação não autorizada.", 403
        
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        prioridade = request.form.get('prioridade')
        data_entrega = request.form.get('data_entrega')
        
        if titulo:
            cursor.execute('''
                INSERT INTO tarefas (titulo, descricao, status, prioridade, data_entrega, projeto_id)
                VALUES (?, ?, 'A Fazer', ?, ?, ?)
            ''', (titulo, descricao, prioridade, data_entrega, projeto_id))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard_projeto', projeto_id=projeto_id))
            
    conn.close()
    return render_template('nova_tarefa.html', projeto=projeto)

@app.route('/tarefa/<int:tarefa_id>/mover/<string:novo_status>')
def mover_tarefa(tarefa_id, novo_status):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT tarefas.projeto_id FROM tarefas 
        JOIN projetos ON tarefas.projeto_id = projetos.id 
        WHERE tarefas.id = ? AND projetos.usuario_id = ?
    ''', (tarefa_id, session['usuario_id']))
    resultado = cursor.fetchone()
    
    if resultado:
        projeto_id = resultado[0]
        cursor.execute('UPDATE tarefas SET status = ? WHERE id = ?', (novo_status, tarefa_id))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard_projeto', projeto_id=projeto_id))
        
    conn.close()
    return "Erro na alteração de estado.", 403

@app.route('/tarefa/<int:tarefa_id>/excluir')
def excluir_tarefa(tarefa_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT tarefas.projeto_id FROM tarefas 
        JOIN projetos ON tarefas.projeto_id = projetos.id 
        WHERE tarefas.id = ? AND projetos.usuario_id = ?
    ''', (tarefa_id, session['usuario_id']))
    resultado = cursor.fetchone()
    
    if resultado:
        projeto_id = resultado[0]
        cursor.execute('DELETE FROM tarefas WHERE id = ?', (tarefa_id,))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard_projeto', projeto_id=projeto_id))
        
    conn.close()
    return "Erro ao remover registro.", 403

# --- ROTA PARA EDITAR TAREFAS ---
@app.route('/tarefa/<int:tarefa_id>/editar', methods=['GET', 'POST'])
def editar_tarefa(tarefa_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Validação de segurança: garante que a tarefa pertence a um projeto do usuário atual
    cursor.execute('''
        SELECT tarefas.* FROM tarefas 
        JOIN projetos ON tarefas.projeto_id = projetos.id 
        WHERE tarefas.id = ? AND projetos.usuario_id = ?
    ''', (tarefa_id, session['usuario_id']))
    tarefa = cursor.fetchone()
    
    if not tarefa:
        conn.close()
        return "Tarefa não encontrada ou acesso não autorizado.", 403
        
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        status = request.form.get('status')
        prioridade = request.form.get('prioridade')
        data_entrega = request.form.get('data_entrega')
        
        if titulo:
            cursor.execute('''
                UPDATE tarefas 
                SET titulo = ?, descricao = ?, status = ?, prioridade = ?, data_entrega = ?
                WHERE id = ?
            ''', (titulo, descricao, status, prioridade, data_entrega, tarefa_id))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard_projeto', projeto_id=tarefa[6])) # Redireciona usando a FK projeto_id
            
    conn.close()
    return render_template('editar.html', tarefa=tarefa)

if __name__ == '__main__':
    app.run(debug=True)