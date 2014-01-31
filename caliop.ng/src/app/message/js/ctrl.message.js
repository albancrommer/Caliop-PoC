(function() {

"use strict";

angular.module('caliop.message')

.config(function config($stateProvider) {
    $stateProvider
        .state('app.inbox.thread', {
            url: '/thread/:id/messages',
            views: {
                // ui-view="tabContent" of inbox/html/layout.tpl.html
                'tabContent@app.inbox': {
                    templateUrl: 'message/html/list.tpl.html',
                    controller: 'MessagesCtrl'
                }
            }
        })
        .state('app.inbox.writeMessage', {
            url: '/write',
            views: {
                // ui-view="tabContent" of inbox/html/layout.tpl.html
                'tabContent@app.inbox': {
                    templateUrl: 'message/html/write.tpl.html',
                    controller: 'WriteMessageCtrl'
                }
            }
        });
})

/**
 * MessagesCtrl
 */
.controller('MessagesCtrl', ['$scope', '$state', '$stateParams', 'message',
    function MessagesCtrl($scope, $state, $stateParams, MessageSrv) {

    var threadId = $stateParams.id;

    if (!threadId) {
        $state.go('app.inbox');
        return;
    }

    MessageSrv.Restangular.one('threads', threadId).getList('messages')
        .then(function(messages) {
            $scope.messages = messages;
        });
}])

/**
 * WriteMessageCtrl
 */
.controller('WriteMessageCtrl', ['$scope',
    function WriteMessageCtrl($scope) {

}]);

}());
