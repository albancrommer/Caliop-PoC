var Login = function() {
    return {
        selector: {
            model: {
                login: 'credentials.login',
                password: 'credentials.password'
            },
            binding: {
                messageError: 'messages.error'
            },
            id: {
                submit: 'submit'
            }
        },
        url: {
            login: '/#/login'
        },

        open: function() {
            browser.get(this.url.login);
            return this;
        },

        login: function(login, password) {
            element(by.model(this.selector.model.login)).clear();
            element(by.model(this.selector.model.login)).sendKeys(login);

            element(by.model(this.selector.model.password)).clear();
            element(by.model(this.selector.model.password)).sendKeys(password);

            element(by.id(this.selector.id.submit)).click();
            return this;
        },

        getError: function() {
            return browser.isElementPresent(
                by.binding(this.selector.binding.messageError));
        },

        getCookie: function() {
            return browser.manage().getCookie('session');
        }
    };
};

var Logout = function() {
    return {
        selector: {
        },
        url: {
            logout: '/#/logout'
        },

        open: function() {
            browser.get(this.url.logout);
        }
    };
};

exports.Login = Login;
exports.Logout = Logout;
