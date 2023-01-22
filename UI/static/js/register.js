function register(){
    try{
        var form = document.getElementById('register-form');
        var formData = new FormData(form);
        if(!ValidateForm())
            throw Error('Form not filled correctly');
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
        console.error(e)
    }
}

function ValidateForm() {
    var validRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
    email = document.getElementById('email').value;
    firstName = document.getElementById('name').value;
    lastName = document.getElementById('last-name').value;
    address = document.getElementById('address').value;
    city = document.getElementById('city').value;
    country = document.getElementById('country').value;
    phoneNumber = document.getElementById('phone-number').value;
    password = document.getElementById('password').value;
    repeat = document.getElementById('repeat_password').value;

    if (!email.match(validRegex)) {
        alert("Invalid email address!");
        return false;
    }
    if(firstName==""|| lastName=="" || address==""||city==""||country==""||phoneNumber==""||password==""||repeat==""){
        alert("All fields must be filled");
        return false;
    }
    return true
}
