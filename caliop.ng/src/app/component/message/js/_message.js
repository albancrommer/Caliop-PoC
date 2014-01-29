(function() {

"use strict";

angular.module('caliop.message', [
    /* internal dependancies */
    'caliop.inbox.thread.entity',
    'caliop.inbox.filter',

    /* external dependancies */
    'caliop.panel',
    'caliop.attachment'
]);


angular.module('caliop.message.message.entity', [
    'restangular',

    'caliop.common.helpers.service'
]);


angular.module('caliop.message.recipient.entity', [
    'restangular',

    'caliop.common.helpers.service'
]);


}());
