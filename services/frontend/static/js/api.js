const API = {
    LIVRES: 'http://localhost:8001/api',
    UTILISATEURS: 'http://localhost:8002/api',
    EMPRUNTS: 'http://localhost:8003/api',
    RECO: 'http://localhost:8004',
};

async function fetchAPI(url, options = {}) {
    try {
        const res = await fetch(url, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        if (!res.ok) throw new Error(`Erreur ${res.status}`);
        return await res.json();
    } catch (e) {
        console.error('API Error:', e);
        throw e;
    }
}

// Livres
const LivresAPI = {
    lister: () => fetchAPI(`${API.LIVRES}/livres/`),
    detail: (id) => fetchAPI(`${API.LIVRES}/livres/${id}/`),
    creer: (data) => fetchAPI(`${API.LIVRES}/livres/`, { method: 'POST', body: JSON.stringify(data) }),
    modifier: (id, data) => fetchAPI(`${API.LIVRES}/livres/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }),
    supprimer: (id) => fetchAPI(`${API.LIVRES}/livres/${id}/`, { method: 'DELETE' }),
    rechercher: (q) => fetchAPI(`${API.LIVRES}/livres/recherche/?q=${encodeURIComponent(q)}`),
};

// Utilisateurs
const UtilisateursAPI = {
    lister: () => fetchAPI(`${API.UTILISATEURS}/utilisateurs/`),
    detail: (id) => fetchAPI(`${API.UTILISATEURS}/utilisateurs/${id}/`),
    creer: (data) => fetchAPI(`${API.UTILISATEURS}/utilisateurs/`, { method: 'POST', body: JSON.stringify(data) }),
};

// Emprunts
const EmpruntsAPI = {
    lister: () => fetchAPI(`${API.EMPRUNTS}/emprunts/`),
    creer: (data) => fetchAPI(`${API.EMPRUNTS}/emprunts/`, { method: 'POST', body: JSON.stringify(data) }),
    retourner: (id) => fetchAPI(`${API.EMPRUNTS}/emprunts/${id}/retour/`, { method: 'POST' }),
    retards: () => fetchAPI(`${API.EMPRUNTS}/emprunts/retards/`),
    historique: (userId) => fetchAPI(`${API.EMPRUNTS}/emprunts/utilisateur/${userId}/`),
};

// Recommandations
const RecoAPI = {
    recommandations: (userId, n = 5) => fetchAPI(`${API.RECO}/recommendations/${userId}?n=${n}`),    entrainer: () => fetchAPI(`${API.RECO}/train`, { method: 'POST' }),
    info: () => fetchAPI(`${API.RECO}/model/info`),
};
