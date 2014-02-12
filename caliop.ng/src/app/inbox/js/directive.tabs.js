(function() {

"use strict";

angular.module('caliop.inbox.directive', [])

/**
 * Display a tag.
 */
.directive('tag', function() {
    return {
        restrict: 'E',
        // replace: true,
        scope: {
            tag: '='
        },
        template:
            '<span class="tag label label-default" style="color: {{tag.color}}; background: {{tag.background}}"">' +
                '{{tag.label}}' +
            '</span>'
    };
});

}());
