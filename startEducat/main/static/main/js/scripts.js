document.getElementById('add-to-cart-form').addEventListener('submit', function (event) {
    event.preventDefault();
    const url = this.getAttribute('data-url');
    const quantity = document.getElementById('quantity').value;
    const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    fetch(url, {
        method: 'POST',
        body: JSON.stringify({quantity}),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Товар добавлен в корзину');
            } else {
                alert('Ошибка: ' + data.error);
            }
        })
        .catch(error => console.error('Error:', error));
});
