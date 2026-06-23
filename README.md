# Gerenciador de Tarefas Kanban — Projeto Final

Um sistema web completo para organização e gerenciamento de tarefas utilizando a metodologia ágil Kanban. O projeto foi desenvolvido com foco em segurança arquitetural, controle estrito de sessões por usuário, níveis de prioridade e uma experiência de usuário (UX) fluida e intuitiva.

---

## Funcionalidades e Regras de Negócio

Para atender aos critérios rigorosos de avaliação, o sistema foi blindado com as seguintes regras de back-end:

* **Autenticação Criptografada:** Cadastro e login de usuários com criptografia baseada em hash utilizando o `Werkzeug Security` (algoritmo PBKDF2). As senhas nunca são salvas em texto limpo no banco de dados.
* **Validação de Unicidade:** O sistema impede nativamente e-mails duplicados através da restrição `UNIQUE` no SQLite, tratando o erro de forma amigável com mensagens interativas (`Flask Flash`).
* **Segurança de Escopo (Isolamento de Dados):** Um usuário logado só tem permissão para visualizar, criar, mover ou deletar as suas próprias tarefas. Se tentar acessar ou alterar o ID de uma tarefa de outro usuário via URL, o back-end micro-framework bloqueia a operação.
* **Controle de Sessão Rígido:** Todas as rotas do CRUD (Criar, Editar, Mover e Deletar) possuem verificações de integridade. Caso a sessão expire ou o usuário tente burlar o sistema digitando o caminho direto no navegador, ele é redirecionado para a tela de login.
* **Organização por Prazo:** No painel Kanban, as tarefas são ordenadas automaticamente de forma ascendente pela data de entrega (`ORDER BY data_entrega ASC`), ajudando o usuário a focar nas atividades mais urgentes.

---

## Fluxo de Navegação e Interface (UX)

O sistema adota uma postura de telas limpas e focadas em tarefas únicas para melhorar a experiência do usuário:

1. **Tela de Acesso:** Centraliza os formulários de Login, link para Cadastro e link para Recuperação de Senha de forma isolada.
2. **Dashboard Principal:** Exibe apenas o Quadro Kanban com as tarefas já cadastradas divididas em três colunas (*A Fazer*, *Em Andamento* e *Concluído*). 
3. **Fluxo de Criação Dinâmico:** Para evitar poluição visual, o formulário de cadastro não fica visível no painel. O usuário clica no botão dinâmico **`＋`** localizado no canto superior direito do cabeçalho, sendo direcionado para uma página dedicada (`/nova-tarefa`). Ao salvar, o Flask processa os dados e o redireciona **automaticamente** de volta ao painel principal com os dados atualizados.

---

## Funcionamento Básico do Sistema

Para entender como a aplicação processa as informações e se comunica entre a tela e o banco de dados, o ciclo de funcionamento segue esta lógica:

1. **Inicialização:** Quando o comando para rodar o servidor é executado, o script verifica se o arquivo `database.db` existe. Se não existir, ele cria o arquivo e monta as tabelas de usuários e tarefas automaticamente.
2. **Gerenciamento de Entrada:** Toda vez que um usuário digita dados nas telas (como e-mail e senha no login ou prazos na nova tarefa) e envia o formulário, o navegador faz uma requisição do tipo `POST` para o back-end.
3. **Processamento Lógico (Flask):** O arquivo `app.py` recebe esses dados, faz as validações necessárias (como verificar se as senhas batem ou se o e-mail já existe) e executa comandos lógicos ou queries no banco de dados.
4. **Armazenamento e Resposta (SQLite):** O banco de dados grava ou atualiza os registros de forma permanente. Em seguida, o Flask atualiza o estado da página e devolve para o navegador a tela HTML renderizada com as novas informações atualizadas.

---

## Tecnologias Utilizadas

* **Back-end:** Python 3 + Flask (Micro-framework)
* **Banco de Dados:** SQLite 3 (Mecanismo relacional local e resiliente)
* **Segurança:** Criptografia baseada em Hash (PBKDF2 com Salt)
* **Front-end:** HTML5 semântico e CSS3 estruturado (Pronto para estilização e design personalizado)

---

## Estrutura de Arquivos do Projeto

```text
PROJETO_FINAL/
│
├── app.py                 # Código-fonte principal (Rotas, Banco de Dados e Lógica)
├── database.db            # Banco de dados relacional (Gerado automaticamente)
├── requirements.txt       # Lista de dependências para instalação
├── README.md              # Documentação técnica do projeto
│
├── static/
│   └── css/
│       └── style.css      # Folha de estilo centralizada para design visual
│
└── templates/             # Camada de Visão (Templates Jinja2)
    ├── login.html         # Tela inicial de autenticação
    ├── cadastro.html      # Formulário de criação de conta de usuário
    ├── recuperar.html     # Formulário de redefinição de senha
    ├── dashboard.html     # Painel Kanban principal e gerenciamento
    ├── nova_tarefa.html   # Tela exclusiva para adição de atividades
    └── editar.html        # Tela exclusiva para modificação de dados da tarefa
```
    ---

## 🏁 Passo a Passo: Como Executar o Projeto Localmente

> ⚠️ **IMPORTANTE (AMBIENTE ISOLADO):** Este projeto utiliza um Ambiente Virtual (`.venv`) para garantir que as dependências do Flask não entrem em conflito com outros projetos no seu computador. É altamente recomendável ativar ou criar a `.venv` antes de instalar os requisitos para manter o seu sistema limpo e isolado.

Siga rigorosamente as instruções abaixo para preparar o ambiente e colocar o sistema para funcionar:

### Passo 0: Baixar o Código na Máquina
Certifique-se de que o código fonte do projeto foi baixado para o seu computador. Caso tenha recebido o projeto compactado em formato `.zip` ou `.rar`, **extraia todos os arquivos** para uma pasta local antes de continuar.

### Passo 1: Acessar a Pasta do Projeto no Terminal
Abra o seu terminal (ou o terminal integrado do VS Code) e mude para o diretório raiz da pasta extraída:
```bash
cd PROJETO_FINAL

---

### 📄 PARTE 2 (Copie e cole logo abaixo da Parte 1, no mesmo arquivo)

```markdown
---

## 👁️ Como Abrir e Visualizar o Código Corretamente

Se você é o **desenvolvedor de design (front-end)** ou o **professor avaliador** e deseja inspecionar, alterar ou analisar a estrutura do código, siga estas instruções:

### 1. Abrir a Pasta no Editor (VS Code recomendado)
1. Abra o seu editor de código (como o VS Code).
2. Vá no menu superior em **File (Arquivo) > Open Folder (Abrir Pasta)**.
3. Selecione a pasta raiz do projeto: `PROJETO_FINAL`.
> ⚠️ **Nota:** Evite abrir os arquivos HTML soltos arrastando-os direto para o navegador. Como eles utilizam a estrutura de rotas do Flask e o motor de renderização Jinja2 (`{{ ... }}`), eles só funcionam corretamente se a pasta inteira estiver aberta no editor e o servidor local estiver rodando de forma ativa.

### 2. Onde encontrar o código de Back-end (Lógica e Banco)
* Abra o arquivo **`app.py`** na raiz do projeto. Nele você encontrará todas as configurações de rotas, validações de sessão, restrições de e-mail e as conexões diretas do SQLite3.

### 3. Onde encontrar o código de Front-end (Design e Telas)
* **Para alterar a estrutura ou textos das páginas:** Abra a pasta `templates/` na barra lateral. Cada arquivo `.html` ali representa uma tela isolada do sistema.
* **Para alterar cores, fontes, layouts e estilos:** Abra a pasta `static/css/` e clique no arquivo **`style.css`**. É neste arquivo que toda a mágica do design e a identidade visual do projeto devem ser construídas.

---

## 🧠 Entendendo o Ambiente de Desenvolvimento (Conceitos Chave)

Antes de rodar o sistema em uma nova máquina, é fundamental compreender o papel dos seguintes componentes técnicos para evitar conflitos no sistema:

### 1. O que é a `.venv` (Ambiente Virtual)?
A pasta `.venv` funciona como uma **caixa isolada** dentro do computador. O Python instalado no sistema operacional pode ter várias bibliotecas em versões diferentes que entram em conflito com este projeto. 
* **Por que ativar?** Ao ativar a `.venv`, garantimos que todos os comandos executados (como a instalação do Flask) fiquem trancados dentro desta pasta específica do projeto, protegendo o resto do computador e garantindo que o sistema rode exatamente com as versões corretas.

### 2. O que é o arquivo `requirements.txt`?
Este arquivo é a **receita/lista de compras** do projeto. Como as bibliotecas de código ocupam muito espaço, elas não devem ser enviadas diretamente por repositórios ou e-mail. Em vez disso, listamos os nomes e versões exatas de tudo o que o projeto precisa para funcionar dentro deste arquivo de texto.
* **Por que instalar?** Quando uma pessoa baixa o projeto pela primeira vez em outra máquina, o Python dela não sabe o que é o Flask. O comando `pip install -r requirements.txt` lê este arquivo e baixa automaticamente todas as ferramentas necessárias direto para dentro da `.venv`.

---

## 🏁 Passo a Passo: Como Executar o Projeto Localmente

> ⚠️ **IMPORTANTE (AMBIENTE ISOLADO):** Este projeto utiliza um Ambiente Virtual (`.venv`) para garantir que as dependências do Flask não entrem em conflito com outros projetos no seu computador. É altamente recomendável ativar ou criar a `.venv` antes de instalar os requisitos para manter o seu sistema limpo e isolado.

Siga rigorosamente as instruções abaixo para preparar o ambiente e colocar o sistema para funcionar:

### Passo 0: Baixar o Código na Máquina
Certifique-se de que o código fonte do projeto foi baixado para o seu computador. Caso tenha recebido o projeto compactado em formato `.zip` ou `.rar`, **extraia todos os arquivos** para uma pasta local antes de continuar.

### Passo 1: Acessar a Pasta do Projeto no Terminal
Abra o seu terminal (ou o terminal integrado do VS Code) e mude para o diretório raiz da pasta extraída:
```bash