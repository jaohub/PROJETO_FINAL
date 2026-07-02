# 📋 Gerenciador de Tarefas e Projetos (Kanban)

Um sistema completo de gerenciamento de projetos e tarefas baseado na metodologia Kanban. Desenvolvido em Python com o ecossistema Flask e persistência de dados em SQLite, a aplicação permite o cadastro de usuários, criação de módulos/projetos e controle total de fluxo de tarefas com níveis de prioridade e prazos de entrega.

## 👥 Integrantes da Dupla
- **João Mateus Leandro da Silva**
- **Abner de Andrade Silva**

## 🚀 Funcionalidades e Regras de Negócio

- **Autenticação Segura:** Cadastro e login de usuários com criptografia de senhas via hash criptográfico (werkzeug.security) em conformidade com as diretrizes do edital.
- **Recuperação de Senha:** Fluxo direto integrado para redefinição segura de credenciais de acesso através do e-mail cadastrado.
- **Gerenciamento de Projetos (CRUD Ativo):** Permite a listagem, criação, atualização e exclusão de módulos/projetos independentes.
- **Painel Kanban Dinâmico (CRUD de Atividades):** Organização e controle visual das tarefas distribuídas entre três estados: *A Fazer*, *Em Andamento* e *Concluído*.
- **Ordenação Automatizada:** Organização inteligente das atividades por ordem ascendente de prazo de entrega (ORDER BY data_entrega ASC) para priorizar urgências.
- **Segurança de Escopo e Controle de Sessão:** Isolamento rígido de dados (um usuário autenticado só visualiza e manipula seus próprios projetos e tarefas, bloqueando acessos via manipulação direta de URLs).
- **Exclusão em Cascata:** Sistema inteligente com integridade referencial via SQLite (PRAGMA foreign_keys = ON), removendo automaticamente as tarefas vinculadas quando um projeto ou usuário é excluído.

## 🛠️ Tecnologias Utilizadas e Justificativa

- **Back-End:** Python 3 + Flask (Micro-framework)
- **Banco de Dados:** SQLite3 (Mecanismo relacional local)
- **Front-End:** HTML5 Semântico, CSS3 Estruturado, Jinja2 (Templates Dinâmicos)
- **Segurança:** Criptografia baseada em Hash (PBKDF2 com Salt via Werkzeug)

**Justificativa de Stack:** A escolha do ecossistema Python com Flask e SQLite foi tomada visando o cumprimento ágil do escopo dentro do cronograma de 3 semanas estipulado pelo edital. O Flask oferece uma arquitetura minimalista e veloz para rotas e tratamento de sessões, enquanto o SQLite elimina a necessidade de infraestruturas de rede complexas por rodar em um arquivo local resiliente, atendendo perfeitamente aos requisitos técnicos exigidos sem custos de infraestrutura adicionais.

## 📋 Arquitetura do Banco de Dados

O banco de dados (database.db) é estruturado em três tabelas relacionais com chaves estrangeiras ativas:

1. **usuarios**: Gerencia as credenciais, e-mails únicos (Restrição UNIQUE) e as sessões de acesso ao sistema.
2. **projetos**: Agrupa as categorias/módulos de tarefas vinculadas a cada conta (Relacionamento 1:N com usuarios).
3. **tarefas**: Armazena as informações das atividades, status e chaves de relacionamento (Relacionamento 1:N com projetos).

---

## 🧠 Dificuldades Encontradas e Decisões Técnicas

1. **Integridade Referencial no SQLite3:** Durante o desenvolvimento da funcionalidade de exclusão em cascata, identificamos que as tarefas permaneciam órfãs no banco após deletar um projeto. Descobrimos que o SQLite mantém a checagem de chaves estrangeiras desativada por padrão. A decisão técnica adotada foi injetar explicitamente o comando `PRAGMA foreign_keys = ON;` em cada nova conexão estabelecida no back-end, garantindo a integridade dos dados de avaliação.
2. **Conflito de Nomenclatura de Chaves:** Houve divergências pontuais na unificação do código entre os termos `project_id` e `projeto_id` no banco de dados. Para mitigar o problema e garantir a compatibilidade sem reescrever tabelas inteiras na reta final, implementamos um mapeamento lógico dinâmico dentro das queries no script principal.
3. **Erros de Renderização do Jinja2 em Inline CSS:** Enfrentamos quebras visuais nas caixas de alertas exibidas na tela de recuperação de senha por misturar operadores condicionais lógicos dentro de atributos de estilo direto das tags HTML. A solução foi refatorar a estrutura visual isolando as estilizações em blocos condicionais independentes `{% if category == 'danger' %}` do motor de templates.

---

## 🔧 Como Executar o Projeto Localmente

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

💡 Nota Importante: O arquivo de banco de dados database.db foi incluído nas regras do .gitignore por motivos de segurança e boas práticas de versionamento. Ao iniciar a aplicação pela primeira vez em um novo ambiente, a função init_db() criará automaticamente um banco de dados local zerado, estruturado e pronto para uso.

---

## 📁 Estrutura de Pastas do Projeto

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

### 💡 Dica extra para o Git:
Antes de fazer o push final, adicione as modificações e realize o commit pelo terminal:
git add README.md .gitignore templates/login.html templates/recuperar_senha.html app.py
git commit -m "Doc: Adiciona README profissional e finaliza fluxos de autenticacao"
git push