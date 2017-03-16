/**
 * Created by richardcj on 5/10/16.
 */
$(document).ready(function () {
    $('.content-markdown').each(function () {
        var content  = $(this).text();
        var marketContent = market(content);
        $(this).html(marketContent);
    })
    //aladimo las clase para que se acapten las imgs al post
    $('.post-detail-item img').each(function () {
        $(this).addClass('img-responsive');
    })


    /***
     * POST Form
     */
    //preview-title
    var titleItem = $('#id_title').val();
    var titlepreview = $('#preview-title').content(titleItem.val());
    console.log(titlepreview)

    //preview-content
    var contentItem  = $('#id_content');
    var preview = $('#preview-content').content(contentItem.val());
    console.log(preview);

})