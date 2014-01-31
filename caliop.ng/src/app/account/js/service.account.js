(function() {

"use strict";

angular.module('caliop.service.account')

.factory('auth', ['session', '$cookieStore', '$q',
    function (SessionSrv, $cookieStore, $q) {

    return {
        /**
         * Return the authed contact from the cookie.
         */
        getContact: function() {
            var contact = $cookieStore.get('session');
            return contact ? SessionSrv.new_(contact) : undefined;
        },

        /**
         * Do a POST query on the API,
         * set the cookie
         * and return a promise object.
         */
        login: function(credentials) {
            var that = this,
                deferred = $q.defer();

            SessionSrv.Restangular.all('sessions').post(credentials, {}, {
                'Content-Type': 'application/x-www-form-urlencoded'
            })
            .then(
                function(contactInfo) {
                    $cookieStore.put('session', contactInfo);
                    deferred.resolve(that.getContact());
                },
                function() {
                    deferred.reject('Bad credentials');
                });

            return deferred.promise;
        },

        /**
         * Do a DELETE query on the API,
         * remove the cookie
         * and return a promise object.
         */
        logout: function() {
            return SessionSrv.Restangular.one('sessions').remove()
                .then(function(response) {
                    if (response.status == 'logout') {
                        $cookieStore.remove('session');
                    }
                });
        }
    };
}]);

}());
