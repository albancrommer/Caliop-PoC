(function() {

"use strict";

angular.module('caliop.message.entity.message', [
    'caliop.common.entity.base'
]);


angular.module('caliop.message', [
    'caliop.inbox.service.tabs',
    'caliop.message.entity.message',
    'caliop.user.filter'
]);


}());
