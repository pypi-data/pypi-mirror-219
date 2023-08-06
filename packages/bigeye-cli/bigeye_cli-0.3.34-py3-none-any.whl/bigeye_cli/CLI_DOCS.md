# **Bigeye CLI**
Version: 0.3.32

## Installation
### Setting up your local/build environment
#### Mac with Pyenv
1. Install [brew](https://brew.sh/)
2. Install [pyenv](https://formulae.brew.sh/formula/pyenv)
3. Install python and define a default global:
```shell
pyenv install 3.8.10
pyenv global 3.8.10
```

#### Conda
1. Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. Create environment with python3.8
```shell
conda create -n bigeye_env python=3.8
conda activate bigeye_env
```

#### Linux
Most linux distributes include a default python distribution and we recommend using that default.

### Installing bigeye
You can install the Bigeye CLI from your command line with the following command:
```shell
pip3 install bigeye-cli
```
## Credential
Run the following command to get logged into your Bigeye workspace from the CLI:

```console
bigeye credential
```

There are two ways to authenticate: basic authentication and browser authentication.

### Basic Authentication
If you select basic authentication, the CLI will prompt you to enter your Bigeye username and password. This will
create a default credential file at ~/.bigeye/default_cred.json. This credential will be used for all CLI commands
calls unless an environment variable is explicitly provided.

```yaml
base_url: "https://app.bigeye.com",
user: "some_user+some_company@bigeye.com",
password: "fakepassword1234"
```

You can create an environment variable for your workspace credential file, this is helpful if you are managing
multiple workspaces and need to flip between them. Add the following to your ~/.bashrc or ~/.zshrc file:

```shell
export BIGEYE_API_CRED_FILE=/some/path/to/bigeye_cred_file.json
```

Lastly, if you want to specify the credential per command, you can always pass a -b parameter with the file path for
the desired credential.

### Browser Authentication
Alternatively, you can use browser authentication. Login to your bigeye workspace on a Chrome, Chromium or
Firefox browser. Run **bigeye credential** and select browser_auth when prompted in the CLI and follow the
instructions. If you use Chrome profiles, make sure to specify the profile email address you are logged into.

Note: your authentication will only be valid so long as your browser session is active.

## Basic Usage
```console
$ bigeye --help
```
## Tab/Auto Completion
Bigeye supports tab/auto completion for many different shells.  For example, run:
```console
$ bigeye --install-completion zsh
```
### ZSH Completion
Verify that the following has been added to your shell rc file:
```shell
autoload -Uz compinit
zstyle :completion:* menu select
fpath+=~/.zfunc
```
If you are having trouble with auto complete then add the following below the 3 lines above.
```shell
compinit
```
# CLI Documentation

# `bigeye workspace`

Workspace Commands for Bigeye CLI

**Usage**:

```console
$ bigeye workspace [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `create-named-schedule`: Create a named, cron based schedule
* `delete-named-schedule`: Delete a named schedule.
* `delete-user`: Remove user from workspace.
* `edit-user-role`: Change user role.
* `invite-user`: Invite a user.
* `schedule-all-metrics`: Schedule all metrics in a workspace.
* `unschedule-all-metrics`: Unschedule all metrics in a workspace.

## `bigeye workspace create-named-schedule`

Create a named, cron based schedule

**Usage**:

```console
$ bigeye workspace create-named-schedule [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-sn, --name TEXT`: The user defined name of the schedule  [required]
* `-c, --cron TEXT`: The cron string to define the schedule  [required]
* `--help`: Show this message and exit.

## `bigeye workspace delete-named-schedule`

Delete a named schedule.

**Usage**:

```console
$ bigeye workspace delete-named-schedule [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-sn, --name TEXT`: The user defined name of the schedule  [required]
* `--help`: Show this message and exit.

## `bigeye workspace delete-user`

Remove user from workspace. Only supports basic auth conf

**Usage**:

```console
$ bigeye workspace delete-user [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration. (browser auth not supported)  [required]
* `-un, --user_name TEXT`: User name.  [required]
* `--help`: Show this message and exit.

## `bigeye workspace edit-user-role`

Change user role. Only supports basic auth conf

**Usage**:

```console
$ bigeye workspace edit-user-role [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration. (browser auth not supported)  [required]
* `-un, --user_name TEXT`: User name.  [required]
* `-role, --user_role TEXT`: The role to assign the user, i.e. OWNER, ADMIN, USER.  [required]
* `--help`: Show this message and exit.

## `bigeye workspace invite-user`

Invite a user. Only supports basic auth conf

**Usage**:

```console
$ bigeye workspace invite-user [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration. (browser auth not supported)  [required]
* `-un, --user_name TEXT`: User name.  [required]
* `-email, --user_email TEXT`: Email where invite will be sent.  [required]
* `--help`: Show this message and exit.

## `bigeye workspace schedule-all-metrics`

Schedule all metrics in a workspace.

**Usage**:

```console
$ bigeye workspace schedule-all-metrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-type, --time_interval_type INTEGER`: Time interval type.
 UNDEFINED_TIME_INTERVAL_TYPE:0
HOURS_TIME_INTERVAL_TYPE:1
MINUTES_TIME_INTERVAL_TYPE:2
SECONDS_TIME_INTERVAL_TYPE:3
DAYS_TIME_INTERVAL_TYPE:4
WEEKDAYS_TIME_INTERVAL_TYPE:5
MARKET_DAYS_TIME_INTERVAL_TYPE:6  [default: 1]
* `-value, --interval_value INTEGER`: Number of intervals to set on all metric schedules.  If 0 use unschedule all metrics.  [required]
* `--help`: Show this message and exit.

## `bigeye workspace unschedule-all-metrics`

Unschedule all metrics in a workspace.

**Usage**:

```console
$ bigeye workspace unschedule-all-metrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `--help`: Show this message and exit.

# `bigeye bigconfig`

Bigconfig Commands for Bigeye CLI

**Usage**:

```console
$ bigeye bigconfig [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `apply`: Applies a purge of deployed metrics or...
* `plan`: Executes a plan for purging sources or...

## `bigeye bigconfig apply`

Applies a purge of deployed metrics or applies Bigconfig files from the input path/current working directory to
the Bigeye workspace.

**Usage**:

```console
$ bigeye bigconfig apply [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Auth Configuration
* `-ip, --input_path TEXT`: List of paths containing Bigconfig files or pointing to a Bigconfig file. E.g. -ip path1 -ip path2. If no input path is defined then current working directory will be used.
* `-op, --output_path TEXT`: Output path where reports and fixme files will be saved. If no output path is defined then current working directory will be used.
* `-psn, --purge_source_name TEXT`: List of source names to purge  E.g. -psn source_1 -psn source_2.
* `-purge_all, --purge_all_sources`: Purge all sources: True or False.
* `-nq, --no_queue`: Don't submit to queue: True or False.
* `-r, --recursive`: Search all input directories recursively.
* `-strict, --strict_mode`: API errors cause an exception if True. (Validation errors still cause an exception)
* `--help`: Show this message and exit.

## `bigeye bigconfig plan`

Executes a plan for purging sources or processing bigconfig files in the input path/current
working directory.

**Usage**:

```console
$ bigeye bigconfig plan [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Auth Configuration
* `-ip, --input_path TEXT`: List of paths containing Bigconfig files or pointing to a Bigconfig file. E.g. -ip path1 -ip path2. If no input path is defined then current working directory will be used.
* `-op, --output_path TEXT`: Output path where reports and fixme files will be saved. If no output path is defined then current working directory will be used.
* `-psn, --purge_source_name TEXT`: List of source names to purge  E.g. -psn source_1 -psn source_2.
* `-purge_all, --purge_all_sources`: Purge all sources: True or False.
* `-r, --recursive`: Search all input directories recursively.
* `-strict, --strict_mode`: API errors cause an exception if True. (Validation errors still cause an exception)
* `--help`: Show this message and exit.

# `bigeye catalog`

Catalog Commands for Bigeye CLI

**Usage**:

```console
$ bigeye catalog [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `add-source`: Adds a source to specified Bigeye workspace.
* `backfill-autothresholds`: Backfills autothresholds by warehouse id,...
* `backfill-metrics`: Backfills metrics by warehouse id, schema...
* `delete-metrics`: Delete metrics in a warehouse id, by...
* `delete-source`: Delete a source from specified Bigeye...
* `delete-template`: Delete a template.
* `delete-virtual-table`: Delete a virtual table.
* `deploy-all-autometrics`: Deploys all Autometrics to specified...
* `get-all-metric-templates`: Retrieve all metric templates and output...
* `get-metric-info`: Outputs metric info to a file.
* `get-metric-queries`: Gets the debug queries for all metrics by...
* `get-table-info`: Outputs table info to a file for an entire...
* `rebuild`: Rebuilds/Reprofiles a source by warehouse...
* `regen-autometrics`: Regenerates Autometrics by warehouse id OR...
* `run-metrics`: Runs metrics by warehouse id, schema...
* `schedule-all-metrics`: Updates schedule for all metrics in a...
* `set-metric-time`: Sets metric times from a list of possible...
* `unschedule-all-metrics`: Unschedule all metrics by warehouse,...
* `unset-metric-time`: Unsets metric times for whole warehouse or...
* `upsert-template`: Create or update a template for a source.
* `upsert-virtual-table`: Create or update a virtual table.

## `bigeye catalog add-source`

Adds a source to specified Bigeye workspace.  Supports either source configs stored in AWS Secrets manager OR
locally in file.

**Usage**:

```console
$ bigeye catalog add-source [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-sn, --secret_name TEXT`: The name of the secret to retrieve from AWS Secrets Manager
* `-srn, --secret_region_name TEXT`: AWS Secret Manager Region Name  [default: us-west-2]
* `-sccf, --source_catalog_config_file TEXT`: The file containing the necessary parameters for adding a source to Bigeye.
* `--help`: Show this message and exit.

## `bigeye catalog backfill-autothresholds`

Backfills autothresholds by warehouse id, schema names, and/or table ids.

**Usage**:

```console
$ bigeye catalog backfill-autothresholds [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Warehouse ID
* `-sn, --schema_name TEXT`: List of Schema Names.  E.g. -sn schema_1 -sn schema_2.
* `-tid, --table_id INTEGER`: Table IDs.  E.g. -tid 123 -tid 124
* `--help`: Show this message and exit.

## `bigeye catalog backfill-metrics`

Backfills metrics by warehouse id, schema names, and/or table ids.

**Usage**:

```console
$ bigeye catalog backfill-metrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Warehouse ID
* `-sn, --schema_name TEXT`: List of Schema Names.  E.g. -sn schema_1 -sn schema_2.
* `-tid, --table_id INTEGER`: Table IDs.  E.g. -tid 123 -tid 124
* `--delete_history`: Delete metric run history
* `--help`: Show this message and exit.

## `bigeye catalog delete-metrics`

Delete metrics in a warehouse id, by schema names, or by table_ids.  Also, can filter by multipe
metric types.

**Usage**:

```console
$ bigeye catalog delete-metrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Warehouse ID
* `-sn, --schema_name TEXT`: List of Schema Names.  E.g. -sn schema_1 -sn schema_2.
* `-tid, --table_id INTEGER`: Table IDs.  E.g. -tid 123 -tid 124
* `-m, --metric_type TEXT`: Delete by name of the metric type.UNDEFINED_PREDEFINED_METRIC_NAME, PERCENT_NULL, COUNT_NULL, PERCENT_EMPTY_STRING, COUNT_EMPTY_STRING, PERCENT_UNIQUE, PERCENT_VALUE_IN_LIST, AVERAGE, MIN, MAX, SUM, COUNT_ROWS, COUNT_DISTINCT, HOURS_SINCE_MAX_DATE, HOURS_SINCE_MAX_TIMESTAMP, COUNT_TRUE, PERCENT_TRUE, COUNT_FALSE, PERCENT_FALSE, COUNT_USA_PHONE, PERCENT_USA_PHONE, COUNT_USA_ZIP_CODE, PERCENT_USA_ZIP_CODE, PERCENT_UUID, COUNT_TIMESTAMP_STRING, PERCENT_TIMESTAMP_STRING, COUNT_DUPLICATES, COUNT_USA_STATE_CODE, PERCENT_USA_STATE_CODE, VARIANCE, SKEW, KURTOSIS, GEOMETRIC_MEAN, HARMONIC_MEAN, COUNT_UUID, COUNT_CUSIP, PERCENT_CUSIP, COUNT_SEDOL, PERCENT_SEDOL, COUNT_ISIN, PERCENT_ISIN, COUNT_LEI, PERCENT_LEI, COUNT_FIGI, PERCENT_FIGI, COUNT_PERM_ID, PERCENT_PERM_ID, COUNT_NAN, PERCENT_NAN, COUNT_LONGITUDE, PERCENT_LONGITUDE, COUNT_LATITUDE, PERCENT_LATITUDE, COUNT_NOT_IN_FUTURE, PERCENT_NOT_IN_FUTURE, COUNT_DATE_NOT_IN_FUTURE, PERCENT_DATE_NOT_IN_FUTURE, MEDIAN, PERCENTILE, COUNT_NOT_NULL, STRING_LENGTH_AVERAGE, STRING_LENGTH_MIN, STRING_LENGTH_MAX, COUNT_SSN, PERCENT_SSN, COUNT_EMAIL, PERCENT_EMAIL, ROWS_INSERTED, HOURS_SINCE_LAST_LOAD, COUNT_READ_QUERIES, PERCENT_NOT_NULL, FRESHNESS, VOLUME
* `--help`: Show this message and exit.

## `bigeye catalog delete-source`

Delete a source from specified Bigeye workspace.

**Usage**:

```console
$ bigeye catalog delete-source [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: The ID of the warehouse to delete.
* `--help`: Show this message and exit.

## `bigeye catalog delete-template`

Delete a template.

**Usage**:

```console
$ bigeye catalog delete-template [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-tid, --template_id INTEGER`: The ID of the metric template  [required]
* `--help`: Show this message and exit.

## `bigeye catalog delete-virtual-table`

Delete a virtual table.

**Usage**:

```console
$ bigeye catalog delete-virtual-table [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-vtn, --table_name TEXT`: The name of the virtual table  [required]
* `-sn, --source_name TEXT`: The name of the source where the template will be defined  [required]
* `--help`: Show this message and exit.

## `bigeye catalog deploy-all-autometrics`

Deploys all Autometrics to specified warehouse OR warehouse and list of schema names OR warehouse and list of
table ids.

**Usage**:

```console
$ bigeye catalog deploy-all-autometrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Deploy autometrics to all tables in warehouse.
* `-sn, --schema_name TEXT`: List of Schema Names.  E.g. -sn schema_1 -sn schema_2.
* `-tid, --table_id INTEGER`: Table IDs.  E.g. -tid 123 -tid 124
* `-lbd, --lookback_days INTEGER`: Look back days for the metrics.  [default: 7]
* `--ops_only`: Deploy only operational metrics  [default: True]
* `--help`: Show this message and exit.

## `bigeye catalog get-all-metric-templates`

Retrieve all metric templates and output to a file.

**Usage**:

```console
$ bigeye catalog get-all-metric-templates [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-ps, --page_size INTEGER`: How many results to return per page  [default: 0]
* `-s, --search TEXT`: A search string to narrow results
* `-op, --output_path TEXT`: The path to output templates
* `-fn, --file_name TEXT`: User defined file name
* `--help`: Show this message and exit.

## `bigeye catalog get-metric-info`

Outputs metric info to a file.  Includes metric configuration and details about recent runs.

**Usage**:

```console
$ bigeye catalog get-metric-info [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Warehouse ID
* `-sn, --schema_name TEXT`: List of Schema Names.  E.g. -sn schema_1 -sn schema_2.
* `-tid, --table_id INTEGER`: Table IDs. E.g. -tid 123 -tid 124or schema names.
* `-ms, --metric_status [HEALTHY|ALERTING|UNKNOWN]`: Used to query metric of particular status.
* `-op, --output_path TEXT`: File to write the failed metric configurations to.  [required]
* `--conf_only`: Output only the metric configuration.
* `--help`: Show this message and exit.

## `bigeye catalog get-metric-queries`

Gets the debug queries for all metrics by warehouse id, schema names, or table ids.

**Usage**:

```console
$ bigeye catalog get-metric-queries [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Warehouse ID
* `-sn, --schema_name TEXT`: List of Schema Names.  E.g. -sn schema_1 -sn schema_2.
* `-tid, --table_id INTEGER`: Table IDs.  E.g. -tid 123 -tid 124
* `-op, --output_path TEXT`: File to write the failed metric configurations to.  [required]
* `--help`: Show this message and exit.

## `bigeye catalog get-table-info`

Outputs table info to a file for an entire warehouse, certain schemas, or certain tables.

**Usage**:

```console
$ bigeye catalog get-table-info [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Warehouse ID
* `-sn, --schema_name TEXT`: List of Schema Names.  E.g. -sn schema_1 -sn schema_2.
* `-tid, --table_id INTEGER`: Table IDs. E.g. -tid 123 -tid 124
* `-tn, --table_name TEXT`: Table Namess. E.g. -tn some_table -tn some_other_table
* `-op, --output_path TEXT`: File to write the failed metric configurations to.  [required]
* `--help`: Show this message and exit.

## `bigeye catalog rebuild`

Rebuilds/Reprofiles a source by warehouse id or a schema by warehouse id and schema name.

**Usage**:

```console
$ bigeye catalog rebuild [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Warehouse ID  [required]
* `-sn, --schema_name TEXT`: Schema Name
* `--help`: Show this message and exit.

## `bigeye catalog regen-autometrics`

Regenerates Autometrics by warehouse id OR warehouse id and list of schema names OR list of table ids.

**Usage**:

```console
$ bigeye catalog regen-autometrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Warehouse ID.  If none will look for Table IDs.  If value then will pull all table ids for warehouse
* `-sn, --schema_name TEXT`: List of Schema Names  E.g. -sn schema_1 -sn schema_2.  Do not include warehouse name -- GREENE_HOMES_DEMO_STANDARD.CONFORMED is fully qualified and CONFORMED is the schema name.
* `-tid, --table_id INTEGER`: List of Table IDs.  E.g. -tid 123 -tid 124
* `--help`: Show this message and exit.

## `bigeye catalog run-metrics`

Runs metrics by warehouse id, schema names, and/or table ids

**Usage**:

```console
$ bigeye catalog run-metrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Warehouse ID
* `-sn, --schema_name TEXT`: List of Schema Names.  E.g. -sn schema_1 -sn schema_2.
* `-tid, --table_id INTEGER`: Table IDs.  E.g. -tid 123 -tid 124
* `--help`: Show this message and exit.

## `bigeye catalog schedule-all-metrics`

Updates schedule for all metrics in a warehouse.

**Usage**:

```console
$ bigeye catalog schedule-all-metrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Warehouse ID
* `-type, --time_interval_type INTEGER`: Time interval type.
 UNDEFINED_TIME_INTERVAL_TYPE:0
HOURS_TIME_INTERVAL_TYPE:1
MINUTES_TIME_INTERVAL_TYPE:2
SECONDS_TIME_INTERVAL_TYPE:3
DAYS_TIME_INTERVAL_TYPE:4
WEEKDAYS_TIME_INTERVAL_TYPE:5
MARKET_DAYS_TIME_INTERVAL_TYPE:6  [default: 1]
* `-value, --interval_value INTEGER`: Number of intervals to set on all metric schedules.  If 0 use unschedule all metrics.  [required]
* `--help`: Show this message and exit.

## `bigeye catalog set-metric-time`

Sets metric times from a list of possible metric column names.  Can set for whole warehouse or for a list of
table IDs.

**Usage**:

```console
$ bigeye catalog set-metric-time [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Warehouse ID
* `-sid, --schema_id INTEGER`: Schema ID
* `-tid, --table_id INTEGER`: List of table IDs.
* `-cn, --metric_column_name TEXT`: Possible metric column names.  [required]
* `-r, --replace`: replace metric times if already present on tables?  Default is false.
* `--help`: Show this message and exit.

## `bigeye catalog unschedule-all-metrics`

Unschedule all metrics by warehouse, schema or tables.

**Usage**:

```console
$ bigeye catalog unschedule-all-metrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Warehouse ID
* `-sn, --schema_name TEXT`: List of Schema Name.  E.g. -sn schema_1.
* `-tid, --table_id INTEGER`: Table IDs.  E.g. -tid 123 -tid 124
* `--help`: Show this message and exit.

## `bigeye catalog unset-metric-time`

Unsets metric times for whole warehouse or for a list og table IDs.

**Usage**:

```console
$ bigeye catalog unset-metric-time [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wid, --warehouse_id INTEGER`: Warehouse ID
* `-tid, --table_id INTEGER`: List of table IDs.
* `--help`: Show this message and exit.

## `bigeye catalog upsert-template`

Create or update a template for a source.

**Usage**:

```console
$ bigeye catalog upsert-template [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-sn, --source_name TEXT`: The name of the source where the template will be defined  [required]
* `-tn, --name TEXT`: The user defined name of the template  [required]
* `-tb, --body TEXT`: The string to define the template  [required]
* `-rt, --returns [BOOLEAN|NUMERIC]`: The data type returned by the template; i.e. NUMERIC, BOOLEAN  [required]
* `-p, --params TEXT`: A list of key/value pairs for parameters; ex. -p column=COLUMN_REFERENCE -p table=STRING  [required]
* `-id, --template_id INTEGER`: The template ID (Only required when updating a template).  [default: 0]
* `--help`: Show this message and exit.

## `bigeye catalog upsert-virtual-table`

Create or update a virtual table.

**Usage**:

```console
$ bigeye catalog upsert-virtual-table [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-vtn, --table_name TEXT`: The name of the virtual table  [required]
* `-s, --sql TEXT`: The SQL to define the table  [required]
* `-sn, --source_name TEXT`: The name of the source where the virtual table will be defined  [required]
* `-u, --update`: Create if false. Update if true.
* `--help`: Show this message and exit.

# `bigeye metric`

Metric Commands for Bigeye CLI

**Usage**:

```console
$ bigeye metric [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `dbt-tests-to-metrics`: Convert tests in a dbt schema.yml to...
* `get-info`: Outputs metric info to a file.
* `get-metric-queries`: Gets the debug queries for all metrics by...
* `run`: Run metric by id(s)
* `upsert`: Upsert single metric from file.
* `upsert-from-path`: Upsert multiple metrics from files stored...

## `bigeye metric dbt-tests-to-metrics`

Convert tests in a dbt schema.yml to metrics in Bigeye

**Usage**:

```console
$ bigeye metric dbt-tests-to-metrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-wn, --warehouse_name TEXT`: The name of the source to deploy metrics  [required]
* `-sn, --schema_name TEXT`: The name of the schema to deploy metrics  [required]
* `-sf, --schema_file TEXT`: The path to the dbt schema file  [required]
* `-auto, --use_auto`: Use autothresholds over default constant
* `--help`: Show this message and exit.

## `bigeye metric get-info`

Outputs metric info to a file.  Includes metric configuration and details about recent runs.

**Usage**:

```console
$ bigeye metric get-info [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-mid, --metric_id INTEGER`: Metric Ids.  [required]
* `-ms, --metric_status [HEALTHY|ALERTING|UNKNOWN]`: Used to query metric of particular status.
* `-op, --output_path TEXT`: File to write the failed metric configurations to.  [required]
* `--conf_only`: Output only the metric configuration.
* `--help`: Show this message and exit.

## `bigeye metric get-metric-queries`

Gets the debug queries for all metrics by warehouse id, schema names, or table ids.

**Usage**:

```console
$ bigeye metric get-metric-queries [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-mid, --metric_id INTEGER`: Metric Ids.  [required]
* `-op, --output_path TEXT`: File to write the failed metric configurations to.  [required]
* `--help`: Show this message and exit.

## `bigeye metric run`

Run metric by id(s)

**Usage**:

```console
$ bigeye metric run [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-mid, --metric_id INTEGER`: Metric Ids.  [required]
* `--help`: Show this message and exit.

## `bigeye metric upsert`

Upsert single metric from file.

**Usage**:

```console
$ bigeye metric upsert [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-f, --file TEXT`: File containing SimpleUpsedrtMetricRequest or MetricConfiguration  [required]
* `-t, --file_type [SIMPLE|FULL]`: Metric File Type.  Simple conforms to SimpleUpsertMetricRequest and Full conforms to MetricConfiguration  [required]
* `-wid, --warehouse_id INTEGER`: (Optional) Warehouse ID.  If specified it will reduce the text based search for the table.warehouse
* `-mid, --metric_id INTEGER`: (Optional) Metric Id.  If specified it will reduce the text based search for existing metric.
* `--help`: Show this message and exit.

## `bigeye metric upsert-from-path`

Upsert multiple metrics from files stored in path.

**Usage**:

```console
$ bigeye metric upsert-from-path [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-twid, --target_warehouse_id INTEGER`: Deploy Metrics to target Warehouse ID.  [required]
* `-sp, --source_path TEXT`: Source path file containing the metrics to migrate.  [required]
* `--help`: Show this message and exit.

# `bigeye issues`

Issues Commands for Bigeye CLI

**Usage**:

```console
$ bigeye issues [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `get-issues`: Gets issues and writes info to files.
* `update-issue`: Updates an issue in Bigeye and returns the...

## `bigeye issues get-issues`

Gets issues and writes info to files.

**Usage**:

```console
$ bigeye issues get-issues [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `-wid, --warehouse_id INTEGER`: Warehouse IDs.
* `-sn, --schema_name TEXT`: Schema names
* `-mid, --metric_id INTEGER`: Metric IDs.
* `-cid, --collection_id INTEGER`: Collection IDs
* `-iid, --issue_id INTEGER`: Issue IDs
* `-op, --output_path TEXT`: File to write the failed metric configurations to.  [required]
* `--help`: Show this message and exit.

## `bigeye issues update-issue`

Updates an issue in Bigeye and returns the Issue object from the protobuff.

**Usage**:

```console
$ bigeye issues update-issue [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `-iid, --issue_id INTEGER`: Issue ID  [required]
* `-status, --issue_status TEXT`: The status update. Options are ACKNOWLEDGED or CLOSED.
* `-by, --updated_by TEXT`: The user providing the update.
* `-m, --message TEXT`: The message to attach to the issue.
* `-cl, --closing_label TEXT`: Used to train Bigeye when closing an issue. Options are TRUE_POSITIVE, FALSE_POSITIVE, EXPECTED.
* `--help`: Show this message and exit.

# `bigeye deltas`

Deltas Commands for Bigeye CLI

**Usage**:

```console
$ bigeye deltas [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `cicd`: Creates a delta based on...
* `create-delta`: Creates deltas between tables from a...
* `run-delta`: Runs a delta by Delta ID.
* `suggest-deltas`: Suggests and creates Deltas with default...

## `bigeye deltas cicd`

Creates a delta based on SimpleDeltaConfiguration and integrates the results with the provided VCS vendor.

**Usage**:

```console
$ bigeye deltas cicd [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration as a base64 encoded string  [required]
* `-dcc, --delta_cicd_config TEXT`: The yaml file containing the parameters for the DeltaCICDConfig class  [required]
* `--help`: Show this message and exit.

## `bigeye deltas create-delta`

Creates deltas between tables from a Simple Delta configuration file that contains multiple delta configurations.
Enforces 1:1 column comparisons by case-insensitive column names if no column mappings are declared in
configuration.

**Usage**:

```console
$ bigeye deltas create-delta [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `-dc, --delta_conf TEXT`: Simple Delta configuration file.  [required]
* `--help`: Show this message and exit.

## `bigeye deltas run-delta`

Runs a delta by Delta ID.

**Usage**:

```console
$ bigeye deltas run-delta [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `-did, --delta_id INTEGER`: Id of delta.  [required]
* `--help`: Show this message and exit.

## `bigeye deltas suggest-deltas`

Suggests and creates Deltas with default behavior and outputs all Simple Delta Configurations to a file.

**Usage**:

```console
$ bigeye deltas suggest-deltas [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `-swid, --source_warehouse_id INTEGER`: Source Warehouse ID
* `-twid, --target_warehouse_id INTEGER`: Source Warehouse ID
* `-swn, --source_warehouse_name TEXT`: Source Warehouse Name
* `-twn, --target_warehouse_name TEXT`: Source Warehouse Name
* `-snp, --schema_name_pair TEXT`: Fully qualified schema name pairs.  e.g. -snp source_schema_1:target_schema_1 -snp source_warehouse.source_schema:target_warehouse.target_schema
* `-op, --output_path TEXT`: File to write the failed metric configurations to.  [required]
* `--help`: Show this message and exit.

# `(Deprecated) bigeye sla`

SLA Commands for Bigeye CLI (use collections command instead)

**Usage**:

```console
$ (Deprecated) bigeye sla [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `add-metric`: Add metric to an SLA.
* `backfill-metrics`: Backfill all metrics in an SLA.
* `get-metric-info`: Get metric info for all metrics in SLA.
* `get-metric-queries`: Gets the debug queries for all metrics by...
* `migrate-from-json`: Loads metrics from SLA oriented metric...
* `run-metrics`: Run all metrics in an SLA.

## `(Deprecated) bigeye sla add-metric`

Add metric to an SLA.

**Usage**:

```console
$ (Deprecated) bigeye sla add-metric [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `-mid, --metric_id INTEGER`: Metric ID  [required]
* `-sid, --sla_id INTEGER`: SLA ID  [required]
* `--help`: Show this message and exit.

## `(Deprecated) bigeye sla backfill-metrics`

Backfill all metrics in an SLA.

**Usage**:

```console
$ (Deprecated) bigeye sla backfill-metrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `--from_slas`: Scrapes all SLAs in customer workspace for Metric Info.
* `--sla_ids INTEGER`: SLA IDs.  Scrape certain SLAs for Metric Info.
* `--delete_history`: Delete metric run history
* `--help`: Show this message and exit.

## `(Deprecated) bigeye sla get-metric-info`

Get metric info for all metrics in SLA.

**Usage**:

```console
$ (Deprecated) bigeye sla get-metric-info [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `--from_slas`: Scrapes all SLAs in customer workspace for Metric Info.
* `--sla_ids INTEGER`: SLA IDs.  Scrape certain SLAs for Metric Info.
* `-op, --output_path TEXT`: File to write the failed metric configurations to.  [required]
* `--help`: Show this message and exit.

## `(Deprecated) bigeye sla get-metric-queries`

Gets the debug queries for all metrics by warehouse id, schema names, or table ids.

**Usage**:

```console
$ (Deprecated) bigeye sla get-metric-queries [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `-sid, --sla_id INTEGER`: SLA ID  [required]
* `-op, --output_path TEXT`: File to write the failed metric configurations to.  [required]
* `--help`: Show this message and exit.

## `(Deprecated) bigeye sla migrate-from-json`

Loads metrics from SLA oriented metric info output.  Used to migrate metrics from one warehouse to
another, identical, warehouse

**Usage**:

```console
$ (Deprecated) bigeye sla migrate-from-json [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `-twid, --target_warehouse_id INTEGER`: Deploy Metrics to target Warehouse ID.  [required]
* `-ip, --input_path TEXT`: Path to read from.  [required]
* `-kn, --keep_notifications`: Keep Notifications from versioned or templated metric configuration.
* `-kid, --keep_ids`: Keep Metric and SLA IDs from versioned or templated metric configuration.  If kept this would update existing metrics and slas.  If not kept it would create new.
* `--help`: Show this message and exit.

## `(Deprecated) bigeye sla run-metrics`

Run all metrics in an SLA.

**Usage**:

```console
$ (Deprecated) bigeye sla run-metrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `-sid, --sla_id INTEGER`: SLA ID  [required]
* `--help`: Show this message and exit.

# `bigeye collections`

Collections Commands for Bigeye CLI

**Usage**:

```console
$ bigeye collections [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `add-metric`: Add metric to a Collection.
* `backfill-metrics`: Backfill all metrics in a Collection.
* `get-metric-info`: Get metric info for all metrics in...
* `get-metric-queries`: Gets the debug queries for all metrics by...
* `migrate-from-json`: Loads metrics from Collection oriented...
* `run-metrics`: Run all metrics in a Collection.

## `bigeye collections add-metric`

Add metric to a Collection.

**Usage**:

```console
$ bigeye collections add-metric [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `-mid, --metric_id INTEGER`: Metric ID  [required]
* `-cid, --collection_id INTEGER`: Collection ID  [required]
* `--help`: Show this message and exit.

## `bigeye collections backfill-metrics`

Backfill all metrics in a Collection.

**Usage**:

```console
$ bigeye collections backfill-metrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `--from_collections`: Scrapes all Collections in customer workspace for Metric Info.
* `--collection_ids INTEGER`: Collection IDs.  Scrape certain Collections for Metric Info.
* `--delete_history`: Delete metric run history
* `--help`: Show this message and exit.

## `bigeye collections get-metric-info`

Get metric info for all metrics in Collection.

**Usage**:

```console
$ bigeye collections get-metric-info [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `--from_collections`: Scrapes all Collections in customer workspace for Metric Info.
* `--collection_ids INTEGER`: Collection IDs.  Scrape certain Collections for Metric Info.
* `-op, --output_path TEXT`: File to write the failed metric configurations to.  [required]
* `--help`: Show this message and exit.

## `bigeye collections get-metric-queries`

Gets the debug queries for all metrics by warehouse id, schema names, or table ids.

**Usage**:

```console
$ bigeye collections get-metric-queries [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `-cid, --collection_id INTEGER`: Collection ID  [required]
* `-op, --output_path TEXT`: File to write the failed metric configurations to.  [required]
* `--help`: Show this message and exit.

## `bigeye collections migrate-from-json`

Loads metrics from Collection oriented metric info output.  Used to migrate metrics from one warehouse to
another, identical, warehouse

**Usage**:

```console
$ bigeye collections migrate-from-json [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `-twid, --target_warehouse_id INTEGER`: Deploy Metrics to target Warehouse ID.  [required]
* `-ip, --input_path TEXT`: Path to read from.  [required]
* `-kn, --keep_notifications`: Keep Notifications from versioned or templated metric configuration.
* `-kid, --keep_ids`: Keep Metric and Collection IDs from versioned or templated metric configuration.  If kept this would update existing metrics and collections.  If not kept it would create new.
* `--help`: Show this message and exit.

## `bigeye collections run-metrics`

Run all metrics in a Collection.

**Usage**:

```console
$ bigeye collections run-metrics [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration File
* `-cid, --collection_id INTEGER`: Collection ID  [required]
* `--help`: Show this message and exit.

# `bigeye lineage`

Lineage Commands for Bigeye CLI

**Usage**:

```console
$ bigeye lineage [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `create-node`: Create a lineage node for an entity
* `create-relation`: Create a lineage relationship for 2 entities
* `delete-node`: Delete a lineage node for an entity
* `delete-relation`: Deletes a single relationship based on...

## `bigeye lineage create-node`

Create a lineage node for an entity

**Usage**:

```console
$ bigeye lineage create-node [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-en, --entity_name TEXT`: The fully qualified table name or name of the tableau workbook  [required]
* `-in, --int_name TEXT`: The name of the BI connection (required for entities outside of Bigeye)
* `--help`: Show this message and exit.

## `bigeye lineage create-relation`

Create a lineage relationship for 2 entities

**Usage**:

```console
$ bigeye lineage create-relation [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-up, --upstream TEXT`: The fully qualified table name  [required]
* `-down, --downstream TEXT`: The fully qualified table name  [required]
* `--help`: Show this message and exit.

## `bigeye lineage delete-node`

Delete a lineage node for an entity

**Usage**:

```console
$ bigeye lineage delete-node [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-en, --entity_name TEXT`: The fully qualified table name or name of the tableau workbook  [required]
* `-in, --int_name TEXT`: The name of the BI connection (required for entities outside of Bigeye)
* `--help`: Show this message and exit.

## `bigeye lineage delete-relation`

Deletes a single relationship based on relation ID or all relationships for a node by name.

**Usage**:

```console
$ bigeye lineage delete-relation [OPTIONS]
```

**Options**:

* `-b, --bigeye_conf TEXT`: Bigeye Basic Auth Configuration
* `-en, --entity_name TEXT`: The fully qualified table name or name of the tableau workbook
* `-rid, --relation_id INTEGER`: The relationship ID to delete  [default: 0]
* `-in, --int_name TEXT`: The name of the BI connection (required for entities outside of Bigeye)
* `--help`: Show this message and exit.

