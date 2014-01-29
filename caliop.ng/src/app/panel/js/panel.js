(function() {

"use strict";

/**
 * Panel components.
 */
angular.module('caliop.panel', [
    'templates-app',
    'ui.router'
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

    $scope.groups = [{
        name: 'Famille',
        people: ['Toto', 'tata', 'titi']
    }, {
        name: 'Boulot',
        people: ['Toto2', 'tata2', 'titi2']
    }, {
        name: 'Pôtes',
        people: ['Toto3', 'tata3', 'titi3']
    }];
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
