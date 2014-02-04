(function() {

"use strict";

angular.module('caliop.user.entity.user')

.factory('user', ['Restangular', 'base',
    function (Restangular, BaseEnt) {

    function User() { BaseEnt.apply(this, arguments); }
    User.prototype = Object.create(BaseEnt.prototype);

    /**
     * Return user's fullname.
     * @return {string} User's fullname.
     */
    User.prototype.displayName = function() {
        return [this.firstName, this.lastName].join(' ');
    };

    User.prototype.getAvatarSrc = function(obj) {
        var avatar = this.avatar || 'avatar.png';
        return '/static/assets/images/avatars/' + avatar;
    };

    User.getList = function() {
        return Restangular.all('users').getList();
    };

    Restangular.addElementTransformer('users', false, function(obj) {
        return new User(obj);
    });

    return User;
}]);

}());
