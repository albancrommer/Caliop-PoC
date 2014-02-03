(function() {

"use strict";

/**
 * Dashboard component.
 */
angular.module('caliop.attachment', [
    'caliop.attachment.entity.attachment'
])

/**
 * MessagesCtrl
 */
.controller('AttachmentCtrl', ['$scope', 'extension', 'attachment',
    function AttachmentCtrl($scope, extension, AttachmentSrv) {

    $scope.attachment = new AttachmentSrv({extension: extension});
}]);

}());

