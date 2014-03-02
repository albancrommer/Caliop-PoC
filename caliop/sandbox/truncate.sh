#!/bin/bash

CASSANDRA_DIR="/Users/mric/Desktop/caliop/ext/apache-cassandra-2.0.4"

$CASSANDRA_DIR/bin/cqlsh << EOT

use cqlengine;
truncate user;
truncate counter;
truncate message;
truncate thread;
truncate thread_lookup;
truncate contact;
truncate contact_lookup;

EOT
