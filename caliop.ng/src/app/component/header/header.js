/**
 * Header component.
 */
angular.module('caliop.component.header', [
    'caliop.service.account'
])

.controller('HeaderCtrl', ['$rootScope', '$scope', 'auth',
    function HeaderCtrl($rootScope, $scope, authSrv) {

    // retrieve the contact asynchronously
    authSrv.getContact();

    // @TOFIX Use $q instead of rootScope ?
    // once retrieved, update the rootScope with the auth contact
    $scope.$watch(function() {
        return authSrv.contact;
    }, function(contact) {
        $rootScope.authContact = contact;
    });
}]);
