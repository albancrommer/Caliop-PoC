(function() {

"use strict";

angular.module('caliop.message.entity.message', [
    'caliop.common.entity.base'
]);


angular.module('caliop.message.entity.recipient', [
    'caliop.common.entity.base'
]);


angular.module('caliop.message', [
    'caliop.message.entity.message',
    'caliop.inbox.filter'
]);


}());
