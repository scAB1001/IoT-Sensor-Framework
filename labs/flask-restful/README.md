# README

## How to

### Setup Locally
Run poetry:
```bash
poetry shell
```

Run api:
```bash
python ./api.py
```

### Setup on cloud - VM needs flask too!

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


### Execute Commands (CRUD)

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
