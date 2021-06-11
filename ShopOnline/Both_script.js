if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
}
else {
    ready()
}
 // Function for responsive dropdown menu ( navigation bar )
    function myFunction() {
        var x = document.getElementById("myTopnav");
        if (x.className === "topnav") {
            x.className += " responsive";
        } else {
            x.className = "topnav";
        }
}

function ready() {

    var addToCartButtons = document.getElementsByClassName('btn')
    for (var i = 0; i < addToCartButtons.length; i++) {
        var button = addToCartButtons[i]
        button.addEventListener('click', addToCartClicked)
    }


    var sortingArea = document.getElementsByClassName('options')
    var sortingValues = sortingArea.getElementsByClassName('option')
    for (var i = 0; i < sortingValues.length; i++) {
        var input = sortingValues[i]
        input.addEventListener('change', sortingChanged)
    }

}

// Function for sorting the items:
function sortingChanged(event) {
    var input = event.target

    var produs = document.getElementsByClassName('product')
    var shoppingSection = produs.parentElement

    var array = []

    var children = shoppingSection.children;
    for (var i = 0; i < children.length; i++) {
        array.push(children[i])
    
    }

    while (shoppingSection.hasChildNodes()) {
        shoppingSection.removeChild(shoppingSection.firstChild)
    }

    if (input.value == "default") {
        for (var j = 0; j < array.length; j++)
            shoppingSection.appendChild(array[j])
    }

    if (input.value == "orderByPriceAsc") {

        var clonedArray = JSON.parse(JSON.stringify(array))

        clonedArray.sort(function (a, b) {
            var price1 = a.getElementsByClassName('shop-item-price')
            var price2 = b.getElementsByClassName('shop-item-price')
            return parseFloat(price1.innerText.replace('$', '')) - parseFloat(price2.innerText.replace('$', ''));
        });

        for (var j = 0; j < array.length; j++)
            shoppingSection.appendChild(clonedArray[j])
    }

    if (input.value == "orderByPriceDesc") {

        var clonedArray = JSON.parse(JSON.stringify(array))

        clonedArray.sort(function (a, b) {
            var price1 = a.getElementsByClassName('shop-item-price')
            var price2 = b.getElementsByClassName('shop-item-price')
            return parseFloat(price2.innerText.replace('$', '')) - parseFloat(price1.innerText.replace('$', ''));
        });

        for (var j = 0; j < array.length; j++)
            shoppingSection.appendChild(clonedArray[j])
    }

       
}



function addToCartClicked(event) {
    var button = event.target
    var shopItem = button.parentElement.parentElement

    if (localStorage.length == 0)
        var items = []
    else
        var items = JSON.parse(localStorage.getItem('itm'))
  
    var title = shopItem.getElementsByClassName('shop-item-title')[0].innerText
    var price = shopItem.getElementsByClassName('shop-item-price')[0].innerText
    var imageSrc = shopItem.getElementsByClassName('shop-item-image')[0].src

    data = {
        titlu: title,
        pret: price,
        imagine: imageSrc
    };

    if (localStorage.length != 0) {
        for (var i = 0; i < items.length; i++)
            if (items[i].titlu == data.titlu) {
                alert('This item was already added to the cart')
                return
            }
    }
    
    items.push(data)
    localStorage.setItem('itm', JSON.stringify(items))
    
    //localStorage.item += JSON.stringify({ "theTitle": title, "thePrice": price, "theImage": imageSrc })

    //localStorage.setItem("theTitle", JSON.stringify(title))
    //localStorage.setItem("thePrice", JSON.stringify(price))
    //localStorage.setItem("theImage", JSON.stringify(imageSrc))
  
}




