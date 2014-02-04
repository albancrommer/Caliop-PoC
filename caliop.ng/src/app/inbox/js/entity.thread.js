(function() {

"use strict";

angular.module('caliop.inbox.entity.thread')

.factory('thread', ['Restangular', '$q', 'base', 'recipient', 'label',
    function (Restangular, $q, BaseEnt, RecipentSrv, LabelSrv) {

    function Thread() { BaseEnt.apply(this, arguments); }
    Thread.prototype = Object.create(BaseEnt.prototype);

    /**
     * Return the list of recipients
     * @return [{caliop.message.entity.recipient}]
     */
    Thread.prototype.getRecipients = function() {
        var that = this;

        var recipients = [];
        angular.forEach(this.recipients, function(recipient) {
            recipients.push(new RecipentSrv(recipient));
        });

        that.recipients = recipients;
        return that.recipients;
    };

    /**
     * Return the last recipient.
     */
    Thread.prototype.getLastRecipient = function() {
        return this.recipients[this.recipients.length - 1];
    };

    /**
     * Return the list of labels
     * @return [{caliop.inbox.entity.label}]
     */
    Thread.prototype.getLabels = function() {
        var that = this;

        var labels = [];
        angular.forEach(this.labels, function(label) {
            labels.push(new LabelSrv(label));
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

    /**
     * Do a POST query to create a new thread.
     */
    Thread.new_ = function(message) {
        var deferred = $q.defer(),
            now = moment().format("YYYY-MM-DD HH:mm:ss"),
            threadParams = {
                "date_updated": now,
                "recipients": _.map(message.recipients, function(recipient) {
                    return recipient.id;
                }),
                "text": message.body,
                "labels": [],
                "security": 50 // @TODO
            };

        Restangular.all('threads').post(threadParams).then(function(thread) {
            var messageParams = {
                "title": message.title,
                "body": message.body,
                "date_sent": now,
                "author": 1,    // for the moment, 1 == authed contact
                "security": 50, // @TODO
                "protocole": message.protocole,
                "answer_to": false,
                "offset": 0,
                "thread_id": thread.threadId
            };

            Restangular
                .one('threads', thread.threadId)
                .all('messages')
                .post(messageParams)
                .then(function() {
                    deferred.resolve(threadParams);
                }, function() {
                    deferred.reject();
                });
        });

        return deferred.promise;
    };

    /**
     * Return the list of threads.
     */
    Thread.getList = function() {
        return Restangular.all('threads').getList();
    };

    Restangular.addElementTransformer('threads', false, function(obj) {
        var thread = new Thread(obj);

        thread.getRecipients();
        thread.getLabels();
        thread.getSecurityColor();

        return thread;
    });

    return Thread;
}]);

}());
