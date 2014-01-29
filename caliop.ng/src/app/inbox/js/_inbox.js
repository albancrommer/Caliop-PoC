(function() {

"use strict";

angular.module('caliop.inbox', [
    /* internal dependancies */
    'caliop.inbox.thread.entity',
    'caliop.inbox.filter',

    /* external dependancies */
    'caliop.panel',
    'caliop.attachment'
]);


angular.module('caliop.inbox.filter', []);


angular.module('caliop.inbox.label.entity', [
    'restangular',

    'caliop.common.helpers.service'
]);


angular.module('caliop.inbox.thread.entity', [
    'restangular',

    /* internal dependancies */
    'caliop.inbox.label.entity',

    /* external dependancies */
    'caliop.common.helpers.service',
    'caliop.message.recipient.entity'
]);


}());
