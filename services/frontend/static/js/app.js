function showAlert(msg, type = 'success') {
    const icon = type === 'success' ? 'ti-circle-check' : 'ti-alert-circle';
    const el = document.getElementById('alert-zone');
    if (!el) return;
    el.innerHTML = `<div class="alert alert-${type}"><i class="ti ${icon}"></i>${msg}</div>`;
    setTimeout(() => el.innerHTML = '', 4000);
}

function setLoading(id, on) {
    const el = document.getElementById(id);
    if (el) el.style.display = on ? 'flex' : 'none';
}

function activerTab(target) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    const btn = document.querySelector(`[data-target="${target}"]`);
    if (btn) btn.classList.add('active');
    const content = document.getElementById(target);
    if (content) content.classList.add('active');
    if (target === 'tab-livres') chargerLivres();
    if (target === 'tab-emprunts') chargerEmprunts();
    if (target === 'tab-utilisateurs') chargerUtilisateurs();
}

function initTabs() {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => activerTab(tab.dataset.target));
    });
}

// ── LIVRES ────────────────────────────────────────────────
async function chargerLivres(q = '') {
    setLoading('loading-livres', true);
    try {
        const data = q ? await LivresAPI.rechercher(q) : await LivresAPI.lister();
        afficherLivres(data.results || []);
    } catch { showAlert('Erreur chargement livres', 'error'); }
    setLoading('loading-livres', false);
}

function afficherLivres(livres) {
    const container = document.getElementById('livres-grid');
    if (!container) return;
    if (!livres.length) {
        container.innerHTML = '<p style="color:#a0aec0;padding:1rem">Aucun livre trouvé.</p>';
        return;
    }
    container.innerHTML = livres.map(l => `
        <div class="livre-card">
            <h3>${l.titre}</h3>
            <div class="livre-meta">
                <span><i class="ti ti-pencil"></i>${l.auteur}</span>
                <span><i class="ti ti-barcode"></i>${l.isbn}</span>
                <span><i class="ti ti-tag"></i>${l.genre || 'Non classifié'}</span>
            </div>
            <div class="card-footer">
                <span class="badge ${l.est_disponible ? 'badge-dispo' : 'badge-indispo'}">
                    <i class="ti ${l.est_disponible ? 'ti-circle-check' : 'ti-circle-x'}"></i>
                    ${l.est_disponible ? `${l.exemplaires_disponibles} disponible(s)` : 'Indisponible'}
                </span>
                ${l.est_disponible
                    ? `<button class="btn btn-primary btn-sm" onclick="ouvrirModalEmprunt(${l.id}, '${l.titre.replace(/'/g,"\\'")}')">
                           <i class="ti ti-book-download"></i> Emprunter
                       </button>`
                    : ''}
            </div>
        </div>
    `).join('');
}

// ── MODAL EMPRUNT ─────────────────────────────────────────
function ouvrirModalEmprunt(livreId, titre) {
    document.getElementById('modal-titre').textContent = titre;
    document.getElementById('modal-livre-id').value = livreId;
    document.getElementById('modal-user-id').value = '';
    document.getElementById('modal-emprunt').style.display = 'flex';
}

function fermerModal() {
    document.getElementById('modal-emprunt').style.display = 'none';
}

async function confirmerEmprunt() {
    const livreId = document.getElementById('modal-livre-id').value;
    const utilisateurId = document.getElementById('modal-user-id').value;
    if (!utilisateurId) { showAlert('Entrez un ID utilisateur', 'error'); return; }
    try {
        await EmpruntsAPI.creer({ livre_id: parseInt(livreId), utilisateur_id: parseInt(utilisateurId) });
        showAlert('Emprunt enregistré avec succès !');
        fermerModal();
        chargerLivres();
    } catch { showAlert("Erreur lors de l'emprunt", 'error'); }
}

// ── EMPRUNTS ──────────────────────────────────────────────
async function chargerEmprunts() {
    setLoading('loading-emprunts', true);
    try {
        const data = await EmpruntsAPI.lister();
        afficherEmprunts(data.results || []);
    } catch { showAlert('Erreur chargement emprunts', 'error'); }
    setLoading('loading-emprunts', false);
}

function afficherEmprunts(emprunts) {
    const tbody = document.getElementById('emprunts-tbody');
    if (!tbody) return;
    if (!emprunts.length) {
        tbody.innerHTML = '<tr><td colspan="6" class="empty-row">Aucun emprunt enregistré</td></tr>';
        return;
    }
    const statutBadge = {
        'en_cours': `<span class="badge badge-encours"><i class="ti ti-clock"></i> En cours</span>`,
        'retourne':  `<span class="badge badge-dispo"><i class="ti ti-circle-check"></i> Retourné</span>`,
        'en_retard': `<span class="badge badge-retard"><i class="ti ti-alert-triangle"></i> En retard</span>`,
    };
    tbody.innerHTML = emprunts.map(e => `
        <tr>
            <td>#${e.id}</td>
            <td><i class="ti ti-user" style="color:#a0aec0"></i> ${e.utilisateur_id}</td>
            <td><i class="ti ti-book" style="color:#a0aec0"></i> ${e.livre_id}</td>
            <td>${new Date(e.date_emprunt).toLocaleDateString('fr-FR')}</td>
            <td>${statutBadge[e.statut] || e.statut}</td>
            <td>
                ${e.statut !== 'retourne'
                    ? `<button class="btn btn-success btn-sm" onclick="retournerLivre(${e.id})">
                           <i class="ti ti-book-upload"></i> Retourner
                       </button>`
                    : '<span style="color:#a0aec0;font-size:0.85rem">—</span>'}
            </td>
        </tr>
    `).join('');
}

async function retournerLivre(empruntId) {
    try {
        await EmpruntsAPI.retourner(empruntId);
        showAlert('Livre retourné avec succès !');
        chargerEmprunts();
    } catch { showAlert('Erreur retour livre', 'error'); }
}

// ── UTILISATEURS ──────────────────────────────────────────
async function chargerUtilisateurs() {
    setLoading('loading-utilisateurs', true);
    try {
        const data = await UtilisateursAPI.lister();
        afficherUtilisateurs(data.results || []);
    } catch { showAlert('Erreur chargement utilisateurs', 'error'); }
    setLoading('loading-utilisateurs', false);
}

const typeIcons = {
    etudiant: 'ti-school',
    professeur: 'ti-chalkboard',
    personnel: 'ti-briefcase'
};

function afficherUtilisateurs(utilisateurs) {
    const tbody = document.getElementById('utilisateurs-tbody');
    if (!tbody) return;
    if (!utilisateurs.length) {
        tbody.innerHTML = '<tr><td colspan="7" class="empty-row">Aucun utilisateur</td></tr>';
        return;
    }
    tbody.innerHTML = utilisateurs.map(u => `
        <tr>
            <td>#${u.id}</td>
            <td><strong>${u.nom_complet}</strong></td>
            <td>${u.email}</td>
            <td>
                <span style="display:flex;align-items:center;gap:0.3rem;font-size:0.85rem">
                    <i class="ti ${typeIcons[u.type_utilisateur] || 'ti-user'}" style="color:#a0aec0"></i>
                    ${u.type_utilisateur}
                </span>
            </td>
            <td><code style="font-size:0.8rem">${u.numero_carte}</code></td>
            <td>
                <span class="badge ${u.actif ? 'badge-dispo' : 'badge-indispo'}">
                    <i class="ti ${u.actif ? 'ti-circle-check' : 'ti-circle-x'}"></i>
                    ${u.actif ? 'Actif' : 'Inactif'}
                </span>
            </td>
            <td>
                <button class="btn btn-ghost btn-sm" onclick="chargerRecos(${u.id})">
                    <i class="ti ti-stars"></i> Recos
                </button>
            </td>
        </tr>
    `).join('');
}

// ── RECOMMANDATIONS ───────────────────────────────────────
async function chargerRecos(userId) {
    activerTab('tab-recos');
    document.getElementById('recos-user-id').value = userId;
    setLoading('loading-recos', true);
    try {
        const data = await RecoAPI.recommandations(userId);
        afficherRecos(data.recommendations || [], userId);
    } catch {
        showAlert('Modèle non disponible. Cliquez sur "Entraîner le modèle".', 'error');
    }
    setLoading('loading-recos', false);
}

function afficherRecos(recos, userId) {
    const container = document.getElementById('recos-grid');
    document.getElementById('recos-titre').innerHTML =
        `<i class="ti ti-sparkles" style="color:#4299e1"></i> Recommandations pour l'utilisateur #${userId}`;
    if (!recos.length) {
        container.innerHTML = '<p style="color:#a0aec0">Aucune recommandation disponible.</p>';
        return;
    }
    container.innerHTML = recos.map((r, i) => `
        <div class="reco-card">
            <div class="reco-rank"><i class="ti ti-medal"></i> Recommandation n°${i + 1}</div>
            <h3><i class="ti ti-book"></i> Livre ID ${r.livre_id}</h3>
            <div class="reco-score">
                <i class="ti ti-chart-bar"></i>
                Score de pertinence : ${(r.score * 100).toFixed(1)}%
            </div>
        </div>
    `).join('');
}

async function entrainerModele() {
    if (!confirm('Lancer l\'entraînement du modèle ML ?')) return;
    const btn = document.getElementById('btn-entrainer');
    btn.innerHTML = '<i class="ti ti-loader"></i> Entraînement...';
    btn.disabled = true;
    try {
        const data = await RecoAPI.entrainer();
        showAlert(`Modèle entraîné — ${data.metrics?.utilisateurs} utilisateurs, ${data.metrics?.livres} livres.`);
    } catch { showAlert('Erreur entraînement modèle', 'error'); }
    btn.innerHTML = '<i class="ti ti-brain"></i> Entraîner le modèle';
    btn.disabled = false;
}

// ── FORMULAIRES ───────────────────────────────────────────
async function ajouterLivre(e) {
    e.preventDefault();
    const form = e.target;
    const data = {
        titre: form.titre.value,
        auteur: form.auteur.value,
        isbn: form.isbn.value,
        editeur: form.editeur.value,
        annee_publication: parseInt(form.annee.value) || null,
        genre: form.genre.value,
        nombre_exemplaires: parseInt(form.exemplaires.value) || 1,
        exemplaires_disponibles: parseInt(form.exemplaires.value) || 1,
    };
    try {
        await LivresAPI.creer(data);
        showAlert('Livre ajouté avec succès !');
        form.reset();
    } catch { showAlert('Erreur ajout livre (ISBN déjà existant ?)', 'error'); }
}

async function ajouterUtilisateur(e) {
    e.preventDefault();
    const form = e.target;
    const data = {
        nom: form.nom.value,
        prenom: form.prenom.value,
        email: form.email.value,
        telephone: form.telephone.value,
        type_utilisateur: form.type_utilisateur.value,
        numero_carte: form.numero_carte.value,
    };
    try {
        await UtilisateursAPI.creer(data);
        showAlert('Utilisateur créé avec succès !');
        form.reset();
    } catch { showAlert('Erreur création utilisateur', 'error'); }
}

// ── INIT ──────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    chargerLivres();

    document.getElementById('search-input')?.addEventListener('input', (e) => {
        clearTimeout(window._searchTimer);
        window._searchTimer = setTimeout(() => chargerLivres(e.target.value), 400);
    });

    document.getElementById('form-livre')?.addEventListener('submit', ajouterLivre);
    document.getElementById('form-utilisateur')?.addEventListener('submit', ajouterUtilisateur);
    document.getElementById('btn-entrainer')?.addEventListener('click', entrainerModele);

    // Fermer le modal en cliquant dehors
    document.getElementById('modal-emprunt')?.addEventListener('click', function(e) {
        if (e.target === this) fermerModal();
    });
});
