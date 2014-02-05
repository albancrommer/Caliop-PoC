describe('Login and redirect to the inbox', function() {
    'use strict';

    var execSync = require('exec-sync');
    execSync('git checkout ../caliop/caliop/views/api/json/*');

    it('should complete the inputs', function() {
      browser.get('/#/');
      var login = 'Alexis';
      var password = 'Mineaud';
      element(by.model('credentials.login')).sendKeys(login);
      element(by.model('credentials.password')).sendKeys(password);

      element(by.model('credentials.password')).getAttribute('value').then(function (data) {
        expect(data).toEqual(password);
      });
      element(by.model('credentials.login')).getAttribute('value').then(function (data) {
        expect(data).toEqual(login);
      });
    });

  it('should submit the form', function() {
    element(by.id('submit')).click();
    expect(browser.isElementPresent(by.binding('messages.error'))).toBe(false);
  });

  it('should redirect to the inbox page', function() {
    expect(browser.getCurrentUrl()).toEqual('http://localhost:6543/#/inbox');
  });

  it('should create a cookie', function() {
    browser.manage().getCookie('session').then(function(cookie) {
        expect(cookie.value).toMatch(/connected/);
    });
  });
});
