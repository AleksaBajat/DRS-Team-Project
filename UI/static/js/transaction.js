function transaction(){
    value = $('input[name=amount]').val()
    if(value == undefined || value <= 0){
        alert('Value must be greater than 0')
        return;
    }

    form = document.getElementById("transaction-form")
    formData = new FormData(form)

    $.ajax({
        type: "POST",
        url: "/transaction",
        data: formData,        
        processData: false,
        contentType: false,
        success: function (response) {
            alert(response)            
        }
    });
}