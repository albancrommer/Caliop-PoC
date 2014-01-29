(function() {

"use strict";

angular.module('caliop.message', [
    /* internal dependancies */
    'caliop.inbox.entity.thread',
    'caliop.inbox.filter',

    /* external dependancies */
    'caliop.panel',
    'caliop.attachment'
]);


angular.module('caliop.message.entity.message', [
    'restangular',

    'caliop.common.service.helpers'
]);


angular.module('caliop.message.entity.recipient', [
    'restangular',

    'caliop.common.service.helpers'
]);


}());
