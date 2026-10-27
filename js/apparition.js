/* =====================================================================
   apparition.js : les éléments « .apparition » apparaissent en fondu
   quand ils arrivent à l'écran pendant le défilement.
   Utilise IntersectionObserver ; si le navigateur ne le connaît pas
   (ou en cas d'erreur), tout est affiché directement.
   ===================================================================== */

document.documentElement.classList.add("js");

try {
  const elements = document.querySelectorAll(".apparition");

  if ("IntersectionObserver" in window) {
    const observateur = new IntersectionObserver(function (entrees) {
      entrees.forEach(function (entree) {
        if (entree.isIntersecting) {
          entree.target.classList.add("visible");
          observateur.unobserve(entree.target); // l'animation ne se joue qu'une fois
        }
      });
    }, { threshold: 0.15 });

    elements.forEach(function (element) {
      observateur.observe(element);
    });
  } else {
    elements.forEach(function (element) {
      element.classList.add("visible");
    });
  }
} catch (erreur) {
  // Sécurité : on affiche tout si quelque chose se passe mal
  document.querySelectorAll(".apparition").forEach(function (element) {
    element.classList.add("visible");
  });
  console.error("apparition.js :", erreur);
}
