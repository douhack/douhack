(function($) {
    $(document).ready(function() {
    	if ($(window).scrollTop() >= 100) {
            $('.main-menu').removeClass('.main-menu_transparent').addClass('.main-menu_white');
        };

        $(window).scroll(function() {
            var scroll = $(this).scrollTop();
            var menu = $('.main-menu');

            if (scroll >= 100) {
                menu.removeClass('main-menu_transparent').addClass('main-menu_white');
            } else {
                menu.removeClass('main-menu_white').addClass('main-menu_transparent');
            }
        });


        $('.menu').on('click', function() {
        	$('#menu-button').prop('checked', false);
        });

        $('.animated').appear(function() {
            var element = $(this);
            var animation = element.data('animation');
            var animationDelay = element.data('delay');
            if (animationDelay) {
                setTimeout(function() {
                    element.addClass(animation + " visible");
                    element.removeClass('hiding');
                    if (element.hasClass('counter')) {
                        element.find('.timer').countTo();
                    }
                }, animationDelay);
            } else {
                element.addClass(animation + " visible");
                element.removeClass('hiding');
                if (element.hasClass('counter')) {
                    element.find('.timer').countTo();
                }
            }
        }, {
            accY: -150
        });


    });
})(jQuery);