# essAI : site vitrine

Projet de programmation web du module **TI504N** (Efrei, 2026-2027).
**Binôme :** Tunui TALFER · Lukyan ROBIN

**essAI** est une application imaginée pour ce projet : un journal personnel à commande vocale. On parle dès qu'une idée arrive, même en vrac ; essAI la transcrit, la reformule dans le style de nos notes et la range au bon endroit (note, tâche, projet, agenda). Ce site en est la vitrine : il présente l'application, la montre en action et détaille ses offres.

## Sommaire
1. [Lancer le site](#1-lancer-le-site)
2. [Pages et arborescence](#2-pages-et-arborescence)
3. [Charte graphique](#3-charte-graphique)
4. [Fonctionnalités JavaScript](#4-fonctionnalités-javascript)
5. [Responsive et accessibilité](#5-responsive-et-accessibilité)
6. [Validation W3C](#6-validation-w3c)
7. [Maquette](#7-maquette)
8. [Répartition du travail](#8-répartition-du-travail)

---

## 1. Lancer le site

Ouvrir `index.html` dans un navigateur suffit. Pour un fonctionnement identique à un vrai serveur, on peut aussi lancer depuis le dossier du projet :

```
python3 -m http.server 8000
```

puis ouvrir http://localhost:8000.

## 2. Pages et arborescence

L'arborescence respecte la limite de **2 niveaux** : chaque page est à un clic de l'accueil.

| Page | Fichier | Contenu |
|---|---|---|
| Accueil | `index.html` | Accroche, démo animée de l'application sur un téléphone, étapes, carrousel d'exemples, intégrations, aperçu des offres |
| Fonctionnalités | `pages/fonctionnalites.html` | Dictée, comparaison avant/après de la reformulation, schéma du rangement, démo du chatbot, approfondissement et agents |
| Tarifs | `pages/tarifs.html` | Les 3 offres, bascule mensuel/annuel, tableau comparatif, « Où va ton argent ? », FAQ |
| À propos | `pages/a-propos.html` | Le problème, nos engagements, l'équipe et le travail de chacun, le projet |
| Contact | `pages/contact.html` | Formulaire de contact vérifié en JavaScript, liste d'attente |

Toutes les pages ont le même **en-tête** (logo, titre du site, navigation) et le même **pied de page** (navigation et lien vers « À propos »).

```
├── index.html
├── pages/          ← fonctionnalites, tarifs, a-propos, contact
├── css/style.css   ← une seule feuille de style, commentée par sections
├── js/             ← un fichier par fonctionnalité
├── img/            ← logo et icône d'onglet
└── maquette/       ← wireframes (livrable)
```

## 3. Charte graphique

| Rôle | Couleur |
|---|---|
| Vert forêt (titres, en-tête, pied de page) | `#12271F` |
| Crème (fond) | `#FBFAF6` |
| Sauge (accents doux) | `#8FB3A0` |
| Ambre (boutons d'action) | `#E0A84F` |

Les couleurs viennent du logo : un trait qui file, comme une idée qui passe, et qui se termine par une étincelle. Polices système, coins arrondis comme l'icône de l'application, illustrations en SVG et en CSS (sans images lourdes).

## 4. Fonctionnalités JavaScript

Aucun framework ni bibliothèque. Chaque script est chargé avec `defer` (il ne bloque pas l'affichage) et protégé par `try/catch` : en cas d'erreur, la page reste lisible.

| Fichier | Page | Ce qu'il fait |
|---|---|---|
| `menu.js` | Toutes | Menu « burger » sur téléphone (ouverture, fermeture, touche Échap) |
| `apparition.js` | Toutes | Apparition en fondu des sections au défilement (`IntersectionObserver`) |
| `demo.js` | Accueil | Démo animée : onde de la voix, transcription lettre par lettre, résultats, destinations |
| `carrousel.js` | Accueil | Carrousel : flèches, points, défilement automatique, pause au survol, glissement du doigt, clavier |
| `comparaison.js` | Fonctionnalités | Curseur pour comparer la dictée brute et la note reformulée |
| `chatbot.js` | Fonctionnalités | Démo du chatbot : suggestions, saisie, réponses préparées selon des mots-clés |
| `tarifs.js` | Tarifs | Bascule mensuel/annuel des prix, FAQ avec une seule question ouverte à la fois |
| `formulaire.js` | Contact | Vérification des champs avec messages d'erreur, compteur de caractères, liste d'attente |

**Sans JavaScript**, le site reste utilisable : la démo affiche le résultat final, le carrousel défile à la main, la FAQ reste dépliable, et le navigateur vérifie lui-même le formulaire.

## 5. Responsive et accessibilité

- Trois mises en page grâce aux media queries : ordinateur, tablette (≤ 960 px) et téléphone (≤ 600 px). Sur téléphone, le menu devient un burger et le tableau des tarifs défile dans son cadre.
- Navigation possible au clavier, avec un contour visible sur l'élément actif.
- Textes alternatifs, libellés de formulaire, messages d'erreur reliés aux champs (`aria-describedby`, `aria-invalid`).
- Les animations sont coupées si l'utilisateur a activé « réduire les animations » dans son système.

## 6. Validation W3C

Toutes les pages HTML sont validées par le [validateur W3C](https://validator.w3.org/) : **0 erreur, 0 avertissement**. La feuille de style est validée par le [validateur CSS du W3C](https://jigsaw.w3.org/css-validator/) : **0 erreur** (il reste deux avertissements d'information, sur les variables CSS et sur un sélecteur propre à Safari pour la FAQ).

## 7. Maquette

Les wireframes sont dans [`maquette/`](maquette/) : plan du site, les 5 pages en version ordinateur et en version téléphone. Ouvrir `maquette/index.html` pour tout voir.

## 8. Répartition du travail

| Membre | Travail réalisé |
|---|---|
| **Tunui TALFER** | Charte graphique et feuille de style commune, en-tête, pied de page et menu burger, page d'accueil (démo animée, carrousel), page Tarifs (bascule, tableau, FAQ, barres) |
| **Lukyan ROBIN** | Logo, maquette, page Fonctionnalités (comparaison avant/après, chatbot), page Contact (formulaire et vérification) |
| **Les deux** | Page À propos, validation W3C, tests sur téléphone |

---

*essAI est une application fictive imaginée pour ce projet : les prix, les exemples et les démonstrations sont fictifs, et aucun formulaire n'envoie de données.*
