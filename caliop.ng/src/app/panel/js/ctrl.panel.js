(function() {

"use strict";

/**
 * Panel components.
 */
angular.module('caliop.panel', [
    'templates-app',
    'ui.router',

    'caliop.user'
])

.config(function config($stateProvider) {
})

.controller('PanelCtrl', ['$scope', '$state', '$controller',
    function PanelCtrl($scope, $state, $controller) {

    $scope.tabs = [{
        id: 1,
        icon: 'user',
        template: 'panel/html/users.tpl.html',
        controller: 'PanelUsersCtrl',
        active: true
    },{
        id: 2,
        icon: 'calendar',
        template: 'panel/html/calendar.tpl.html',
        controller: 'PanelCalendarCtrl',
        active: false
    },{
        id: 3,
        icon: 'file',
        template: 'panel/html/files.tpl.html',
        controller: 'PanelFilesCtrl',
        active: false
    }];

    $scope.tabSelected = $scope.tabs[0];

    $scope.loadPanelContent = function(tab) {
        $scope.tabSelected = tab;
    };
}])

.directive('resolveController', ['$controller', function($controller) {
    return {
        scope: true,
        link: function(scope, elem, attrs) {
            var resolve = scope.$eval(attrs.resolve);
            angular.extend(resolve, {$scope: scope});
            $controller(attrs.resolveController, resolve);
        }
    };
}])

.controller('PanelUsersCtrl', ['$scope', 'resolve-tab',
    function PanelCtrl($scope, tab) {

    console.log('PanelUsersCtrl');

    // userSrv.Restangular.all('users').then(function(users) {
    //     $scope.users = users;
    // });

    $scope.groups = [{
        name: 'Famille',
        users: [{
            name: 'Toto',
            connectionStatus: 1
        }, {
            name: 'Toto2',
            connectionStatus: 0
        }]
    }, {
        name: 'Boulot',
        users: [{
            name: 'Toto',
            connectionStatus: 0
        }, {
            name: 'Toto2',
            connectionStatus: 1
        }]
    }, {
        name: 'Pôtes',
        users: [{
            name: 'Toto',
            connectionStatus: 1
        }, {
            name: 'Toto2',
            connectionStatus: 1
        }, {
            name: 'Toto3',
            connectionStatus: 1
        }]
    }];

    // count the number of connected users
    _.map($scope.groups, function(group) {
        group.connectedUsersCount = _.filter(group.users, function(user) {
            return user.connectionStatus == 1;
        }).length;
    });
}])

.controller('PanelCalendarCtrl', ['$scope', 'resolve-tab',
    function PanelCtrl($scope, tab) {

    console.log('PanelCalendarCtrl');
}])

.controller('PanelFilesCtrl', ['$scope', 'resolve-tab',
    function PanelCtrl($scope, tab) {

    console.log('PanelFilesCtrl');
}]);

}());
