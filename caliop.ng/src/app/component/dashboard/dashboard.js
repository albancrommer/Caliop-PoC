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

.config(function config($stateProvider) {
    $stateProvider
        .state('app.dashboard', {
            url: 'dashboard',
            views: {
                'layout@': {
                    templateUrl: 'component/common/2columns.tpl.html'
                },
                'main@app.dashboard': {
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
 * DashboardCtrl
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
 * MessagesCtrl
 */
.controller('MessagesCtrl', ['$scope',
    function DashboardCtrl($scope) {

    // console.log('MessagesCtrl');
}]);
