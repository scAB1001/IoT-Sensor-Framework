# README

## How to

https://github.com/MichealNestor01/azure-functions-sensor-network/blob/main/StatisticsFunctionProject/StatisticsFunction/function.json

### Setup Poetry Locally
Run poetry / venv:
```bash
poetry shell
source .venv/bin/activate
```

Run api:
```bash
# python ./api.py

# Start func
func start -p 5000

# Test by curl and pass in query
curl -w "\n" "https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api/http_trigger?code=TDHxylRCiXft87Ak2CIJ__WDydWfJ0VeZL206pUad7epAzFuaFjcMQ%3D%3D?name=Andreas"

curl -s "\n" "https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api/http_trigger?code=TDHxylRCiXft87Ak2CIJ__WDydWfJ0VeZL206pUad7epAzFuaFjcMQ%3D%3D?name=Andreas" | python3 -m json.tool

# Test with POST JSON
curl -X POST "https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api/http_trigger?code=TDHxylRCiXft87Ak2CIJ__WDydWfJ0VeZL206pUad7epAzFuaFjcMQ%3D%3D?name=Andreas" \
  -H "Content-Type: application/json" \
  -d '{"name": "Andreas"}'

```

### Setup on cloud - VM needs flask too!

```bash
poetry install --no-root
poetry self add poetry-plugin-shell
poetry self update
poetry shell
```

You need to setup the environment on the new VM.
```bash
# Terminal 1: SSH to VM
ssh sc222ab@20.90.147.180
# Choose 'yes' and type in password
```

Install dependencies:
```bash
sudo apt update

python3 --version

sudo apt install python3-pip -y; python3 -m pip install --upgrade pip

pip3 --version

pip3 -r reqs.txt
```

### Run

#### Terminal 1: Use VM localhost
```bash
curl http://localhost:5000/todos
```

#### Terminal 2: From personal machine, execute commands to VM ip
```bash
curl http://20.90.147.180:5000/todos
```

#### Tunnelling
Setup a tunnel from machine localhost to VM ip
```bash
# Terminal 1&2- Connect to the VM (Personal machine)
ssh sc222ab@20.90.147.180
python3 ./api.py # Run the python file (VM terminal)

# Terminal 3 - Create the tunnel (Personal machine)
ssh -L 5000:localhost:5000 sc222ab@20.90.147.180
# Choose 'yes' and type in password

# Terminal 4 - Commands run locally will execute remotely (Personal machine)
curl http://localhost:5000/todos
```


#### Execute Commands (CRUD)

```bash
# GET the list of todos
curl http://<HOST-IP>:5000/todos

# GET a single task from the list
curl http://<HOST-IP>:5000/todos/todo3

# DELETE a task
curl http://<HOST-IP>:5000/todos/todo2 -X DELETE -v

# CREATE a task
curl http://<HOST-IP>:5000/todos -d "task=new task!" -X POST -v

# UPDATE a task
curl http://<HOST-IP>:5000/todos/todo3 -d "task=something different" -X PUT -v
```

## CWK2

### Task 1
- Create a `simulate_data_function` function
- This function should store the sensor data in an Azure Database made with JDBC in java, not python (it doesn't matter because this simply creates the db on azure which is sql and can be extracted by a python script.
- - SensorData model: `sensor_id`, `temperature`, `wind_speed`, `relative_humidity`, `co2_level`

### Task 2
- Create a `statistics_function` function
- This function reads the previous task's database and generates statistics
- Calculate: `minimum`, `maximum` and `average`, do not store these calculations in the database

### Task 3
- (a) Make the `simulate_data_function` function run every `T` seconds
- (b) Once in the database, a Database Change Tracking Trigger (new) should run
- (c) This trigger should run the Statistics function.

## Submit
Only submit java files from jdbc (don't give config.properties)

#### Get AZ info
```bash
# List all function apps in your subscription
az functionapp list --output table

# List all storage accounts
az storage account list --output table
```

**Results**
- *function app name*:  func-app-sc222ab
- *subscription type*:  UoL-Teaching-SOC-MCC
- *resource group*:     uol_feps_soc_comp_3211_sc222ab
- *storage account*:    uolfepssoccomp3211sb64c

#### Deploy
```bash
# Deploy (every time the function app is modified)
func azure functionapp publish func-app-sc222ab --python

# Test
curl "https://func-app-sc222ab.azurewebsites.net/api/simulate-data/5"

Functions in func-app-sc222ab:
  SimulateDataFunction - [httpTrigger]
    Invoke url: https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api/simulate-data/{sensor_count?}

  StatisticsFunction - [httpTrigger]
    Invoke url: https://func-app-sc222ab-ahekeeg5b7e3bge9.uksouth-01.azurewebsites.net/api/statistics/{data_limit?}

```