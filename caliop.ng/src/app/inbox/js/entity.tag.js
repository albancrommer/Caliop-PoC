(function() {

"use strict";

angular.module('caliop.inbox.entity.tag')

.factory('tag', ['Restangular', 'base',
    function (Restangular, BaseEnt) {

    function Tag() { BaseEnt.apply(this, arguments); }
    Tag.prototype = Object.create(BaseEnt.prototype);

    /**
     * Create a tag from a GET query for a given id.
     */
    Tag.byId = function(tagId) {
        return Restangular.all('tags').one('by_id', tagId).get();
    };

    /**
     ** Create a tag from a GET query for a given label.
     */
    Tag.byLabel = function(label) {
        return Restangular.all('tags').one('by_label', label).get();
    };

    Restangular.addElementTransformer('tags', false, function(obj) {
        return new Tag(obj);
    });

    return Tag;
}]);

}());
