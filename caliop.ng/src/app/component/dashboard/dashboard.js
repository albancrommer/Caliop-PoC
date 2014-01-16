/**
 * Dashboard component.
 */
angular.module('caliop.component.dashboard', [
    'ui.router',

    'caliop.service.entity.message',

    'ui.bootstrap',
    'ngAnimate'
])

/**
 * Each section or module of the site can also have its own routes. AngularJS
 * will handle ensuring they are all available at run-time, but splitting it
 * this way makes each module more "self-contained".
 */
.config(function config($stateProvider) {
    $stateProvider
        .state('dashboard', {
            url: '/dashboard',
            templateUrl: 'component/dashboard/dashboard.tpl.html',
            controller: 'DashboardCtrl',
            data: {
                pageTitle: 'Dashboard'
            }
        })
            .state('dashboard.messages', {
                url: '/messages',
                templateUrl: 'component/dashboard/messages.tpl.html',
                controller: 'MessagesCtrl',
                data: {
                    pageTitle: 'Here your messages'
                }
            })
            .state('dashboard.writeMessage', {
                url: '/messages',
                templateUrl: 'component/dashboard/write-message.tpl.html',
                controller: 'MessagesCtrl',
                data: {
                    pageTitle: 'Write a new message'
                }
            });
})

/**
 * And of course we define a controller for our route.
 */
.controller('DashboardCtrl', ['$scope', 'message',
    function DashboardCtrl($scope, MessageSrv) {

    $scope.tabs = [];

    var addNewTab = function() {
        var id = $scope.tabs.length + 1;
        $scope.tabs.push({
            id: id,
            title: "Workspace " + id,
            content: "Workspace " + id,
            active: true
        });
    };

    MessageSrv.getList().then(function(messages) {
        $scope.tabs = [
            { id: 1, title: 'Messages', content: messages, active: true }
        ];

        $scope.addTab = function() {
            addNewTab();
        };
    });
}])

/**
 * And of course we define a controller for our route.
 */
.controller('MessagesCtrl', ['$scope',
    function DashboardCtrl($scope) {

    console.log('MessagesCtrl');


}]);
