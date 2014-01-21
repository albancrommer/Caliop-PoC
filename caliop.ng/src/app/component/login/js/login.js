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
                    templateUrl: 'component/common/html/fullpage.tpl.html'
                },
                'main@app.login': {
                    templateUrl: 'component/login/html/login.tpl.html',
                    controller: 'LoginCtrl'
                }
            }
        })
        .state('app.logout', {
            url: 'logout',
            views: {
                'layout@': {
                    templateUrl: 'component/common/html/fullpage.tpl.html'
                },
                'main@app.logout': {
                    controller: 'LogoutCtrl'
                }
            }
        });
})

/**
 * LoginCtrl
 */
.controller('LoginCtrl', ['$rootScope', '$scope', 'auth', '$state',
    function LoginCtrl($rootScope, $scope, authSrv, $state) {

    if (authSrv.getContact()) {
        $state.go('app.dashboard');
    }

    $scope.messages = {};

    $scope.login = function() {
        //if login successful, retrieve the contact asynchronously
        authSrv.login($scope.credentials).then(function(contact) {
            $rootScope.authContact = contact;
            $state.go('app.dashboard');

        }, function(error) {
            $scope.messages.error = 'Identifiant ou mot de passe incorrect.';
        });
    };
}])

/**
 * LogoutCtrl
 */
.controller('LogoutCtrl', ['$rootScope', 'auth', '$state',
    function LogoutCtrl($rootScope, authSrv, $state) {

    authSrv.logout();
    $rootScope.authContact = undefined;

    $state.go('app.login');
}]);
