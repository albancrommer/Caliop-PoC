(function() {

"use strict";

angular.module('caliop', [
    /* grunt builds stuff */
    'templates-app',
    'templates-common',

    /* utils */
    'ui.router',
    'ui.bootstrap',
    'ngCookies',
    'ngSanitize',

    /* services */
    'caliop.common.config.service',
    'caliop.account.service',

    /* components */
    'caliop.header',
    'caliop.footer',
    'caliop.account',
    'caliop.inbox',
    'caliop.login'
])

.config(function myAppConfig($urlRouterProvider, $stateProvider, $tooltipProvider) {
    $urlRouterProvider.otherwise('/login');

    $stateProvider
        .state('app', {
            url: '/',
            views: {
                'layout': {
                    templateUrl: 'common/html/fullpage.tpl.html',
                    controller: 'AppCtrl'
                }
            }
        });

    /* Display tooltip after 500 ms */
    $tooltipProvider.options({
        popupDelay: 250
    });
})

.run(['$rootScope', 'config', 'auth', '$state', 'Restangular',
    function run($rootScope, configSrv, authSrv, $state, restangularPvdr) {

    var contact = authSrv.getContact();

    // if a user is connected, save the contact in the rootScope
    if (contact) {
        $rootScope.authContact = contact;
    }
    else {
        authSrv.logout();
        $state.go('app.login');
    }

    // redirect to the app if already logged in
    $rootScope.$on('$stateChangeStart', function(next, current) {
        if (current.name != 'app.login' && !contact) {
            $state.go('app.login');
        }
    });

    // display route state for debug (@TODO use configSrv ?)
    $rootScope.$on('$stateChangeSuccess', function(e, current) {
        console.log('Current state:', current.name);
    });

    // set optional config from the querystring
    configSrv.configure();

    // update the title of the page according to the ui-router pageTitle data
    $rootScope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
        if (toState.data && toState.data.pageTitle) {
            $rootScope.pageTitle = toState.data.pageTitle + ' | Caliop' ;
        }
    });

    // use mocks or not
    var useMocks = configSrv.get('useMocks') || 1;
    var baseUrl = useMocks ? '/api/mock' : '/api';
    restangularPvdr.setBaseUrl(baseUrl);
}])

/**
 * AccountCtrl
 */
.controller('AppCtrl', ['$scope',
    function AppCtrl($scope) {

    console.log('AppCtrl');

    // $scope.contact = authSrv.getContact();
}]);

}());
