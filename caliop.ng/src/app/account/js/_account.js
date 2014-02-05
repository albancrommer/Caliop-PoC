(function() {

"use strict";

angular.module('caliop.account', [
    'caliop.account.service.account'
]);


angular.module('caliop.account.service.account', [
    'restangular',
    'caliop.account.entity.session'
]);


angular.module('caliop.account.entity.session', [
    'caliop.common.entity.base'
]);

}());
