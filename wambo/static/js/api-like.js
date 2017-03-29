$('button').on('click', function (event) {
    event.preventDefault();
    $.ajax({
        url:'/like_post/',
        type: 'get',
        data: {
            post_id : $(this).attr('data-id')
        },
        success : function (response) {
            $(this).html(''+ response);
        }
    })
});