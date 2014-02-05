var TestLogin = function() {
    describe('The login view', function() {
        'use strict';

        var loginPage = require('./page.authentification').Login();

        it('should open the correct login page', function() {
            loginPage.open();
            expect(browser.getCurrentUrl()).toEqual('http://localhost:6543/#/login');
        });

        it('should display errors status', function() {
            loginPage.login('Bad', 'Bad');

            loginPage.getError().then(function(bool) {
                expect(bool).toBe(true);
            });

            loginPage.login('Alexis', 'Mineaud');
        });

        it('should redirect to the inbox page if succeeded', function() {
            expect(browser.getCurrentUrl()).toEqual('http://localhost:6543/#/inbox');
        });

        it('should create a cookie if succeeded', function() {
            loginPage.getCookie().then(function (cookie) {
                expect(cookie.value).toMatch(/connected/);
            });
        });
    });
};

exports.TestLogin = TestLogin;
