# 🚀 Deploy no Firebase Hosting - Link Público

## ✅ **Status Atual:**
- ✅ Firebase configurado
- ✅ Credenciais inseridas
- ✅ Sistema funcionando localmente

## 🌐 **Para gerar link público:**

### **Método 1: Console do Firebase (Recomendado)**

1. **Acesse:** https://console.firebase.google.com/project/alubras-logistica/hosting
2. **Clique "Get started"** ou **"Começar"**
3. **Instale o Firebase CLI** (se necessário):
   ```
   npm install -g firebase-tools
   ```
4. **Faça login:**
   ```
   firebase login
   ```
5. **Inicialize o projeto:**
   ```
   firebase init hosting
   ```
6. **Deploy:**
   ```
   firebase deploy
   ```

### **Método 2: Upload Manual**

1. **No Firebase Console → Hosting**
2. **Clique "Connect domain"** ou use o domínio padrão
3. **Upload dos arquivos** (arrastar e soltar)

## 🎯 **Resultado:**
Você terá um link público como:
- `https://alubras-logistica.web.app`
- `https://alubras-logistica.firebaseapp.com`

## 📱 **Links atuais para usar:**

**Imediato (Rede Local):**
- `http://192.168.0.204:8000`

**Usuários de teste:**
- Email: `admin@alubras.com`
- Senha: `admin123`

## 🔧 **Próximos passos:**
1. Configure o Firestore Database (modo teste)
2. Configure Authentication (Email/Senha)
3. Crie o primeiro usuário
4. Faça deploy no Hosting para link público
