(function() {

"use strict";

angular.module('caliop.service.account', [
    'caliop.service.entity.contact'
])

.factory('auth', ['contact',
    function (contactSrv) {

    return {
        contact: undefined,

        login: function(credentials) {
            return contactSrv.one('contact').post('login', credentials, {}, {
                'Content-Type': 'application/x-www-form-urlencoded'
            });
        },

        logout: function() {
            this.contact = undefined;
        },

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
}]);

}());
