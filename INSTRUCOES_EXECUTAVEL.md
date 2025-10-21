# Como Criar e Usar o Executável do Sistema de Esquadrias

## 📋 Pré-requisitos

- Python instalado no sistema
- Todas as dependências instaladas (`pip install -r requirements.txt`)

## 🔨 Como Construir o Executável

### Método 1: Usando o Script Automático (RECOMENDADO)

1. Execute o arquivo `build_executavel.bat`
2. Aguarde o processo completar (pode levar alguns minutos)
3. O executável estará em: `dist\Sistema_Esquadrias\`

### Método 2: Manual

1. Instale o PyInstaller:
   ```
   pip install pyinstaller==6.1.0
   ```

2. Execute o build:
   ```
   pyinstaller sistema_esquadrias.spec --clean
   ```

3. O executável estará em: `dist\Sistema_Esquadrias\`

## 🚀 Como Executar o Sistema

### Opção 1: Usando o Launcher
1. Vá para a pasta `dist\Sistema_Esquadrias\`
2. Execute o arquivo `executar.bat`
3. O navegador abrirá automaticamente em `http://localhost:5000`

### Opção 2: Manual
1. Vá para a pasta `dist\Sistema_Esquadrias\`
2. Execute `Sistema_Esquadrias.exe`
3. Abra seu navegador em `http://localhost:5000`

## 👤 Credenciais Padrão

- **Usuário:** admin
- **Senha:** admin123

## 📦 Distribuindo o Sistema

Para distribuir o sistema para outros computadores:

1. Copie toda a pasta `dist\Sistema_Esquadrias\` para o computador de destino
2. Execute o arquivo `executar.bat` ou `Sistema_Esquadrias.exe`
3. Não é necessário instalar Python ou dependências!

## 📁 Estrutura do Executável

```
dist\Sistema_Esquadrias\
├── Sistema_Esquadrias.exe  (Executável principal)
├── executar.bat            (Launcher com abertura automática do navegador)
├── templates\              (Arquivos HTML)
├── static\                 (CSS, JS, Imagens)
├── instance\               (Banco de dados)
└── [diversos arquivos DLL e dependências]
```

## ⚠️ Observações Importantes

1. **Banco de Dados:** O banco de dados SQLite está na pasta `instance\`. Os dados são salvos lá.

2. **Primeiro Uso:** Na primeira execução, o sistema criará automaticamente:
   - O banco de dados
   - O usuário administrador padrão

3. **Firewall:** O Windows pode pedir permissão para o programa acessar a rede. Permita o acesso.

4. **Antivírus:** Alguns antivírus podem alertar sobre executáveis criados com PyInstaller. Isso é um falso positivo comum.

5. **Porta 5000:** O sistema usa a porta 5000. Certifique-se de que ela está disponível.

## 🔧 Resolução de Problemas

### Erro: "Porta já em uso"
- Outra aplicação está usando a porta 5000
- Feche outros processos ou mude a porta no código

### Erro: "Arquivo não encontrado"
- Certifique-se de executar o .exe de dentro da pasta `dist\Sistema_Esquadrias\`
- Não mova o .exe para outra pasta sozinho

### Sistema não abre no navegador
- Abra manualmente: `http://localhost:5000`
- Ou tente: `http://127.0.0.1:5000`

### Banco de dados não persiste
- Verifique se a pasta `instance\` tem permissão de escrita
- Execute como administrador se necessário

## 📝 Personalização

### Mudar Porta ou Host
Edite o arquivo `app.py` antes de construir:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Adicionar Ícone
1. Coloque um arquivo .ico na raiz do projeto
2. Edite `sistema_esquadrias.spec`:
   ```python
   icon='seu_icone.ico',
   ```
3. Reconstrua o executável

## 📞 Suporte

Para problemas ou dúvidas:
- Verifique os logs no console
- Verifique a pasta `logs\` (se existir)
- Execute em modo debug para mais informações

