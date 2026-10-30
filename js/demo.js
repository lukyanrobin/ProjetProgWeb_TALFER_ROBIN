/* =====================================================================
   demo.js : démo animée du téléphone sur la page d'accueil
   Déroulé (en boucle) :
     1. essAI écoute : l'onde de la voix s'anime ;
     2. la transcription s'écrit lettre par lettre ;
     3. les résultats (note, tâche, rappel) apparaissent un par un ;
     4. les destinations (Notes, Agenda, Notion) s'allument tour à tour ;
     5. pause, puis on recommence.
   Le bouton « Voir la démo » relance l'animation depuis le début.
   Sans JavaScript, ou si l'utilisateur a désactivé les animations,
   le téléphone affiche directement le résultat final.
   ===================================================================== */

try {
  const demo = document.querySelector(".demo");
  const reduireAnimations = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (demo && !reduireAnimations) {
    const statut = demo.querySelector(".demo__texte-statut");
    const transcription = demo.querySelector(".demo__transcription");
    const resultats = demo.querySelectorAll(".demo__resultat li");
    const destinations = demo.querySelectorAll(".demo__destinations li");
    const boutonRejouer = document.getElementById("rejouer-demo");
    const texteComplet = transcription.textContent;

    // Numéro de la lecture en cours : sert à arrêter une lecture quand on la relance
    let lectureEnCours = 0;

    // Petite fonction d'attente utilisable avec « await »
    function attendre(millisecondes) {
      return new Promise(function (resolve) {
        setTimeout(resolve, millisecondes);
      });
    }

    // Remet le téléphone dans son état de départ
    function reinitialiser() {
      demo.classList.add("demo--animee");
      demo.classList.remove("demo--ecoute", "demo--ecriture", "demo--resultats");
      transcription.textContent = "";
      resultats.forEach(function (li) { li.classList.remove("visible"); });
      destinations.forEach(function (li) { li.classList.remove("active"); });
    }

    async function jouer() {
      lectureEnCours += 1;
      const maLecture = lectureEnCours;
      // Vrai si une nouvelle lecture a été lancée entre-temps : on s'arrête alors
      const interrompue = function () { return maLecture !== lectureEnCours; };

      reinitialiser();

      // 1. Écoute
      statut.textContent = "essAI t'écoute…";
      demo.classList.add("demo--ecoute");
      await attendre(1500);
      if (interrompue()) return;

      // 2. Transcription lettre par lettre
      demo.classList.add("demo--ecriture");
      for (let i = 1; i <= texteComplet.length; i += 1) {
        transcription.textContent = texteComplet.slice(0, i);
        await attendre(28);
        if (interrompue()) return;
      }
      demo.classList.remove("demo--ecoute", "demo--ecriture");

      // 3. Résultats un par un
      statut.textContent = "essAI range ton idée…";
      for (const li of resultats) {
        await attendre(600);
        if (interrompue()) return;
        demo.classList.add("demo--resultats");
        li.classList.add("visible");
      }

      // 4. Destinations qui s'allument tour à tour
      for (const li of destinations) {
        await attendre(450);
        if (interrompue()) return;
        li.classList.add("active");
      }
      statut.textContent = "essAI a rangé ton idée";

      // 5. Pause puis nouvelle boucle
      await attendre(4500);
      if (interrompue()) return;
      jouer();
    }

    if (boutonRejouer) {
      boutonRejouer.addEventListener("click", function () {
        jouer(); // le lien fait aussi défiler jusqu'au téléphone (#demo)
      });
    }

    jouer();
  }
} catch (erreur) {
  // En cas d'erreur, on revient à l'affichage statique du résultat final
  const demo = document.querySelector(".demo");
  if (demo) {
    demo.classList.remove("demo--animee", "demo--ecoute", "demo--ecriture", "demo--resultats");
  }
  console.error("demo.js :", erreur);
}
