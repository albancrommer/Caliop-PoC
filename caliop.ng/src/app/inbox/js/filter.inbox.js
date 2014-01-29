(function() {

"use strict";

angular.module('caliop.inbox.filter')

/**
 * Display the list of recipients.
 * Optionnal limit parameter to display only n recipients.
 */
.filter('joinRecipients', function () {
    return function (recipients, limit) {
        limit = limit || 4;

        var names = _.map(recipients, function(r) {
            return r.displayName();
        });

        var finalNames = names;

        if (limit > 0 && names.length > limit) {
            var namesLeft = _.remove(names, function(name, i) {
                if (i > limit-1) {
                    return name;
                }
            });

            // display someting like '+2...'
            var moar = '+' + namesLeft.length;
            moar = '<span class="moar-recipients">'+moar+'...</span>';
            finalNames.push(moar);
        }

        return finalNames.join(', ');
    };
});

}());
