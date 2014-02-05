(function() {

"use strict";

angular.module('caliop.account')

.config(['$stateProvider',
    function config($stateProvider) {

    $stateProvider
        .state('app.account', {
            url: 'account',
            views: {
                // ui-view="layout" of index.tpl.html
                'layout@': {
                    templateUrl: 'common/html/fullpage.tpl.html'
                },
                // ui-view="main" of fullpage.tpl.html
                'main@app.account': {
                    templateUrl: 'account/html/account.tpl.html',
                    controller: 'AccountCtrl'
                }
            }
        })
        .state('app.preferences', {
            url: 'preferences',
            views: {
                // ui-view="layout" of index.tpl.html
                'layout@': {
                    templateUrl: 'common/html/fullpage.tpl.html'
                },
                // ui-view="main" of fullpage.tpl.html
                'main@app.preferences': {
                    templateUrl: 'account/html/preferences.tpl.html',
                    controller: 'PreferencesCtrl'
                }
            }
        });
}])

/**
 * AccountCtrl
 */
.controller('AccountCtrl', ['$scope', 'auth',
    function AccountCtrl($scope, authSrv) {

}])

/**
 * PreferencesCtrl
 */
.controller('PreferencesCtrl', ['$scope', 'auth',
    function PreferencesCtrl($scope, authSrv) {

}]);

}());
