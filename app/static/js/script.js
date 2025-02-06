document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".flip").forEach(card => {
        card.addEventListener("click", function () {
            this.classList.toggle("flipped");
        });
    });
});
