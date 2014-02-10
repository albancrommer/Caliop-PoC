(function() {

"use strict";

angular.module('caliop.inbox.entity.thread')

.factory('thread', ['Restangular', '$q', 'base', 'auth', 'user', 'tag',
    function (Restangular, $q, BaseEnt, AuthSrv, UserSrv, TagSrv) {

    function Thread() { BaseEnt.apply(this, arguments); }
    Thread.prototype = Object.create(BaseEnt.prototype);

    /**
     * Return the list of users
     * @return [{caliop.message.entity.user}]
     */
    Thread.prototype.getUsers = function() {
        var that = this;

        var users = [];
        angular.forEach(this.users, function(user) {
            users.push(new UserSrv(user));
        });

        that.users = users;
        return that.users;
    };

    /**
     * Return the last user.
     */
    Thread.prototype.getLastUser = function() {
        return this.users[this.users.length - 1];
    };

    /**
     * Return the list of tags
     * @return [{caliop.inbox.entity.tag}]
     */
    Thread.prototype.getTags = function() {
        var that = this;

        var tags = [];
        angular.forEach(this.tags, function(tag) {
            tags.push(new TagSrv(tag));
        });

        that.tags = tags;
        return that.tags;
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
     * Return true is the thread is flagged as 'unread' and if the authed
     * contact is not the last who has replied.
     */
    Thread.prototype.isUnread = function() {
        return this.unread && this.getLastUser().id != AuthSrv.getContact().id;
    };

    /**
     * Flag the thread as read.
     */
    Thread.prototype.setRead = function() {
        if (thread.unread) {
            Restangular
                .one('threads', this.id)
                .customPUT({unread: 0});
        }
    };

    /**
     * Do a POST query to create a new thread.
     */
    Thread.new_ = function(message) {
        var deferred = $q.defer(),
            now = moment().format("YYYY-MM-DD HH:mm:ss"),
            // unify the union of the auth contact + all selected users
            usersId = _.uniq(
                _.union(
                    _.map(message.users, function(user) { return user.id; }),
                    [AuthSrv.getContact().id]
                )
            ),
            threadParams = {
                "date_updated": now,
                "users": usersId,
                "text": message.body,
                "tags": [],
                "security": 50 // @TODO
            };

        Restangular
            .all('threads')
            .post(threadParams)
            .then(function(thread) {
                var messageParams = {
                    "title": message.title,
                    "body": message.body,
                    "date_sent": now,
                    "author": AuthSrv.getContact().id,
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
            }, function() {
                deferred.reject();
            }
        );

        return deferred.promise;
    };

    /**
     * Add a message in the thread.
     * @return [{caliop.message.entity.message}]
     */
    Thread.newMessage = function(threadId, message) {
        var deferred = $q.defer(),
            now = moment().format("YYYY-MM-DD HH:mm:ss"),
            threadParams = {
                "date_updated": now,
                // "users": [AuthSrv.getContact().id],
                "text": message.body,
                // "tags": [],
                "security": 50 // @TODO
            };

        // update the existing thread
        Restangular
            .one('threads', threadId)
            .customPUT(threadParams)
            .then(function(thread) {
                var messageParams = {
                    "title": message.title,
                    "body": message.body,
                    "date_sent": now,
                    "author": AuthSrv.getContact().id,
                    "security": 50, // @TODO
                    "protocole": 'Mail', // @TODO
                    "answer_to": false,
                    "offset": 0,
                    "unread": 1,
                    "thread_id": threadId
                };

                // add the new message
                Restangular
                    .one('threads', threadId)
                    .all('messages')
                    .post(messageParams)
                    .then(function() {
                        // merge the message and the author object
                        deferred.resolve(angular.extend(messageParams, {
                            author: AuthSrv.getContact()
                        }));
                    }, function() {
                        deferred.reject();
                    });
            }, function() {
                deferred.reject();
            }
        );

        return deferred.promise;
    };

    /**
     * Return the list of threads.
     */
    Thread.getList = function() {
        return Restangular.all('threads').getList.apply(null, arguments);
    };

    Restangular.addElementTransformer('threads', false, function(obj) {
        var thread = new Thread(obj);

        thread.getUsers();
        thread.getTags();
        thread.getSecurityColor();

        return thread;
    });

    return Thread;
}]);

}());
