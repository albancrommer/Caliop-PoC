angular.module('caliop', [
    'templates-app',
    'templates-common',

    'caliop.service.config',

    /* components */
    'caliop.component.header',
    'caliop.component.footer',
    'caliop.component.account',
    'caliop.component.dashboard',
    'caliop.component.login',
    'ui.router'
])

.config(function myAppConfig($urlRouterProvider, $stateProvider) {
    $urlRouterProvider.otherwise('/dashboard');

    $stateProvider
        .state('app', {
            url: '/',
            views: {
                'header': {
                    templateUrl: 'component/header/header.tpl.html',
                    controller: 'HeaderCtrl'
                },
                'main': {
                    template: 'main'
                },
                'panel': {
                    template: 'panel'
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
            console.log(toState.data);
            $rootScope.pageTitle = toState.data.pageTitle + ' | Caliop' ;
        }
    });

    // use mocks or not
    var useMocks = configSrv.get('useMocks') || 1;
    var baseUrl = useMocks ? '/api/mock' : '/api';
    restangularPvdr.setBaseUrl(baseUrl);
}]);
