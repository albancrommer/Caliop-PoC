(function() {

"use strict";

angular.module('caliop.inbox')

/**
 * TabsManagementCtrl
 */
.controller('TabsManagementCtrl', ['$scope', '$state', 'tabs',
    function TabsManagementCtrl($scope, $state, tabsSrv) {

    console.log('TabsManagementCtrl');

    // watch the tabs list in the service
    $scope.$watch(function() {
        return tabsSrv.tabs;
    }, function(tabs) {
        $scope.tabs = tabs;
    });

    /**
     * Load the content of a tab.
     */
    $scope.loadContent = function(tab) {
        if (tab.state) {
            var params = tab.stateParams || {};
            $state.go(tab.state, params);
        }
    };

    /**
     * Redirect to the write message interface.
     */
    $scope.writeMessage = function(tab) {
        $state.go('app.inbox.writeMessage');
    };

    /**
     * Close a tab.
     */
    $scope.closeTab = function(tab) {
        tabsSrv.close(tab);
    };
}]);

}());
