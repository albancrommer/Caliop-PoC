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

}]);

}());
