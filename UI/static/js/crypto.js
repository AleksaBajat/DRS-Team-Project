
function buyCrypto(id){
    console.log(item)
    var data = JSON.parse(item)
    console.log(data)
    $('.show-div').show();
    console.log(data.name)

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

    $('#money').on('input', function () {
        let value = $(this).val()
        if(value != undefined && value != 0){
            $('#priceValue').text(value)
            let main = ((1 / localStorage['price']) * value)
            main = Math.round(main * 100000) / 100000

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
        console.log(e)
        e.stopPropagation()
    })
});
