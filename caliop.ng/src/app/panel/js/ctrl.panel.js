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

.controller('PanelUsersCtrl', ['$scope', '$state', 'resolve-tab', 'tabs', 'user',
    function PanelCtrl($scope, $state, tab, InBoxTabsSrv, userSrv) {

    // retrieve the list of groups/users
    userSrv.Restangular.all('users').getList().then(function(users) {
        // index users by groups
        var groups = {};
        _.map(users, function(user) {
            _.forEach(user.groups, function(group) {
                if (!groups[group.id]) {
                    groups[group.id] = {
                        'group': group,
                        'users': []
                    };
                }

                groups[group.id].users.push(user);
            });
        });

        // count the number of connected users
        _.map(groups, function(group) {
            group.group.connectedUsersCount = _.filter(group.users, function(user) {
                return user.connected;
            }).length;
        });

        $scope.groups = groups;
    });

    /**
     * Add a tab and redirect to the user creation
     */
    $scope.createUser = function() {
        InBoxTabsSrv.add({
            title: 'Créer un contact',
            state: 'app.user.create',
            stateParams: {
                type: 'createUser',
                id: 'createUser'
            }
        });
    };

    /**
     * Redirection to the group creation.
     */
    $scope.createGroup = function() {
        InBoxTabsSrv.add({
            title: 'Créer un groupe',
            state: 'app.user.createGroup'
        });
    };
}])

.controller('PanelCalendarCtrl', ['$scope', 'resolve-tab',
    function PanelCtrl($scope, tab) {

}])

.controller('PanelFilesCtrl', ['$scope', 'resolve-tab',
    function PanelCtrl($scope, tab) {

}]);

}());
