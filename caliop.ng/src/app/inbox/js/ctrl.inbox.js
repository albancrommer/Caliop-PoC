(function() {

"use strict";

angular.module('caliop.inbox')

.config(['$stateProvider',
    function config($stateProvider) {

    $stateProvider
        .state('app.inbox', {
            url: 'inbox',
            views: {
                // ui-view="layout" of index.tpl.html
                'layout@': {
                    templateUrl: 'common/html/2columns.tpl.html'
                },
                // ui-view="main" of 2columns.tpl.html
                'main@app.inbox': {
                    templateUrl: 'inbox/html/layout.tpl.html',
                    controller: 'InBoxLayoutCtrl'
                },
                // ui-view="tabContent" of inbox/html/layout.tpl.html
                'tabContent@app.inbox': {
                    templateUrl: 'inbox/html/list.tpl.html',
                    controller: 'InBoxCtrl'
                },
                // ui-view="panel" of 2columns.tpl.html
                'panel@app.inbox': {
                    templateUrl: 'panel/html/panel.tpl.html',
                    controller: 'PanelCtrl'
                }
            }
        });
}])

/**
 * InBoxLayoutCtrl
 */
.controller('InBoxLayoutCtrl', ['$rootScope', '$scope', 'tabs', 'filter',
    function TabsManagementCtrl($rootScope, $scope, tabsSrv, FilterSrv) {

    /**
     * Watch the tabs list in the service.
     */
    $scope.$watch(function() {
        return tabsSrv.tabs;
    }, function(tabs) {
        $scope.tabs = tabs;
    });

    /**
     * Load the content of a tab.
     */
    $scope.loadContent = function(tab) {
        tabsSrv.select(tab);
    };

    /**
     * Close a tab.
     */
    $scope.closeTab = function(tab) {
        tabsSrv.close(tab);
    };

    /**
     * Initialize a shared variable between this controller and its children
     * which allows to refresh labels in the filter and to reload threads list
     * when being updated.
     */
    $scope.filter = {
        labels: []
    };

    /**
     * Remove a label from the filter.
     */
    $scope.removeFilterLabel = function(label) {
        FilterSrv.removeLabel(label);
        $scope.filter.labels = FilterSrv.labels;
    };
}])

/**
 * InBoxCtrl
 */
.controller('InBoxCtrl', [
    '$rootScope', '$scope', '$state', '$filter', '$modal',
    'tabs', 'thread', 'label', 'filter',

    function InBoxCtrl(
        $rootScope, $scope, $state, $filter, $modal,
        TabsSrv, ThreadSrv, LabelSrv, FilterSrv) {

    /**
     * Go inside a thread to list messages.
     */
    $scope.openThread = function(thread) {
        var stateMessages = 'app.inbox.thread';

        TabsSrv.add({
            title: $filter('joinUsers')(thread.users, 3),
            tooltip: $filter('joinUsers')(thread.users, -1),
            state: stateMessages,
            stateParams: {
                type: 'thread',
                id: thread.id
            }
        });
    };

    /**
     * Open a modalbow to download the attachment.
     */
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

    /**
     * Show actions icons if a (or more) thread has been selected.
     */
    $scope.showThreadActions = function() {
        return _.filter($scope.threads, function(thread) {
            return thread.selected;
        }).length > 0;
    };

    /**
     * Add a label to the filters.
     */
    $scope.filterByLabel = function(labelId) {
        LabelSrv.byId(labelId).then(function(label) {
            FilterSrv.addLabel(label);
            $scope.filter.labels = FilterSrv.labels;
        });
    };

    /**
     * Select/unselect all threads.
     */
    $scope.$watch('selectAllThreads', function(checked) {
        angular.forEach($scope.threads, function(thread) {
            thread.selected = checked;
        });
    });

    /**
     * When filter changes, reload the list of threads with the selected labels.
     */
    $scope.$watch('filter.labels', function(labels) {
        var params = {
            label: _.map(labels, function(label) {
                return label.id;
            })
        };

        ThreadSrv.getList(params).then(function(threads) {
            $scope.threads = threads;
        });
    }, true);

    /**
     * Load threads.
     */
    ThreadSrv.getList().then(function(threads) {
        $scope.threads = threads;
    });
}]);

}());
