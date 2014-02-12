(function() {

"use strict";

angular.module('caliop.inbox.service.tabs', [])

.factory('tabs', ['$cookieStore', '$state',
    function ($cookieStore, $state) {

    // @TODO Fix the cookie name to be session based
    var COOKIE_NAME = 'inBoxTabs';

    return {
        tabs: $cookieStore.get(COOKIE_NAME) || [{
            id: 1,
            title: 'Conversations',
            state: 'app.inbox',
            active: true,
            closable: false,
            last: false
        }, {
            id: 2,
            icon: 'pencil',
            state: 'app.inbox.writeMessage',
            active: false,
            closable: false,
            last: true
        }],

        /**
         * Add a new tab.
         */
        add: function(object) {
            // if some stateParams has been filled, use them to retrieve an
            // already opened tab
            var tabFound;
            if (object.stateParams && object.stateParams.id && object.stateParams.type) {
                var tabsFound = _.filter(this.tabs, function(tab) {
                    return tab.stateParams  &&
                        (tab.stateParams.id == object.stateParams.id) &&
                        (tab.stateParams.type == object.stateParams.type);
                });

                if (tabsFound.length) {
                    tabFound = tabsFound[0];
                }
            }

            // select the found if found
            if (tabFound) {
                this.select(tabFound);
            }

            // otherwise, create a new tab
            else {
                var tabObject = angular.extend({
                    id: this.tabs.length + 1,
                    closable: true,
                    active: true,
                    last: false
                }, object);

                this.tabs.push(tabObject);
            }

            // keep the write message tab at the end
            this.tabs = _.sortBy(this.tabs, function(tab) {
                return tab.last;
            });

            this.updateCookie();

            // redirect
            $state.go(object.state, object.stateParams);
        },

        /**
         * Select an existing tab.
         */
        select: function(tab) {
            var tabFound;

            _.map(this.tabs, function(tab_) {
                var found = tab_.id == tab.id;
                if (found) {
                    tabFound = tab_;
                }
                // activate the clicked tab, deactivate others
                tab_.active = found;
            });

            if (tabFound && tabFound.state) {
                var params = tabFound.stateParams || {};
                $state.go(tabFound.state, params);
            }

            this.updateCookie();
        },

        /**
         * Close a tab.
         */
        close: function(tab) {
            var that = this;
            var previousTab;

            _.remove(this.tabs, function(tab_, i) {
                var tabFound = tab_.id == tab.id && tab_.type == tab.type;
                if (tabFound) {
                    previousTab = that.tabs[i-1];
                }
                return tabFound;
            });

            // activate and go to the state of the previous tab
            previousTab.active = true;
            $state.go(previousTab.state, previousTab.stateParams || {});

            this.updateCookie();
        },

        /**
         * Save tabs in a cookie to keep persistence.
         */
        updateCookie: function() {
            $cookieStore.put(COOKIE_NAME, this.tabs);
        }
    };
}]);

}());
