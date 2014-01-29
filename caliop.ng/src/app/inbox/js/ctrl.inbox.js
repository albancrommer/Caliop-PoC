(function() {

"use strict";

angular.module('caliop.inbox')

.config(function config($stateProvider) {
    $stateProvider
        .state('app.dashboard', {
            url: 'inbox',
            abstract: true,
            views: {
                // ui-view="layout" of index.tpl.html
                'layout@': {
                    templateUrl: 'common/html/2columns.tpl.html'
                },
                // ui-view="main" of 2columns.tpl.html
                'main@app.dashboard': {
                    templateUrl: 'inbox/html/layout.tpl.html',
                    controller: 'InBoxCtrl'
                },
                // ui-view="panel" of 2columns.tpl.html
                'panel@app.dashboard': {
                    templateUrl: 'panel/html/panel.tpl.html',
                    controller: 'PanelCtrl'
                }
            }
        })
        .state('app.dashboard.threads', {
            url: '/',
            views: {
                // ui-view="tabContent" of inbox/html/layout.tpl.html
                'tabContent': {
                    templateUrl: 'inbox/html/list.tpl.html',
                    controller: 'ThreadsCtrl'
                }
            }
        });
})

/**
 * InBoxCtrl
 */
.controller('InBoxCtrl', ['$scope', '$state',
    function InBoxCtrl($scope, $state) {

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
            $state.transitionTo(tab.state, params);
        }
    };
}])

/**
 * ThreadsCtrl
 */
.controller('ThreadsCtrl', ['$scope', '$state', '$filter', '$modal', 'thread',
    function ThreadsCtrl($scope, $state, $filter, $modal, ThreadSrv) {

    ThreadSrv.Restangular.all('threads').getList().then(function(threads) {
        $scope.threads = threads;
    });

    // if any thread is selected, show actions icons
    $scope.showThreadActions = function() {
        return _.filter($scope.threads, function(thread) {
            return thread.selected;
        }).length > 0;
    };

    // select all/none threads
    $scope.$watch('selectAllThreads', function(checked) {
        angular.forEach($scope.threads, function(thread) {
            thread.selected = checked;
        });
    });

    // open the thread
    $scope.openThread = function(thread) {
        var stateMessages = 'app.dashboard.threads.messages';

        $scope.addTab({
            title: $filter('joinRecipients')(thread.recipients, 3),
            tooltip: $filter('joinRecipients')(thread.recipients, -1),
            state: stateMessages,
            stateParams: {id: thread.id},
            active: true
        });

        $state.go(stateMessages, {id:thread.id});
    };

    $scope.openAttachment = function(extension) {
        var modalInstance = $modal.open({
            templateUrl: 'attachment/html/download.tpl.html',
            controller: 'AttachmentCtrl',
            resolve: {
                extension: function () {
                    return extension;
                }
            }
        });
    };
}]);

}());
