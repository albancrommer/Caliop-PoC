(function() {

"use strict";

angular.module('caliop.service.entity.recipient', [
    'restangular',
    'caliop.service.helpers'
])

.factory('recipient', ['Restangular', 'string',
    function (Restangular, stringSrv) {

    var Recipient = function Recipient(obj) {
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

    Recipient.prototype.displayName = function(obj) {
        return [this.firstName, this.lastName].join(' ');
    };

    Recipient.prototype.getAvatarSrc = function(obj) {
        var avatar = this.avatar || 'avatar.png';
        return '/static/assets/images/avatars/' + avatar;
    };

    Recipient.new_ = function(obj) {
        return new Recipient(obj);
    };

    Restangular.addElementTransformer('recipients', false, function(obj) {
        return new Recipient(obj);
    });

    return {
        new_: Recipient.new_,
        Restangular: Restangular
    };
}]);

}());
