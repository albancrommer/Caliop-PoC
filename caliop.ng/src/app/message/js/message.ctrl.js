(function() {

"use strict";

angular.module('caliop.inbox')

.config(function config($stateProvider) {
    $stateProvider
        .state('app.dashboard.threads.messages', {
            url: '/:id',
            views: {
                // ui-view="tabContent" of inbox/html/layout.tpl.html
                'tabContent@app.dashboard': {
                    templateUrl: 'message/html/list.tpl.html',
                    controller: 'MessagesCtrl'
                }
            }
        })
        .state('app.dashboard.writeMessage', {
            url: '/write',
            views: {
                // ui-view="tabContent" of inbox/html/layout.tpl.html
                'tabContent@app.dashboard': {
                    templateUrl: 'message/html/write.tpl.html',
                    controller: 'WriteMessageCtrl'
                }
            }
        });
})

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
}])

/**
 * WriteMessageCtrl
 */
.controller('WriteMessageCtrl', ['$scope',
    function WriteMessageCtrl($scope) {

    console.log('WriteMessageCtrl');
}]);

}());
