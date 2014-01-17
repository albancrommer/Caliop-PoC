/**
 * Dashboard component.
 */
angular.module('caliop.component.dashboard', [
    'templates-app',
    'ui.router',

    'caliop.service.entity.message',

    'caliop.component.panel',

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
        .state('app.dashboard', {
            url: 'dashboard',
            views: {
                'main@': {
                    templateUrl: 'component/dashboard/dashboard.tpl.html',
                    controller: 'DashboardCtrl'
                },
                'panel@': {
                    templateUrl: 'component/panel/panel.tpl.html',
                    controller: 'PanelCtrl'
                }
            }
        });
})

/**
 * And of course we define a controller for our route.
 */
.controller('DashboardCtrl', ['$scope', 'message',
    function DashboardCtrl($scope, MessageSrv) {

    $scope.tabs = [];

    var addNewTab = function() {
        var id = $scope.tabs.length + 1;
        $scope.tabs.push({
            id: id,
            title: "Workspace " + id,
            content: "Workspace " + id,
            active: true
        });
    };

    MessageSrv.getList().then(function(messages) {
        $scope.tabs = [
            { id: 1, title: 'Messages', content: messages, active: true }
        ];

        $scope.addTab = function() {
            addNewTab();
        };
    });
}])

/**
 * And of course we define a controller for our route.
 */
.controller('MessagesCtrl', ['$scope',
    function DashboardCtrl($scope) {

    console.log('MessagesCtrl');


}]);
