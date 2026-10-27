/* =====================================================================
   menu.js : menu « burger » sur téléphone et tablette (toutes les pages)
   - un clic sur le burger ouvre ou ferme le menu ;
   - un clic sur un lien du menu, ou la touche Échap, le referme.
   Sans JavaScript, le menu reste affiché en entier (voir style.css).
   ===================================================================== */

// Indique au CSS que le JavaScript fonctionne (sert au menu et aux animations)
document.documentElement.classList.add("js");

try {
  const burger = document.querySelector(".burger");
  const menu = document.getElementById("menu-principal");

  if (burger && menu) {
    // Ouvre ou ferme le menu, et met à jour les attributs pour l'accessibilité
    function basculerMenu(ouvrir) {
      menu.classList.toggle("ouvert", ouvrir);
      burger.setAttribute("aria-expanded", String(ouvrir));
      burger.setAttribute("aria-label", ouvrir ? "Fermer le menu" : "Ouvrir le menu");
    }

    burger.addEventListener("click", function () {
      const estOuvert = burger.getAttribute("aria-expanded") === "true";
      basculerMenu(!estOuvert);
    });

    // Quand on choisit une page, le menu se referme
    menu.querySelectorAll("a").forEach(function (lien) {
      lien.addEventListener("click", function () {
        basculerMenu(false);
      });
    });

    // La touche Échap referme le menu
    document.addEventListener("keydown", function (evenement) {
      if (evenement.key === "Escape") {
        basculerMenu(false);
      }
    });
  }
} catch (erreur) {
  // En cas d'erreur, on retire la classe « js » : le menu reste visible et utilisable
  document.documentElement.classList.remove("js");
  console.error("menu.js :", erreur);
}
