(function() {

"use strict";

angular.module('caliop.inbox.service.filter')

.factory('filter', [
    function () {

    return {
        labels: [],

        addLabel: function(label) {
            this.labels = _.uniq(_.union(
                this.labels,
                [label]
            ), function(label) {
                // filter on labelId
                return label.id;
            });
        },

        removeLabel: function(label) {
            _.remove(this.labels, function(label_) {
                return label_.id == label.id;
            });
        }
    };
}]);

}());
