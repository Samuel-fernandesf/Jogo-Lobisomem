document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".flip").forEach(card => {
        card.addEventListener("click", function () {
            this.classList.toggle("flipped");
        });
    });
});

document.getElementById('revelar-papel').addEventListener('click', function() {
    document.getElementById('papel').style.display = 'block';
    document.getElementById('entregar-dispositivo').style.display = 'none'
});

document.getElementById('imagem')?.addEventListener('click', function() {
    let botaoProximo = document.getElementById('botao_proximo');
    let mensagem = document.getElementById('mensagem');
    let mensagem2 = document.getElementById('mensagem2');
    let mensagem3 = document.getElementById('mensagem3');
    let mensagemAlianca = document.getElementById('mensagem_aliança');

    if (botaoProximo) botaoProximo.style.display = 'block';
    if (mensagem) mensagem.style.display = 'block';
    if (mensagem2) mensagem2.style.display = 'none';
    if (mensagemAlianca) mensagemAlianca.style.display = 'block';
    if (mensagem3) mensagem3.style.display = 'block';
});
