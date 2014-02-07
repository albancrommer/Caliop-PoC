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
.controller('InBoxLayoutCtrl', [
    '$scope',
    'tabs', 'filter', 'tag',

    function InBoxLayoutCtrl(
        $scope,
        TabsSrv, FilterSrv) {

    /**
     * Watch the tabs list in the service.
     */
    $scope.$watch(function() {
        return TabsSrv.tabs;
    }, function(tabs) {
        $scope.tabs = tabs;
    });

    /**
     * Load the content of a tab.
     */
    $scope.loadContent = function(tab) {
        TabsSrv.select(tab);
    };

    /**
     * Close a tab.
     */
    $scope.closeTab = function(tab) {
        TabsSrv.close(tab);
    };

    /**
     * Initialize a shared variable between this controller and its children
     * which allows to refresh the filter query.
     */
    $scope.filter = {query: ''};

    /**
     * When submitting the filter form, refresh the query.
     * The watchers in the child controller will observe the filter service
     * and reload threads.
     */
    $scope.submitFilter = function() {
        FilterSrv.parseQuery($scope.filter.query).then(function() {
            $scope.filter.query = FilterSrv.makeQuery();
        });
    };
}])

/**
 * InBoxCtrl
 */
.controller('InBoxCtrl', [
    '$scope', '$state', '$filter', '$modal',
    'tabs', 'thread', 'tag', 'filter',

    function InBoxCtrl(
        $scope, $state, $filter, $modal,
        TabsSrv, ThreadSrv, TagSrv, FilterSrv) {

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
     * Select/unselect all threads.
     */
    $scope.$watch('selectAllThreads', function(checked) {
        angular.forEach($scope.threads, function(thread) {
            thread.selected = checked;
        });
    });

    /**
     * Add a tag to the filters.
     */
    $scope.filterByTag = function(tagId) {
        TagSrv.byId(tagId).then(function(tag) {
            FilterSrv.addTag(tag);
        });
    };

    /**
     * When adding/removing tags,
     *  - update filter query,
     *  - reload the list of threads.
     */
    $scope.$watch(function() {
        return FilterSrv.tags.length;
    }, function(tags) {
        // update the filter query
        $scope.filter.query = FilterSrv.makeQuery();

        // make query parameters to reload threads
        ThreadSrv.getList({
            tag: _.map(FilterSrv.tags, function(tag) {
                return tag.id;
            })
        }).then(function(threads) {
            $scope.threads = threads;
        });
    });

    /**
     * Load threads.
     */
    ThreadSrv.getList().then(function(threads) {
        $scope.threads = threads;
    });
}]);

}());
