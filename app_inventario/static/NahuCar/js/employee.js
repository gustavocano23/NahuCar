$(() => {

    function notify(style, msg) {
        $.notify.defaults({ className: style });
        $.notify(msg, {position: 'top right', });
    }

    $('#btn-save-employee').click((event)=>{
        event.preventDefault()
        
        var dni = $('#employee-dni')
        var employeeName = $('#employee-name')
        var employeeLastName = $('#employee-last-name')
        var telphone = $('#employee-telphone')
        var address = $('#employee-address')

        if (!dni.val().trim() ||dni.val().length !== 13 || isNaN(dni.val())){
            notify('error', 'Debe de llenar el campo o Ingrese 13 dígitos')
            dni.focus()
            return
        }

        if (!employeeName.val().trim()){
            notify('error', 'Debe de llenar el campo')
            employeeName.focus()
            return
        }
        if (!employeeLastName.val().trim()){
            notify('error', 'Debe de llenar el campo')
            employeeLastName.focus()
            return
        }
        if (!telphone.val().trim()){
            notify('error', 'Debe de llenar el campo')
            telphone.focus()
            return
        }
        if (!address.val().trim()){
            notify('error', 'Debe de llenar el campo')
            address.focus()
            return
        }
        
        $('#form-employee').submit()

    })

})