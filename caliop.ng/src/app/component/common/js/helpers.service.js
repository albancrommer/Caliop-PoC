(function() {

"use strict";

angular.module('caliop.common.helpers.service', [])

.factory('string', [function () {
    return {
        /**
         * @desc Replace some value in a string. A sprintf light.
         * @return {string}
         */
        replace: function () {
            var string = arguments[0];
            var list = angular.isArray(arguments[1]) ?
                arguments[1] : [].slice.call(arguments, 1);

            angular.forEach(list, function(v, i) {
                string = string.replace(/\$[0-9a-zA-Z]+|%[a-z]{1}/,
                    (v === undefined ? '' : v));
            });

            return string;
        },

        /**
         * @desc Camelcase str.
         * @param  {string} str The string to camelcase
         * @return {string}
         */
        toCamelCase: function (str) {
            return str
                .replace(/_/g, '-')
                .replace(/\W+(.)/g, function (x, chr) {
                    return chr.toUpperCase();
                });
        }
    };
}])

.factory('number', [function () {
    return {
        /**
         * @desc Replace some value in a string. A sprintf light.
         * @return {string}
         */
        random: function (schema) {
            schema = schema || 'xxxxxxxx';
            schema.replace(/[xy]/g, function(c) {
                var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
                return v.toString(16);
            });
        }
    };
}]);

}());
