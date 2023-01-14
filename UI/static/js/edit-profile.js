function editProfile(){
    try{
        var form = document.getElementById('edit-profile-form');
        var formData = new FormData(form);                
    
        $.ajax({
            type: "POST",        
            url: "/editProfile",
            data: formData,        
            processData: false,
            contentType: false,
            success: function (response) {
                console.info(response);        
            }
        });
    }catch(e){
        console.log(e)
    }
}

