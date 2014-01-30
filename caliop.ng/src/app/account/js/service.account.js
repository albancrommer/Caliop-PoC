(function() {

"use strict";

angular.module('caliop.service.account')

.factory('auth', ['contact', '$cookieStore', '$q',
    function (contactSrv, $cookieStore, $q) {

    return {
        /**
         * Return the authed contact from the cookie.
         */
        getContact: function() {
            var contact = $cookieStore.get('contact');
            return contact ? contactSrv.new_(contact) : undefined;
        },

        /**
         * Do a POST query on the API,
         * set the cookie
         * and return a promise object.
         */
        login: function(credentials) {
            var that = this,
                deferred = $q.defer();

            contactSrv.Restangular.all('sessions').post(credentials, {}, {
                'Content-Type': 'application/x-www-form-urlencoded'
            })
            .then(
                function() {
                    contactSrv.Restangular.one('contact', 'info').get()
                    .then(
                        function(contact) {
                            $cookieStore.put('contact', contact);
                            deferred.resolve(that.getContact());
                        },
                        function() {
                            deferred.reject('Contact info failed');
                        });
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
            return contactSrv.Restangular.one('sessions').remove()
                .then(function(response) {
                    if (response.status == 'logout') {
                        $cookieStore.remove('contact');
                    }
                });
        }
    };
}]);

}());
