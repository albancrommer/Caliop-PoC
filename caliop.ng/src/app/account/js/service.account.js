(function() {

"use strict";

angular.module('caliop.account.service.account')

.factory('auth', ['$cookieStore', '$q', 'session',
    function ($cookieStore, $q, SessionSrv) {

    return {
        /**
         * Return the authed contact from the cookie.
         */
        getContact: function() {
            var contact = $cookieStore.get('session');
            return contact ? new SessionSrv(contact) : undefined;
        },

        /**
         * Do a POST query on the API,
         * set the cookie
         * and return a promise object.
         */
        login: function(credentials) {
            var that = this,
                deferred = $q.defer();

            SessionSrv.postCredentials(credentials).then(
                function(contactInfo) {
                    $cookieStore.put('session', contactInfo);
                    deferred.resolve(that.getContact());
                },
                function() {
                    deferred.reject('Bad credentials');
                }
            );

            return deferred.promise;
        },

        /**
         * Do a DELETE query on the API,
         * remove the cookie
         * and return a promise object.
         */
        logout: function() {
            return SessionSrv.remove().then(function(response) {
                if (response.status == 'logout') {
                    $cookieStore.remove('session');
                }
            });
        }
    };
}]);

}());
