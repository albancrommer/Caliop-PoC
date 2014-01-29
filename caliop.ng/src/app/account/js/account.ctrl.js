(function() {

"use strict";

angular.module('caliop.account')

.config(function config($stateProvider) {
    $stateProvider
        .state('app.account', {
            url: 'account',
            views: {
                // ui-view="header" of index.html
                'header@': {
                    templateUrl: 'header/html/header.tpl.html',
                    controller: 'HeaderCtrl'
                },
                // ui-view="layout" of index.html
                'layout@': {
                    templateUrl: 'common/html/fullpage.tpl.html'
                },
                // ui-view="main" of fullpage.html
                'main@app.account': {
                    templateUrl: 'account/html/account.tpl.html',
                    controller: 'AccountCtrl'
                },
                // ui-view="footer" of index.html
                'footer@': {
                    templateUrl: 'footer/html/footer.tpl.html',
                    controller: 'FooterCtrl'
                }
            }
        })
        .state('app.preferences', {
            url: 'preferences',
            views: {
                // ui-view="header" of index.html
                'header@': {
                    templateUrl: 'header/html/header.tpl.html',
                    controller: 'HeaderCtrl'
                },
                // ui-view="layout" of index.html
                'layout@': {
                    templateUrl: 'common/html/fullpage.tpl.html'
                },
                // ui-view="main" of fullpage.html
                'main@app.preferences': {
                    templateUrl: 'account/html/preferences.tpl.html',
                    controller: 'PreferencesCtrl'
                },
                // ui-view="footer" of index.html
                'footer@': {
                    templateUrl: 'footer/html/footer.tpl.html',
                    controller: 'FooterCtrl'
                }
            }
        });
})

/**
 * AccountCtrl
 */
.controller('AccountCtrl', ['$scope', 'auth',
    function AccountCtrl($scope, authSrv) {

    console.log('AccountCtrl');

    // $scope.contact = authSrv.getContact();
}])

/**
 * PreferencesCtrl
 */
.controller('PreferencesCtrl', ['$scope', 'auth',
    function PreferencesCtrl($scope, authSrv) {

    console.log('PreferencesCtrl');

    // console.log('PreferencesCtrl');
}]);

}());
