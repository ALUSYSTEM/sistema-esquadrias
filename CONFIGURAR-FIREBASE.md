# 🔥 Configuração Rápida do Firebase

## 🚨 **Erro Atual:** `auth/api-key-not-valid`

Isso acontece porque você está usando as configurações de exemplo. Siga estes passos:

## 📋 **Passo a Passo - 5 minutos**

### 1. **Criar Projeto Firebase**
1. Vá para: https://console.firebase.google.com/
2. Clique em **"Criar um projeto"**
3. Nome: `sistema-esquadrias` (ou qualquer nome)
4. Ative Google Analytics: **NÃO** (opcional)
5. Clique **"Criar projeto"**

### 2. **Configurar Firestore Database**
1. No menu lateral, clique **"Firestore Database"**
2. Clique **"Criar banco de dados"**
3. Escolha **"Modo de teste"** ✅
4. Localização: **us-east1** (recomendado)
5. Clique **"Concluído"**

### 3. **Configurar Authentication**
1. No menu lateral, clique **"Authentication"**
2. Clique na aba **"Sign-in method"**
3. Clique em **"Email/Senha"**
4. Ative a primeira opção ✅
5. Clique **"Salvar"**

### 4. **Obter Configurações**
1. No menu lateral, clique na **engrenagem** ⚙️
2. Clique **"Configurações do projeto"**
3. Role para baixo até **"Seus aplicativos"**
4. Clique no ícone **"</>"** (Web)
5. Nome do app: `Sistema Esquadrias`
6. **NÃO** marque "Também configure o Firebase Hosting"
7. Clique **"Registrar app"**

### 5. **Copiar e Colar**
Copie as configurações que aparecem assim:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSyC...", // ← Sua chave real
  authDomain: "seu-projeto.firebaseapp.com",
  projectId: "seu-projeto-id",
  storageBucket: "seu-projeto.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef123456"
};
```

### 6. **Atualizar Arquivo**
1. Abra o arquivo `firebase-config.js`
2. Substitua as linhas 3-10 pelas suas configurações reais
3. Salve o arquivo
4. Recarregue a página no navegador

## 🧪 **Criar Primeiro Usuário**

### Método 1: Firebase Console
1. Vá para **Authentication** → **Users**
2. Clique **"Add user"**
3. Email: `admin@sistema.com`
4. Senha: `admin123`
5. Clique **"Add user"**

### Método 2: Registrar no Sistema
Após configurar, o sistema permitirá criar usuários automaticamente.

## 🔧 **Regras de Segurança (Opcional)**

No Firestore Database → Rules, cole:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.auth != null;
    }
  }
}
```

## ✅ **Teste Final**

1. Recarregue a página
2. Faça login com o usuário criado
3. Você deve ver o dashboard funcionando!

---

**Tempo total: ~5 minutos** ⏱️
