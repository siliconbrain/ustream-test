# The Items Service command line client

## Installation

### Prerequisites
Python 3.4+ should be already installed on your system, along with `pip`.

**Note:** If you'd like to install into a virtual environment, activate the environment before proceeding.

Install dependencies of the client with `pip`:
```bash
pip install -r requirements.txt
```


## Usage
You can run the command line client using Python, providing a URL and a command.
E.g.:
```bash
python main.py http://localhost:11111/items -l
```

For a list of commands and options, see `python main.py --help`.


## Testing
You can run tests with:
```bash
python tests.py
```
