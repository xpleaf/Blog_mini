//JS For manage-articles when select articles
$(document).ready(function () {
    $('#select-all').click(function () {
        if ($(this).attr('checked')) {
            $('.select-article').attr('checked', true);
        } else {
            $('.select-article').attr('checked', false);
        }
    });
});

//JS For submit article id to delete article
function delCfm(articleId) {
    $('#cfmClick').click(function(){
        formSubmit(articleId);
    });
    $('#delCfmModel').modal();
}
function formSubmit(articleId) {
    $('#delForm'+articleId).submit();
}