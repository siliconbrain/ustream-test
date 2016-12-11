# The Items Service

## Installation

### Prerequisites
Python 3.4+ should be already installed on your system, along with `pip`.

**Note:** If you'd like to install into a virtual environment, activate the environment before proceeding.

Install dependencies of the service with `pip`:
```bash
pip install -r requirements.txt
```

## Deployment

### Prerequisites
To run the service, you'll need a running Redis instance.

First, you'll need to set up some environment variables describing how to connect to your Redis database:
```bash
# provide your own values!
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB=0
```

### Using the built-in Flask server
You can run the service via `main.py`.
```bash
python main.py --port 11111 --path /items
```

For more options, see `python main.py --help`.


### Using WSGI
In your WSGI configuration you should reference `application` inside the `wsgi` module.
Also, the URL path has to be set via the environment variable `URL_PATH`:
```bash
export URL_PATH=/items  # customize this!
```

#### Example: Gunicorn
Gunicorn is a Python WSGI HTTP Server for UNIX.

1. Install Gunicorn
   
   ```bash
   pip install gunicorn
   ```
2. Run Gunicorn
   
   ```bash
   gunicorn -w 4 -b localhost:11111 wsgi:application
   ```

## Testing
You can run tests with:
```bash
python tests.py
```
