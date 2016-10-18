var goTop = function () {
    var top = $("#gotop")
    top.click(function (e) {
        $('body,html').animate({scrollTop: 0}, 1000);
    });

    top.mouseover(function (e) {
        $(this).css("background", "url(http://oexqautw4.bkt.clouddn.com/static/img/backtop.png) no-repeat 0px 0px");
        $(this).css('cursor', 'pointer');
        $(this).css('opacity', '1');
    });

    top.mouseout(function (e) {
        $(this).css("background", "url(http://oexqautw4.bkt.clouddn.com/static/img/backtop.png) no-repeat -70px 0px");
        $(this).css("opacity", "0.5");
    });

    $(window).scroll(function (e) {
        if ($(window).scrollTop() > 1000)
            $("#gotop").fadeIn(1000);
        else
            $("#gotop").fadeOut(1000);
    });
}