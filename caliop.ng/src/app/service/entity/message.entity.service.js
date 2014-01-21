// (function() {

// "use strict";

// angular.module('caliop.service.entity.message', [
//     'restangular',
//     'caliop.service.helpers'
// ])

// .factory('message', ['Restangular', 'string',
//     function (Restangular, stringSrv) {

//     var Message = function Message(obj) {
//         var self = this;

//         angular.extend(self, obj);

//         // save obj struct in the object
//         angular.forEach(obj, function(value, key) {
//             key = stringSrv.toCamelCase(key);
//             self[key] = value;

//             // convert dates to moment objects
//             if (/^date/.test(key)) {
//                 self[key] = moment(self[key]);
//             }
//         });
//     };

//     // Message.prototype.getTitle = function() {
//     //     return this.title;
//     // };

//     Restangular.addElementTransformer('messages', false, function(obj) {
//         return new Message(obj);
//     });

//     return Restangular.all('messages');

// }]);

// }());
