angular.module('caliop', [
    'templates-app',
    'templates-common',

    /* Declared modules */
    'caliop.service',
    'caliop.component.header',
    'caliop.component.dashboard',

    'ui.router'
])

.config(function myAppConfig($urlRouterProvider) {
    $urlRouterProvider.otherwise('/dashboard');
})

.run(['config', function run(configSrv) {
    // set optional config from the querystring
    configSrv.configure();
}])

.controller('AppCtrl', ['$scope', 'config', 'Restangular',
    function AppCtrl($scope, configSrv, restangularPvdr) {

    // update the title of the page according to the ui-router pageTitle data
    $scope.$on('$stateChangeSuccess', function(event, toState, toParams, fromState, fromParams) {
        if (angular.isDefined(toState.data.pageTitle)) {
            $scope.pageTitle = toState.data.pageTitle + ' | Caliop' ;
        }
    });

    // A good rule of thumb to determine where we should configure our Restangular instances:
    // If we need to use any other service in configuring Restangular, then we should configure
    // it in the run() method, otherwise we’ll keep it in the config() method.
    // (http://www.ng-newsletter.com/posts/restangular.html)
    var useMocks = configSrv.get('useMocks') || 1;
    var baseUrl = useMocks ? '/api/mock' : '/api';
    restangularPvdr.setBaseUrl(baseUrl);
}]);
