var buttonBuy = document.getElementById("action--buy");
buttonBuy.onclick = function(){
    let quantity = document.getElementById("quantity")
    let selectedOption = document.getElementById("options")
    let quantityInput = document.createElement("input");
    let form = document.getElementById("product-form");
    quantityInput.type = 'hidden';
    quantityInput.name = 'quantity';
    quantityInput.value = quantity.value;
    if (selectedOption) {
        let selectedOptionInput = document.createElement("input");
        selectedOptionInput.type = 'hidden';
        selectedOptionInput.name = 'selectedOption';
        selectedOptionInput.value = selectedOption[selectedOption.selectedIndex].id;
        form.appendChild(selectedOptionInput);
    }

    form.appendChild(quantityInput);
}