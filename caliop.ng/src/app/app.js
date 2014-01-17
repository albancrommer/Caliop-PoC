angular.module('caliop', [
    /* grunt builds stuff */
    'templates-app',
    'templates-common',

    /* services */
    'caliop.service.config',

    /* components */
    'caliop.component.header',
    'caliop.component.footer',
    'caliop.component.account',
    'caliop.component.dashboard',
    'caliop.component.login',

    /* utils */
    'ui.router'
])

.config(function myAppConfig($urlRouterProvider, $stateProvider) {
    $urlRouterProvider.otherwise('/login');

    $stateProvider
        .state('app', {
            url: '/',
            views: {
                'header': {
                    templateUrl: 'component/header/header.tpl.html',
                    controller: 'HeaderCtrl'
                },
                'layout': {
                    templateUrl: 'component/common/fullpage.tpl.html'
                },
                'footer': {
                    templateUrl: 'component/footer/footer.tpl.html',
                    controller: 'FooterCtrl'
                }
            }
        });
})

.run(['$rootScope', 'config', 'Restangular',
    function run($rootScope, configSrv, restangularPvdr) {

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
}]);
