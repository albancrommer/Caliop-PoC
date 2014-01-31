(function() {

"use strict";

angular.module('caliop.inbox')

/**
 * TabsManagementCtrl
 */
.controller('TabsManagementCtrl', ['$scope', 'tabs',
    function TabsManagementCtrl($scope, tabsSrv) {

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
        tabsSrv.select(tab);
    };

    /**
     * Close a tab.
     */
    $scope.closeTab = function(tab) {
        tabsSrv.close(tab);
    };
}]);

}());
