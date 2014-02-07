(function() {

"use strict";

angular.module('caliop.inbox')

/**
 * TabsManagementCtrl
 */
.controller('TabsManagementCtrl', ['$rootScope', '$scope', 'tabs', 'filter',
    function TabsManagementCtrl($rootScope, $scope, tabsSrv, FilterSrv) {

    /**
     * Watch the tabs list in the service.
     */
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

    /* @TODO Move the code below to a FilterCtrl + ui-views */

    /**
     * Initialize a shared variable between this controller and its children
     * which allows to refresh labels in the filter and to reload threads list
     * when being updated.
     */
    $scope.filter = {
        labels: []
    };

    /**
     * Remove a label from the filter.
     */
    $scope.removeFilterLabel = function(label) {
        FilterSrv.removeLabel(label);
        $scope.filter.labels = FilterSrv.labels;
    };
}]);

}());
