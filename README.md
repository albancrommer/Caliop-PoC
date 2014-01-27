Caliop-PoC
==========

> A sample pre-alpha interface for Caliop.

## Architecture

The Caliop PoC consists of two projects:
  - a Pyramid app
  - an Angular app.

The Pyramid app provides a REST API and serves the Angular app.

## Prepare your environment

```shell
# Get the code
$ cd ~/workspace
$ git clone https://github.com/Gandi/Caliop-PoC.git
```

## Installation of the Angular app

```shell
$ cd ~/workspace/Caliop-PoC/caliop.ng

# Install dependancies

# This is not mandatory, if you have installed grunt-cli karma bower globally
# inspired by python virtual env to add node_modules bin in path
# use ndeactivate for deactivate it
$ source nactictivate

$ npm install
$ bower install

# Build the app
$ grunt build
```

### You don't have chrome:

if you want to use chromium,
```shell
export CHROME_BIN=/usr/bin/chromium
```

or if you want to use firefox instead of chrome during grunt build,
Change the karma  continuous browser in the karma configuration section
from Grunfile.fs


### Known issues:

if you have problem with the ui-router:
```shell
Chrome 32.0.1700 (Linux) DashboardCtrl isCurrentUrl should pass a dummy test FAILED
        Error: [$injector:modulerr] Failed to instantiate module caliop due to:
        Error: [$injector:modulerr] Failed to instantiate module ui.router due to:
        Error: [$injector:nomod] Module 'ui.router' is not available! You either misspelled the module name or forgot to load it. If registering a module ensure that you specify the dependencie
s as the second argument.
```

You can execute:
```shell
 cd vendor/
 git clone git@github.com:angular-ui/ui-router.git
 rm -rf angular-ui-router
 mv ui-router angular-ui-router
 cd ..
```

## Installation of the Pyramid app

```shell
# Create a virtualenv
$ virtualenv2 ~/.virtualenvs/caliop

# Activate it
$ source ~/.virtualenvs/caliop/bin/activate

# Install dependancies
$ cd ~/workspace/Caliop-PoC/caliop
$ python setup.py develop

# Copy (and adapt if needed) your ini file
$ cp development.ini.sample development.ini

# Start the app
$ pserve development.ini

# Start a modern browser and go to http://localhost:6543
# Enjoy.
```
