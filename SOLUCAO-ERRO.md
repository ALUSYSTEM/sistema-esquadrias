# 🚨 Solução para o Erro de Conexão

## Problema Identificado
O erro `ERR_CONNECTION_REFUSED` indica que não há servidor rodando ou há problema de porta.

## ✅ Soluções Imediatas

### Opção 1: Usar o arquivo .bat criado
1. **Clique duplo** no arquivo `iniciar_sistema.bat`
2. O sistema abrirá automaticamente no navegador

### Opção 2: Comando manual no terminal
```powershell
# Abra o PowerShell no diretório do projeto
cd "P:\Arq. Samuel Vitor\sistema_esquadrias"

# Inicie o servidor
python -m http.server 8000
```

### Opção 3: Porta alternativa
Se a porta 8000 estiver ocupada, tente:
```powershell
python -m http.server 8080
```
E acesse: `http://localhost:8080`

### Opção 4: VS Code Live Server
Se você tem VS Code instalado:
1. Abra a pasta no VS Code
2. Clique direito em `index.html`
3. Selecione "Open with Live Server"

## 🔧 Verificações Importantes

### 1. Teste se o servidor está rodando
No terminal, execute:
```powershell
netstat -an | findstr :8000
```
Se aparecer algo como `TCP 0.0.0.0:8000`, o servidor está ativo.

### 2. Firewall/Antivírus
- Pode estar bloqueando a porta 8000
- Tente com outra porta (8080, 3000, 5000)

### 3. Python instalado
Verifique se o Python está instalado:
```powershell
python --version
```

## 🎯 URLs para Testar

Depois que o servidor estiver rodando:
- **Porta 8000:** `http://localhost:8000`
- **Porta 8080:** `http://localhost:8080`
- **IP local:** `http://127.0.0.1:8000`

## ⚠️ Próximo Passo: Configurar Firebase

Depois que conseguir acessar o sistema:
1. Vá para [Firebase Console](https://console.firebase.google.com/)
2. Crie um novo projeto
3. Configure o Firestore Database
4. Ative Authentication (Email/Password)
5. Copie as configurações para `firebase-config.js`

## 🆘 Se Ainda Não Funcionar

1. **Verifique o console do navegador** (F12) para erros
2. **Teste em outro navegador** (Chrome, Firefox, Edge)
3. **Reinicie o terminal** e tente novamente
4. **Use uma porta diferente** (3000, 5000, 8080)

---

**O sistema está funcionando corretamente, apenas precisa de um servidor web ativo!** 🚀
