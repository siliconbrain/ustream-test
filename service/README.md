# The Items Service

## Installation
Python 3 should be already installed on your system.
If you'd like to install into a virtual environment, activate the environment before proceeding.
Run `setup.sh` to install dependencies of the service.

## Running the service
To run the service, you'll need a running Redis instance.
For testing purposes the service can be run using Flask's server but it's recommended to use a Python WSGI capable HTTP server in production.

### Settings
You'll need to setup some environment variables:
```
export ITEMS_SERVICE_REDIS_HOST=127.0.0.1
export ITEMS_SERVICE_REDIS_PORT=6379
export ITEMS_SERVICE_REDIS_DB=0
export ITEMS_SERVICE_URL_PATH=/items
```

### Using the built-in Flask server
**Only for testing purposes.**

```
export ITEMS_SERVICE_HOST=127.0.0.1
export ITEMS_SERVICE_PORT=11111
python main.py
```

### Using Gunicorn
Gunicorn is a Python WSGI HTTP Server for UNIX.
```
pip install gunicorn
# Inside the service's directory, start Gunicorn.
gunicorn -b $ITEMS_SERVICE_HOST:$ITEMS_SERVICE_PORT main:app
```

