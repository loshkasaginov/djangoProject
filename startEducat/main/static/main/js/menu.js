document.addEventListener('DOMContentLoaded', function () {
    const menu = document.querySelector('.menu');
    let previousScroll = window.pageYOffset;

    window.addEventListener('scroll', function () {
        const currentScroll = window.pageYOffset;
        if (currentScroll <= 0) {
            menu.style.display = 'block';
        } else if (currentScroll < previousScroll) {
            menu.style.display = 'block';
        } else {
            menu.style.display = 'none';
        }
        previousScroll = currentScroll;
    });
});


