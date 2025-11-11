https://github.com/MichealNestor01/azure-functions-sensor-network/blob/main/StatisticsFunctionProject/StatisticsFunction/function.json
# IoT Sensor Framework - COMP3211 Distributed Systems

A serverless IoT framework for environmental data collection and analysis using Azure Functions.

## Prerequisites

- **Azure CLI** installed and logged in
- **Azure Functions Core Tools**
- **Python 3.8+**
- **Java 11+** (for database setup)
- **Azure Subscription** with Function App and SQL Database

## Quick Start

### 1. Local Development Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# Install dependencies
pip install azure-functions

# Test locally
func start
```

### 2. Azure Database Setup (Java with JDBC)
```bash
cd java-db-setup

# Compile and run database setup
javac CreateDB.java QueryDB.java
java CreateDB    # Creates table structure
java QueryDB     # Verifies database connection
```

### 3. Deployment
```bash
# Deploy to Azure
./exec.sh deploy

# Or manually:
func azure functionapp publish func-app-sc222ab --python
```

### 4. Testing the System
```bash
# Make executable
chmod +x exec.sh

# Test individual tasks
./exec.sh task1    # Data simulation
./exec.sh task2    # Statistics
./exec.sh task3    # Automated pipeline
./exec.sh all      # Run all tests
./exec.sh status   # Check system health
```

**API Endpoints**
- `GET /api/simulate-data?sensor_count=20` - Generate sensor data
- `GET /api/statistics?data_limit=100` - Get analytics

**Architecture**
Task 1: HTTP-triggered data simulation → Azure SQL Database
Task 2: HTTP-triggered statistics calculation ← Azure SQL Database
Task 3:
- Timer-triggered automatic data collection (every 10 minutes)
- SQL-triggered automatic statistics on data insertion

### Project Structure
```text
root/
├── azfunc/
│   ├── function_app.py          # Main Azure Functions
│   ├── sensor_data_function.py  # Data generation module
│   ├── statistics_function.py   # Analytics module
│   ├── exec.sh                  # Test script
│   └── *.json                   # Configuration
├── java-db-setup/
│   ├── CreateDB.java           # Database initialization
│   ├── QueryDB.java            # Database queries
│   └── sqljdbc/                # SQL Server JDBC driver
└── README.md
```