(function() {

"use strict";

angular.module('caliop.account', [
    'caliop.service.account'
]);


angular.module('caliop.service.account', [
    'caliop.entity.account'
]);


angular.module('caliop.entity.account', [
    'restangular',

    'caliop.common.service.helpers'
]);

}());
