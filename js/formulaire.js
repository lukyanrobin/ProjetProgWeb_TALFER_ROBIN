/* =====================================================================
   formulaire.js : vérification des formulaires de la page Contact
   1. Formulaire de contact : chaque champ est vérifié quand on le quitte
      et au moment de l'envoi ; un message d'erreur clair s'affiche sous
      le champ concerné ; un compteur suit la longueur du message.
   2. Liste d'attente : vérification de l'adresse e-mail.
   Le site est statique : rien n'est envoyé, on affiche une confirmation.
   Sans JavaScript, le navigateur fait lui-même une vérification simple
   grâce aux attributs required, type="email" et minlength.
   ===================================================================== */

// Format d'adresse e-mail : quelque chose@quelque chose.extension
const FORMAT_EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

// 1. Formulaire de contact ---------------------------------------------------
try {
  const formulaire = document.getElementById("formulaire-contact");

  if (formulaire) {
    // On remplace la vérification du navigateur par la nôtre (messages plus clairs)
    formulaire.setAttribute("novalidate", "");

    const champs = {
      nom: formulaire.querySelector("#nom"),
      email: formulaire.querySelector("#email"),
      sujet: formulaire.querySelector("#sujet"),
      message: formulaire.querySelector("#message"),
      accord: formulaire.querySelector("#accord")
    };
    const compteur = formulaire.querySelector("#compteur-message");
    const confirmation = formulaire.querySelector(".formulaire__confirmation");

    // Chaque règle renvoie un message d'erreur, ou "" si le champ est correct
    const regles = {
      nom: function (valeur) {
        return valeur.trim().length < 2 ? "Indique ton nom (2 caractères minimum)." : "";
      },
      email: function (valeur) {
        if (valeur.trim() === "") return "Indique ton adresse e-mail.";
        return FORMAT_EMAIL.test(valeur.trim()) ? "" : "Cette adresse e-mail n'est pas valide (exemple : prenom.nom@mail.fr).";
      },
      sujet: function (valeur) {
        return valeur === "" ? "Choisis un sujet dans la liste." : "";
      },
      message: function (valeur) {
        const longueur = valeur.trim().length;
        return longueur < 20 ? "Ton message est trop court : encore " + (20 - longueur) + " caractère(s)." : "";
      },
      accord: function (valeur, champ) {
        return champ.checked ? "" : "Coche la case pour que l'on puisse te répondre.";
      }
    };

    // Vérifie un champ, affiche ou efface son message d'erreur, et renvoie true s'il est correct
    function verifier(nom) {
      const champ = champs[nom];
      const erreur = regles[nom](champ.value, champ);
      const zoneErreur = formulaire.querySelector("#erreur-" + nom);
      zoneErreur.textContent = erreur;
      champ.setAttribute("aria-invalid", erreur ? "true" : "false");
      return erreur === "";
    }

    // Vérification quand on quitte un champ, puis à chaque frappe une fois qu'il est en erreur
    Object.keys(champs).forEach(function (nom) {
      champs[nom].addEventListener("blur", function () { verifier(nom); });
      champs[nom].addEventListener("input", function () {
        if (champs[nom].getAttribute("aria-invalid") === "true") verifier(nom);
      });
    });

    // Compteur de caractères du message
    champs.message.addEventListener("input", function () {
      compteur.textContent = champs.message.value.length + " / 1000 caractères (20 minimum)";
    });

    formulaire.addEventListener("submit", function (evenement) {
      evenement.preventDefault();
      confirmation.textContent = "";

      // On vérifie tous les champs (pas de « && » : on veut afficher toutes les erreurs d'un coup)
      const resultats = Object.keys(champs).map(verifier);
      const toutEstCorrect = resultats.every(function (ok) { return ok; });

      if (!toutEstCorrect) {
        // On place le curseur sur le premier champ en erreur
        const premierEnErreur = formulaire.querySelector("[aria-invalid='true']");
        if (premierEnErreur) premierEnErreur.focus();
        return;
      }

      const prenom = champs.nom.value.trim().split(" ")[0];
      confirmation.textContent = "Merci " + prenom + " ! Ton message a bien été pris en compte. On te répond sous 48 heures.";
      formulaire.reset();
      compteur.textContent = "0 / 1000 caractères (20 minimum)";
      Object.keys(champs).forEach(function (nom) { champs[nom].removeAttribute("aria-invalid"); });
    });
  }
} catch (erreur) {
  console.error("formulaire.js (contact) :", erreur);
}

// 2. Liste d'attente -----------------------------------------------------------
try {
  const listeAttente = document.getElementById("liste-attente");

  if (listeAttente) {
    listeAttente.setAttribute("novalidate", "");
    const champEmail = listeAttente.querySelector("#email-attente");
    const message = listeAttente.querySelector(".liste-attente__message");

    listeAttente.addEventListener("submit", function (evenement) {
      evenement.preventDefault();
      const email = champEmail.value.trim();

      if (!FORMAT_EMAIL.test(email)) {
        message.textContent = "Cette adresse e-mail n'est pas valide.";
        message.classList.remove("liste-attente__message--ok");
        champEmail.setAttribute("aria-invalid", "true");
        champEmail.focus();
        return;
      }

      message.textContent = "C'est noté ! On t'écrira à " + email + " dès l'ouverture.";
      message.classList.add("liste-attente__message--ok");
      champEmail.removeAttribute("aria-invalid");
      listeAttente.reset();
    });
  }
} catch (erreur) {
  console.error("formulaire.js (liste d'attente) :", erreur);
}
