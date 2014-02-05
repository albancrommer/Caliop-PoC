describe('Login and redirect to the inbox', function() {
  it('should complete the inputs', function() {
    browser.get('/#/');

    element(by.model('credentials.login')).sendKeys('Alexis');
    element(by.model('credentials.password')).sendKeys('Mineaud');
  });

  it('should submit the form', function() {
    element(by.id('submit')).click();
  });

  it('should redirect to the inbox page', function() {
    expect(browser.getCurrentUrl()).toEqual('http://localhost:6543/#/inbox');

    // Make sure the cookie is set.
    browser.manage().getCookie('session').then(function(cookie) {
        expect(cookie.value).toMatch(/connected/);
    });
  });

  it('should create a cookie', function() {
    browser.manage().getCookie('session').then(function(cookie) {
        expect(cookie.value).toMatch(/connected/);
    });
  });
});
