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
        .state('app.account', {
            url: 'account',
            views: {
                'main@': {
                    templateUrl: 'component/account/account.tpl.html',
                    controller: 'AccountCtrl'
                }
                // 'panel@': {
                //     templateUrl: 'component/panel/panel.tpl.html',
                //     controller: 'PanelCtrl'
                // }
            }
        });
})

/**
 * And of course we define a controller for our route.
 */
.controller('AccountCtrl', ['$scope', 'auth',
    function AccountCtrl($scope, authSrv) {

    // $scope.contact = authSrv.getContact();
}])

;

