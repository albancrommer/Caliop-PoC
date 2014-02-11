(function() {

"use strict";

angular.module('caliop.user.filter')

/**
 * Display the list of users.
 * Optionnal limit parameter to display only n users.
 */
.filter('joinUsers', function () {
    return function (users, limit) {
        limit = limit || 4;

        var names = _.map(users, function(r) {
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
            moar = '<span class="filter-join-users_moar-users">'+moar+'...</span>';
            finalNames.push(moar);
        }

        return finalNames.join(', ');
    };
});

}());
