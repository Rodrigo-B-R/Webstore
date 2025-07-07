

document.addEventListener('DOMContentLoaded', function () {
  console.log('cart.js cargado');
  const updateBtns = document.querySelectorAll('.update-quantity');

  updateBtns.forEach(btn => {
    btn.addEventListener('click', function () {
      const productId = this.dataset.product;
      const action = this.dataset.action;
      const productUrl = this.dataset.url;

      fetch(productUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ action: action }),
      })
        .then(response => response.json())
        .then(data => {
          location.reload(); // O puedes actualizar la cantidad sin recargar
        });
    });
  });

  function getCSRFToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
  }
});
