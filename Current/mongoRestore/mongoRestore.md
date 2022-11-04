# Tutorial to make context broker independent of internet connection

Main Idea: Once you have a internet connection you setup your context broker as you like. When everything is up and running, all the necessary files for the context broker are stored in the mongo-database. So you do a dump of the mongo-database. When you want to run the context broker without an internet connection you simply restore the mongo-database while you start it.

## Dump the mongo-database

Setup your context broker with an active internet connection and make sure erverything is running properly. Then execute this command in a terminal in the working directory of your context broker:

```sh
docker exec db-mongo sh -c 'mongodump --archive' > backups/db.dump
```

Now you should have a folder `backups` with a file `db.dump` inside it.

## Create a script to restore the mongo-database

Create a script. For example `mongoRestore/mongoRestore.sh`. Add the following code:

```sh
#!/bin/sh
exec mongorestore --archive < backups/db.dump
```


## Changes in docker-compose file

Add to mongo-db:

```yml
environment:
      - MONGO_INITDB_DATABASE=/docker-entrypoint-initdb.d/mongoRestore.sh
volumes:
      - ../backups/db.dump:/backups/db.dump
      - ../mongoRestore/mongoRestore.sh:/docker-entrypoint-initdb.d/mongoRestore.sh
```

This code makes sure that the database is restored when it is started.

To make this code work you should have the following two files at the relative path to the docker-compose file: `../backups/db.dump` and `../mongoRestore/mongoRestore.sh`.
If you have other paths, change it accordingly in the volumes-section of the mongo-db in the docker-compose file.