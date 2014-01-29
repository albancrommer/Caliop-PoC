(function() {

"use strict";

angular.module('caliop.inbox', [
    /* internal dependancies */
    'caliop.inbox.entity.thread',
    'caliop.inbox.filter',

    /* external dependancies */
    'caliop.panel',
    'caliop.attachment'
]);


angular.module('caliop.inbox.filter', []);


angular.module('caliop.inbox.entity.label', [
    'restangular',

    'caliop.common.service.helpers'
]);


angular.module('caliop.inbox.entity.thread', [
    'restangular',

    /* internal dependancies */
    'caliop.inbox.entity.label',

    /* external dependancies */
    'caliop.common.service.helpers',
    'caliop.message.entity.recipient'
]);


}());
