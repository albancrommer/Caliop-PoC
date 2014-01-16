/**
 * Dashboard component.
 */
angular.module('caliop.component.dashboard', [
    'ui.router',

    'caliop.service.entity.message',

    'ui.bootstrap',
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
            templateUrl: 'component/dashboard/dashboard.tpl.html',
            controller: 'DashboardCtrl',
            data: {
                pageTitle: 'Dashboard'
            }
        });
            // .state('dashboard.panel', {
            //     url: '/panel',
            //     templateUrl: 'component/dashboard/panel.tpl.html',
            //     controller: 'DashboardPanelCtrl',
            //     data: {
            //         pageTitle: 'Here your panel.'
            //     }
            // });
})

/**
 * And of course we define a controller for our route.
 */
.controller('DashboardCtrl', ['$scope', 'message',
    function DashboardCtrl($scope, MessageSrv) {

    MessageSrv.getList().then(function(messages) {
        $scope.messages = messages;
    });

}])

;

