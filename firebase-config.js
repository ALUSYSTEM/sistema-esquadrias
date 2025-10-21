// Configuração do Firebase
// IMPORTANTE: Substitua essas configurações pelas suas próprias do Firebase Console
const firebaseConfig = {
    apiKey: "AIzaSyCQ0NaNrF4gT9BqZQrXnMfJ60d5fsHyhTY",
    authDomain: "alubras-logistica.firebaseapp.com",
    projectId: "alubras-logistica",
    storageBucket: "alubras-logistica.firebasestorage.app",
    messagingSenderId: "504511643307",
    appId: "1:504511643307:web:aca9eb724c785de1e101ee"
};

// Aguardar carregamento dos módulos Firebase
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Importar módulos Firebase dinamicamente
        const { initializeApp } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js');
        const { getFirestore, collection, doc, addDoc, updateDoc, deleteDoc, getDocs, getDoc, query, orderBy, where, onSnapshot } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js');
        const { getAuth, signInWithEmailAndPassword, signOut, onAuthStateChanged, createUserWithEmailAndPassword } = await import('https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js');

        // Inicializar Firebase
        const app = initializeApp(firebaseConfig);
        const db = getFirestore(app);
        const auth = getAuth(app);

        // Exportar para uso global
        window.firebase = {
            db,
            auth,
            app,
            collection,
            doc,
            addDoc,
            updateDoc,
            deleteDoc,
            getDocs,
            getDoc,
            query,
            orderBy,
            where,
            onSnapshot,
            signInWithEmailAndPassword,
            signOut,
            onAuthStateChanged,
            createUserWithEmailAndPassword
        };

        console.log('Firebase inicializado com sucesso!');
        
        // Disparar evento customizado quando Firebase estiver pronto
        window.dispatchEvent(new CustomEvent('firebaseReady'));
        
    } catch (error) {
        console.error('Erro ao inicializar Firebase:', error);
        
        // Mostrar mensagem de erro mais clara
        if (error.message.includes('api-key-not-valid') || firebaseConfig.apiKey === 'sua-api-key-aqui') {
            setTimeout(() => {
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-danger position-fixed';
                alertDiv.style.top = '20px';
                alertDiv.style.right = '20px';
                alertDiv.style.zIndex = '9999';
                alertDiv.style.maxWidth = '400px';
                alertDiv.innerHTML = `
                    <h5><i class="fas fa-exclamation-triangle"></i> Configuração Firebase Necessária</h5>
                    <p><strong>Erro:</strong> API Key inválida</p>
                    <p><strong>Solução:</strong></p>
                    <ol>
                        <li>Abra <code>firebase-config.js</code></li>
                        <li>Substitua as configurações pelas suas credenciais do Firebase Console</li>
                        <li>Consulte <code>CONFIGURAR-FIREBASE.md</code> para instruções</li>
                    </ol>
                    <button class="btn btn-sm btn-outline-danger" onclick="this.parentElement.remove()">Fechar</button>
                `;
                document.body.appendChild(alertDiv);
            }, 1000);
        }
    }
});
