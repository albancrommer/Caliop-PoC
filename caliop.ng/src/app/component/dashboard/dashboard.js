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
        title: 'Conversations',
        state: 'app.dashboard.messages',
        active: true
    }];

    $scope.loadContent = function(tab) {
        if (tab.state) {
            $state.go(tab.state);
        }
    };

    $scope.writeMessage = function(tab) {
        $state.go('app.dashboard.writeMessage');
    };

    // $scope.addTab = function() {
    //     var id = $scope.tabs.length + 1;
    //     $scope.tabs.push({
    //         id: id,
    //         title: "Workspace " + id,
    //         content: "Workspace " + id,
    //         active: true
    //     });
    // };
}]);
