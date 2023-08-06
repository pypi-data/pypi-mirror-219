Tests for --help options of all commands

  $ pglift --help
  Usage: pglift [OPTIONS] COMMAND [ARGS]...
  
    Deploy production-ready instances of PostgreSQL
  
  Options:
    -L, --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                    Set log threshold (default to INFO when
                                    logging to stderr or WARNING when logging to
                                    a file).
    -l, --log-file LOGFILE          Write logs to LOGFILE, instead of stderr.
    --interactive / --non-interactive
                                    Interactively prompt for confirmation when
                                    needed (the default), or automatically pick
                                    the default option for all choices.
    --version                       Show program version.
    --completion [bash|fish|zsh]    Output completion for specified shell and
                                    exit.
    --help                          Show this message and exit.
  
  Commands:
    instance  Manage instances.
    pgconf    Manage configuration of a PostgreSQL instance.
    role      Manage roles.
    database  Manage databases.


Site settings

  $ PATRONI=$(which patroni)
  $ cat > $TMPDIR/config.json <<EOF
  > {
  >   "cli": {
  >     "log_format": "%(levelname)-4s %(message)s"
  >   },
  >   "prefix": "$TMPDIR",
  >   "run_prefix": "$TMPDIR/run",
  >   "patroni": {
  >     "execpath": "$PATRONI"
  >   },
  >   "pgbackrest": {
  >     "repository": {
  >       "path": "$TMPDIR/backups"
  >     }
  >   },
  >   "postgresql": {
  >     "auth": {
  >       "passfile": null
  >     }
  >   },
  >   "powa": {},
  >   "prometheus": {
  >     "execpath": "/usr/bin/prometheus-postgres-exporter"
  >   }
  > }
  > EOF
  $ export SETTINGS="@$TMPDIR/config.json"
  $ pglift site-settings --no-defaults -o json \
  >   | jq '.pgbackrest, .prometheus, .prefix, .run_prefix'
  {
    "configpath": "$TMPDIR/etc/pgbackrest",
    "repository": {
      "path": "$TMPDIR/backups"
    },
    "logpath": "$TMPDIR/log/pgbackrest",
    "spoolpath": "$TMPDIR/srv/pgbackrest/spool",
    "lockpath": "$TMPDIR/run/pgbackrest/lock"
  }
  {
    "execpath": "/usr/bin/prometheus-postgres-exporter",
    "configpath": "$TMPDIR/etc/prometheus/postgres_exporter-{name}.conf",
    "queriespath": "$TMPDIR/etc/prometheus/postgres_exporter_queries-{name}.yaml",
    "pid_file": "$TMPDIR/run/prometheus/{name}.pid"
  }
  "$TMPDIR"
  "$TMPDIR/run"

Site configuration

  $ pglift --log-level=INFO site-configure install
  INFO installing base pgbackrest configuration
  INFO creating pgbackrest include directory
  INFO creating pgbackrest repository path
  INFO creating common pgbackrest directories
  INFO creating postgresql log directory
  $ trap "pglift --non-interactive --log-level=INFO site-configure uninstall" EXIT

Instance commands

  $ pglift instance --help
  Usage: pglift instance [OPTIONS] COMMAND [ARGS]...
  
    Manage instances.
  
  Options:
    --schema  Print the JSON schema of instance model and exit.
    --help    Show this message and exit.
  
  Commands:
    alter       Alter PostgreSQL INSTANCE
    backup      Back up PostgreSQL INSTANCE
    backups     List available backups for INSTANCE
    create      Initialize a PostgreSQL instance
    drop        Drop PostgreSQL INSTANCE
    env         Output environment variables suitable to handle to...
    exec        Execute command in the libpq environment for PostgreSQL...
    get         Get the description of PostgreSQL INSTANCE.
    list        List the available instances
    logs        Output PostgreSQL logs of INSTANCE.
    privileges  List privileges on INSTANCE's databases.
    promote     Promote standby PostgreSQL INSTANCE
    reload      Reload PostgreSQL INSTANCE
    restart     Restart PostgreSQL INSTANCE
    restore     Restore PostgreSQL INSTANCE
    start       Start PostgreSQL INSTANCE
    status      Check the status of instance and all satellite components.
    stop        Stop PostgreSQL INSTANCE
    upgrade     Upgrade INSTANCE using pg_upgrade
  $ pglift instance alter --help
  Usage: pglift instance alter [OPTIONS] [INSTANCE]
  
    Alter PostgreSQL INSTANCE
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
    Required if there is more than one instance on system.
  
  Options:
    --port PORT                     TCP port the postgresql instance will be
                                    listening to. If unspecified, default to
                                    5432 unless a 'port' setting is found in
                                    'settings'.
    --data-checksums / --no-data-checksums
                                    Enable or disable data checksums. If
                                    unspecified, fall back to site settings
                                    choice.
    --state [started|stopped]       Runtime state.
    --powa-password TEXT            Password of PostgreSQL role for PoWA.
    --prometheus-port PORT          TCP port for the web interface and telemetry
                                    of Prometheus.
    --prometheus-password TEXT      Password of PostgreSQL role for Prometheus
                                    postgres_exporter.
    --patroni-restapi-connect-address CONNECT_ADDRESS
                                    IP address (or hostname) and port, to access
                                    the Patroni's REST API.
    --patroni-restapi-listen LISTEN
                                    IP address (or hostname) and port that
                                    Patroni will listen to for the REST API.
                                    Defaults to connect_address if not provided.
    --patroni-postgresql-connect-host POSTGRESQL_CONNECT_HOST
                                    Host or IP address through which PostgreSQL
                                    is externally accessible.
    --help                          Show this message and exit.
  $ pglift instance create --help
  Usage: pglift instance create [OPTIONS] NAME
  
    Initialize a PostgreSQL instance
  
  Options:
    --version [15|14|13|12|11]      PostgreSQL version.
    --port PORT                     TCP port the postgresql instance will be
                                    listening to. If unspecified, default to
                                    5432 unless a 'port' setting is found in
                                    'settings'.
    --surole-password TEXT          Super-user role password.
    --replrole-password TEXT        Replication role password.
    --data-checksums / --no-data-checksums
                                    Enable or disable data checksums. If
                                    unspecified, fall back to site settings
                                    choice.
    --locale LOCALE                 Default locale.
    --encoding ENCODING             Character encoding of the PostgreSQL
                                    instance.
    --auth-local [trust|reject|md5|password|scram-sha-256|gss|sspi|ident|peer|pam|ldap|radius|cert]
                                    Authentication method for local-socket
                                    connections.
    --auth-host [trust|reject|md5|password|scram-sha-256|gss|sspi|ident|pam|ldap|radius|cert]
                                    Authentication method for local TCP/IP
                                    connections.
    --standby-for FOR               DSN of primary for streaming replication.
    --standby-password TEXT         Password for the replication user.
    --standby-slot SLOT             Replication slot name. Must exist on
                                    primary.
    --state [started|stopped]       Runtime state.
    --powa-password TEXT            Password of PostgreSQL role for PoWA.
    --prometheus-port PORT          TCP port for the web interface and telemetry
                                    of Prometheus.
    --prometheus-password TEXT      Password of PostgreSQL role for Prometheus
                                    postgres_exporter.
    --patroni-cluster CLUSTER       Name (scope) of the Patroni cluster.
    --patroni-node NODE             Name of the node (usually the host name).
    --patroni-restapi-connect-address CONNECT_ADDRESS
                                    IP address (or hostname) and port, to access
                                    the Patroni's REST API.
    --patroni-restapi-listen LISTEN
                                    IP address (or hostname) and port that
                                    Patroni will listen to for the REST API.
                                    Defaults to connect_address if not provided.
    --patroni-postgresql-connect-host POSTGRESQL_CONNECT_HOST
                                    Host or IP address through which PostgreSQL
                                    is externally accessible.
    --pgbackrest-stanza STANZA      Name of pgBackRest stanza. Something
                                    describing the actual function of the
                                    instance, such as 'app'.  [required]
    --pgbackrest-password TEXT      Password of PostgreSQL role for pgBackRest.
    --drop-on-error / --no-drop-on-error
                                    On error, drop partially initialized
                                    instance by possibly rolling back operations
                                    (true by default).
    --help                          Show this message and exit.
  $ pglift instance drop --help
  Usage: pglift instance drop [OPTIONS] [INSTANCE]...
  
    Drop PostgreSQL INSTANCE
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
    Required if there is more than one instance on system.
  
  Options:
    --help  Show this message and exit.
  $ pglift instance env --help
  Usage: pglift instance env [OPTIONS] [INSTANCE]
  
    Output environment variables suitable to handle to PostgreSQL INSTANCE.
  
    This can be injected in shell using:
  
        export $(pglift instance env myinstance)
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
    Required if there is more than one instance on system.
  
  Options:
    -o, --output-format [json]  Specify the output format.
    --help                      Show this message and exit.
  $ pglift instance exec --help
  Usage: pglift instance exec [OPTIONS] INSTANCE COMMAND...
  
    Execute command in the libpq environment for PostgreSQL INSTANCE.
  
    COMMAND parts may need to be prefixed with -- to separate them from options
    when confusion arises.
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
  
  Options:
    --help  Show this message and exit.
  $ pglift instance list --help
  Usage: pglift instance list [OPTIONS]
  
    List the available instances
  
  Options:
    --version [15|14|13|12|11]  Only list instances of specified version.
    -o, --output-format [json]  Specify the output format.
    --help                      Show this message and exit.
  $ pglift instance logs --help
  Usage: pglift instance logs [OPTIONS] [INSTANCE]
  
    Output PostgreSQL logs of INSTANCE.
  
    This assumes that the PostgreSQL instance is configured to use file-based
    logging (i.e. log_destination amongst 'stderr' or 'csvlog').
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
    Required if there is more than one instance on system.
  
  Options:
    -f, --follow / --no-follow  Follow log output.
    --help                      Show this message and exit.
  $ pglift instance get --help
  Usage: pglift instance get [OPTIONS] [INSTANCE]
  
    Get the description of PostgreSQL INSTANCE.
  
    Unless --output-format is specified, 'settings' and 'state' fields are not
    shown as well as 'standby' information if INSTANCE is not a standby.
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
    Required if there is more than one instance on system.
  
  Options:
    -o, --output-format [json]  Specify the output format.
    --help                      Show this message and exit.
  $ pglift instance privileges --help
  Usage: pglift instance privileges [OPTIONS] [INSTANCE]
  
    List privileges on INSTANCE's databases.
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
    Required if there is more than one instance on system.
  
  Options:
    -d, --database TEXT         Database to inspect. When not provided, all
                                databases are inspected.
    -r, --role TEXT             Role to inspect
    --default                   Display default privileges
    -o, --output-format [json]  Specify the output format.
    --help                      Show this message and exit.
  $ pglift instance promote --help
  Usage: pglift instance promote [OPTIONS] [INSTANCE]
  
    Promote standby PostgreSQL INSTANCE
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
    Required if there is more than one instance on system.
  
  Options:
    --help  Show this message and exit.
  $ pglift instance reload --help
  Usage: pglift instance reload [OPTIONS] [INSTANCE]...
  
    Reload PostgreSQL INSTANCE
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
    Required if there is more than one instance on system.
  
  Options:
    --all   Reload all instances.
    --help  Show this message and exit.
  $ pglift instance restart --help
  Usage: pglift instance restart [OPTIONS] [INSTANCE]...
  
    Restart PostgreSQL INSTANCE
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
    Required if there is more than one instance on system.
  
  Options:
    --all   Restart all instances.
    --help  Show this message and exit.
  $ pglift instance start --help
  Usage: pglift instance start [OPTIONS] [INSTANCE]...
  
    Start PostgreSQL INSTANCE
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
    Required if there is more than one instance on system.
  
  Options:
    --foreground  Start the program in foreground.
    --all         Start all instances.
    --help        Show this message and exit.
  $ pglift instance status --help
  Usage: pglift instance status [OPTIONS] [INSTANCE]
  
    Check the status of instance and all satellite components.
  
    Output the status string value ('running', 'not running') for each
    component. If not all services are running, the command exit code will be 3.
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
    Required if there is more than one instance on system.
  
  Options:
    --help  Show this message and exit.
  $ pglift instance stop --help
  Usage: pglift instance stop [OPTIONS] [INSTANCE]...
  
    Stop PostgreSQL INSTANCE
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
    Required if there is more than one instance on system.
  
  Options:
    --all   Stop all instances.
    --help  Show this message and exit.
  $ pglift instance upgrade --help
  Usage: pglift instance upgrade [OPTIONS] [INSTANCE]
  
    Upgrade INSTANCE using pg_upgrade
  
    INSTANCE identifies target instance as <version>/<name> where the <version>/
    prefix may be omitted if there is only one instance matching <name>.
    Required if there is more than one instance on system.
  
  Options:
    --version [15|14|13|12|11]  PostgreSQL version of the new instance (default
                                to site-configured value).
    --name TEXT                 Name of the new instance (default to old
                                instance name).
    --port INTEGER              Port of the new instance.
    --jobs INTEGER              Number of simultaneous processes or threads to
                                use (from pg_upgrade).
    --help                      Show this message and exit.

Role commands

  $ pglift role --help
  Usage: pglift role [OPTIONS] COMMAND [ARGS]...
  
    Manage roles.
  
  Options:
    -i, --instance <version>/<name>
                                    Instance identifier; the <version>/ prefix
                                    may be omitted if there's only one instance
                                    matching <name>. Required if there is more
                                    than one instance on system.
    --schema                        Print the JSON schema of role model and
                                    exit.
    --help                          Show this message and exit.
  
  Commands:
    alter       Alter a role in a PostgreSQL instance
    create      Create a role in a PostgreSQL instance
    drop        Drop a role
    get         Get the description of a role
    list        List roles in instance
    privileges  List privileges of a role.
  $ pglift role alter --help
  Usage: pglift role alter [OPTIONS] ROLNAME
  
    Alter a role in a PostgreSQL instance
  
  Options:
    --password TEXT                 Role password.
    --encrypted-password TEXT       Role password, already encrypted.
    --inherit / --no-inherit        Let the role inherit the privileges of the
                                    roles it is a member of.
    --login / --no-login            Allow the role to log in.
    --superuser / --no-superuser    Whether the role is a superuser.
    --createdb / --no-createdb      Whether role can create new databases.
    --createrole / --no-createrole  Whether role can create new roles.
    --replication / --no-replication
                                    Whether the role is a replication role.
    --connection-limit CONNECTION_LIMIT
                                    How many concurrent connections the role can
                                    make.
    --validity VALIDITY             Date and time after which the role's
                                    password is no longer valid.
    --help                          Show this message and exit.
  $ pglift role create --help
  Usage: pglift role create [OPTIONS] NAME
  
    Create a role in a PostgreSQL instance
  
  Options:
    --password TEXT                 Role password.
    --encrypted-password TEXT       Role password, already encrypted.
    --inherit / --no-inherit        Let the role inherit the privileges of the
                                    roles it is a member of.
    --login / --no-login            Allow the role to log in.
    --superuser / --no-superuser    Whether the role is a superuser.
    --createdb / --no-createdb      Whether role can create new databases.
    --createrole / --no-createrole  Whether role can create new roles.
    --replication / --no-replication
                                    Whether the role is a replication role.
    --connection-limit CONNECTION_LIMIT
                                    How many concurrent connections the role can
                                    make.
    --validity VALIDITY             Date and time after which the role's
                                    password is no longer valid.
    --in-role IN_ROLE               List of roles to which the new role will be
                                    added as a new member.
    --help                          Show this message and exit.
  $ pglift role drop --help
  Usage: pglift role drop [OPTIONS] NAME
  
    Drop a role
  
  Options:
    --drop-owned / --no-drop-owned  Drop all PostgreSQL's objects owned by the
                                    role being dropped.
    --reassign-owned REASSIGN_OWNED
                                    Reassign all PostgreSQL's objects owned by
                                    the role being dropped to the specified role
                                    name.
    --help                          Show this message and exit.
  $ pglift role get --help
  Usage: pglift role get [OPTIONS] NAME
  
    Get the description of a role
  
  Options:
    -o, --output-format [json]  Specify the output format.
    --help                      Show this message and exit.
  $ pglift role list --help
  Usage: pglift role list [OPTIONS]
  
    List roles in instance
  
  Options:
    -o, --output-format [json]  Specify the output format.
    --help                      Show this message and exit.
  $ pglift role privileges --help
  Usage: pglift role privileges [OPTIONS] NAME
  
    List privileges of a role.
  
  Options:
    -d, --database TEXT         Database to inspect
    --default                   Display default privileges
    -o, --output-format [json]  Specify the output format.
    --help                      Show this message and exit.

Database commands

  $ pglift database --help
  Usage: pglift database [OPTIONS] COMMAND [ARGS]...
  
    Manage databases.
  
  Options:
    -i, --instance <version>/<name>
                                    Instance identifier; the <version>/ prefix
                                    may be omitted if there's only one instance
                                    matching <name>. Required if there is more
                                    than one instance on system.
    --schema                        Print the JSON schema of database model and
                                    exit.
    --help                          Show this message and exit.
  
  Commands:
    alter       Alter a database in a PostgreSQL instance
    create      Create a database in a PostgreSQL instance
    drop        Drop a database
    dump        Dump a database
    dumps       List the database dumps
    get         Get the description of a database
    list        List databases (all or specified ones)
    privileges  List privileges on a database.
    restore     Restore a database dump
    run         Run given command on databases of a PostgreSQL instance
  $ pglift database alter --help
  Usage: pglift database alter [OPTIONS] DBNAME
  
    Alter a database in a PostgreSQL instance
  
  Options:
    --owner OWNER  The role name of the user who will own the database.
    --help         Show this message and exit.
  $ pglift database create --help
  Usage: pglift database create [OPTIONS] NAME
  
    Create a database in a PostgreSQL instance
  
  Options:
    --owner OWNER            The role name of the user who will own the
                             database.
    --schema SCHEMA          List of schemas to create in the database.
    --extension EXTENSION    List of extensions to create in the database.
    --clone-from CLONE_FROM  Data source name of the database to clone into this
                             one, specified as a libpq connection URI.
    --help                   Show this message and exit.
  $ pglift database drop --help
  Usage: pglift database drop [OPTIONS] NAME
  
    Drop a database
  
  Options:
    --force / --no-force  Force the drop.
    --help                Show this message and exit.
  $ pglift database dump --help
  Usage: pglift database dump [OPTIONS] DBNAME
  
    Dump a database
  
  Options:
    --help  Show this message and exit.
  $ pglift database dumps --help
  Usage: pglift database dumps [OPTIONS] [DBNAME]...
  
    List the database dumps
  
  Options:
    -o, --output-format [json]  Specify the output format.
    --help                      Show this message and exit.
  $ pglift database get --help
  Usage: pglift database get [OPTIONS] NAME
  
    Get the description of a database
  
  Options:
    -o, --output-format [json]  Specify the output format.
    --help                      Show this message and exit.
  $ pglift database list --help
  Usage: pglift database list [OPTIONS] [DBNAME]...
  
    List databases (all or specified ones)
  
    Only queried databases are shown when DBNAME is specified.
  
  Options:
    -o, --output-format [json]  Specify the output format.
    --help                      Show this message and exit.
  $ pglift database privileges --help
  Usage: pglift database privileges [OPTIONS] NAME
  
    List privileges on a database.
  
  Options:
    -r, --role TEXT             Role to inspect
    --default                   Display default privileges
    -o, --output-format [json]  Specify the output format.
    --help                      Show this message and exit.
  $ pglift database restore --help
  Usage: pglift database restore [OPTIONS] DUMP_ID [TARGETDBNAME]
  
    Restore a database dump
  
    DUMP_ID identifies the dump id.
  
    TARGETDBNAME identifies the (optional) name of the database in which the
    dump is reloaded. If provided, the database needs to be created beforehand.
  
    If TARGETDBNAME is not provided, the dump is reloaded using the database
    name that appears in the dump. In this case, the restore command will create
    the database so it needs to be dropped before running the command.
  
  Options:
    --help  Show this message and exit.
  $ pglift database run --help
  Usage: pglift database run [OPTIONS] SQL_COMMAND
  
    Run given command on databases of a PostgreSQL instance
  
  Options:
    -d, --database TEXT          Database to run command on
    -x, --exclude-database TEXT  Database to not run command on
    -o, --output-format [json]   Specify the output format.
    --help                       Show this message and exit.

PostgreSQL configuration commands

  $ pglift pgconf --help
  Usage: pglift pgconf [OPTIONS] COMMAND [ARGS]...
  
    Manage configuration of a PostgreSQL instance.
  
  Options:
    -i, --instance <version>/<name>
                                    Instance identifier; the <version>/ prefix
                                    may be omitted if there's only one instance
                                    matching <name>. Required if there is more
                                    than one instance on system.
    --help                          Show this message and exit.
  
  Commands:
    edit    Edit managed configuration.
    remove  Remove configuration items.
    set     Set configuration items.
    show    Show configuration (all parameters or specified ones).
  $ pglift pgconf edit --help
  Usage: pglift pgconf edit [OPTIONS]
  
    Edit managed configuration.
  
  Options:
    --help  Show this message and exit.
  $ pglift pgconf remove --help
  Usage: pglift pgconf remove [OPTIONS] PARAMETERS...
  
    Remove configuration items.
  
  Options:
    --help  Show this message and exit.
  $ pglift pgconf set --help
  Usage: pglift pgconf set [OPTIONS] <PARAMETER>=<VALUE>...
  
    Set configuration items.
  
  Options:
    --help  Show this message and exit.
  $ pglift pgconf show --help
  Usage: pglift pgconf show [OPTIONS] [PARAMETER]...
  
    Show configuration (all parameters or specified ones).
  
    Only uncommented parameters are shown when no PARAMETER is specified. When
    specific PARAMETERs are queried, commented values are also shown.
  
  Options:
    --help  Show this message and exit.

(Cleanup)
  INFO deleting pgbackrest include directory
  INFO uninstalling base pgbackrest configuration
  INFO deleting common pgbackrest directories
  INFO deleting postgresql log directory (no-eol)
