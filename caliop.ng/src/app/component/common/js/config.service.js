(function() {

"use strict";

angular.module('caliop.common.config.service', [])

/**
 * Service used to:
 *  - get configuration from the localstorage
 *  - set configuration from the querystring.
 */
.service('config', ['$location', function ($location) {
    var LOCALSTORAGE_KEY = 'caliop.config';

    /**
     * Retrieve the configuration from the localstorage
     */
    this.init = function() {
        var values = localStorage.getItem(LOCALSTORAGE_KEY);
        this.config = values ? JSON.parse(values) : {};
    };

    /**
     * Save each /^config\./ keys of the querystring to the object.
     * @return {[type]} [description]
     */
    this.configure = function() {
        var that = this,
            params = $location.search(),
            prefixRegex = new RegExp(/^config\./);

        angular.forEach(params, function(value, key) {
            if (prefixRegex.test(key)) {
                var key_ = key.replace(prefixRegex, '');
                that.config[key_] = value;
            }
        });

        // save in the localstorage
        this.save();
    };

    /**
     * Save the configuration in the localstorage.
     */
    this.save = function() {
        var values = JSON.stringify(this.config);
        window.localStorage.setItem(LOCALSTORAGE_KEY, values);
    };

    /**
     * Return a value of the config.
     */
    this.get = function(key) {
        return this.config[key];
    };

    this.init();
}]);

}());
