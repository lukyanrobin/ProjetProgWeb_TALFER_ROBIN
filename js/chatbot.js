/* =====================================================================
   chatbot.js : démo du chatbot avec l'avatar (page Fonctionnalités)
   - les boutons de suggestion et le champ de saisie envoient un message ;
   - essAI « écrit… » un instant, puis répond avec une réponse préparée,
     choisie selon les mots-clés du message (pas d'IA réelle : c'est une démo).
   Sans JavaScript, on voit un exemple de conversation déjà écrit.
   ===================================================================== */

try {
  const chat = document.querySelector(".chat");

  if (chat) {
    const zoneMessages = chat.querySelector(".chat__messages");
    const formulaire = chat.querySelector(".chat__formulaire");
    const champ = chat.querySelector("#chat-message");
    const suggestions = chat.querySelectorAll(".chat__suggestion");

    chat.classList.add("chat--js");

    // L'exemple de conversation sert quand le JavaScript ne marche pas :
    // avec le JavaScript, on ne garde que le message d'accueil et l'utilisateur joue lui-même
    zoneMessages.querySelectorAll(".bulle").forEach(function (bulle, indice) {
      if (indice > 0) bulle.remove();
    });

    // Réponses préparées : la première dont un mot-clé apparaît dans le message est choisie
    const reponses = [
      {
        motsCles: ["semaine", "agenda", "planning", "organise", "emploi du temps"],
        texte: "Je regarde ton agenda… Tu as 3 créneaux libres. Je place ta séance de sport mercredi à 18 h et je décale la réunion d'équipe à jeudi ?"
      },
      {
        motsCles: ["idée", "idee", "projet", "appli", "créer", "creer"],
        texte: "Super ! Je crée le projet et je te propose 3 pistes à explorer. Avec l'offre Plus, je peux aussi le développer en plan détaillé."
      },
      {
        motsCles: ["sais", "peux", "fonction", "faire", "aide"],
        texte: "Je transcris tes dictées, je les reformule dans ton style et je les range : notes, tâches, projets, agenda. Je peux aussi faire des recherches pour toi."
      },
      {
        motsCles: ["rappel", "rappelle", "oublie", "demain"],
        texte: "C'est noté : je t'ajoute un rappel dans ton agenda. Tu veux qu'il sonne la veille ou le jour même ?"
      },
      {
        motsCles: ["prix", "gratuit", "abonnement", "payer", "tarif"],
        texte: "L'essentiel est gratuit ! Plus et Pro débloquent l'approfondissement et les agents autonomes. Tout est détaillé sur la page Tarifs."
      },
      {
        motsCles: ["bonjour", "salut", "hello", "coucou"],
        texte: "Salut ! Raconte-moi ce qui te passe par la tête, je m'occupe de le ranger."
      }
    ];
    const reponseParDefaut = "Je l'ai noté dans ton journal. Dans l'appli, je pourrais le ranger en note, en tâche ou dans un projet : tu préfères quoi ?";

    // Choisit la réponse selon le contenu du message
    function trouverReponse(message) {
      const texte = message.toLowerCase();
      for (const reponse of reponses) {
        if (reponse.motsCles.some(function (mot) { return texte.includes(mot); })) {
          return reponse.texte;
        }
      }
      return reponseParDefaut;
    }

    // Ajoute une bulle dans la conversation et fait défiler jusqu'en bas
    function ajouterBulle(texte, auteur) {
      const bulle = document.createElement("p");
      bulle.className = "bulle bulle--" + auteur;
      bulle.textContent = texte; // textContent : le texte saisi n'est jamais interprété comme du HTML
      zoneMessages.appendChild(bulle);
      zoneMessages.scrollTop = zoneMessages.scrollHeight;
      return bulle;
    }

    function envoyer(message) {
      const texte = message.trim();
      if (texte === "") return;

      ajouterBulle(texte, "moi");
      const enTrainDEcrire = ajouterBulle("essAI écrit…", "essai");
      enTrainDEcrire.classList.add("bulle--ecrit");

      // Petit délai pour imiter le temps de réflexion
      setTimeout(function () {
        enTrainDEcrire.remove();
        ajouterBulle(trouverReponse(texte), "essai");
      }, 900);
    }

    suggestions.forEach(function (bouton) {
      bouton.addEventListener("click", function () {
        envoyer(bouton.textContent);
      });
    });

    formulaire.addEventListener("submit", function (evenement) {
      evenement.preventDefault(); // pas d'envoi réel : la page ne se recharge pas
      envoyer(champ.value);
      champ.value = "";
      champ.focus();
    });
  }
} catch (erreur) {
  console.error("chatbot.js :", erreur);
}
