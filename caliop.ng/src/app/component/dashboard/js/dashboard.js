(function() {

"use strict";

/**
 * Dashboard component.
 */
angular.module('caliop.component.dashboard', [
    'templates-app',
    'ui.router',

    'caliop.service.entity.thread',
    'caliop.service.entity.attachment',

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

    /**
     * Add a new tab.
     */
    $scope.addTab = function(object) {
        // search if the tab is already opened
        var threadId = object.stateParams.id;

        var tabsFound = _.filter($scope.tabs, function(tab) {
            return tab.stateParams && (tab.stateParams.id == threadId);
        });

        // select the found tab
        if (tabsFound.length) {
            $scope.selectTab(tabsFound[0]);
        }

        // create a new tab
        else {
            var tabObject = angular.extend({
                id: $scope.tabs.length + 1
            }, object);

            $scope.tabs.push(tabObject);
        }
    };

    /**
     * Select an existing tab.
     */
    $scope.selectTab = function(tab) {
        tab.active = true;
        $state.go(tab.state, tab.stateParams || {});
    };

    /**
     * Close a tab.
     */
    $scope.closeTab = function(tab) {
        _.remove($scope.tabs, function(tab_) {
            return tab_.id == tab.id;
        });

        // go to the state of the previous tab
        var lastTab = $scope.tabs[$scope.tabs.length-1];
        $state.go(lastTab.state, lastTab.stateParams || {});
    };

    /**
     * Load the content of a tab.
     */
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
