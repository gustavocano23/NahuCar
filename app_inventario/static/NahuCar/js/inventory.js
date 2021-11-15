$(()=> {
    
    //Llenar la informacion del modal dependiendo del usuario
    $('.show-inventory-info').click(event => {
        $('.modal-insert').modal('show')
    })

    $('#btn-update-inventory').click((event)=> {
        event.preventDefault()
        var $me = $('#btn-update-inventory')
        //Capturar las variables del formulario
        var action = $('#type-action')
        var quantity = $('#quantity')
        var typeAction= $me.data("action")
        alert(typeAction)

    })

})