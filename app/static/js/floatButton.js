//JS For FloatButton to goTop, goBottom and refresh
$(document).ready(function(){
    //$('#goTop').click(function(){
    //    $(window).scrollTop(0);
    //});
    $('#goTop').click(function(){
        $('html, body').animate({scrollTop: '0px'}, 800);
    });
    $('#refresh').click(function(){
        window.location.reload();
    });
    $('#goBottom').click(function(){
        $('html, body').animate({scrollTop: $('.footer').offset().top}, 800);
    });
});


