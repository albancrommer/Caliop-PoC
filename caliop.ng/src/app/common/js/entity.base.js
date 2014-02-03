(function() {

"use strict";

angular.module('caliop.common.entity.base', [
    'restangular'
])

.factory('base', ['Restangular', 'string',
    function (Restangular, stringSrv) {

    var Base = function Base(obj) {
        var self = this;

        // save obj struct in the object
        angular.forEach(obj, function(value, key) {
            var camelCaseKey = stringSrv.toCamelCase(key);
            obj[camelCaseKey] = value;

            // remove the dash key
            if (camelCaseKey != key) {
                delete obj[key];
            }

            // convert dates to moment objects
            if (/^date/.test(camelCaseKey)) {
                obj[camelCaseKey] = moment(obj[camelCaseKey], 'YYYY-MM-DD HH:mm:ss');
            }
        });

        angular.extend(self, obj);
    };

    return Base;
}]);

}());
