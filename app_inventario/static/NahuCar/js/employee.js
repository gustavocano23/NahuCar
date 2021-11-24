$(() => {
    
    $('#btn-save-employee').click((event)=>{
        event.preventDefault()
        
        var dni = $('#employee-dni')
        var employeeName = $('#employee-name')
        var employeeLastName = $('#employee-last-name')
        var telphone = $('#employee-telphone')
        var address = $('#employee-address')

        if (!dni.val().trim() ||dni.val().length !== 13 || isNaN(dni.val())){
            dni.focus()
            return
        }

        if (!employeeName.val().trim()){
            employeeName.focus()
            return
        }
        if (!employeeLastName.val().trim()){
            employeeLastName.focus()
            return
        }
        if (!telphone.val().trim()){
            telphone.focus()
            return
        }
        if (!address.val().trim()){
            address.focus()
            return
        }
        
        $('#form-employee').submit()

    })

})