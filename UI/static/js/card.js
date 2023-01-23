function addCard() {
    try {
        var form = document.getElementById('card-form');
        if(!validateForm(form)){
            throw new Error('Error');
        }
        var formData = new FormData(form);

        $.ajax({
            type: "POST",
            url: "/card",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                window.location.href = "/index"
            },
            error: function (ajaxContext) {
                if(ajaxContext.status == 401){
                    alert('Invalid card')
                }
                else{
                    console.log(ajaxContext.responseText)
                }
            } 
        });
    } catch (e) {
        console.log(e)
    }

}


function transferMoney() {
    money = $('#money').val()
    if(money == undefined || money <= 0){
        alert('Value must be greater than 0')
        return
    }

    try {
        var form = document.getElementById('card-form');
        var formData = new FormData(form);

        $.ajax({
            type: "POST",
            url: "/transferFromCard",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                window.location.href = "/index"
            }
        });
    } catch (e) {
        console.log(e)
    }
}

function validateForm(form) {
    var cardNumber = form["cardNumber"].value;
    var year = form["year"].value;
    var month= form["month"].value;
    var csc = form["csc"].value;
    var cardHolder = form["name"].value;
   
    cardNumber=cardNumber.replaceAll('-','');
    if (cardNumber.length != 16) {
        alert("Card number must be 16 digits");
        return false;
    }
    if (year == "" || month == "") {
        alert("Expiration date is required");
        return false;
    }
    if (csc == "") {
        alert("CVV is required");
        return false;
    }
    if (csc.length != 3) {
        alert("CVV must be 3 digits");
        return false;
    }
    if (cardHolder == "") {
        alert("Card holder name is required");
        return false;
    }

    return true;
}
