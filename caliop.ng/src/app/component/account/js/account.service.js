(function() {

"use strict";

angular.module('caliop.account.service')

.factory('auth', ['contact', '$cookieStore', '$q',
    function (contactSrv, $cookieStore, $q) {

    return {
        getContact: function() {
            var contact = $cookieStore.get('contact');
            return contact ? contactSrv.new_(contact) : undefined;
        },

        login: function(credentials) {
            var that = this,
                deferred = $q.defer();

            contactSrv.Restangular.one('contact').post('login', credentials, {}, {
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

        logout: function() {
            $cookieStore.remove('contact');
        }
    };
}]);

}());
