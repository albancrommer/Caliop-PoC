(function() {

"use strict";

angular.module('caliop.inbox.entity.label')

.factory('label', ['Restangular', 'base',
    function (Restangular, BaseEnt) {

    function Label() { BaseEnt.apply(this, arguments); }
    Label.prototype = Object.create(BaseEnt.prototype);

    Restangular.addElementTransformer('labels', false, function(obj) {
        return new Label(obj);
    });

    return Label;
}]);

}());
