(function() {

"use strict";

angular.module('caliop.entity.session')

.factory('session', ['Restangular', 'base',
    function (Restangular, BaseEnt) {

    function Session() { BaseEnt.apply(this, arguments); }
    Session.prototype = Object.create(BaseEnt.prototype);

    /**
     * Return the fullname of the logged user.
     */
    Session.prototype.fullname = function() {
        return [this.firstName, this.lastName].join(' ');
    };

    /**
     * Do a POST to login in.
     */
    Session.postCredentials = function(credentials) {
        return Restangular.all('sessions').post(credentials, {}, {
            'Content-Type': 'application/x-www-form-urlencoded'
        });
    };

    /**
     * Do a DELETE query to remove the session.
     */
    Session.remove = function() {
        return Restangular.one('sessions').remove();
    };

    Restangular.addElementTransformer('sessions', false, function(obj) {
        return new Session(obj);
    });

    return Session;
}]);

}());
