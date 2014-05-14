$('.glyphicon-circle-arrow-up').click(function() {
    var id = $(this).attr('name');
    var $csrftoken = $.cookie('csrftoken');
    var $this = $(this);
    $.ajax({
        url:'/vote/',
        data: {id: id},
        type: 'POST',
        context: this,
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", $csrftoken);
        },
        success: function(data) {
            $this.removeClass('vote').addClass('voted');
        }
    });

});