(function($) {

    $(window).load(function() {
        if ($(window).width() > 768) {
            var delay = 0;
            $(".menu__item").addClass("animated flipInX visible").removeClass("hiding");
            $(".menu__item").each(function() {
                $(this).css("animation-delay", delay/4+"s");
                delay++;
            });
        } else {
            $(".menu__item").addClass("visible").removeClass("hiding");
        }
    });

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

        if ($(window).width() < 768) {
            $('.animated').removeClass('animated').removeClass('hiding');
        }

        $(document).on('click', function(event) {
            if($(".menu").is(":visible")) {
                if($(event.target).closest(".custom-dropdown").size() <= 0){
                    $(".custom-dropdown input").prop("checked", false);
                }
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
                    element.addClass(animation + ' visible');
                    element.removeClass('hiding');
                    if (element.hasClass('counter')) {
                        element.find('.timer').countTo();
                    }
                }, animationDelay);
            } else {
                element.addClass(animation + ' visible');
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