(function() {

"use strict";

angular.module('caliop.service.account', [
    'caliop.service.entity.contact'
])

.factory('auth', ['contact',
    function (contactSrv) {

    return {
        contact: undefined,

        getContact: function() {
            if (!this.contact) {
                this.retrieveContact();
            }

            // @TODO return defered
            return this.contact;
        },

        retrieveContact: function(contact) {
            var that = this;

            contactSrv.get().then(function(contact) {
                that.contact = contact;
            });
        }
    };

}]).factory ('login', ['Restangular', 'string', 'contact',
    function (Restangular, stringSrv, contactSrv) {
    console.log('message1');
    return {
        trylogin: function (credentials, scope) {
            var baseAccounts = contactSrv.post('login', credentials).then(
                function (success) {
                    scope.loginitreturn = success.firstName + ' successfully loggued, wait redirect';
                }, function (error) {
                    scope.loginitreturn = error;
                }
            );
        }
    };

}]);

}());
