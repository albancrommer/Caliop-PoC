module.exports = function (request, response) {

describe('Login and redirect to the inbox', function() {
    'use strict';
    var execSync = require('exec-sync');
    execSync('git checkout ../caliop/caliop/views/api/json/*');
    var loginPage = require('./login.page.js')();
    var cred = {login: 'Alexis', password: 'Mineaud'};

    it('should load login page', function() {
        loginPage.goLogin();
        expect(browser.getCurrentUrl()).toEqual(loginPage.loginURL);
    });

    it('should filling form', function() {
        loginPage.fillingAllForm(cred);

        loginPage.getLoginForm().then(function (value) {
            expect(cred.login).toEqual(value);
        });

        loginPage.getPasswordForm().then(function (value) {
            expect(cred.password).toEqual(value);
        });
    });

    it('should submit the form', function() {
        loginPage.submitForm();
        loginPage.hasError().then(function (bool) {
            expect(bool).toBe(false);
        });
    });

    it('should redirect to the inbox page', function() {
        expect(browser.getCurrentUrl()).toEqual(loginPage.inboxURL);
    });

    it('should create a cookie', function() {
        loginPage.getCookies().then(function (cookies) {
              expect(cookies.value).toMatch(/connected/);
        });
    });

});

};