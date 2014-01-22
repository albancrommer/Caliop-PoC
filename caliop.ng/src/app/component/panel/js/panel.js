(function() {

"use strict";

/**
 * Panel components.
 */
angular.module('caliop.component.panel', [
])

.config(function config($stateProvider) {
    $stateProvider
        .state('app.dashboard.panel', {
            views: {
                'panelContent@app.dashboard': {
                    templateUrl: 'component/panel/html/panel.tpl.html',
                    controller: 'PanelCtrl'
                }
            }
    });
})

.controller('PanelCtrl', ['$scope', '$state',
    function PanelCtrl($scope, $state) {

    $scope.tabs = [{
        id: 1,
        icon: 'user',
        state: 'app.dashboard.threads.userlist',
        active: true
    },{
        id: 2,
        icon: 'calendar',
        state: 'app.dashboard.calendar',
        active: false
    },{
        id: 3,
        icon: 'file',
        state: 'app.dashboard.filelist',
        active: false
    }];

    $scope.loadPanelContent = function(tab) {
        console.log('PanelCtrl in fucntion ', tab);
        $state.go(tab.state);
    };

}]);

}());
