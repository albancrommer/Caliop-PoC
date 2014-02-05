(function() {

"use strict";

angular.module('caliop.account.service.account')

.factory('auth', ['$cookieStore', '$q', 'session', 'Restangular',
    function ($cookieStore, $q, SessionSrv, RestangularPrvd) {

    return {
        // @TODO implements a token regeneration in the API/client
        token: $cookieStore.get('token'),

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
                    that.token = contactInfo.token;

                    if (!that.token) {
                        deferred.reject('Token not found.');
                        return;
                    }

                    $cookieStore.put('session', contactInfo);
                    $cookieStore.put('token', that.token);

                    that.configureRestangularHeaders();

                    deferred.resolve(contactInfo);
                },
                function() {
                    deferred.reject('Bad credentials');
                }
            );

            return deferred.promise;
        },

        /**
         * Return the token of the logged contact.
         * It will be sent in the headers of any REST calls.
         */
        getToken: function() {
            return $cookieStore.get('token');
        },

        /**
         * Save the token in the default headers of Restangular.
         */
        configureRestangularHeaders: function() {
            RestangularPrvd.setDefaultHeaders({'X-Auth-Token': this.token});
        },

        /**
         * Do a DELETE query on the API,
         * remove the cookie
         * and return a promise object.
         */
        logout: function() {
            return SessionSrv.remove().then(function(response) {
                if (response.status == 'logout') {
                    // @TODO Manager to get/save/delete all cookies of the app
                    $cookieStore.remove('session');
                    $cookieStore.remove('token');
                    $cookieStore.remove('inBoxTabs');

                    // remove the token from the default headers
                    RestangularPrvd.setDefaultHeaders({'X-Auth-Token': ''});
                }
            });
        }
    };
}]);

}());
