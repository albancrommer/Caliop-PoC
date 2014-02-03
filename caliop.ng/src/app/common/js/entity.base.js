(function() {

"use strict";

angular.module('caliop.common.entity.base', [])

.factory('base', ['Restangular', 'string',
    function (Restangular, stringSrv) {

    var Base = function Base(obj) {
        var self = this;

        angular.extend(self, obj);

        // save obj struct in the object
        angular.forEach(obj, function(value, key) {
            var camelCaseKey = stringSrv.toCamelCase(key);
            self[camelCaseKey] = value;

            // remove the dash key
            if (camelCaseKey != key) {
                delete self[key];
            }

            // convert dates to moment objects
            if (/^date/.test(key)) {
                self[key] = moment(self[key]);
            }
        });
    };

    return Base;
}]);

}());
