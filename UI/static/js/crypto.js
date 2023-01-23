
function buyCrypto(id){
    var data = JSON.parse(item)
    $('.show-div').show();

    $('#buyHeader').text(item['name'])
}

$(document).ready(function() {
    $('td').click(function (e) { 
        $('.show-div').show()
        var data = []
        e.preventDefault();
        $(this).parent().children().each(function () {
            data.push($(this).text())
        });

        localStorage['price'] = data[2]

        $('#buyHeader').text(data[1])
        $('#priceValue').text(data[2])
        $('#priceSymnol').text(data[0])

    });

    $('.buy-btn').click(function(e){
        $('.show-div').hide()
    })

    $('#moneyDollar').on('input', function () {
        let value = $(this).val()
        if(value != undefined && value != 0){
            $('#priceValue').text(value)
            let main = ((1 / localStorage['price']) * value)
            main = Math.round(main * 10000000) / 10000000

            $('#mainValue').text(main)
        }
        else{
            $('#priceValue').text(localStorage['price'])
            $('#mainValue').text(1)
        }
    });

    $('.crypto-popup-wrapper').click(function (e) {
        $('.show-div').hide()
    })

    $('.crypto-popup').click(function (e) {
        e.stopPropagation()
    })
});


function submitCrypto(){
    let symbol = $('#priceSymnol').text()
    $('#symbol').val(symbol)
    $('#rate').val(localStorage['price'])

    money = $('#moneyDollar').val()
    
    if(money == undefined || money <= 0){
        alert("Money must be greater than 0")
        return
    }

    try{
        var form = document.getElementById('buy-form');
        var formData = new FormData(form);        
    
        $.ajax({
            type: "POST",        
            url: "/buyCrypto",
            data: formData,        
            processData: false,
            contentType: false,
            success: function (response) {
                window.location.reload()
            },
            error: function (ajaxContext) {
                if(ajaxContext.status == 500){
                    alert('You dont have enough money')
                }
                else{
                    alert(ajaxContext.responseText)
                }
                
            } 
        });
    }catch(e){
        console.log(e)
    }
}