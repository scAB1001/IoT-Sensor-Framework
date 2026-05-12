
# Internet of Things (IoT) Simulated Sensor Network (COMP3811 Coursework 2 - 2025)


## Description

The following README provides a guide to my COMP3811 Coursework 2 solution.
The guide follows how I have implemented and performed the tasks.

## Demonstration Video


### Preview

![IoT Simulation Demonstration](./assets/task_1.gif)

---

Raw Text: `https://www.youtube.com/embed/Ts7zStJf9dw`
Embedded link: [https://www.youtube.com/embed/Ts7zStJf9dw](https://www.youtube.com/embed/Ts7zStJf9dw) \


## Installation


### Prerequisites

A machine using a Linux distribution for its operating system and access to Admin privileges are required to run shell scripts and executables.
For example, my machine is running *Linux-mint*:

```bash
NAME="Linux Mint"
VERSION="22.2 (Zara)"
ID=linuxmint
ID_LIKE="ubuntu debian"
PRETTY_NAME="Linux Mint 22.2"
VERSION_ID="22.2"
HOME_URL="https://www.linuxmint.com/"
SUPPORT_URL="https://forums.linuxmint.com/"
BUG_REPORT_URL="http://linuxmint-troubleshooting-guide.readthedocs.io/en/latest/"
PRIVACY_POLICY_URL="https://www.linuxmint.com/"
VERSION_CODENAME=zara
UBUNTU_CODENAME=noble
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=24.04
DISTRIB_CODENAME=noble
DISTRIB_DESCRIPTION="Ubuntu Noble Numbat"
```


### Requirements

A file `requirements.txt` has been provided which includes all *version specific* packages needed to run this project. \
If errors arise with specific versions, remove the constraint on each line so that each package simply looks like this: `azure-functions` -omitting the `==0.0.0`.

*Note: The core coursework function tasks only require that **azure-functions** is installed. The rest pertains to performance testing and Java database creation*


#### Azure Environment

A valid Student Microsoft Azure account is needed to create both resources: The *Function App* and *Azure SQL Database (Azure SQL)*:
- **Subscription**: *UoL-Teaching-SOC-MCC*
- **Resource group**: *uol_feps_soc_comp_3211_sc222ab*
- **OPTIONAL**: The Azure Tools Extension Pack and Azure Functions Extension were installed for my IDE - Visual Studio Code.


#### Python Environment

Python was used for the Azure Function code as well as performance testing:
- *Python* version 3.12.12
- *Pip* package installer for Python
- **OPTIONAL**: These package were installed inside a configured *virtual environment* for the project but this is not explicitly necessary for setup.


#### Java Environment

Java was used for the database creation and querying during development:
- *openjdk 25* 2025-09-16
- OpenJDK Runtime Environment (build 25+36-Ubuntu-124.04.2)
- OpenJDK 64-Bit Server VM (build 25+36-Ubuntu-124.04.2, mixed mode, sharing)
- *javac 25*
- Microsoft JDBC Driver for SQL Server version 12.8, providing mssql-jdbc-12.8.0.jre8.jar and mssql-jdbc-12.8.0.jre11.jar class library files. (JAR files were included in my machine's *classpath*)

*Note: The CreateDB.java template file, QueryDB.java template file and JDBC Driver with the corresponding JAR files were provided as part of the in-course lab materials in a file **sqljdbc_12.8.1.0_enu.zip***


## Usage

Ensure prerequisites are satisfied to begin with the setup.


### Setup

Provide your password in the configuration files, replacing `YOUR_PASSWORD_HERE`:
- *java-db/config.properties*
- *azfunc/local.settings.json*


#### Azfunc directory

Within the azfunc/ directory, a shell script, `setup.sh`, has been provided for simplicity.

**Focused structural view**

```text
root/
├── azfunc/
│   ├── *.py                     # Python files
│   ├── setup.sh                 # Setup script
│   └── *.json                   # Configuration files
├── java-db/
```

Run the following:

```bash
# Ensure you are in the azure function directory
cd ./azfunc/

# Make this file executable
chmod +x ./setup.sh

# First, run the `check` command to verify dependencies
./setup.sh check

# Second, run the `init` command with source to initialise and activate the virtual environment
source ./setup.sh init
# Alternatively, run this after ./setup.sh init:
source .venv/bin/activate

# Finally, run the `populate` command to install the requirements with pip
/setup.sh populate
```

A successful example output can be seen below:

```bash
# Output for dependency check
========================================
  Checking Dependencies
========================================
✅  python3 found:
    Python 3.12.12


# Output for virtual environment initialisation
========================================
  Setting up Python Virtual Environment
========================================
ℹ️  Creating virtual environment '.venv'...
✅  Virtual environment created.
ℹ️  Activating virtual environment...
✅  Virtual environment activated.
ℹ️  Use command 'deactivate' to exit the virtual environment.


# Output for the requirements installation
========================================
  Populating Python Virtual Environment
========================================
ℹ️  Upgrading pip to the latest version...
Requirement already satisfied: pip in ./.venv/lib/python3.12/site-packages (25.3)
✅  pip is using the latest version.

ℹ️  Installing required packages from requirements.txt...
Collecting azure-functions==1.24.0 (from -r requirements.txt (line 1))
  Using cached azure_functions-1.24.0-py3-none-any.whl.metadata (7.4 kB)
# other packages...
✅  Required packages installed.

ℹ️  Verifying installation by listing installed packages...
Package            Version
------------------ -----------
azure-functions    1.24.0
# other packages...

# You should now see a ((.venv)) preceding your active terminal input line e.g.,
((.venv) ) andreas@Lenovo-V15-G4-AMN:~/github-projects/uni/comp3211/cwk-02/azfunc$
```


#### Java Database directory

Within the java-db/ directory, a shell script, `build.sh`, has been provided for simplicity.

**Focused structural view**

```text
root/
├── java-db/
│   ├── *.java                   # Java source files
│   ├── *.class                  # Java class files
│   ├── build.sh                 # Setup and test script
│   └── config.properties        # Configuration properties
│   └── sqljdbc_12.8/            # JDBC Driver for SQL Server
├── azfunc/
```

Run the following:

```bash
# Ensure you are in the java database directory
cd ./java-db/

# Make this file executable
chmod +x ./build.sh

# First, run the `check` command to verify dependencies
./build.sh check

# Then, run the `exec` command to compile and execute `CreateDB.java`
./build.sh exec CreateDB.java
```

A successful example output can be seen below:

```bash
# Output for dependency check
========================================
  Checking Dependencies
========================================
✅ javac found:
    javac 25
✅ java found:
    openjdk 25 2025-09-16
OpenJDK Runtime Environment (build 25+36-Ubuntu-124.04.2)
OpenJDK 64-Bit Server VM (build 25+36-Ubuntu-124.04.2, mixed mode, sharing)
✅ JDBC Driver found at ./sqljdbc_12.8/enu/jars/mssql-jdbc-12.8.1.jre11.jar
ℹ️  Located in directory: ./sqljdbc_12.8/enu/jars


# Output for database creation
========================================
  Building and Executing specified file
========================================
ℹ️  Compiling CreateDB.java...
✅ Compilation successful
ℹ️  Executing: CreateDB
✅ Connected to Azure SQL Database
✅ Database setup complete - ready for Azure Functions
✅ Database-level change tracking enabled
✅ Table-level change tracking enabled for sensor_data
# further output is dependent on the contents of CreateDB.java
```


### Executing Tasks

In order to execute the tasks, we must ensure both the Azure Database and Function App are running. \
The Database will appear offline until you create or query the database for the first time -or your request times out as the resource is starting. In that case: retry.

To run and verify each of these tasks, the relevant endpoint is called and a JSON output can be extracted. Furthermore, the `QueryDB.java` file is ran to further verify and provide a more detailed insight.

Within the azfunc/ directory, a shell script, `exec.sh`, has been provided for simplicity.

**Focused structural view**

```text
root/
├── azfunc/
│   ├── *.py                     # Python files
│   ├── setup.sh                 # Setup script
│   ├── exec.sh                  # Test script
│   └── *.json                   # Configuration files
├── java-db/
```
1. **Pre-test: Setup**

We must execute all tests under the same variables, within the same environment.

```bash
# Ensure you are in the azure function directory
cd ./azfunc/

# Make this file executable
chmod +x ./exec.sh

# Check for required dependencies
./exec.sh check

# Check the current status of the Azure Resources
./exec.sh status
```

A successful example output can be seen below:

```bash
# Output for check
========================================
  Checking Data Transfer Dependencies
========================================
✅  curl is installed.
    curl 8.5.0 (x86_64-pc-linux-gnu) libcurl/8.5.0 OpenSSL/3.0.13 zlib/1.3 brotli/1.1.0 zstd/1.5.5 libidn2/2.3.7 libpsl/0.21.2 (+libidn2/2.3.7) libssh/0.10.6/openssl/zlib nghttp2/1.59.0 librtmp/2.3 OpenLDAP/2.6.7

========================================
  Checking Virtual Environment Status
========================================
✅  Virtual environment is activated.
ℹ️  Use command 'deactivate' to exit the virtual environment.

========================================
  Checking Azure SQL Database Status
========================================
ℹ️  Querying database for verification...

========================================
  Building and Executing QueryDB.java
========================================
ℹ️  Compiling QueryDB.java...
✅  Compilation successful
ℹ️  Executing: QueryDB
Connected to Azure SQL Database

=== DATABASE STATISTICS ===
Total records: 5420
Unique sensors: 20
Date range: 2025-11-18 23:14:36 to 2025-11-19 00:26:10

=== QUERY MENU ===
1. View data grouped by sensor
2. View data grouped by timestamp
3. View data for a specific sensor
4. Exit
Select an option (1-4):


# Output for azure status
========================================
  Checking Azure Functions and Database Status
========================================
ℹ️  Pinging Azure Functions and Database...
{
    "timestamp": "2025-11-19T01:09:11.019220+00:00",
    "sensor_count": 20,
    "sensors": [
        {
            "sensor_id": 1,
            "temperature": 9.3,
            # and so on...
        },
        {
            "sensor_id": 2,
            # and so on...
        }
    ],
    "database_status": "Stored 20 records"
}
✅ Data insertion for trigger successful
{
    "timestamp": "2025-11-19T01:09:14.590881+00:00",
    "data_analyzed": 5440,
    "analytics": [
        [
            1,
            {
                "temperature": {
                    "minimum": 5.1,
                    "maximum": 17.9,
                    "average": 11.57
                },
                "wind_speed": {
                    # and so on...
                # and so on...
                }
            }
        ], # and so on...
    ]
}
✅ Statistics calculation successful
✅ Azure Functions: ONLINE
ℹ️  Querying database for verification...
Connected to Azure SQL Database

=== DATABASE STATISTICS ===
Total records: 5440
# and so on...

=== QUERY MENU ===
1. View data grouped by sensor
# and so on...
```

1. **Task 1: Data Simulation**

We expect a function to generate data and then store it in our database.

We will call the Data Simulation function.

```bash
# Run task 1: Make a GET request to endpoint '/simulate-data', verify success
./exec.sh task1
```

A successful example output can be seen below:

2. **Task 2**

We expect a function to retrieve existing data and then another to calculate its statistics.

We will call the Data Statistics function.

```bash
# Run task 2: Make a GET request to endpoint '/statistics', verify success
./exec.sh task2
```

A successful example output can be seen below:

```bash
Connected to Azure SQL Database

=== DATABASE STATISTICS ===
Total records: 5300
Unique sensors: 20
Date range: 2025-11-18 23:14:36 to 2025-11-19 00:25:10

=== QUERY MENU ===
1. View data grouped by sensor
2. View data grouped by timestamp
3. View data for a specific sensor
4. Exit
Select an option (1-4):
```

3. **Task 3**

For this task, you must uncomment and redeploy the code to Azure, so that the new changes take effect. This was commented out to avoid the function running in the background and wasting money and energy.

This task simply activates the schedule and enables the database change trigger on startup. This means that every *T* seconds.

```bash
# Tests the chron schedule, redeploys, queries database, verifies regular intervals
./exec.sh task3a

# Tests the automatic database trigger and automatic statistics function
./exec.sh task3b
```

A successful example output can be seen below:

```bash
# Deployment output
Getting site publishing info...
[2025-11-18T19:54:13.234Z] Starting the function app deployment...
[2025-11-18T19:54:13.240Z] Creating archive for current directory...
Performing remote build for functions project.
Deleting the old .python_packages directory
Uploading 337.95 KB [#############################################################################]
Deployment in progress, please wait...
Starting deployment pipeline.
[Kudu-SourcePackageUriDownloadStep] Skipping download. Zip package is present at /tmp/zipdeploy/31444265-c815-4ac3-8a6c-ec12e27a0b06.zip
[Kudu-ValidationStep] starting.
[Kudu-ValidationStep] completed.
# other steps...

Checking the app health...Host status endpoint: https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/admin/host/status
. done
Host status: {"id":"7e2c7da6b9d556f8ec5140e450763bd3","state":"Running","version":"4.1044.400.0","versionDetails":"4.1044.400-dev.0.0+ac5f4d4d963db7316fa7516d0b349528452421b4","platformVersion":"","instanceId":"0--3ab66b92-133a-4f28-a926-a9d088e033ac","computerName":"","processUptime":187086,"functionAppContentEditingState":"NotAllowed","extensionBundle":{"id":"Microsoft.Azure.Functions.ExtensionBundle","version":"4.29.0"}}
[2025-11-18T19:56:41.403Z] The deployment was successful!
Functions in func-app-sc222ab:
    ScheduledDataCollection - [timerTrigger]

    SensorDataChangeTrigger - [sqlTrigger]

    SimulateDataFunction - [httpTrigger]
        Invoke url: https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api/simulate-data

    StatisticsFunction - [httpTrigger]
        Invoke url: https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api/statistics

✅  Deployment completed successfully!
ℹ️  Waiting 20s for scheduled data collection to occur...
ℹ️  Verifying scheduled data collection...
ℹ️  Querying database for verification...
Connected to Azure SQL Database

=== DATABASE STATISTICS ===
# and so on...

=== QUERY MENU ===
# and so on...
```


### Project Structure
```text
root/
├── azfunc/
│   ├── function_app.py          # Main Azure Functions
│   ├── sensor_data_function.py  # Data generation module
│   ├── statistics_function.py   # Analytics module
│   ├── setup.sh                 # Setup script
│   ├── exec.sh                  # Test script
│   └── *.json                   # Configuration files
├── java-db-setup/
│   ├── CreateDB.java           # Database initialisation
│   ├── QueryDB.java            # Database queries
│   ├── build.sh                # Setup and Test script
│   └── sqljdbc/                # SQL Server JDBC driver
└── README.md
```


## Project status

This project had a short deadline and development was delayed due to other ongoing courseworks. I would have liked to implement cleaner, more modularised and user-friendly code. If time permits, I will return to this project, however, this will not contribute to the coursework grade. \

In future I would research:
- Caching: Redis cache for frequent statistics
- Circuit Breakers: Prevent cascade failures during high load
- Message Queues: Azure Service Bus for better load leveling
- Database Indexing: Optimise queries with proper indexes


## Reference Material

- [1] Oracle. 2025. *Java JDBC API*. [Online]. [Accessed 18 November 2025]. Available from: [https://docs.oracle.com/javase/8/docs/technotes/guides/jdbc/](https://docs.oracle.com/javase/8/docs/technotes/guides/jdbc/)

- [2] Microsoft Learn. 2025. *Quickstart: Create a single database - Azure SQL Database*. [Online]. [Accessed 18 November 2025]. Available from: [https://learn.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?view=azuresql&tabs=azure-portal](https://learn.microsoft.com/en-us/azure/azure-sql/database/single-database-create-quickstart?view=azuresql&tabs=azure-portal)

- [3] Microsoft Learn. 2025. *Create a function app in the Azure portal*. [Online]. [Accessed 18 November 2025]. Available from: [https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-function-app-portal?tabs=core-tools&pivots=flex-consumption-plan](https://learn.microsoft.com/en-us/azure/azure-functions/functions-create-function-app-portal?tabs=core-tools&pivots=flex-consumption-plan)

- [4] Python Docs. 2025. *ThreadPoolExecutor*. [Online]. [Accessed 18 November 2025]. Available from: [https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor)

- [5] Microsoft Learn. 2025. *Timer trigger for Azure Functions*. [Online]. [Accessed 18 November 2025]. Available from: [https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=python-v2%2Cisolated-process%2Cnodejs-v4&pivots=programming-language-python](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=python-v2%2Cisolated-process%2Cnodejs-v4&pivots=programming-language-python)

- [6] Microsoft Learn. 2025. *Azure SQL trigger for Functions*. [Online]. [Accessed 18 November 2025]. Available from: [https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-azure-sql-trigger?tabs=isolated-process%2Cpython-v2%2Cportal&pivots=programming-language-python](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-azure-sql-trigger?tabs=isolated-process%2Cpython-v2%2Cportal&pivots=programming-language-python)









