(function() {

"use strict";

angular.module('caliop.inbox.service.filter')

.factory('filter', ['tag', '$q',
    function (TagSrv, $q) {

    return {
        tags: [],

        /**
         * Add a tag (Restangular object).
         * Unify tags by id.
         */
        addTag: function(tag) {
            var that = this;

            this.tags = _.uniq(_.union(
                that.tags,
                [tag]
            ), function(tag) {
                // filter on tagId
                return tag.id;
            });
        },

        /**
         * Remove a tag.
         */
        removeTag: function(tag) {
            _.remove(this.tags, function(tag_) {
                return tag_.id == tag.id;
            });
        },

        /**
         * Make the filter query from filters added in the service.
         */
        makeQuery: function() {
            // update the filter value
            var tagsJoined = _.map(this.tags, function(tag) {
                return tag.label;
            }).join(',');

            var stringParts = [];
            if (tagsJoined.length) {
                stringParts.push('tag:' + tagsJoined);
            }

            return stringParts.join(' ');
        },

        /**
         * Do a inverse job of make query.
         * Parse the string to extract the different search clauses to save into
         * the service.
         */
        parseQuery: function(query) {
            var promises = [];

            // remove all tags
            this.tags = [];

            var that = this,
                parts = query.split(/\s*&\s*/);

            _.map(parts, function(part) {
                var splits = part.split(/\s*:\s*/),
                    key = splits[0],
                    values = splits[1] && splits[1].split(/\s*,\s*/);

                if (key == 'tag') {
                    // for each tag,
                    //  - retrieve it
                    //  - add it to the service
                    //  - resolved the deferred
                    _.forEach(values, function(label) {
                        var deferred = new $q.defer();
                        promises.push(deferred.promise);

                        TagSrv.byLabel(label).then(function(tag) {
                            that.addTag(tag);
                            deferred.resolve(tag);
                        }, function() {
                            // if not found, resolved the deferred without
                            // adding the tag
                            deferred.resolve();
                        });
                    });
                }
            });

            // return a global deferred resolved once every tags have been
            // processed
            return $q.all(promises);
        }
    };
}]);

}());
