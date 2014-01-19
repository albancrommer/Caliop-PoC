#!/bin/sh

npm install && \
bower install && \
grunt build && \
grunt watch
