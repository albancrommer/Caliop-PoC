(function() {

"use strict";

/**
 * Login component.
 */
angular.module('caliop.login', [
    'ui.router',

    'caliop.account.service.account'
])

.config(function config($stateProvider) {
    $stateProvider
        .state('app.login', {
            url: 'login',
            views: {
                // ui-view="layout" of index.tpl.html
                'header@': {
                    template: ''
                },
                // ui-view="layout" of index.tpl.html
                'layout@': {
                    templateUrl: 'common/html/fullpage.tpl.html'
                },
                // ui-view="main" of fullpage.tpl.html
                'main@app.login': {
                    templateUrl: 'login/html/login.tpl.html',
                    controller: 'LoginCtrl'
                },
                'footer@': {
                    template: ''
                }
            }
        })
        .state('app.logout', {
            url: 'logout',
            views: {
                // ui-view="layout" of index.tpl.html
                'layout@': {
                    templateUrl: 'common/html/fullpage.tpl.html'
                },
                // ui-view="main" of fullpage.tpl.html
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
        $state.go('app.inbox');
    }

    $scope.messages = {};

    $scope.login = function() {
        //if login successful, retrieve the contact asynchronously
        authSrv.login($scope.credentials).then(function(contact) {
            $rootScope.authContact = contact;
            $state.go('app.inbox');

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

    authSrv.logout().then(function() {
        $rootScope.authContact = undefined;
        $state.go('app.login');
    });
}]);

}());
