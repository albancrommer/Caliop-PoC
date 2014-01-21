(function() {

"use strict";

describe( 'DashboardCtrl', function() {
    describe( 'isCurrentUrl', function() {
        var AppCtrl, $location, $scope;

        beforeEach( module( 'caliop' ) );

        beforeEach( inject( function( $controller, _$location_, $rootScope ) {
            $location = _$location_;
            $scope = $rootScope.$new();
            AppCtrl = $controller( 'DashboardCtrl', { $location: $location, $scope: $scope });
        }));

        it( 'should pass a dummy test', inject( function() {
            expect( AppCtrl ).toBeTruthy();
        }));
    });
});

}());
