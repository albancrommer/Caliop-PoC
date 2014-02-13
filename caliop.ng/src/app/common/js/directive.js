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
            topOffset = parseInt(attrs.topoffset, 10),
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
})

/**
 * Handle the prop value of a checkbox (none, indetermediate, checked).
 */
.directive('checkedStatus', function() {
    return function(scope, element, attrs) {
        var state = parseFloat(attrs.checkedStatus),
            $el = $(element);

        if (state === 0) {
            $el.prop('checked', false);
        }
        else if (state == 1) {
            $el.prop('checked', true);
        }
        else {
            $el.prop('indeterminate', true);
        }
    };
});

}());
