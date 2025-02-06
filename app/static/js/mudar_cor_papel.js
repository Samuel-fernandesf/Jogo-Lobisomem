function mudarCorPapel() {
    let textoPapel = document.getElementById("papel-atual");
    if (!textoPapel) return;

    let papel = textoPapel.textContent.trim();

    let classes = {
        "Vampiro": "vampiro",
        "Condessa": "condessa",
        "Caçador": "cacador",
        "Açougueiro": "acougueiro",
        "Campones": "campones"
    };

    // Remove todas as classes de cor antes de aplicar a nova
    textoPapel.classList.remove(...Object.values(classes));

    // Adiciona a classe correspondente ao papel
    if (classes[papel]) {
        textoPapel.classList.add(classes[papel]);
    }
}