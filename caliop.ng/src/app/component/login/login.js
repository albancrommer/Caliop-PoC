/**
 * Login component.
 */
angular.module('caliop.component.login', [
    'ui.router',
    'caliop.service.account'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config($stateProvider) {
    $stateProvider
        .state('login', {
            url: '/account/login',
            templateUrl: 'component/login/login.tpl.html',
            controller: 'LoginCtrl',
            data: {
                pageTitle: 'login'
            }
        });
})

/**
 * And of course we define a controller for our route.
 */
.controller('LoginCtrl', ['$scope', 'login',
    function LoginCtrl($scope, authSrv) {
        var credentials = angular.copy($scope.user);
        $scope.onSubmit = function(){
            $scope.loginitreturn = credentials + ' wait login';
            authSrv.trylogin(credentials, $scope);
        };
}]);
