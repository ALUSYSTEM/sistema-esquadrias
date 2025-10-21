# Configuração do Firebase para Sistema de Esquadrias

## 1. Configuração do Projeto Firebase

### Passo 1: Criar Projeto no Firebase
1. Acesse [Firebase Console](https://console.firebase.google.com/)
2. Clique em "Criar um projeto"
3. Nome do projeto: `sistema-esquadrias` (ou seu nome preferido)
4. Ative o Google Analytics (opcional)
5. Clique em "Criar projeto"

### Passo 2: Configurar Firestore Database
1. No menu lateral, clique em " Firestore Database"
2. Clique em "Criar banco de dados"
3. Escolha "Modo de teste" (para desenvolvimento)
4. Selecione uma localização (us-east1 recomendado para Brasil)

### Passo 3: Configurar Authentication
1. No menu lateral, clique em "Authentication"
2. Clique na aba "Sign-in method"
3. Habilite "Email/Password"
4. Configure as regras conforme necessário

### Passo 4: Obter Configurações do Projeto
1. No menu lateral, clique na engrenagem → "Configurações do projeto"
2. Role para baixo até "Seus aplicativos"
3. Clique em "</>" para adicionar app web
4. Registre o app com o nome "Sistema Esquadrias"
5. Copie as configurações do Firebase

## 2. Atualizar Configurações

Altere o arquivo `firebase-config.js` com suas configurações:

```javascript
const firebaseConfig = {
    apiKey: "sua-api-key-aqui",
    authDomain: "seu-projeto.firebaseapp.com",
    projectId: "seu-projeto-id",
    storageBucket: "seu-projeto.appspot.com",
    messagingSenderId: "123456789",
    appId: "1:123456789:web:abcdef123456"
};
```

## 3. Estrutura de Dados no Firestore

### Coleção: `usuarios`
```json
{
  "uid": "string (ID do usuário Firebase Auth)",
  "email": "string",
  "nome": "string",
  "role": "admin" | "user",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Coleção: `obras`
```json
{
  "nome": "string",
  "endereco": "string",
  "cliente": "string",
  "data_inicio": "timestamp",
  "data_prevista": "timestamp",
  "status": "Em Andamento" | "Concluída" | "Pausada",
  "observacoes": "string",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Coleção: `esquadrias`
```json
{
  "obra_id": "string (ID da obra)",
  "tipo": "string",
  "dimensoes": "string",
  "material": "string",
  "cor": "string",
  "quantidade": "number",
  "status": "Pendente" | "Produzida" | "Entregue",
  "data_producao": "timestamp",
  "data_entrega": "timestamp",
  "observacoes": "string",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Coleção: `materiais`
```json
{
  "nome": "string",
  "tipo": "string",
  "descricao": "string",
  "quantidade_estoque": "number",
  "quantidade_minima": "number",
  "unidade": "string",
  "preco_unitario": "number",
  "fornecedor": "string",
  "especificacoes": "string",
  "status_alerta": "normal" | "atencao" | "critico",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Coleção: `movimentacoes_estoque`
```json
{
  "material_id": "string (ID do material)",
  "tipo_movimentacao": "entrada" | "saida" | "ajuste",
  "quantidade": "number",
  "quantidade_anterior": "number",
  "quantidade_atual": "number",
  "motivo": "string",
  "observacoes": "string",
  "usuario_id": "string (ID do usuário)",
  "created_at": "timestamp"
}
```

### Coleção: `manutencao_caminhoes`
```json
{
  "placa": "string",
  "data_manutencao": "timestamp",
  "tipo_manutencao": "string",
  "descricao": "string",
  "valor_total": "number",
  "km_veiculo": "number",
  "fornecedor_servico": "string",
  "observacoes": "string",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

### Coleção: `programacao_entrega`
```json
{
  "numero_expedicao": "string",
  "obra_id": "string (ID da obra)",
  "percentual_liberacao": "number (1-100)",
  "data_carregamento": "timestamp",
  "data_entrega": "timestamp",
  "caminhoneiro": "string",
  "status": "Programado" | "Carregado" | "Entregue" | "Cancelado",
  "observacoes": "string",
  "created_at": "timestamp",
  "updated_at": "timestamp"
}
```

## 4. Regras de Segurança do Firestore

Configure no Firebase Console → Firestore Database → Regras:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Usuários autenticados podem ler/escrever seus próprios dados
    match /usuarios/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Apenas usuários autenticados podem acessar outras coleções
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## 5. Como Executar

1. Abra o arquivo `index.html` em um servidor web local
2. Use o Live Server (VS Code) ou qualquer servidor HTTP
3. Acesse através do navegador
4. Faça login com as credenciais configuradas no Firebase Auth

## 6. Primeiro Usuário

Para criar o primeiro usuário admin, você pode:

1. Usar o Firebase Console → Authentication → Users → Add user
2. Ou implementar um formulário de registro no sistema
3. Adicionar manualmente o documento na coleção `usuarios` com role: "admin"

## 7. Funcionalidades em Tempo Real

O sistema utiliza listeners do Firestore para atualizações em tempo real:
- Dashboard com estatísticas atualizadas automaticamente
- Lista de materiais sincronizada
- Alertas de estoque em tempo real
- Notificações de mudanças

## 8. Estrutura de Arquivos

```
sistema_esquadrias/
├── index.html              # Página principal
├── firebase-config.js      # Configuração do Firebase
├── css/
│   └── style.css          # Estilos customizados
├── js/
│   └── app.js            # Lógica principal da aplicação
└── firebase-setup.md     # Este arquivo de instruções
```
