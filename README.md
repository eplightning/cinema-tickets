# Cinema tickets
Simple project made as an assignment for SRDS lecture

## How to develop

Prepare virtualenv and setup:
```
virtualenv env
source env/bin/activate
pip install -e .

export FLASK_APP=cinema_tickets
export FLASK_DEBUG=1
```

Running application:
```
flask run
```

Adding movie:
```
flask add_movie --name=Moviename --cover=pathtocover.jpg --description=desc
```
