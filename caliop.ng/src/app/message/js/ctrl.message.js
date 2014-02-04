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

    MessageSrv.getThreadList(threadId).then(function(messages) {
        $scope.messages = messages;
    });
}])

/**
 * WriteMessageCtrl
 */
.controller('WriteMessageCtrl', ['$scope', 'user', 'thread',
    function WriteMessageCtrl($scope, UserSrv, ThreadSrv) {

    $scope.availableProtocoles = ['Caliop', 'Mail', 'XMPP'];

    $scope.message = {
        protocole: $scope.availableProtocoles[0]
    };

    // retrieve the list of groups/users
    UserSrv.getList().then(function(users) {
        $scope.users = users;

        $scope.message.users = [];
        $scope.$watch('to', function(userName) {
            // remove it from the available users
            var removedUsers = _.remove($scope.users, function(user) {
                return userName == user.displayName();
            });

            if (removedUsers.length) {
                // add a user to the message
                $scope.message.users = _.union(
                    $scope.message.users,
                    removedUsers
                );
                $scope.to = '';
            }
        });
    });

    $scope.removeUser = function(user) {
        var removedUsers = _.remove($scope.message.users, function(user_) {
            return user_.displayName() == user.displayName();
        });

        // merge the list of users with the list of removed users
        $scope.users = _.union($scope.users, removedUsers);

        // focus the input by using the directive 'focusOn'
        $scope.$broadcast('userRemoved');
    };

    $scope.submitMessage = function() {
        // @TODO Check inputs/validations etc.

        // create a new thread with the message inside
        ThreadSrv.new_($scope.message).then(function(thread) {
            console.log('thread postaid !', thread);
        });
    };
}])

/**
 * Allow to focus an element by broadcasting an event in the scope.
 */
.directive('focusOn', function() {
   return function(scope, elem, attr) {
      scope.$on(attr.focusOn, function(e) {
          elem[0].focus();
      });
   };
});

}());
