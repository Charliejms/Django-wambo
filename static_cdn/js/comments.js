/**
 * Created by karinacacuangosandoval on 22/11/16.
 */

$(".comment-reply-btn").click(function (event) {
    event.preventDefault();
    $(this).parent().next(".comment-reply").fadeToggle();
});