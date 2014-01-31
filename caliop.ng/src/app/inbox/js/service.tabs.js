(function() {

"use strict";

angular.module('caliop.inbox')

.factory('tabs', ['$cookieStore', '$state',
    function ($cookieStore, $state) {

    return {
        tabs: [{
            id: 1,
            title: 'Conversations',
            state: 'app.inbox',
            active: true,
            closable: false
        }],

        /**
         * Add a new tab.
         */
        add: function(object) {
            var tabFound;
            if (object.stateParams && object.stateParams.id) {
                // search if the tab is already opened
                var stateParamId = object.stateParams.id;

                var tabsFound = _.filter(this.tabs, function(tab) {
                    return tab.stateParams && (tab.stateParams.id == stateParamId);
                });

                if (tabsFound.length) {
                    tabFound = tabsFound[0];
                }
            }

            // select the found tab
            if (tabFound) {
                this.select(tabFound);
            }

            // create a new tab
            else {
                var tabObject = angular.extend({
                    id: this.tabs.length + 1,
                    closable: true
                }, object);

                this.tabs.push(tabObject);
            }
        },

        /**
         * Select an existing tab.
         */
        select: function(tab) {
            tab.active = true;
            $state.go(tab.state, tab.stateParams || {});
        },

        /**
         * Close a tab.
         */
        close: function(tab) {
            _.remove(this.tabs, function(tab_) {
                return tab_.id == tab.id;
            });

            // go to the state of the previous tab
            var lastTab = this.tabs[this.tabs.length-1];
            $state.go(lastTab.state, lastTab.stateParams || {});
        }
    };
}]);

}());
