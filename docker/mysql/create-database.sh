#!/usr/bin/env bash

mysql --user=root --password="$MYSQL_ROOT_PASSWORD" <<-EOSQL
    CREATE DATABASE IF NOT EXISTS portaldatransparencia;
    GRANT ALL PRIVILEGES ON \`portaldatransparencia%\`.* TO '$MYSQL_USER'@'%';  

    FLUSH PRIVILEGES;

EOSQL
