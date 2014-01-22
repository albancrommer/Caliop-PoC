(function() {

"use strict";

angular.module('caliop.service.entity.message', [
    'restangular',
    'caliop.service.helpers'
])

.factory('message', ['Restangular', 'string',
    function (Restangular, stringSrv) {

    var Message = function Message(obj) {
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

    Message.new_ = function(obj) {
        var message = new Message(obj);
        return message;
    };

    // Restangular.addElementTransformer('messages', false, function(obj) {
    //     return Message.new_(obj);
    // });

    return {
        new_: Message.new_,
        Restangular: Restangular
    };

}]);

}());
