module.exports = function() {
  return {
    loginURL: 'http://localhost:6543/#/login',
    inboxURL: 'http://localhost:6543/#/inbox',
    goLogin: function () {
      browser.get('/#/');
    },
    fillingAllForm: function (credentials) {
      element(by.model('credentials.login')).sendKeys(credentials.login);
      element(by.model('credentials.password')).sendKeys(credentials.password);
    },
    getLoginForm: function () {
      return element(by.model('credentials.login')).getAttribute('value');
    },
    getPasswordForm: function () {
      return element(by.model('credentials.password')).getAttribute('value');
    },
    submitForm: function () {
      element(by.id('submit')).click();
    },
    hasError: function () {
        return browser.isElementPresent(by.binding('messages.error'));
    },
    getCookies: function () {
        return browser.manage().getCookie('session');
    }
  };
};