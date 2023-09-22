var updateBuyButtons = document.querySelectorAll("#update--buy");
var updateBuyForms = document.querySelectorAll("#product-form-update");
var quantityAll = document.querySelectorAll("#quantity");


updateBuyForms.forEach(function(updateBuyForm, index) {
  updateBuyForm.querySelector('#update--buy').addEventListener('click', function() {

    quantity = quantityAll[index];
    let quantityInput = document.createElement("input");
    quantityInput.type = 'hidden';
    quantityInput.name = 'quantity';
    quantityInput.value = quantity.value;

    updateBuyForm.appendChild(quantityInput);
  })});