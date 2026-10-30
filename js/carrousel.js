/* =====================================================================
   carrousel.js : carrousel « Ce que tu peux lui dire » (page d'accueil)
   - flèches précédent / suivant et points de navigation ;
   - défilement automatique toutes les 5 secondes, en pause au survol
     ou quand un élément du carrousel a le focus ;
   - glissement du doigt sur téléphone, flèches du clavier.
   Sans JavaScript, les cartes défilent simplement à la main (voir style.css).
   ===================================================================== */

try {
  const carrousel = document.querySelector(".carrousel");

  if (carrousel) {
    const piste = carrousel.querySelector(".carrousel__piste");
    const cartes = carrousel.querySelectorAll(".carrousel__carte");
    const boutonPrec = carrousel.querySelector(".carrousel__fleche--prec");
    const boutonSuiv = carrousel.querySelector(".carrousel__fleche--suiv");
    const zonePoints = carrousel.querySelector(".carrousel__points");
    const reduireAnimations = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    let position = 0;       // indice de la première carte visible
    let minuterie = null;   // identifiant du défilement automatique

    carrousel.classList.add("carrousel--js");

    // Nombre de cartes visibles en même temps (dépend de la largeur de l'écran)
    function cartesVisibles() {
      const largeurCarte = cartes[0].getBoundingClientRect().width;
      const largeurFenetre = piste.parentElement.getBoundingClientRect().width;
      return Math.max(1, Math.round(largeurFenetre / largeurCarte));
    }

    // Nombre de positions possibles (on s'arrête quand la dernière carte est visible)
    function nombrePositions() {
      return cartes.length - cartesVisibles() + 1;
    }

    // Crée un point par position possible
    function creerPoints() {
      zonePoints.innerHTML = "";
      for (let i = 0; i < nombrePositions(); i += 1) {
        const point = document.createElement("button");
        point.type = "button";
        point.setAttribute("aria-label", "Aller à l'exemple " + (i + 1));
        point.addEventListener("click", function () { allerA(i); });
        zonePoints.appendChild(point);
      }
    }

    // Déplace la piste pour afficher la carte numéro « indice » en premier
    function allerA(indice) {
      const total = nombrePositions();
      position = (indice + total) % total; // revient au début après la fin, et inversement
      const decalage = cartes[position].offsetLeft - cartes[0].offsetLeft;
      piste.style.transform = "translateX(" + (-decalage) + "px)";
      zonePoints.querySelectorAll("button").forEach(function (point, i) {
        point.setAttribute("aria-current", i === position ? "true" : "false");
      });
    }

    function demarrerAuto() {
      if (reduireAnimations || minuterie) return;
      minuterie = setInterval(function () { allerA(position + 1); }, 5000);
    }

    function arreterAuto() {
      clearInterval(minuterie);
      minuterie = null;
    }

    boutonPrec.addEventListener("click", function () { allerA(position - 1); });
    boutonSuiv.addEventListener("click", function () { allerA(position + 1); });

    // Pause quand la souris est dessus ou quand on navigue au clavier dedans
    carrousel.addEventListener("mouseenter", arreterAuto);
    carrousel.addEventListener("mouseleave", demarrerAuto);
    carrousel.addEventListener("focusin", arreterAuto);
    carrousel.addEventListener("focusout", demarrerAuto);

    // Flèches du clavier
    carrousel.addEventListener("keydown", function (evenement) {
      if (evenement.key === "ArrowLeft") allerA(position - 1);
      if (evenement.key === "ArrowRight") allerA(position + 1);
    });

    // Glissement du doigt : on compare la position de départ et d'arrivée
    let departX = null;
    piste.addEventListener("touchstart", function (evenement) {
      departX = evenement.touches[0].clientX;
      arreterAuto();
    }, { passive: true });
    piste.addEventListener("touchend", function (evenement) {
      if (departX === null) return;
      const ecart = evenement.changedTouches[0].clientX - departX;
      if (ecart < -50) allerA(position + 1);
      if (ecart > 50) allerA(position - 1);
      departX = null;
      demarrerAuto();
    });

    // Si la largeur de la fenêtre change, le nombre de cartes visibles aussi
    window.addEventListener("resize", function () {
      creerPoints();
      allerA(Math.min(position, nombrePositions() - 1));
    });

    creerPoints();
    allerA(0);
    demarrerAuto();
  }
} catch (erreur) {
  // En cas d'erreur, on revient au défilement à la main
  const carrousel = document.querySelector(".carrousel");
  if (carrousel) {
    carrousel.classList.remove("carrousel--js");
    const piste = carrousel.querySelector(".carrousel__piste");
    if (piste) piste.style.transform = "";
  }
  console.error("carrousel.js :", erreur);
}
