Two instances on localhost managed with pglift invoked with different site
settings in order to emulate different hosts. The password file is common, as
well as the pgbackrest repository path (emulating a shared storage for
backup). Both instances use the same stanza.

Site settings and configuration

  $ PASSWORDS=$TMPDIR/passwords.json
  $ cat > $PASSWORDS << 'EOF'
  > {
  >   "postgres": "s3per",
  >   "replication": "r3pl",
  >   "pgbackrest": "b@ckUp"
  > }
  > EOF

  $ PREFIX1=$TMPDIR/1
  $ RUN_PREFIX1=$PREFIX1/run
  $ cat > $TMPDIR/config1.json <<EOF
  > {
  >   "cli": {
  >     "log_format": "%(levelname)-4s %(message)s"
  >   },
  >   "prefix": "$PREFIX1",
  >   "run_prefix": "$RUN_PREFIX1",
  >   "postgresql": {
  >     "auth": {
  >       "local": "scram-sha-256",
  >       "password_command": [
  >         "jq",
  >         "-r",
  >         ".{role}",
  >         "$PASSWORDS"
  >       ]
  >     },
  >     "backuprole": {
  >       "name": "pgbackrest"
  >     }
  >   },
  >   "pgbackrest": {
  >     "repository": {
  >       "path": "$TMPDIR/backups"
  >     }
  >   }
  > }
  > EOF
  $ SETTINGS1="@$TMPDIR/config1.json"

  $ PREFIX2=$TMPDIR/2
  $ RUN_PREFIX2=$PREFIX2/run
  $ cat > $TMPDIR/config2.json <<EOF
  > {
  >   "cli": {
  >     "log_format": "%(levelname)-4s %(message)s"
  >   },
  >   "prefix": "$PREFIX2",
  >   "run_prefix": "$RUN_PREFIX2",
  >   "postgresql": {
  >     "auth": {
  >       "local": "scram-sha-256",
  >       "password_command": [
  >         "jq",
  >         "-r",
  >         ".{role}",
  >         "$PASSWORDS"
  >       ]
  >     },
  >     "backuprole": {
  >       "name": "pgbackrest"
  >     }
  >   },
  >   "pgbackrest": {
  >     "repository": {
  >       "path": "$TMPDIR/backups"
  >     }
  >   }
  > }
  > EOF

  $ SETTINGS2="@$TMPDIR/config2.json"

  $ alias pglift1="env SETTINGS=$SETTINGS1 pglift --log-level=INFO --non-interactive"
  $ alias pglift2="env SETTINGS=$SETTINGS2 pglift --log-level=INFO --non-interactive"

  $ pglift1 site-configure install
  INFO installing base pgbackrest configuration
  INFO creating pgbackrest include directory
  INFO creating pgbackrest repository path
  INFO creating common pgbackrest directories
  INFO creating postgresql log directory
  $ pglift2 site-configure install
  INFO installing base pgbackrest configuration
  INFO creating pgbackrest include directory
  INFO creating pgbackrest repository path
  INFO creating common pgbackrest directories
  INFO creating postgresql log directory

Define ports

  $ PG1PORT=$(port-for pg1)
  $ PG2PORT=$(port-for pg2)

(Cleanup steps)

  $ trap "
  >     pglift1 instance drop; \
  >     pglift2 instance drop; \
  >     pglift1 site-configure uninstall; \
  >     pglift2 site-configure uninstall; \
  >     port-for -u pg1; port-for -u pg2" \
  >     EXIT

Create a primary and a standby instances

  $ pglift1 instance create main --port=$PG1PORT --pgbackrest-stanza=app \
  >   --surole-password=s3per --pgbackrest-password=b@ckUp \
  >   --replrole-password=r3pl
  INFO initializing PostgreSQL
  INFO configuring PostgreSQL authentication
  INFO configuring PostgreSQL
  INFO starting PostgreSQL 1\d-main (re)
  INFO creating role 'replication'
  INFO creating role 'pgbackrest'
  INFO altering role 'pgbackrest'
  INFO setting up pgBackRest
  INFO creating pgBackRest stanza app

  $ pglift2 instance create main \
  >   --standby-for="host=$RUN_PREFIX1/postgresql port=$PG1PORT user=replication" \
  >   --standby-password=r3pl \
  >   --port=$PG2PORT --pgbackrest-stanza=app \
  >   --surole-password=s3per --pgbackrest-password=b@ckUp
  INFO initializing PostgreSQL
  INFO configuring PostgreSQL authentication
  INFO configuring PostgreSQL
  INFO starting PostgreSQL 1\d-main (re)
  INFO setting up pgBackRest
  INFO creating pgBackRest stanza app
  WARNING not checking pgBackRest configuration on a standby

Add some data to the primary, check replication

  $ pglift1 database run -d postgres \
  >   "CREATE TABLE t AS (SELECT generate_series(1, 3) i)"
  INFO running "CREATE TABLE t AS \(SELECT generate_series\(1, 3\) i\)" on postgres database of 1\d\/main (re)
  INFO SELECT 3
  $ pglift2 database run -o json -d postgres "SELECT i FROM t"
  INFO running "SELECT i FROM t" on postgres database of 1\d\/main (re)
  INFO SELECT 3
  {
    "postgres": [
      {
        "i": 1
      },
      {
        "i": 2
      },
      {
        "i": 3
      }
    ]
  }
  $ pglift2 instance get -o json \
  >   | jq '.standby.replication_lag, .standby.wal_sender_state, .state, .pgbackrest'
  0
  "streaming"
  "started"
  {
    "stanza": "app"
  }

Backup the primary

  $ pglift1 instance backup
  INFO backing up instance 1\d\/main with pgBackRest (re)
  $ pglift1 instance backups -o json | jq '.[] | .type, .databases'
  "full"
  [
    "postgres"
  ]

Attempt to backup from the standby

  $ pglift2 instance backup 2>&1 | grep ERROR
  ERROR: [056]: unable to find primary cluster - cannot proceed

Switchover

  $ pglift1 instance stop
  INFO stopping PostgreSQL 1\d-main (re)
  $ pglift2 instance promote
  INFO promoting PostgreSQL instance
  INFO checking pgBackRest configuration

  $ pglift2 database run -d postgres \
  >   "INSERT INTO t VALUES (42)"
  INFO running "INSERT INTO t VALUES \(42\)" on postgres database of 1\d\/main (re)
  INFO INSERT 0 1
  $ pglift2 database run -d postgres "SELECT pg_switch_wal()" > /dev/null
  INFO running "SELECT pg_switch_wal\(\)" on postgres database of 1\d\/main (re)
  INFO SELECT 1

  $ pglift2 instance get -o json \
  >   | jq '.standby.replication_lag, .standby.wal_sender_state, .state, .pgbackrest'
  null
  null
  "started"
  {
    "stanza": "app"
  }

Check backup on the new primary (the one from the old primary is there, and we
can make a new one)

  $ pglift2 instance backups -o json | jq '.[] | .type, .databases'
  "full"
  [
    "postgres"
  ]

  $ pglift2 instance backup
  INFO backing up instance 1\d\/main with pgBackRest (re)
  $ pglift2 instance backups -o json | jq '.[] | .type, .databases'
  "incr"
  [
    "postgres"
  ]
  "full"
  [
    "postgres"
  ]

Rebuild the old primary as a standby (using the pgBackRest backup)

  $ pglift1 instance drop
  INFO dropping instance 1\d\/main (re)
  WARNING instance 1\d\/main is already stopped (re)
  INFO deconfiguring pgBackRest
  INFO deleting PostgreSQL cluster
  $ pglift1 instance create main \
  >   --standby-for="host=$RUN_PREFIX2/postgresql port=$PG2PORT user=replication" \
  >   --standby-password=r3pl \
  >   --port=$PG1PORT --pgbackrest-stanza=app \
  >   --surole-password=s3per --pgbackrest-password=b@ckUp
  INFO initializing PostgreSQL
  INFO restoring from a pgBackRest backup
  INFO configuring PostgreSQL authentication
  INFO configuring PostgreSQL
  INFO starting PostgreSQL 1\d-main (re)
  INFO setting up pgBackRest
  INFO creating pgBackRest stanza app
  WARNING not checking pgBackRest configuration on a standby
  $ pglift1 instance get -o json \
  >   | jq '.standby.replication_lag, .standby.wal_sender_state, .state, .pgbackrest'
  0
  "streaming"
  "started"
  {
    "stanza": "app"
  }
  $ pglift1 instance backups -o json | jq '.[] | .type, .databases'
  "incr"
  [
    "postgres"
  ]
  "full"
  [
    "postgres"
  ]

(Cleanup)

  INFO dropping instance 1\d\/main (re)
  INFO stopping PostgreSQL 1\d-main (re)
  INFO deconfiguring pgBackRest
  INFO deleting PostgreSQL cluster
  INFO dropping instance 1\d\/main (re)
  INFO stopping PostgreSQL 1\d-main (re)
  INFO deconfiguring pgBackRest
  INFO deleting PostgreSQL cluster
  INFO deleting pgbackrest include directory
  INFO uninstalling base pgbackrest configuration
  INFO deleting common pgbackrest directories
  INFO deleting postgresql log directory
  INFO deleting pgbackrest include directory
  INFO uninstalling base pgbackrest configuration
  INFO deleting common pgbackrest directories
  INFO deleting postgresql log directory (no-eol)
