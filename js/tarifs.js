/* =====================================================================
   tarifs.js : page Tarifs
   1. Bascule mensuel / annuel : chaque élément qui porte les attributs
      data-mensuel et data-annuel affiche le texte de la période choisie
      (prix des cartes et ligne « Prix » du tableau).
   2. FAQ : une seule question ouverte à la fois.
   Sans JavaScript, la page affiche les prix mensuels et toutes les
   questions de la FAQ restent dépliables (balises <details>).
   ===================================================================== */

// 1. Bascule mensuel / annuel ------------------------------------------------
try {
  const options = document.querySelectorAll(".bascule__option");
  const elementsPrix = document.querySelectorAll("[data-mensuel][data-annuel]");

  // Affiche les prix de la période demandée (« mensuel » ou « annuel »)
  function afficherPeriode(periode) {
    elementsPrix.forEach(function (element) {
      element.textContent = element.dataset[periode];
    });
    options.forEach(function (option) {
      option.setAttribute("aria-pressed", String(option.dataset.periode === periode));
    });
  }

  options.forEach(function (option) {
    option.addEventListener("click", function () {
      afficherPeriode(option.dataset.periode);
    });
  });
} catch (erreur) {
  console.error("tarifs.js (bascule) :", erreur);
}

// 2. FAQ : quand on ouvre une question, les autres se referment ---------------
try {
  const questions = document.querySelectorAll(".faq details");

  questions.forEach(function (question) {
    // L'évènement « toggle » se déclenche quand un <details> s'ouvre ou se ferme
    question.addEventListener("toggle", function () {
      if (question.open) {
        questions.forEach(function (autre) {
          if (autre !== question) {
            autre.open = false;
          }
        });
      }
    });
  });
} catch (erreur) {
  console.error("tarifs.js (FAQ) :", erreur);
}
