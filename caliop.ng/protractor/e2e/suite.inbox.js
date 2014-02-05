describe('The inbox suite', function() {
    'use strict';

    // reset json
    var execSync = require('exec-sync');
    execSync('git checkout ../caliop/caliop/views/api/json/*');

    it('should test the inbox view.', function() {
        require('./test.inbox.js').TestInbox();
    });
});
