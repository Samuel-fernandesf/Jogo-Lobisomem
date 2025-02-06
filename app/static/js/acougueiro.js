document.addEventListener("DOMContentLoaded", function () {
    let botaoRevelar = document.getElementById("revelar-papel");
    let divPapel = document.getElementById("papel");
    let divBotao = document.getElementById("botoes");
    let divEntrega = document.getElementById('entregar-dispositivo');
    let divMensagem = document.getElementById("mensagem")
    if (!botaoRevelar || !divPapel) return; 

    botaoRevelar.addEventListener("click", function () {
        divEntrega.style.display = 'none';
        divPapel.style.display = "block"; 
        divBotao.style.display = "block";
        divMensagem.style.display = "block";
        console.log(divMensagem)
    });

});