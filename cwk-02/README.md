
# Internet of Things (IoT) simulation Framework (COMP3811 Coursework 2 - 2025)


## Description

The following README provides a guide to my COMP3811 Coursework 2 solution.
To run...


## Demonstration (Video)

TODO: Insert YT video link


## Installation

### Prerequisites

A machine using a Linux distribution for its operating system and access to Admin privileges are required to run shell scripts and executables.


### Requirements

A file `requirements.txt` has been provided which includes all *version specific* packages needed to run this project. \\
If errors arise with specific versions, remove the constraint on each line so that each package simply looks like this: `azure-functions` -omitting the `==0.0.0.`.

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

*Note: The CreateDB.java template file, QueryDB.java template file and JDBC Driver with the corresponding JAR files were provided as part of the in-course lab materials in a file *sqljdbc_12.8.1.0_enu.zip*




TODO: Shell script setup?


## Usage

Ensure prerequisites are satisfied to begin with the setup. \\

### Setup


#### Azfunc directory

within the azfunc/ directory, a shell script, `setup.sh`, has been provided for simplicity.

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


Enable and Execute this script

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

# You should also see a ((.venv)) preceding your active terminal input line
```


#### Java Database directory

within the java-db/ directory, a shell script, `build.sh`, has been provided for simplicity.

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


Enable and Execute this script

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

Ensure both the Azure Database and Function App are running. \\
The Database will appear offline until you create or query the database for the first time.

To run and verify each of these tasks, the relevant endpoint is called and a JSON output can be extracted. Furthermore, the `QueryDB.java` file is ran to further verify and provide a more detailed insight.
TODO: Include via shell script

**Task 1**
Will call the first Data Simulation function.
```bash
# Call the function endpoint with optional sensor count specified via <?sensor_count=>
curl "https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api/simulate-data?sensor_count=20"

# Example output
TODO: Example JSON output


TODO: Shell script to do this!
# See verbose insights
java QueryDB

# Example output

```

**Task 2**

```bash
# Call the function endpoint
curl "https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api/statistics"

# Example output
TODO: Example JSON output


# See verbose insights
java QueryDB

# Example output

```

**Task 3**

For this task, you must uncomment and redeploy the code to Azure, so that the new changes take effect. This was commented out to avoid the function running when I am not actively using it. \\

This tasks simply activates the schedule and enables the database change trigger on startup. This means that every T seconds (**TODO**: MODIFIABLE).


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
│   ├── CreateDB.java           # Database initialization
│   ├── QueryDB.java            # Database queries
│   ├── build.sh                # Setup and Test script
│   └── sqljdbc/                # SQL Server JDBC driver
└── README.md
```


## Project status

Tis project had a short deadline and development was delayed due to other ongoing courseworks. I would have liked to implement cleaner, more modularised and user-friendly code. If time permits, I will return to this project, however, this will not contribute to the coursework grade.


## Reference Material

- TODO: Include all MS Azure sites used and code found online.