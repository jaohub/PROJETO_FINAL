#  Gerenciador de Tarefas e Projetos (Kanban)

Um sistema completo de gerenciamento de projetos e tarefas baseado na metodologia Kanban. Desenvolvido em Python com o ecossistema Flask e persistência de dados em SQLite, a aplicação permite o cadastro de usuários, criação de módulos/projetos e controle total de fluxo de tarefas com níveis de prioridade e prazos de entrega.

##  Funcionalidades

- **Autenticação Segura:** Cadastro e login de usuários com criptografia de senhas via hash criptográfico (werkzeug.security).
- **Recuperação de Senha:** Fluxo direto integrado para redefinição segura de credenciais de acesso através do e-mail cadastrado.
- **Gerenciamento de Projetos:** Criação e exclusão de módulos/projetos independentes por usuário.
- **Painel Kanban Dinâmico:** Organização visual das tarefas em estados (A Fazer, Em Andamento, Concluído).
- **Controle de Tarefas:** Atribuição de descrição, níveis de prioridade (Alta, Média, Baixa) e datas limite de entrega para cada atividade.
- **Exclusão em Cascata:** Sistema inteligente com integridade referencial via SQLite (PRAGMA foreign_keys = ON), removendo automaticamente as tarefas vinculadas quando um projeto é excluído.

##  Tecnologias Utilizadas

- **Back-End:** Python 3 + Flask
- **Banco de Dados:** SQLite3
- **Front-End:** HTML5, CSS3, Jinja2 (Templates Dinâmicos)
- **Segurança:** Criptografia PBKDF2 (Werkzeug)

##  Arquitetura do Banco de Dados

O banco de dados (database.db) é estruturado em três tabelas principais com relacionamentos relacionais:

1. **usuarios**: Gerencia as credenciais e sessões de acesso do sistema.
2. **projetos**: Agrupa as tarefas criadas pelos usuários (Relacionamento 1:N com usuarios).
3. **tarefas**: Armazena as informações detalhadas e o status do quadro Kanban (Relacionamento 1:N com projetos).

---

##  Como Executar o Projeto Localmente

Siga o passo a passo abaixo para configurar o ambiente e rodar o sistema na sua máquina:

### 1. Clonar o Repositório
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

### 2. Criar e Ativar o Ambiente Virtual (.venv)
No terminal da pasta do projeto, execute:

No Windows:
python -m venv .venv
.venv\Scripts\activate

No Linux/macOS:
python3 -m venv .venv
source .venv/bin/activate

### 3. Instalar as Dependências
Com o ambiente virtual ativo, instale o Flask e as bibliotecas necessárias:
pip install Flask werkzeug

### 4. Inicializar a Aplicação
Execute o arquivo principal do ecossistema:
python app.py

O servidor local será iniciado. Abra o seu navegador e acesse: http://127.0.0.1:5000/

 Nota Importante: O arquivo de banco de dados database.db foi incluído nas regras do .gitignore por motivos de segurança e boas práticas de versionamento. Ao iniciar a aplicação pela primeira vez em um novo ambiente, a função init_db() criará automaticamente um banco de dados local zerado, estruturado e pronto para uso.

---

##  Estrutura de Pastas do Projeto

├── static/
│   └── css/
│       └── style.css          # Estilização visual da aplicação e dos cards Kanban
├── templates/
│   ├── cadastro.html          # Tela de registro de novos usuários
│   ├── dashboard.html         # Painel Kanban com colunas de estados das tarefas
│   ├── editar.html            # Formulário de modificação de tarefas existentes
│   ├── login.html             # Painel de acesso ao sistema
│   ├── nova_tarefa.html       # Formulário de criação de atividades
│   ├── projetos.html          # Listagem e gerenciador de módulos do usuário
│   └── recuperar_senha.html   # Tela de redefinição de senha
├── app.py                     # Código central do Flask (Back-end, Rotas e Banco)
├── .gitignore                 # Arquivo de exclusão de arquivos locais (banco, venv)
└── README.md                  # Documentação do projeto

###  Dica extra para o Git:
Antes de fazer o push final, adicione as modificações e realize o commit pelo terminal:
git add README.md .gitignore templates/login.html templates/recuperar_senha.html app.py
git commit -m "Doc: Adiciona README profissional e finaliza fluxos de autenticacao"
git push