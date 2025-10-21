// Script para testar limites de armazenamento
function testarLimitesLocalStorage() {
    console.log('🧪 Testando limites de armazenamento...');
    
    // Verificar espaço total disponível
    function getStorageSize() {
        let total = 0;
        for (let key in localStorage) {
            if (localStorage.hasOwnProperty(key)) {
                total += localStorage[key].length + key.length;
            }
        }
        return total;
    }
    
    // Converter bytes para formato legível
    function formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    const tamanhoAtual = getStorageSize();
    console.log(`📊 Tamanho atual usado: ${formatBytes(tamanhoAtual)}`);
    
    // Testar quantos registros cabem
    function testarCapacidade() {
        const prefix = 'sistema_esquadrias_teste_';
        const tamanhoRegistro = JSON.stringify({
            id: Date.now(),
            nome: 'Teste de Obra',
            cliente: 'Cliente Teste',
            endereco: 'Endereço de teste com informações completas',
            status: 'Em Andamento',
            data_inicio: new Date().toISOString(),
            data_prevista: new Date().toISOString(),
            descricao: 'Descrição detalhada da obra para teste de capacidade',
            created_at: new Date().toISOString()
        }).length;
        
        console.log(`📝 Tamanho médio por registro: ${formatBytes(tamanhoRegistro)}`);
        
        // Limite típico do localStorage: 5-10MB
        const limiteMB = 5; // MB
        const limiteBytes = limiteMB * 1024 * 1024;
        
        const registrosPossiveis = Math.floor(limiteBytes / tamanhoRegistro);
        
        console.log(`🔢 Registros possíveis (estimativa): ~${registrosPossiveis.toLocaleString()}`);
        
        return {
            tamanhoRegistro,
            limiteMB,
            registrosPossiveis
        };
    }
    
    const stats = testarCapacidade();
    
    console.log(`
📋 RESUMO DOS LIMITES:

💾 LocalStorage (navegador):
   • Limite total: ~${stats.limiteMB}MB
   • Registros estimados: ~${stats.registrosPossiveis.toLocaleString()}
   • Tamanho por item: ~${formatBytes(stats.tamanhoRegistro)}

🔥 Firebase (nuvem):
   • Limite: Ilimitado (plano gratuito: 1GB)
   • Registros: Milhões de documentos
   • Backup: Automático em múltiplos servidores

📊 Seu uso atual: ${formatBytes(tamanhoAtual)}
    `);
    
    return stats;
}

// Executar teste
if (typeof window !== 'undefined') {
    window.testarLimites = testarLimitesLocalStorage;
}
