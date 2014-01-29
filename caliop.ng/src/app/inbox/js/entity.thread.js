(function() {

"use strict";

angular.module('caliop.inbox.entity.thread')

.factory('thread', ['Restangular', 'string', 'recipient', 'label',
    function (Restangular, stringSrv, recipientSrv, labelSrv) {

    var Thread = function Thread(obj) {
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
     * Return the list of recipients
     * @return [{caliop.message.entity.recipient}]
     */
    Thread.prototype.getRecipients = function() {
        var that = this;

        var recipients = [];
        angular.forEach(this.recipients, function(recipient) {
            recipients.push(recipientSrv.new_(recipient));
        });

        that.recipients = recipients;
        return that.recipients;
    };

    /**
     * Return the list of labels
     * @return [{caliop.inbox.entity.label}]
     */
    Thread.prototype.getLabels = function() {
        var that = this;

        var labels = [];
        angular.forEach(this.labels, function(label) {
            labels.push(labelSrv.new_(label));
        });

        that.labels = labels;
        return that.labels;
    };

    /**
     * Return the security color.
     */
    Thread.prototype.getSecurityColor = function() {
        var n = Math.floor((this.security * parseInt('ffffff', 16)) / 100);
        this.securityColor = n.toString(16);
    };

    /**
     * Return the last recipient.
     */
    Thread.prototype.getLastRecipient = function() {
        return this.recipients[this.recipients.length - 1];
    };

    /**
     * Return the icon src of the attachment (last message attachment).
     */
    Thread.prototype.getAttachmentIconSrc = function() {
        var file = this.attachment + '.png';
        return '/static/assets/images/attachments/' + file;
    };

    /**
     * Return the messages of the thread.
     * @return [{caliop.message.entity.message}]
     */
    Thread.prototype.getMessages = function() {
        return Restangular.one('threads', this.id).getList('messages');
    };

    Thread.new_ = function(obj) {
        var thread = new Thread(obj);
        thread.getRecipients();
        thread.getLabels();
        thread.getSecurityColor();
        return thread;
    };

    Thread.by_id = function(id) {
        return Restangular.one('threads', id).get();
    };

    Restangular.addElementTransformer('threads', false, function(obj) {
        return Thread.new_(obj);
    });

    return {
        new_: Thread.new_,
        by_id: Thread.by_id,
        Restangular: Restangular
    };
}]);

}());
