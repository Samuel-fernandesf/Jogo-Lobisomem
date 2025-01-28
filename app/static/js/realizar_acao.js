const poder_acougueiro = document.getElementById('poder_acougueiro');
const button_inspecionar = document.getElementById('inspecionar');
const enviar_inspecao = document.getElementById('enviar_inspecao');

button_inspecionar.addEventListener('click', () => {
    poder_acougueiro.style.display = 'block';
    enviar_inspecao.style.display = 'block';
    poder_acougueiro.style.display = 'none';

});


enviar_inspecao.addEventListener('submit', () => {
    poder_acougueiro.style.display = 'none';
})