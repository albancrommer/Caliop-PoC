(function() {

"use strict";

angular.module('caliop.message.entity.recipient')

.factory('recipient', ['Restangular', 'base',
    function (Restangular, BaseEnt) {

    function Recipient() { BaseEnt.apply(this, arguments); }
    Recipient.prototype = Object.create(BaseEnt.prototype);

    Recipient.prototype.displayName = function(obj) {
        return [this.firstName, this.lastName].join(' ');
    };

    Recipient.prototype.getAvatarSrc = function(obj) {
        var avatar = this.avatar || 'avatar.png';
        return '/static/assets/images/avatars/' + avatar;
    };

    Restangular.addElementTransformer('recipients', false, function(obj) {
        return new Recipient(obj);
    });

    return Recipient;
}]);

}());
