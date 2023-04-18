$(document).ready(function () {
    // Получите модальное окно и его элементы
    var modal = document.getElementById("imageModal");
    var img = document.getElementById("product-image");
    var modalImg = document.getElementById("modalImage");
    var span = document.getElementsByClassName("close")[0];

    // Откройте модальное окно при клике на изображение
    img.onclick = function () {
        modal.style.display = "block";
        modalImg.src = this.src;
    };

    // Закройте модальное окно при клике на крестик
    span.onclick = function () {
        modal.style.display = "none";
    };

    // Закройте модальное окно при клике вне его
    $(window).click(function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});
