
//Rest the value when reply-dialog-box dismiss
function undo_reply() {
    $('#follow').val(-1);
}

function go_to_reply(id, author_name) {
    $('html, body').animate({scrollTop:  $('#submit-comment').offset().top}, 800);
    $('#follow').val(id);
    $('#reply-dialog-box').remove();
    $('#submit-comment-container').prepend('<div class="alert alert-info alert-dismissable" id="reply-dialog-box">' +
            '<button type="button" class="close" data-dismiss="alert" onclick="undo_reply()">&times;</button>' +
            '回复给<strong><i>' + author_name +'</i></strong> </div>');
}

//Reset the follow value when refresh page
window.onload = function(){
    $('#follow').val(-1);
}



