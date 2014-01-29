(function() {

"use strict";

describe( 'Hello World', function() {
    var element;
    var $scope;

    beforeEach(inject(function($compile, $rootScope) {
        $scope = $rootScope;

        element = angular.element('<div>{{2 + 2}}</div>');
        element = $compile(element)($rootScope);
    }));

    it('should be equals to 4', function() {
        $scope.$digest();
        expect(element.html()).toBe('4');
    });
});


describe( 'InBoxCtrl', function() {
    describe( 'isCurrentUrl', function() {
        var AppCtrl, $location, $scope;

        beforeEach( module( 'caliop' ) );

        beforeEach( inject( function( $controller, _$location_, $rootScope ) {
            $location = _$location_;
            $scope = $rootScope.$new();
            AppCtrl = $controller( 'InBoxCtrl', { $location: $location, $scope: $scope });
        }));

        it( 'should pass a dummy test', inject( function() {
            expect( AppCtrl ).toBeTruthy();
        }));
    });
});

}());
