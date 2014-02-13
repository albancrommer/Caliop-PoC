(function() {

"use strict";

angular.module('caliop.inbox', [
    'caliop.inbox.entity.thread',
    'caliop.inbox.service.filter',
    'caliop.user.filter',
    'caliop.inbox.directive',

    'caliop.message',
    'caliop.attachment'
])

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

.controller('TagSelectorCtrl', ['$scope', 'tag', 'thread',
    function TagSelectorCtrl($scope, TagSrv, ThreadSrv) {

    /**
     * Tags selector popover.
     */
    $scope.openTagSelector = function() {
        var selectedThreads = $scope.getSelectedThreads();

        // stack threads by tag
        var threadsByTags = {};
        _.forEach(selectedThreads, function(thread) {
            _.forEach(thread.tags, function(tag) {
                if (!threadsByTags[tag.id]) {
                    threadsByTags[tag.id] = [];
                }
                threadsByTags[tag.id].push(thread);
            });
        });

        // for each tag, compare the number of tags and the number of selected tags
        // to know which checkbox status to display (none, indetermediate, checked)
        TagSrv.getList().then(function(tags) {
            _.forEach(tags, function(tag) {
                if (!threadsByTags[tag.id] || threadsByTags[tag.id].length === 0) {
                    tag.isSelected = 0;
                }
                else if (threadsByTags[tag.id].length == selectedThreads.length) {
                    tag.isSelected = 1;
                }
                else {
                    // indetermediate
                    tag.isSelected = 0.5;
                }
            });

            $scope.tags = tags;
        });
    };

    /**
     * Add or remove tags to thread(s).
     */
    $scope.setTags = function(tag) {
        var selectedThreads = $scope.getSelectedThreads();

        // inverse the status of the selected tags
        _.forEach($scope.tags, function(tag_) {
            if (tag_.id == tag.id) {
                // if indetermediate, a click enable the checkbox
                if (tag.isSelected == 0.5) {
                    tag.isSelected = true;
                }
                else {
                    tag_.isSelected = !tag_.isSelected;
                }

                // stop loop
                return false;
            }
        });

        var threadsId = _.map(selectedThreads, function(thread) {
            return thread.id;
        });

        // group tags by set/unset keys, corresponding to the queries to make
        var tagsIdMapping = _.reduce($scope.tags, function(result, tag) {
            var action = tag.isSelected ? 'set' : 'unset';

            // do nothing for indetermediate state
            if (tag.isSelected != 0.5) {
                if (!result[action]) {
                    result[action] = [];
                }

                result[action].push(tag.id);
            }
            return result;
        }, {});

        // set tags and refresh the threads
        ThreadSrv.setTags(threadsId, tagsIdMapping['set']).then(function() {
            // index stuff
            var threadsById = _.groupBy(selectedThreads, 'id');
            var tagsById = _.groupBy($scope.tags, 'id');

            _.forEach(selectedThreads, function(thread) {
                var threadTags = [];
                _.forEach(tagsIdMapping['set'], function(tagId) {
                    threadTags.push(tagsById[tagId][0]);
                });
                threadsById[thread.id][0].tags = threadTags;
            });
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

    // init
    $scope.threads = {};

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

        // set the thread as read
        thread.setRead();
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
     * Return the selected threads.
     */
    $scope.getSelectedThreads = function() {
        return _.filter($scope.threads.list, function(thread) {
            return thread.selected;
        });
    };

    /**
     * Show actions icons if a (or more) thread has been selected.
     */
    $scope.showThreadActions = function() {
        return $scope.getSelectedThreads().length > 0;
    };

    /**
     * Select/unselect all threads.
     */
    $scope.$watch('selectAllThreads', function(checked) {
        angular.forEach($scope.threads.list, function(thread) {
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

        // filter by tags
        var params = {};
        if (FilterSrv.tags.length) {
            params = {tag: _.map(FilterSrv.tags, function(tag) {
                return tag.id;
            })};
        }

        $scope.reloadThreads(params);
    });

    /**
     * Reload threads with optional search params
     */
    $scope.reloadThreads = function(params) {
        // make query parameters to reload threads
        ThreadSrv.getList(params).then(function(threads) {
            $scope.threads.list = threads;

            // count unread threads
            $scope.threads.unread = _.filter($scope.threads.list, function(thread) {
                return thread.isUnread();
            }).length;
        });
    };
}]);

}());
