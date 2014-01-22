(function() {

"use strict";

/**
 * Dashboard component.
 */
angular.module('caliop.component.dashboard')

.config(function config($stateProvider) {
    $stateProvider
        .state('app.dashboard.calendar', {
            views: {
                'panelContent@app.dashboard': {
                    templateUrl: 'component/panel/html/panel.calendar.tpl.html',
                    controller: 'PanelCalendarCtrl'
                }
            }
        });
})

/**
 * DashboardCtrl
 */
.controller('PanelCalendarCtrl', ['$scope',
    function PanelCalendarCtrl($scope) {

    console.log('PanelCalendarCtrl');
}]);
}());
