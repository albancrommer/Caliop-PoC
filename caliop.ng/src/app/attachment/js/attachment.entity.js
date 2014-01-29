(function() {

"use strict";

angular.module('caliop.attachment.attachment.entity', [
    // 'restangular',
    'caliop.common.helpers.service'
])

.factory('attachment', ['string',
    function (stringSrv) {

    var Attachment = function Attachment(obj) {
        var self = this;

        angular.extend(self, obj);

        // save obj struct in the object
        angular.forEach(obj, function(value, key) {
            key = stringSrv.toCamelCase(key);
            self[key] = value;

            // convert dates to moment objects
            if (/^date/.test(key)) {
                self[key] = moment(self[key]);
            }
        });
    };

    /**
     * Return the icon src of the attachment.
     */
    Attachment.prototype.getIconSrc = function() {
        var file = this.extension + '.png';
        return '/static/assets/images/attachments/' + file;
    };

    Attachment.new_ = function(obj) {
        var attachment = new Attachment(obj);
        return attachment;
    };

    // Restangular.addElementTransformer('attachments', false, function(obj) {
    //     return Attachment.new_(obj);
    // });

    return {
        new_: Attachment.new_
        // Restangular: Restangular
    };

}]);

}());
