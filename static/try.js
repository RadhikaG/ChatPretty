$(document).ready(function() {
    $(window).scroll(function() {
        var distanceFromTop = $(document).scrollTop();
        if (distanceFromTop >= $('#header').height())
        {
            $('#sticky').fadeIn(400).addClass('fixed');
        }
        else
        {
            $('#sticky').fadeOut(400).removeClass('fixed');
        }
    });
});