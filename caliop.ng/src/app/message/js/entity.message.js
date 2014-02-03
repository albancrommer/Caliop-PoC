(function() {

"use strict";

angular.module('caliop.message.entity.message')

.factory('message', ['Restangular', 'base', 'recipient',
    function (Restangular, BaseEnt, RecipientSrv) {

    function Message() { BaseEnt.apply(this, arguments); }
    Message.prototype = Object.create(BaseEnt.prototype);

    /**
     * Return the author of the message.
     * @return {caliop.service.entity.recipient}
     */
    Message.prototype.getAuthor = function() {
        var that = this;

        this.author = new RecipientSrv(this.author);
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

    /**
     * Return the list of messages for a given thread.
     */
    Message.getThreadList = function(threadId) {
        return Restangular.one('threads', threadId).getList('messages');
    };

    Restangular.addElementTransformer('messages', false, function(obj) {
        var message = new Message(obj);

        message.getAuthor();
        message.getSecurityColor();

        return message;
    });

    return Message;
}]);

}());
