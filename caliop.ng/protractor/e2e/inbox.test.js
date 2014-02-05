module.exports = function (request, response) {

describe(' inbox  ', function() {

    var includeLogin = require('./login.test.js')();

    // Lets do some stuff after login.test.js correctly exec

    it('should be in the inbox page', function() {
        expect(browser.getCurrentUrl()).toEqual('http://localhost:6543/#/inbox');
    });



});

};