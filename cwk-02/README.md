
# Internet of Things (IoT) simulation Framework (COMP3811 Coursework 2 - 2025)



## Description

The following README provides a guide to my COMP3811 Coursework 2 solution.
To run...


## Demonstration (Video)

TODO: Insert YT video link


## Installation


### Prerequisites

Admin privileges are required on your machine to run shell scripts and executables.


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


##### Requirements

A file `requirements.txt` has been provided which includes all packages and the *specific version* installed in order to run this project. If errors arise with specific versions, remove the constraint on each line so that each package simply looks like this: `azure-functions`

*Note: The core coursework function tasks only require that **azure-functions** is installed. The rest pertains to performance testing and Java database creation*

TODO: Shell script setup?


## Usage

Ensure both the Azure Database and Function App are running. \\
The Database will appear offline until you create or query the database for the first time.

To run and verify each of these tasks, the relevant endpoint is called and a JSON output can be extracted. Furthermore, the `QueryDB.java` file is ran to further verify and provide a more detailed insight.
TODO: Include via shell script


### Setup
TODO: Scripts

### Executing Tasks

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


## Project status

Tis project had a short deadline and development was delayed due to other ongoing courseworks. I would have liked to implement cleaner, more modularised and user-friendly code. If time permits, I will return to this project, however, this will not contribute to the coursework grade.


## Reference Material

- TODO: Include all MS Azure sites used and code found online.