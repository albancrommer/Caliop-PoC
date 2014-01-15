/**
 * Account component.
 */
angular.module('caliop.component.account', [
    'ui.router',

    'caliop.service.account'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config($stateProvider) {
    $stateProvider
        .state('account', {
            url: '/account',
            templateUrl: 'component/account/account.tpl.html',
            controller: 'AccountCtrl',
            data: {
                pageTitle: 'Your account'
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
.controller('AccountCtrl', ['$scope', 'auth',
    function AccountCtrl($scope, authSrv) {

    // $scope.contact = authSrv.getContact();
}])

;

