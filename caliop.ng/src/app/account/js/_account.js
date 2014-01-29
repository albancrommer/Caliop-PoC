(function() {

"use strict";

angular.module('caliop.account', [
    'caliop.account.service'
]);


angular.module('caliop.account.service', [
    'caliop.account.entity'
]);


angular.module('caliop.account.entity', [
    'restangular',

    'caliop.common.helpers.service'
]);

}());
