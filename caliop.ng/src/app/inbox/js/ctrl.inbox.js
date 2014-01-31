(function() {

"use strict";

angular.module('caliop.inbox')

.config(function config($stateProvider) {
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
                    controller: 'TabsManagementCtrl'
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
})

/**
 * InBoxCtrl
 */
.controller('InBoxCtrl', ['$injector', '$scope', '$state', '$filter', '$modal', 'tabs', 'thread',
    function InBoxCtrl($injector, $scope, $state, $filter, $modal, tabsSrv, ThreadSrv) {

    // if any thread is selected, show actions icons
    $scope.showThreadActions = function() {
        return _.filter($scope.threads, function(thread) {
            return thread.selected;
        }).length > 0;
    };

    // open the thread
    $scope.openThread = function(thread) {
        var stateMessages = 'app.inbox.thread';

        tabsSrv.add({
            title: $filter('joinRecipients')(thread.recipients, 3),
            tooltip: $filter('joinRecipients')(thread.recipients, -1),
            state: stateMessages,
            stateParams: {
                type: 'thread',
                id: thread.id
            },
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

    ThreadSrv.Restangular.all('threads').getList().then(function(threads) {
        $scope.threads = threads;
    });

    // select all/none threads
    $scope.$watch('selectAllThreads', function(checked) {
        angular.forEach($scope.threads, function(thread) {
            thread.selected = checked;
        });
    });
}]);

}());
