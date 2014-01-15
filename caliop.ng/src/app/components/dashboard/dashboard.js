/**
 * Map controller.
 *
 * Serve the isometric map.
 */
angular.module('caliop.component.dashboard', [
    'ui.router',

    'caliop.service.account',
    'caliop.directive.sample',

    'ngAnimate'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config($stateProvider) {
    $stateProvider
        .state('dashboard', {
            url: '/dashboard',
            templateUrl: 'components/dashboard/dashboard.tpl.html',
            controller: 'DashboardCtrl',
            data: {
                pageTitle: 'Dashboard'
            }
        });
            // .state('dashboard.panel', {
            //     url: '/panel',
            //     templateUrl: 'components/dashboard/panel.tpl.html',
            //     controller: 'DashboardPanelCtrl',
            //     data: {
            //         pageTitle: 'Here your panel.'
            //     }
            // });
})

/**
 * And of course we define a controller for our route.
 */
.controller('DashboardCtrl', ['$scope',
    function DashboardCtrl($scope) {

    $scope.helloword = 'Hi dude';
}])

;

