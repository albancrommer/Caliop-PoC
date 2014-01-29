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
    function AttachmentCtrl($scope, extension, attachmentSrv) {

    $scope.attachment = attachmentSrv.new_({extension: extension});
}]);

}());

