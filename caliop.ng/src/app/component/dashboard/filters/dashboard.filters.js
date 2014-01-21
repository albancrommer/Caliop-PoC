(function() {

"use strict";

angular.module('caliop.component.dashboard.filters', [])

/**
 * Display the list of recipients.
 * Optionnal limit parameter to display only n recipients.
 */
.filter('joinRecipients', function () {
    return function (recipients, limit) {
        limit = limit || 5;

        var parts = _.map(recipients, function(r) {
            return r.displayName();
        });

        if (parts.length > limit) {
            parts = parts.splice(0, limit);
            parts.push('...');
        }

        return parts.join(', ');
    };
});

}());
