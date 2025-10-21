# Sistema de Esquadrias - Versão Firebase

## 🚀 Nova Arquitetura

O sistema foi completamente migrado de Flask/SQLite para **HTML5 + CSS + Firebase**, proporcionando:

- ✅ **Sincronização em tempo real** de todos os dados
- ✅ **Interface moderna e responsiva** 
- ✅ **Autenticação segura** via Firebase Auth
- ✅ **Banco de dados NoSQL** escalável
- ✅ **Acesso via navegador** sem necessidade de servidor local

## 📁 Estrutura do Projeto

```
sistema_esquadrias/
├── index.html              # Página principal única
├── firebase-config.js      # Configuração do Firebase
├── css/
│   └── style.css          # Estilos customizados
├── js/
│   └── app.js            # Lógica completa da aplicação
├── firebase-setup.md     # Guia de configuração do Firebase
└── README-FIREBASE.md    # Este arquivo
```

## 🛠️ Como Configurar

### 1. Configuração do Firebase

1. **Crie um projeto no Firebase Console:**
   - Acesse [Firebase Console](https://console.firebase.google.com/)
   - Crie um novo projeto chamado `sistema-esquadrias`

2. **Configure o Firestore Database:**
   - Ative o Firestore Database em modo de teste
   - Configure as regras de segurança (veja `firebase-setup.md`)

3. **Configure Authentication:**
   - Ative Email/Password no Firebase Auth

4. **Obtenha as configurações:**
   - Copie as configurações do projeto (web app)
   - Cole no arquivo `firebase-config.js`

### 2. Executar o Sistema

1. **Servidor Local:**
   ```bash
   # Usando Python
   python -m http.server 8000
   
   # Usando Node.js
   npx serve .
   
   # Usando VS Code Live Server
   # Clique direito em index.html → "Open with Live Server"
   ```

2. **Acessar:**
   - Abra o navegador em `http://localhost:8000`
   - Faça login com as credenciais do Firebase Auth

## 🎯 Funcionalidades

### ✅ Implementadas
- **Dashboard** com estatísticas em tempo real
- **Autenticação** completa via Firebase Auth
- **Gestão de Materiais** com CRUD completo
- **Alertas de Estoque** automáticos
- **Interface Responsiva** para mobile/desktop
- **Sincronização em Tempo Real** de todos os dados

### 🚧 Em Desenvolvimento
- Gestão completa de Obras
- Gestão de Esquadrias
- Manutenção de Caminhões
- Programação de Entregas
- Sistema de Usuários
- Relatórios e Exportações

## 🔥 Vantagens da Nova Arquitetura

### Tempo Real
- Dados sincronizados instantaneamente entre todos os usuários
- Notificações automáticas de mudanças
- Dashboard sempre atualizado

### Escalabilidade
- Firebase escala automaticamente
- Suporta milhares de usuários simultâneos
- Backup automático dos dados

### Mobilidade
- Funciona em qualquer dispositivo
- Interface adaptável (mobile-first)
- Acesso offline com sincronização posterior

### Segurança
- Autenticação robusta do Firebase
- Regras de segurança configuráveis
- Dados criptografados em trânsito

## 🎨 Interface

### Design Moderno
- **Bootstrap 5** para componentes
- **Font Awesome** para ícones
- **CSS Customizado** para identidade visual
- **Animações suaves** e transições

### Páginas Principais
1. **Login** - Autenticação segura
2. **Dashboard** - Visão geral do sistema
3. **Materiais** - Gestão completa de estoque
4. **Obras** - Controle de projetos
5. **Esquadrias** - Gestão de produtos
6. **Manutenção** - Controle de veículos
7. **Entregas** - Programação logística

## 🔧 Desenvolvimento

### Tecnologias Utilizadas
- **HTML5** - Estrutura semântica
- **CSS3** - Estilos modernos e responsivos
- **JavaScript ES6+** - Lógica da aplicação
- **Firebase** - Backend completo
- **Bootstrap 5** - Framework CSS
- **Font Awesome** - Ícones

### Estrutura do Código
```javascript
class SistemaEsquadrias {
    // Gerenciamento de estado
    // Autenticação
    // CRUD operations
    // Real-time updates
    // UI management
}
```

## 📱 Responsividade

O sistema é totalmente responsivo:
- **Desktop** - Interface completa
- **Tablet** - Layout adaptado
- **Mobile** - Navegação otimizada

## 🚀 Próximos Passos

1. **Configurar Firebase** seguindo `firebase-setup.md`
2. **Testar funcionalidades** básicas
3. **Adicionar dados** de teste
4. **Implementar** funcionalidades restantes
5. **Deploy** para produção (Firebase Hosting)

## 🆘 Suporte

Para dúvidas ou problemas:
1. Verifique o console do navegador (F12)
2. Confirme a configuração do Firebase
3. Teste a conexão com o Firestore
4. Consulte `firebase-setup.md` para detalhes

---

**Sistema de Esquadrias ALUBRAS** - Versão Firebase ✨
