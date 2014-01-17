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

            contactSrv.one('contact', 'info').get().then(function(contact) {
                that.contact = contact;
            });
        }
    };
}])

.factory ('login', ['Restangular', 'string', 'contact',
    function (Restangular, stringSrv, contactSrv) {

    return {
        // @TOFIX the factory DONT MUST manipulate the scope!
        trylogin: function (credentials, scope) {
            var baseAccounts = contactSrv.one('contact').post('login', credentials).then(
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
