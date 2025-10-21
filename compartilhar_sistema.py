#!/usr/bin/env python3
"""
Script para compartilhar o sistema ALUBRAS via rede local
"""

import socket
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import time

def get_local_ip():
    """Obtém o IP local da máquina"""
    try:
        # Conecta a um endereço remoto para descobrir o IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def start_server(port=8000):
    """Inicia o servidor HTTP"""
    try:
        server = HTTPServer(('', port), SimpleHTTPRequestHandler)
        print(f"🔥 Sistema ALUBRAS rodando em:")
        print(f"   Local: http://localhost:{port}")
        print(f"   Rede:  http://{get_local_ip()}:{port}")
        print(f"   📱 Compartilhe este link com seus usuários!")
        print(f"   Pressione Ctrl+C para parar")
        
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Servidor parado!")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    port = 8000
    
    # Tenta encontrar uma porta livre
    while port < 8010:
        try:
            start_server(port)
            break
        except OSError:
            port += 1
            if port >= 8010:
                print("❌ Nenhuma porta disponível encontrada!")
                exit(1)
