# README

## How to

### Setup
Run poetry:
```bash
poetry shell
```

Run the api:
```bash
python ./api.py
```

### Run (CRUD)

```bash
# GET the list of todos
curl http://localhost:5000/todos

# GET a single task from the list
curl http://localhost:5000/todos/todo3

# DELETE a task
curl http://localhost:5000/todos/todo2 -X DELETE -v

# CREATE a task
curl http://localhost:5000/todos -d "task=new task!" -X POST -v

# UPDATE a task
curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v
```