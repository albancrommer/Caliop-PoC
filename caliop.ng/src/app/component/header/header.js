/**
 * Header...
 */
angular.module('caliop.component.header', [
    'caliop.service.account'
])

/**
 * And of course we define a controller for our route.
 */
.controller('HeaderCtrl', ['$rootScope', '$scope', 'auth',
    function HeaderCtrl($rootScope, $scope, authSrv) {

    // retrieve the contact asynchronously
    authSrv.getContact();

    // once retrieved, update the rootScope with the auth contact
    $scope.$watch(function() {
        return authSrv.contact;
    }, function(contact) {
        $rootScope.contact = contact;
    });

}])

;

