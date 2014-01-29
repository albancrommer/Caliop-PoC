(function() {

"use strict";

angular.module('caliop.message.entity.message')

.factory('message', ['Restangular', 'string', 'recipient',
    function (Restangular, stringSrv, recipientSrv) {

    var Message = function Message(obj) {
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

    /**
     * Return the author of the message.
     * @return {caliop.service.entity.recipient}
     */
    Message.prototype.getAuthor = function() {
        var that = this;

        this.author = recipientSrv.new_(this.author);
        return this.author;
    };

    /**
     * Return the security color.
     */
    Message.prototype.getSecurityColor = function() {
        var n = Math.floor((this.security * parseInt('ffffff', 16)) / 100);
        this.securityColor = n.toString(16);
        return this.securityColor;
    };

    /**
     * Return the protocole translation.
     */
    Message.prototype.displayProtocole = function() {
        return this.protocole;
    };

    Message.new_ = function(obj) {
        var message = new Message(obj);
        message.getAuthor();
        message.getSecurityColor();
        return message;
    };

    Restangular.addElementTransformer('messages', false, function(obj) {
        return Message.new_(obj);
    });

    return {
        new_: Message.new_,
        Restangular: Restangular
    };

}]);

}());
