(function() {

"use strict";

/**
 * Dashboard component.
 */
angular.module('caliop.component.dashboard')

.config(function config($stateProvider) {
    $stateProvider
        .state('app.dashboard.files', {
            views: {
                'panelContent@app.dashboard': {
                    templateUrl: 'component/panel/html/panel.files.tpl.html',
                    controller: 'FilesListCtrl'
                }
            }
        });
})

/**
 * DashboardCtrl
 */
.controller('FilesListCtrl', ['$scope',
    function FilesListCtrl($scope) {

    console.log('FilesListCtrl');
}]);
}());