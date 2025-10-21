# 🚀 Deploy Atualizado - Sistema com Login e Usuários

## ⚠️ **AVISO IMPORTANTE**

O sistema atual **MUDOU** de arquivos HTML estáticos para uma **aplicação Flask completa** com:
- ✅ Sistema de usuários
- ✅ Login com e-mail
- ✅ Banco de dados SQLite
- ✅ Controle de permissões

**O deploy anterior (Netlify/Firebase) não funcionará** porque não suporta Python Flask.

## 🆕 **OPÇÕES PARA DEPLOY ATUALIZADO:**

### **Opção 1: Railway.app (RECOMENDADO - Gratuito)**

1. **Acesse:** https://railway.app
2. **Crie conta gratuita**
3. **Clique "Deploy from GitHub repo"**
4. **Selecione seu projeto** (se estiver no GitHub)

**OU**

1. **Instale Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```
2. **No terminal:**
   ```bash
   railway login
   railway init
   railway up
   ```

### **Opção 2: Render.com (Gratuito)**

1. **Acesse:** https://render.com
2. **Conecte sua conta GitHub**
3. **Create New → Web Service**
4. **Selecione seu repositório**
5. **Build Command:** `pip install -r requirements.txt`
6. **Start Command:** `python app.py`

### **Opção 3: PythonAnywhere (Fácil)**

1. **Acesse:** https://pythonanywhere.com
2. **Crie conta gratuita**
3. **Upload dos arquivos**
4. **Configure Web App**

### **Opção 4: Vercel (Limitado)**

1. **Acesse:** https://vercel.com
2. **Upload projeto**
3. **Configure para Python**

## 📁 **Arquivos Necessários para Deploy:**

```
sistema_esquadrias/
├── app.py                 # ← APLICACAO PRINCIPAL
├── requirements.txt       # ← DEPENDENCIAS
├── config.py
├── templates/            # ← TEMPLATES ATUALIZADOS
├── static/
├── instance/            # ← BANCO DE DADOS (será criado)
└── README.md
```

## ⚡ **RAILWAY - Passo a Passo Rápido:**

1. **GitHub Setup:**
   ```bash
   git init
   git add .
   git commit -m "Sistema atualizado com usuários"
   git remote add origin SEU_REPOSITORIO_GITHUB
   git push -u origin main
   ```

2. **Railway Deploy:**
   - Login em railway.app
   - "Deploy from GitHub repo"
   - Selecione repositório
   - **AUTO DEPLOY!** 🎉

## 🎯 **Resultado:**

Você terá um link como:
- `https://sistema-esquadrias.railway.app`
- `https://sistema-esquadrias.onrender.com`

## 📋 **Verificações Pós-Deploy:**

✅ Sistema funciona em: `https://SEU-LINK.com`
✅ Login funciona: `admin` / `admin123`
✅ E-mail de login funciona
✅ Menu "Usuários" aparece para admin
✅ Criação de usuários funciona

## 🔧 **Se Houver Problemas:**

1. **Verificar logs** na plataforma de deploy
2. **Banco de dados** será criado automaticamente
3. **Dependências** serão instaladas automaticamente

---

**IMPORTANTE:** O deploy anterior (HTML estático) não terá essas funcionalidades. 
É necessário fazer um novo deploy com suporte a Python Flask.
