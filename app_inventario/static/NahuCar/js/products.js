$(() => {

    $('#btn-save-product').click((event) => {
        event.preventDefault()

        var productName = $('#product-name')
        var productPrice = $('#price')
        var productQuantity = $('#quantity')
        var productCategory = $('#category')

        
        //Validar que todos lo campos no esten vacios
        if (!productName.val().trim()){
            productName.focus()
            return
        }

        if (!productPrice.val().trim() || isNaN(productPrice.val())){
            productPrice.focus()
            return
        }

        if (!productQuantity.val().trim() || isNaN(productQuantity.val())){
            productQuantity.focus()
            return
        }

        if (!productCategory.val().trim() || isNaN(productCategory.val())){
            productCategory.focus()
            return
        }


        
        $('#form-product').submit()
    })

})