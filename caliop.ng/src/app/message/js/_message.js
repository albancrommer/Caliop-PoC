(function() {

"use strict";

angular.module('caliop.message.entity.message', [
    'restangular',

    'caliop.common.service.helpers'
]);


angular.module('caliop.message.entity.recipient', [
    'restangular',

    'caliop.common.service.helpers'
]);


angular.module('caliop.message', [
    /* internal dependancies */
    'caliop.message.entity.message',
    'caliop.inbox.filter'
]);


}());
