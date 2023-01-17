function register(){
    try{
        var form = document.getElementById('register-form');
        var formData = new FormData(form);

        formData.delete('repeatPassword')
    
        $.ajax({
            type: "POST",        
            url: "/register",
            data: formData,        
            processData: false,
            contentType: false,
            success: function (response) {
                console.info(response);       
                alert("Successfully registered!")
                window.location.href="/login" 
            }
        });
    }catch(e){
        console.log(e)
    }
}

