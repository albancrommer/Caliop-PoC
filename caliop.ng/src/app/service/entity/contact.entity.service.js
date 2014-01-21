(function() {

"use strict";

angular.module('caliop.service.entity.contact', [
    'restangular',
    'caliop.service.helpers'
])

.factory('contact', ['Restangular', 'string',
    function (Restangular, stringSrv) {

    var Contact = function Contact(obj) {
        var self = this;

        angular.extend(self, obj);

        // save obj struct in the object
        angular.forEach(obj, function(value, key) {
            key = stringSrv.toCamelCase(key);
            self[key] = value;

            // convert dates to moment objects
            if (/^date/.test(key)) {
                self[key] = moment(self[key]);
            }
        });
    };

    Contact.prototype.fullname = function() {
        return [this.firstName, this.lastName].join(' ');
    };

    Contact.new_ = function(obj) {
        return new Contact(obj);
    };

    Restangular.addElementTransformer('contact', function(obj) {
        return new Contact(obj);
    });

    return {
        new_: Contact.new_,
        Restangular: Restangular
    };
}]);

}());
