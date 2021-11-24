$(() => {

    function notify(style, msg) {
        $.notify.defaults({ className: style });
        $.notify(msg, {position: 'top right', });
    }

    $('#btn-save-product').click((event) => {
        event.preventDefault()

        var productName = $('#product-name')
        var productPrice = $('#price')
        var productQuantity = $('#quantity')
        var productCategory = $('#category')

        
        //Validar que todos lo campos no esten vacios
        if (!productName.val().trim()){
            notify('error', 'Debe de llenar el campo')
            productName.focus()
            return
        }

        if (!productPrice.val().trim() || isNaN(productPrice.val())){
            notify('error', 'Debe de llenar el campo o Ingrese un valor númerico')
            productPrice.focus()
            return
        }

        if (!productQuantity.val().trim() || isNaN(productQuantity.val())){
            notify('error', 'Debe de llenar el campo o Ingrese un valor númerico')
            productQuantity.focus()
            return
        }

        if (!productCategory.val().trim() || isNaN(productCategory.val())){
            notify('error', 'Debe de llenar el campo o Ingrese un valor númerico')
            productCategory.focus()
            return
        }
        
        $('#form-product').submit()
        
    })


})