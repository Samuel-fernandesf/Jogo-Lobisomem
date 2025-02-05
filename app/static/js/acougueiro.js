document.addEventListener("DOMContentLoaded", function () {
    let botaoRevelar = document.getElementById("revelar-papel");
    let divPapel = document.getElementById("papel");
    let tituloEntregar = document.getElementById("entregar-dispositivo");

    if (!botaoRevelar || !divPapel) return; 

    botaoRevelar.addEventListener("click", function () {
        divPapel.style.display = "block"; 
        botaoRevelar.style.display = "none"; 
        if (tituloEntregar) tituloEntregar.style.display = "none";
        mudarCorPapel();
    });
});