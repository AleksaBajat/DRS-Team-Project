function login(){
    try{
        var form = document.getElementById('login-form');
        var formData = new FormData(form);        
    
        $.ajax({
            type: "POST",        
            url: "/login",
            data: formData,        
            processData: false,
            contentType: false,
            success: function (response) {
                window.location.href="/index" 
            }
        });
    }catch(e){
        console.log(e)
    }
}
