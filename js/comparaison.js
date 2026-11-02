/* =====================================================================
   comparaison.js : comparaison « avant / après » (page Fonctionnalités)
   La note « après » est posée par-dessus la dictée « avant ». Le curseur
   (<input type="range">) règle la part visible de chacune : à gauche du
   curseur on voit la note essAI, à droite la dictée brute.
   Sans JavaScript, les deux cartes s'affichent simplement côte à côte.
   ===================================================================== */

try {
  document.querySelectorAll(".comparaison").forEach(function (comparaison) {
    const curseur = comparaison.querySelector("input[type='range']");
    const apres = comparaison.querySelector(".comparaison__carte--apres");

    if (!curseur || !apres) return;

    comparaison.classList.add("comparaison--js");

    // Montre la carte « après » jusqu'à la position du curseur (en %)
    function mettreAJour() {
      const position = Number(curseur.value);
      apres.style.clipPath = "inset(0 " + (100 - position) + "% 0 0)";
    }

    curseur.addEventListener("input", mettreAJour);
    mettreAJour();
  });
} catch (erreur) {
  console.error("comparaison.js :", erreur);
}
