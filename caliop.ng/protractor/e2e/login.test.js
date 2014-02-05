describe('Login and redirect to the inbox', function() {
    'use strict';

    var execSync = require('exec-sync');
    execSync('git checkout ../caliop/caliop/views/api/json/*');

    it('should complete the inputs, submit the form and redirect to the inbox page.', function() {
        browser.get('/#/');

        element(by.model('credentials.login')).sendKeys('Alexis');
        element(by.model('credentials.password')).sendKeys('Mineaud');
        element(by.id('submit')).click();

        expect(browser.getCurrentUrl()).toEqual('http://localhost:6543/#/inbox');
    });

    it('should create a cookie.', function() {
        browser.manage().getCookie('session').then(function(cookie) {
            expect(cookie.value).toMatch(/connected/);
        });
    });
});
