(function($) {
    $(document).ready(function() {
    	if ($(window).scrollTop() >= 100) {
            $('.main-menu').removeClass('.main-menu_transparent').addClass('.main-menu_white');
        };

        $(window).scroll(function() {
            var scroll = $(this).scrollTop();
            var menu = $('.main-menu');
            console.log('scrolling');

            if (scroll >= 100) {
                menu.removeClass('main-menu_transparent').addClass('main-menu_white');
            } else {
                menu.removeClass('main-menu_white').addClass('main-menu_transparent');
            }
        });

    });
})(jQuery);