(function() {

"use strict";

/**
 * Dashboard component.
 */
angular.module('caliop.component.dashboard', [
    'templates-app',
    'ui.router',

    'caliop.service.entity.thread',

    'caliop.component.panel',
    'caliop.component.dashboard.filters',

    'ui.bootstrap',

    'ngSanitize'
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

    $scope.writeMessage = function(tab) {
        $state.go('app.dashboard.writeMessage');
    };

    /**
     * Tabs management.
     */
    $scope.addTab = function(object) {
        var tabObject = angular.extend({
            id: $scope.tabs.length + 1
        }, object);

        $scope.tabs.push(tabObject);
    };

    $scope.closeTab = function(tab) {
        _.remove($scope.tabs, function(tab_) {
            return tab_.id == tab.id;
        });

        // go to the state of the previous tab
        var lastTab = $scope.tabs[$scope.tabs.length-1];
        $state.go(lastTab.state, lastTab.stateParams || {});
    };

    $scope.loadContent = function(tab) {
        if (tab.state) {
            var params = tab.stateParams || {};
            $state.go(tab.state, params);
        }
    };

    // redirect to the list of threads
    // @TODO check if it's possible to manage the redirection via the ui-router
    if ($state.current.name == 'app.dashboard') {
        $scope.loadContent($scope.tabs[0]);
    }
}]);

}());
