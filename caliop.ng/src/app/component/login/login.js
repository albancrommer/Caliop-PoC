/**
 * Login component.
 */
angular.module('caliop.component.login', [
    'ui.router',
    'caliop.service.account'
])

.config(function config($stateProvider) {
    $stateProvider
        .state('app.login', {
            url: 'login',
            views: {
                'layout@': {
                    templateUrl: 'component/common/fullpage.tpl.html'
                },
                'main@app.login': {
                    templateUrl: 'component/login/login.tpl.html',
                    controller: 'LoginCtrl'
                }
            }
        });
})

/**
 * LoginCtrl
 */
.controller('LoginCtrl', ['$scope', 'login',
    function LoginCtrl($scope, authSrv) {
        var credentials = angular.copy($scope.user);
        $scope.onSubmit = function(){
            $scope.loginitreturn = credentials + ' wait login';
            authSrv.trylogin(credentials, $scope);
        };
}]);
