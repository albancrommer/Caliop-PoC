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
    'caliop.common.service.config',

    /* components */
    'caliop.header',
    'caliop.footer',
    'caliop.account',
    'caliop.inbox',
    'caliop.login',
    'caliop.user',
    'caliop.panel'
])

.config(function myAppConfig($urlRouterProvider, $stateProvider, $tooltipProvider) {
    $urlRouterProvider.otherwise('/login');

    $stateProvider
        .state('app', {
            url: '',
            views: {
                // ui-view="header" of index.tpl.html
                'header': {
                    templateUrl: 'header/html/header.tpl.html',
                    controller: 'HeaderCtrl'
                },
                // ui-view="layout" of index.tpl.html
                'layout': {
                    templateUrl: 'common/html/fullpage.tpl.html',
                    controller: 'AppCtrl'
                },
                // ui-view="footer" of index.tpl.html
                'footer': {
                    templateUrl: 'footer/html/footer.tpl.html',
                    controller: 'FooterCtrl'
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

    // use mocks or not
    var useMocks = configSrv.get('useMocks') || 1;
    var baseUrl = useMocks ? '/api/mock' : '/api';
    restangularPvdr.setBaseUrl(baseUrl);

    // if a user is connected, save the contact in the rootScope
    var contact = authSrv.getContact();
    if (contact) {
        $rootScope.authContact = contact;
    }
    else {
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
