(function() {

"use strict";

angular.module('caliop.entity.session')

.factory('session', ['Restangular', 'string',
    function (Restangular, stringSrv) {

    var Session = function Session(obj) {
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

    Session.prototype.fullname = function() {
        return [this.firstName, this.lastName].join(' ');
    };

    Session.new_ = function(obj) {
        return new Session(obj);
    };

    Restangular.addElementTransformer('sessions', false, function(obj) {
        var session = Session.new_(obj);
        return session;
    });

    return {
        new_: Session.new_,
        Restangular: Restangular
    };
}]);

}());
