var TestInbox = function() {
    describe('The inbox view', function() {
        'use strict';

        var ptor = protractor.getInstance();

        beforeEach(function() {
            require('./page.authentification').Login()
                .open()
                .login('Alexis', 'Mineaud');
        });

        afterEach(function() {
            require('./page.authentification').Logout()
                .open();
        });

        it('should be automatically opened if logged in.', function() {
            expect(browser.getCurrentUrl()).toEqual('http://localhost:6543/#/inbox');
        });
    });
};

exports.TestInbox = TestInbox;
