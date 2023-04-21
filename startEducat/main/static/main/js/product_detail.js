// static/js/product_detail.js

document.addEventListener('DOMContentLoaded', () => {
    const addToCartForm = document.getElementById('add-to-cart-form');

    if (addToCartForm) {
        addToCartForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const form = event.target;
            const url = form.dataset.url;

            const formData = new FormData(form);
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            });

            const response_data = await response.json();
            if (response_data.status === 'success') {
                alert(response_data.message);
            } else {
                alert(response_data.message);
            }
        });
    }
});
