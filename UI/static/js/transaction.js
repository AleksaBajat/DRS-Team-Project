function transaction(){
    form = document.getElementById("transaction-form")
    formData = new FormData(form)

    $.ajax({
        type: "POST",
        url: "/transaction",
        data: formData,        
        processData: false,
        contentType: false,
        success: function (response) {
            console.log(response)            
        }
    });
}