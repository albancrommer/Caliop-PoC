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
.controller('DashboardCtrl', ['$scope', '$state', 'message',
    function DashboardCtrl($scope, $state, MessageSrv) {

    $scope.tabs = [{
            id: 1,
            title: 'Messages 1',
            state: 'app.dashboard.messages',
            active: true
        }, {
            id: 2,
            title: 'Messages 2',
            state: 'app.dashboard.writeMessage',
            active: false
        }];

    $scope.loadContent = function(tab) {
        $state.go(tab.state);
    };

    $scope.addTab = function() {
        var id = $scope.tabs.length + 1;
        $scope.tabs.push({
            id: id,
            title: "Workspace " + id,
            content: "Workspace " + id,
            active: true
        });
    };
}]);
