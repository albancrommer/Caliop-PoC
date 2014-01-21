(function() {

"use strict";

/**
 * Dashboard component.
 */
angular.module('caliop.component.dashboard', [
    'templates-app',
    'ui.router',

    'caliop.component.dashboard.filters',

    'caliop.service.entity.thread',

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
                    templateUrl: 'component/common/html/2columns.tpl.html'
                },
                'main@app.dashboard': {
                    templateUrl: 'component/dashboard/html/dashboard.tpl.html',
                    controller: 'DashboardCtrl'
                },
                'panel@app.dashboard': {
                    templateUrl: 'component/panel/html/panel.tpl.html',
                    controller: 'PanelCtrl'
                }
            }
        });
})

/**
 * DashboardCtrl
 */
.controller('DashboardCtrl', ['$scope', '$state',
    function DashboardCtrl($scope, $state) {

    $scope.tabs = [{
        id: 1,
        title: 'Conversations',
        state: 'app.dashboard.threads',
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

}());
