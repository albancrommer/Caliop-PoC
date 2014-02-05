exports.config = {
    seleniumAddress: 'http://localhost:4444/wd/hub',

    specs: [
        'e2e/*.test.js'
    ],

    capabilities: {
        'browserName': 'chrome'
    },

    onPrepare: function() {
        // The require statement must be down here, since jasmine-reporters
        // needs jasmine to be in the global and protractor does not guarantee
        // this until inside the onPrepare function.
        require('jasmine-reporters');

        jasmine.getEnv().addReporter(
            new jasmine.JUnitXmlReporter('protractor/xmlreports/', true, true));
    },

    baseUrl: 'http://localhost:6543'
};
