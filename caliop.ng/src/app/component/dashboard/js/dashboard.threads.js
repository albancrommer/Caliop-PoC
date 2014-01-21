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
        });
})

/**
 * ThreadsCtrl
 */
.controller('ThreadsCtrl', ['$scope', 'thread',
    function ThreadsCtrl($scope, ThreadSrv) {

    ThreadSrv.Restangular.all('threads').getList().then(function(threads) {
        $scope.threads = threads;
    });

    $scope.openThread = function(thread) {
        console.log('open thread', thread);
    };
}]);
