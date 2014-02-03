(function() {

"use strict";

angular.module('caliop.attachment.entity.attachment', [
    'caliop.common.service.helpers'
])

.factory('attachment', ['base',
    function (BaseEnt) {

    function Attachment() { BaseEnt.apply(this, arguments); }
    Attachment.prototype = Object.create(BaseEnt.prototype);

    /**
     * Return the icon src of the attachment.
     */
    Attachment.prototype.getIconSrc = function() {
        var file = this.extension + '.png';
        return '/static/assets/images/attachments/' + file;
    };

    // Restangular.addElementTransformer('attachments', false, function(obj) {
    //     return Attachment.new_(obj);
    // });

    return Attachment;

}]);

}());
