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

## Installation of the Pyramid app

```shell
# Create a virtualenv
$ virtualenv2 ~/.virtualenvs/caliop

# Activate it
$ source ~/.virtualenvs/caliop/bin/activate

# Install dependancies
$ cd ~/workspace/Caliop-PoC/caliop
$ python setup.py develop

# Start the app
$ pserve development.ini

# Start a modern browser and go to http://localhost:6543
# Enjoy.
```
