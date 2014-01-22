(function() {

"use strict";

angular.module('caliop', [
    /* grunt builds stuff */
    'templates-app',
    'templates-common',

    /* services */
    'caliop.service.config',
    'caliop.service.account',

    /* components */
    'caliop.component.header',
    'caliop.component.footer',
    'caliop.component.account',
    'caliop.component.dashboard',
    'caliop.component.login',

    /* utils */
    'ui.router'
])

.config(function myAppConfig($urlRouterProvider, $stateProvider, $tooltipProvider) {
    $urlRouterProvider.otherwise('/login');

    $stateProvider
        .state('app', {
            url: '/',
            views: {
                'header': {
                    templateUrl: 'component/header/html/header.tpl.html',
                    controller: 'HeaderCtrl'
                },
                'layout': {
                    templateUrl: 'component/common/html/fullpage.tpl.html'
                },
                'panel': {
                    templateUrl: 'component/panel/html/panel.tpl.html',
                    controller: 'PanelCtrl'
                },
                'footer': {
                    templateUrl: 'component/footer/html/footer.tpl.html',
                    controller: 'FooterCtrl'
                }
            }
        });

    /* Display tooltip after 500 ms */
    $tooltipProvider.options({
        popupDelay: 500
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

    // set optional config from the querystring
    configSrv.configure();

    // redirect to the app if already logged in
    $rootScope.$on('$stateChangeStart', function(next, current) {
        if (current.name != 'app.login' && !contact) {
            $state.go('app.login');
        }
    });

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
}]);

}());
