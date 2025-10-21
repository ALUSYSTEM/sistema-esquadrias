#!/usr/bin/env python3
"""
Script para testar o sistema de esquadrias
"""

import sys
import os

def testar_imports():
    """Testa se todas as dependências estão disponíveis"""
    print("🔍 Testando imports...")
    
    try:
        import flask
        print("✅ Flask OK")
    except ImportError as e:
        print(f"❌ Flask: {e}")
        return False
    
    try:
        import flask_sqlalchemy
        print("✅ Flask-SQLAlchemy OK")
    except ImportError as e:
        print(f"❌ Flask-SQLAlchemy: {e}")
        return False
    
    try:
        import flask_login
        print("✅ Flask-Login OK")
    except ImportError as e:
        print(f"❌ Flask-Login: {e}")
        return False
    
    try:
        import werkzeug
        print("✅ Werkzeug OK")
    except ImportError as e:
        print(f"❌ Werkzeug: {e}")
        return False
    
    return True

def testar_estrutura():
    """Testa se a estrutura de arquivos está correta"""
    print("\n📁 Testando estrutura de arquivos...")
    
    arquivos_necessarios = [
        'app.py',
        'requirements.txt',
        'config.py',
        'templates/base.html',
        'templates/login.html',
        'templates/dashboard.html',
        'static/css/style.css',
        'static/js/main.js'
    ]
    
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")
            return False
    
    return True

def testar_app():
    """Testa se a aplicação pode ser importada"""
    print("\n🚀 Testando aplicação...")
    
    try:
        # Adicionar o diretório atual ao path
        sys.path.insert(0, os.getcwd())
        
        # Importar a aplicação
        from app import app, db, User
        
        print("✅ Aplicação importada com sucesso")
        
        # Testar criação do contexto
        with app.app_context():
            print("✅ Contexto da aplicação criado")
            
            # Testar criação das tabelas
            db.create_all()
            print("✅ Tabelas do banco criadas")
            
            # Testar criação do usuário admin
            admin = User.query.filter_by(username='admin').first()
            if admin:
                print("✅ Usuário admin encontrado")
            else:
                print("⚠️  Usuário admin não encontrado (será criado na primeira execução)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar aplicação: {e}")
        return False

def main():
    """Função principal de teste"""
    print("=" * 50)
    print("🧪 TESTE DO SISTEMA DE ESQUADRIAS")
    print("=" * 50)
    
    # Testar imports
    if not testar_imports():
        print("\n❌ FALHA: Dependências não encontradas")
        print("Execute: pip install -r requirements.txt")
        return False
    
    # Testar estrutura
    if not testar_estrutura():
        print("\n❌ FALHA: Estrutura de arquivos incompleta")
        return False
    
    # Testar aplicação
    if not testar_app():
        print("\n❌ FALHA: Erro na aplicação")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 TODOS OS TESTES PASSARAM!")
    print("=" * 50)
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Execute: python app.py")
    print("2. Acesse: http://localhost:5000")
    print("3. Login: admin / admin123")
    print("\n🚀 Sistema pronto para uso!")
    
    return True

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1)
