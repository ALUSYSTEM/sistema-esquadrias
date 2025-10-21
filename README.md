# Sistema de Esquadrias

Sistema completo para gerenciamento de obras, esquadrias e materiais de embalagem.

## 🚀 Funcionalidades

- **Dashboard** com estatísticas em tempo real
- **Gestão de Obras** - Cadastro e acompanhamento de obras
- **Gestão de Esquadrias** - Controle de produção e entrega
- **Materiais de Embalagem** - Controle de estoque
- **Sistema de Usuários** - Controle de acesso e permissões
- **Interface Responsiva** - Funciona em desktop e mobile

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

1. **Clone ou baixe o projeto**
   ```bash
   # Se estiver usando git
   git clone <url-do-repositorio>
   cd sistema_esquadrias
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o sistema**
   ```bash
   python app.py
   ```

4. **Acesse o sistema**
   - Abra seu navegador
   - Acesse: `http://localhost:5000`
   - **Usuário padrão:** `admin`
   - **Senha padrão:** `admin123`

## 📁 Estrutura do Projeto

```
sistema_esquadrias/
├── app.py                 # Aplicação principal
├── config.py             # Configurações
├── requirements.txt      # Dependências
├── README.md            # Este arquivo
├── templates/           # Templates HTML
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── obras.html
│   ├── esquadrias.html
│   └── materiais.html
├── static/              # Arquivos estáticos
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
├── instance/            # Banco de dados
└── logs/               # Logs do sistema
```

## 🎯 Como Usar

### 1. Primeiro Acesso
- Faça login com `admin` / `admin123`
- Altere a senha padrão em "Usuários"
- Crie novos usuários conforme necessário

### 2. Cadastrar Obra
- Vá em "Obras" → "Nova Obra"
- Preencha as informações da obra
- Salve para começar a cadastrar esquadrias

### 3. Cadastrar Esquadrias
- Vá em "Esquadrias" → "Nova Esquadria"
- Selecione a obra
- Preencha tipo, dimensões, material, etc.
- Acompanhe o status (Pendente → Produzida → Entregue)

### 4. Gerenciar Materiais
- Vá em "Materiais" → "Novo Material"
- Cadastre materiais de embalagem
- Configure estoque mínimo
- Acompanhe alertas de estoque baixo

## 🔧 Configurações

### Banco de Dados
- O sistema usa SQLite por padrão
- O banco é criado automaticamente na pasta `instance/`
- Para usar outro banco, edite `config.py`

### Personalização
- Edite `static/css/style.css` para personalizar cores e layout
- Modifique `templates/` para alterar a interface
- Adicione funcionalidades em `app.py`

## 📱 Acesso Mobile

O sistema é totalmente responsivo e funciona em:
- Computadores
- Tablets
- Smartphones

## 🔒 Segurança

- Sistema de login com hash de senhas
- Controle de sessão
- Proteção contra CSRF
- Validação de dados

## 🚀 Deploy em Produção

### Opção 1: Servidor Local
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar em produção
export FLASK_ENV=production
python app.py
```

### Opção 2: Servidor Web
- Use Gunicorn ou similar
- Configure proxy reverso (Nginx)
- Use banco PostgreSQL para produção

## 📊 Relatórios

O sistema gera relatórios automáticos:
- Dashboard com estatísticas
- Status de obras e esquadrias
- Alertas de estoque baixo
- Histórico de atividades

## 🆘 Suporte

### Problemas Comuns

1. **Erro de dependências**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Erro de banco de dados**
   - Delete o arquivo `instance/esquadrias.db`
   - Execute `python app.py` novamente

3. **Erro de porta em uso**
   - Mude a porta no `app.py` (linha final)
   - Ou pare outros processos na porta 5000

### Logs
- Verifique a pasta `logs/` para logs de erro
- Use o console do navegador (F12) para debug

## 🔄 Atualizações

Para atualizar o sistema:
1. Faça backup do banco de dados
2. Substitua os arquivos
3. Execute `python app.py`

## 📝 Licença

Este sistema foi desenvolvido para uso interno da empresa.

---

**Desenvolvido com ❤️ para gestão eficiente de esquadrias**
