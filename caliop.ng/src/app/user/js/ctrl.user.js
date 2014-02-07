(function() {

"use strict";

angular.module('caliop.user')

.config(function config($stateProvider) {
    $stateProvider
        .state('app.user', {
            url: 'user/',
            abstract: true,
            views: {
                // ui-view="layout" of index.tpl.html
                'layout@': {
                    templateUrl: 'common/html/2columns.tpl.html'
                },
                // ui-view="main" of 2columns.tpl.html
                'main@app.user': {
                    templateUrl: 'inbox/html/layout.tpl.html',
                    controller: 'InBoxLayoutCtrl'
                },
                // ui-view="tabContent" of inbox/html/layout.tpl.html
                'tabContent@app.user': {
                    templateUrl: 'user/html/create-user.tpl.html',
                    controller: 'UserCreationCtrl'
                },
                // ui-view="panel" of 2columns.tpl.html
                'panel@app.user': {
                    templateUrl: 'panel/html/panel.tpl.html',
                    controller: 'PanelCtrl'
                }
            }
        })
        .state('app.user.create', {
            url: 'create'
        })
        .state('app.user.createGroup', {
            url: 'create-group',
            views: {
                // ui-view="tabContent" of inbox/html/layout.tpl.html
                'tabContent@app.user': {
                    templateUrl: 'user/html/create-group.tpl.html',
                    controller: 'GroupCreationCtrl'
                }
            }
        });
})

/**
 * UserCreationCtrl
 */
.controller('UserCreationCtrl', ['$scope',
    function AccountCtrl($scope) {

    $scope.telephones = [{
        number: undefined
    }];

    $scope.addTelephone = function() {
        $scope.telephones.push({
            number: undefined
        });
    };

    $scope.removeTelephone = function(index) {
        $scope.telephones.splice(index, 1);
    };
}])

/**
 * GroupCreationCtrl
 */
.controller('GroupCreationCtrl', ['$scope',
    function AccountCtrl($scope) {

}]);

}());
