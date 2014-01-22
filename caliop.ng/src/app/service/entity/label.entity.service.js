(function() {

"use strict";

angular.module('caliop.service.entity.label', [
    'restangular',
    'caliop.service.helpers'
])

.factory('label', ['Restangular', 'string',
    function (Restangular, stringSrv) {

    var Label = function Label(obj) {
        var self = this;

        angular.extend(self, obj);

        // save obj struct in the object
        angular.forEach(obj, function(value, key) {
            key = stringSrv.toCamelCase(key);
            self[key] = value;

            // convert dates to moment objects
            if (/^date/.test(key)) {
                self[key] = moment(self[key]);
            }
        });
    };

    // Label.prototype.displayName = function(obj) {
    //     return [this.firstName, this.lastName].join(' ');
    // };

    Label.new_ = function(obj) {
        return new Label(obj);
    };

    Restangular.addElementTransformer('labels', false, function(obj) {
        return new Label(obj);
    });

    return {
        new_: Label.new_,
        Restangular: Restangular
    };
}]);

}());
