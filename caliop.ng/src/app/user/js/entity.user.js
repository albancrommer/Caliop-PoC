(function() {

"use strict";

angular.module('caliop.user.entity.user')

.factory('user', ['Restangular', 'string',
    function (Restangular, stringSrv) {

    var User = function User(obj) {
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

    User.prototype.displayName = function(obj) {
        return [this.firstName, this.lastName].join(' ');
    };

    User.new_ = function(obj) {
        return new User(obj);
    };

    Restangular.addElementTransformer('users', false, function(obj) {
        return User.new_(obj);
    });

    return {
        new_: User.new_,
        Restangular: Restangular
    };
}]);

}());
