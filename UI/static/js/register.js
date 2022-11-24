function register(){
    try{
        var form = document.getElementById('register-form');
        var formData = new FormData(form);
    
        $.ajax({
            type: "POST",        
            url: "/register",
            data: formData,        
            processData: false,
            contentType: false,
            success: function (response) {
                console.info("User registered!");
            }
        });
    }catch(e){
        console.log(e)
    }
    

    return false;
}

