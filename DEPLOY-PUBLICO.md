# 🌐 Criar Link Público - Sistema ALUBRAS

## 🚀 **Opção 1: Netlify Drop (MAIS RÁPIDO - 2 minutos)**

### **Passos:**
1. **Vá para:** https://app.netlify.com/drop
2. **Arraste seus arquivos** para a área de drop:
   - `index.html`
   - `firebase-config.js`
   - `js/` (pasta inteira)
   - `css/` (pasta inteira)
   - `static/` (pasta inteira)
3. **Aguarde 30 segundos** para o deploy
4. **Receba seu link:** `https://insane-nome-aleatorio.netlify.app`

### **Vantagens:**
- ✅ Gratuito
- ✅ Link público instantâneo
- ✅ HTTPS automático
- ✅ Sem configuração

## 🔥 **Opção 2: Firebase Hosting (PERMANENTE)**

### **Método 1: Console Web**
1. **Acesse:** https://console.firebase.google.com/project/alubras-logistica/hosting
2. **Clique "Get started"**
3. **Clique "Next"** até chegar na opção de upload
4. **Arraste os arquivos** principais
5. **Deploy automático**

### **Método 2: CLI (se tiver Node.js)**
```bash
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy
```

## 📁 **Arquivos necessários para upload:**

```
📦 Arquivos principais:
├── index.html
├── firebase-config.js
├── firebase.json
├── css/
│   └── style.css
├── js/
│   ├── app.js
│   └── local-storage.js
└── static/
    ├── css/
    ├── js/
    └── images/
```

## 🎯 **Resultado Final:**

**Link público que você receberá:**
- Netlify: `https://sua-app.netlify.app`
- Firebase: `https://alubras-logistica.web.app`

**Ambos funcionarão perfeitamente com seu sistema!**
