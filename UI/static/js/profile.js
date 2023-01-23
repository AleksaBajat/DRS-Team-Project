function getCurrencies(){  
    let symbols = []
    $('.crypto_row').each(function () {
        symbols.push($(this).children(':first').text())
    })
    symbols = symbols.join(',')

    parameters = {
        symbol:symbols,
        convert:'USD'
    } 
    try{
        $.ajax({
            type: "POST",        
            url: "/swap",
            data: parameters,        
            success: function (response) {
                openPopup(response)
            },
            error: function (ajaxContext) {
                alert(ajaxContext.responseText)
            }      
        });
        $('.show-div').show()
    }catch(e){
        console.log(e)
    }
}

$(document).ready(function() {

    localStorage['fromSymbol'] = '$'
    localStorage['toSymbol'] = '$'

    $('.crypto-popup-wrapper').click(function (e) {
        $('.show-div').hide()
        $('.from-select').empty()
        $('.to-select').empty()
        $('#fromValue').text(1)
        $('#toValue').text(1)
        $('#fromSymbol').text('$')
        $('#toSymbol').text('$')
    })

    $('.crypto-popup').click(function (e) {
        e.stopPropagation()
    })

    $('.from-select').on('change', function (e) {
        var optionSelected = $("option:selected", this);
        var valueSelected = this.value;

        let toSymbol = $('#toSymbol').text()
        localStorage['fromSymbol'] = valueSelected

        let value2 = 1
        let value1 = 0
        let data = JSON.parse(localStorage['filteredData'])
        data.forEach(element => {
            if(element.symbol == valueSelected){
                value1 = element.quote.USD.price
            }
            if(element.symbol == toSymbol){
                value2 = element.quote.USD.price
            }
        });

        if(value1 == 0) value1 = 1
        if(value2 == 0) value2 = 1

        main = Math.round((value2/value1) * 10000000) / 10000000

        $('#fromValue').text(main)
        $('#toValue').text(1)
        $('#fromSymbol').text(valueSelected)
    });

    $('.to-select').on('change', function (e) {
        var optionSelected = $("option:selected", this);
        var valueSelected = this.value;
        
        let fromSymbol = $('#fromSymbol').text()
        localStorage['toSymbol'] = valueSelected

        let value2 = 1
        let value1 = 0
        let data = JSON.parse(localStorage['filteredData'])
        data.forEach(element => {
            if(element.symbol == valueSelected){
                value2 = element.quote.USD.price
            }
            if(element.symbol == fromSymbol){
                value1 = element.quote.USD.price
            }
        });

        if(value1 == 0) value1 = 1
        if(value2 == 0) value2 = 1

        let rate = value1/value2
        $('#rate').val(rate)

        main = Math.round((value2/value1) * 10000000) / 10000000

        $('#fromValue').text(main)
        $('#toValue').text(1)
        $('#toSymbol').text(valueSelected)
    });

    $('#moneyDollar').on('input', function () {
        let value = $(this).val()
        if(value != undefined && value > 0){
            let data = JSON.parse(localStorage['filteredData'])

            from = localStorage['fromSymbol']
            to = localStorage['toSymbol']
            console.log(from)
            console.log(to)
            if(from == undefined) from = '$'
            if(to == undefined) to = '$'

            data.forEach(element => {
                if(element.symbol == from){
                    value1 = element.quote.USD.price
                }
                if(element.symbol == to){
                    value2 = element.quote.USD.price
                }
            });

            if(value1 == 0) value1 = 1
            if(value2 == 0) value2 = 1

            let rate = value1/value2
            $('#rate').val(rate)

            let main = (value1/value2) * value
            main = Math.round(main * 10000000) / 10000000

            $('#fromValue').text(value)
            $('#toValue').text(main)
        }
        else{

        }
        
    });
});

function openPopup(data){
    var crypto = []
    response = JSON.parse(data)
    response = response['data']
    for(const key in response) {
        crypto.push(response[key])
    }

    localStorage['filteredData'] = JSON.stringify(crypto)

    $('.from-select').empty()
    $('.to-select').empty()
    crypto.forEach(element => {
        $('.from-select').append('<option value="' + element.symbol + '">' + element.symbol + '</option>');
        $('.to-select').append('<option value="' + element.symbol + '">' + element.symbol + '</option>');
    });

    $('#fromValue').text(1)
    $('#toValue').text(1)
    $('#fromSymbol').text('$')
    $('#toSymbol').text('$')
    
}

function submitCrypto(){
    try{
        var form = document.getElementById('buy-form');
        var formData = new FormData(form);
        
        money = $('#moneyDollar').val()
        if(money <= 0){
            alert('Number must be greater than 0')
            e.stopPropagation()
            return;
        }

        $.ajax({
            type: "POST",        
            url: "/swapCurrencies",
            data: formData,        
            processData: false,
            contentType: false,
            success: function (response) {
                $('.from-select').empty()
                $('.to-select').empty()
                $('#fromValue').text(1)
                $('#toValue').text(1)
                $('#fromSymbol').text('$')
                $('#toSymbol').text('$')
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