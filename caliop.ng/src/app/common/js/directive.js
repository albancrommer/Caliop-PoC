(function() {

"use strict";

angular.module('caliop.directive', [])

/**
 * Set the height of a container dynamically and add scrollbars.
 */
.directive('overflowed', function() {
    return function(scope, element, attrs) {
        var $el = $(element),
            // offset() ignores blocks padding, so we hardore here an offset value
            topOffset = parseInt(attrs.topoffset),
            elementTopOffset = $el.offset().top,
            timeout;

        var setHeight = function() {
            timeout = window.setTimeout(function() {
                var height = $(window).height() - elementTopOffset - topOffset;

                $el .css('height', height + 'px')
                    .css('overflow', 'auto');
            }, 50);
        };

        $(window).on('resize', function() {
            if (timeout) {
                window.clearTimeout(timeout);
                setHeight();
            }
        });

        setHeight();
    };
});

}());
