(function() {

"use strict";

/**
 * Dashboard component.
 */
angular.module('caliop.component.dashboard')

.config(function config($stateProvider) {
    $stateProvider
        .state('app.dashboard.writeMessage', {
            url: '/write',
            views: {
                'tabContent@app.dashboard': {
                    templateUrl: 'component/dashboard/html/write-message.tpl.html',
                    controller: 'WriteMessageCtrl'
                }
            }
        });
})

/**
 * DashboardCtrl
 */
.controller('WriteMessageCtrl', ['$scope',
    function WriteMessageCtrl($scope) {

    console.log('WriteMessageCtrl');
}]);

}());
