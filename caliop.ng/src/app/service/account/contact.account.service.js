(function() {

"use strict";

angular.module('caliop.service.account')

.factory('contact', ['string', function (stringSrv) {

    var Contact = function Contact(json) {
        this.name = 'FooUser';
    };

    return new Contact();

}]);

}());
