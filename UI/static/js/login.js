function login(){
    try{
        var form = document.getElementById('login-form');
        var formData = new FormData(form);
        if(!ValidateEmail())
            throw Error('Invalid email address!');        
        $.ajax({
            type: "POST",        
            url: "/login",
            data: formData,        
            processData: false,
            contentType: false,
            success: function (response) {
                window.location.href="/index" 
            },
            error: function (ajaxContext) {
                alert(ajaxContext.responseText)
            }      
        });
    }catch(e){
        console.log(e)
    }
}

function ValidateEmail() {
    var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    input = document.getElementById('email')
    if (input.value.match(validRegex)) {
        return true;
    } else {
        alert("Invalid email address!");
        return false;
    }
}