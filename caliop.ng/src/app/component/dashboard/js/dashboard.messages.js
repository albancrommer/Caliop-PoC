/**
 * Dashboard component.
 */
angular.module('caliop.component.dashboard')

.config(function config($stateProvider) {
    $stateProvider
        .state('app.dashboard.messages', {
            url: '/messages',
            views: {
                'tabContent@app.dashboard': {
                    templateUrl: 'component/dashboard/html/messages.tpl.html',
                    controller: 'MessagesCtrl'
                }
            }
        });
})

/**
 * DashboardCtrl
 */
.controller('MessagesCtrl', ['$scope', 'message',
    function MessagesCtrl($scope, MessageSrv) {

    MessageSrv.getList().then(function(messages) {
        $scope.messages = messages;
    });

    console.log('MessagesCtrl');
}]);
