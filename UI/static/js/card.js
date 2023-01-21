function addCard(){
    try{
        var form = document.getElementById('card-form');
        var formData = new FormData(form);        
    
        $.ajax({
            type: "POST",        
            url: "/card",
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