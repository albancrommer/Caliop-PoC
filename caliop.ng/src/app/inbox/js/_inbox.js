(function() {

"use strict";

angular.module('caliop.inbox', [
    /* internal dependancies */
    'caliop.inbox.entity.thread',
    'caliop.user.filter',

    /* external dependancies */
    'caliop.message',
    'caliop.attachment'
]);


angular.module('caliop.inbox.entity.label', [
    'caliop.common.entity.base',

    'caliop.common.service.helpers'
]);


angular.module('caliop.inbox.entity.thread', [
    'caliop.common.entity.base',
    'caliop.account.service.account',
    'caliop.inbox.entity.label',
    'caliop.user.entity.user'
]);


}());
