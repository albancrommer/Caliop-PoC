describe('The login suite', function() {
    'use strict';

    // reset json
    var execSync = require('exec-sync');
    execSync('git checkout ../caliop/caliop/views/api/json/*');

    it('should test the login view.', function() {
        require('./test.login.js').TestLogin();
    });
});
