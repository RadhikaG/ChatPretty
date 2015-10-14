$(document).ready(function() {
    $(window).scroll(function() {
        var distanceFromTop = $(document).scrollTop();
        if (distanceFromTop >= $('#header').height())
        {
            $('#sticky-header').fadeIn(400).addClass('fixed');
        }
        else
        {
            $('#sticky-header').fadeOut(400).removeClass('fixed');
        }
    });
});