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
        })
        .state('app.logout', {
            url: 'logout',
            views: {
                'layout@': {
                    templateUrl: 'component/common/fullpage.tpl.html'
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

    $scope.messages = {};
    authSrv.logout();

    $scope.login = function(){
        $scope.statusMessage = 'Wait for login...';

        // if login successful, retrieve the contact asynchronously
        authSrv.login($scope.credentials).then(function() {
            authSrv.getContact();
        }, function() {
            $scope.messages.error = 'Bad login or password.';
        });
    };

    // save the contact in the rootScope and redirect if a contact has been
    // retrieved
    $rootScope.$watch(function() {
        return authSrv.contact;
    }, function(contact) {
        // console.log('authSrv.contact modified');
        $rootScope.authContact = contact;

        if (contact) {
            // redirect
            $state.go('app.dashboard');
        }
    });
}])

/**
 * LogoutCtrl
 */
.controller('LogoutCtrl', ['$rootScope', 'auth', '$state',
    function LogoutCtrl($rootScope, authSrv, $state) {

    authSrv.logout();
    $state.go('app.login');
}]);
