(function() {

"use strict";

/**
 * Dashboard component.
 */
angular.module('caliop.component.dashboard')

.config(function config($stateProvider) {
    $stateProvider
        .state('app.dashboard.threads.userlist', {
            views: {
                'panelContent@app.dashboard': {
                    templateUrl: 'component/panel/html/panel.userlist.tpl.html',
                    controller: 'UserListCtrl'
                }
            }
        });
})

/**
 * DashboardCtrl
 */
.controller('UserListCtrl', ['$scope',
    function UserListCtrl($scope) {

    console.log('UserListCtrl');
}]);
}());