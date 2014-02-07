(function() {

"use strict";

angular.module('caliop.inbox', [
    'caliop.inbox.entity.thread',
    'caliop.inbox.service.filter',
    'caliop.user.filter',

    'caliop.message',
    'caliop.attachment'
]);


angular.module('caliop.inbox.service.tabs', []);


angular.module('caliop.inbox.service.filter', [
    'caliop.inbox.entity.tag',
]);


angular.module('caliop.inbox.entity.tag', [
    'caliop.common.entity.base',

    'caliop.common.service.helpers'
]);


angular.module('caliop.inbox.entity.thread', [
    'caliop.common.entity.base',
    'caliop.account.service.account',
    'caliop.inbox.entity.tag',
    'caliop.user.entity.user'
]);


}());
