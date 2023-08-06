# Perun proxy utils

## Scripts

### run_probes.py

- script designed to execute multiple monitoring probes
- output is compatible with CheckMK
- it is required to put configuration file to `/etc/run_probes_cfg.yaml`
- for usage run: `./run_probes.py` or `python3 -m perun.proxy.utils.run_probes`

### separate_ssp_script.py

- Script for remove all logs from test accounts from SimpleSAMLlogs

- Params:
  - 1 - The file name

### backup_database.sh

- Do mysqldump into `/opt/mariadb_backup` and remove all dump file older than 7 days

### separate_oidc_logs.py

- Script for remove all logs from test accounts from OIDC logs

### metadata_expiration.py

- This script checks whether there are some metadata close to expiration date

- Params:
  - 1 - url to a page which prints a time when expires the metadata closest to expiration

### print_docker_versions.py

- This script collects system info, docker engine info and the versions of running containers and then prints it to the stdout in the JSON format
- A python [docker library](https://pypi.org/project/docker/) is needed to run the script

- Options:
  - -e,--exclude NAMES - space delimited string of container names to exclude from the listing

### run_version_script.py

- This scripts runs the print_docker_version.py script on the given machines. The collected versions are then printed as a MD table to the stdout

- Options:
  - -e,--exclude NAMES - space delimited string of container names to exclude from the listing
- Params:
  - 1... - machines to run the script on in the form of user@adress, the user needs root privileges to execute the script

## Nagios probes

All nagios scripts are located under `nagios` directory.

### check_mongodb.py

- nagios monitoring probe for mongodb

- connect, connections, replication_lag, replset_state monitoring options are tested (some possible options may not work since there are constructs which are not supported by latest mongodb versions)

- for usage run:
  `python3 check_mongodb.py --help`

### check_saml.py

- SAML authentication check

- for usage run:
  `python3 check_saml.py --help`

### check_user_logins.py

- check users which login in repeatedly more often than a specified threshold (logins per seconds)

- for usage run:
  `python3 check_user_logins.py --help`

- example:

```
python3 check_user_logins.py
    -p /var/log/proxyaai/simplesamlphp/simplesamlphp/simplesamlphp.log
    -l 5
    -s 60
    -r "^(?P<datetime>.{20}).*audit-login.* (?P<userid>[0-9]+)@muni\.cz$"
    -d "%b %d %Y %H:%M:%S"
```

### check_ldap.py

- check whether LDAP is available
- to use this check, you must install the ldap extra:

  ```sh
  pip install perun.proxy.utils[ldap]
  ```

  and the [build prerequisites of the python-ldap library](https://www.python-ldap.org/en/latest/installing.html#build-prerequisites)

- for usage run:

  ```sh
  python3 check_ldap.py --help
  ```
