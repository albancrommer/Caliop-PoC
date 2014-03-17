#!/bin/bash

CASSANDRA_DIR="/home/mric/Downloads/apache-cassandra-2.0.5"

$CASSANDRA_DIR/bin/cqlsh << EOT

use cqlengine;
truncate user;
truncate counter;
truncate message;
truncate message_part;
truncate message_lookup;
truncate thread;
truncate contact;
truncate contact_lookup;

EOT
