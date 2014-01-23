(function() {

"use strict";

/**
 * Dashboard component.
 */
angular.module('caliop.component.dashboard')

.config(function config($stateProvider) {
    $stateProvider
        .state('app.dashboard.threads', {
            url: '/threads',
            views: {
                'tabContent@app.dashboard': {
                    templateUrl: 'component/dashboard/html/threads.tpl.html',
                    controller: 'ThreadsCtrl'
                }
            }
        })
        .state('app.dashboard.threads.messages', {
            url: '/:id',
            views: {
                'tabContent@app.dashboard': {
                    templateUrl: 'component/dashboard/html/messages.tpl.html',
                    controller: 'MessagesCtrl'
                }
            }
    });
})

/**
 * ThreadsCtrl
 */
.controller('ThreadsCtrl', ['$scope', '$state', '$filter', 'thread',
    function ThreadsCtrl($scope, $state, $filter, ThreadSrv) {

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
}])

/**
 * MessagesCtrl
 */
.controller('MessagesCtrl', ['$scope', '$state', '$stateParams', 'thread',
    function MessagesCtrl($scope, $state, $stateParams, ThreadSrv) {

    var threadId = $stateParams.id;

    if (!threadId) {
        $state.go('app.dashboard.threads');
        return;
    }

    ThreadSrv.by_id(threadId).then(function(thread) {
        $scope.thread = thread;
        $scope.messages = thread.getMessages().$object;
    });

}]);

}());

