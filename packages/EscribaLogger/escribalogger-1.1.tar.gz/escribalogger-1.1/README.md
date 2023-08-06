# Get Started

## install

`python -m pip install EscribaLogger`

## Usage

Just import, add drivers and use:

> You can output your logs using a pre-configured builtin [rich](https://rich.readthedocs.io/en/stable/introduction.html) stdout handler

```python
from EscribaLogger import Log

Log.add_driver('stdout') # important!
Log.set_logger_name('CustomName')

Log.info('My info message')
# > [07/16/23 17:01:06] INFO  CustomName - My info message
```

## Log file driver

```python
# You can add another driver. In this case, we will add the file driver
Log.add_driver('file')


Log.info('Some message', extra={"context_var": "value"})
# > The message will be stored in "logs/2023-07-16.log"
# > [2023-07-16 16:13:55,100] EscribaLogger.INFO - Some message - {"context_var": "value"}
```

> In the default logging system, handle context variables is a exhausting task. EscribaLogger added the "extra_context" log variable to solve this. You add the context info for any custom driver.

### Change default log files storage

```python
# You can change default path to store log files in:
Log.add_driver('file', driver_option={'file_location': 'another/path'})


Log.info('Some message', extra={"context_var": "value"})
# > The message will be stored in "another/path/2023-07-16.log"
# > [2023-07-16 16:13:55,100] EscribaLogger.INFO - Some message - {"context_var": "value"}
```

# Contributing

## Setup env

1. init the pyenv:

   - Windows: `python -m venv env --prompt escriba-logger-pyenv`
   - Linux/Unix: `python3 -m venv env --prompt escriba-logger-pyenv`

1. activate pyenv:

   - Windows (**CMD/PowerShell**): `env/Scripts/activate.bat`
   - Windows (**GitBash/Cygwin**): `source env/Scripts/activate`
   - Linux/Unix: `source env/bin/activate`

1. Install Dependencies:

   - Windows (**CMD/PowerShell**): `python -m pip install -r requirements.dev.txt`
   - Linux/Unix: `python -m pip install -r requirements.dev.txt`

## Tests

We are using [pytest](https://docs.pytest.org/en/7.4.x/) and [coverage.py](https://coverage.readthedocs.io/en/7.2.7/) to maintain this project.
You can run the tests by using:

```console
# Don't forget activate pyenv!!!

[~/EscribaLogger] -> source env/bin/activate

# run the pytests + coverage
(escriba-logger-pyenv) [~/EscribaLogger] -> python -m coverage run -m pytest -l -v
# it can be simplified using "coverage run -m pytest -l -v"


====================================test session starts ====================================
platform win32 -- Python 3.11.4, pytest-7.4.0, pluggy-1.2.0 -- C:\Users\strov\Documents\github\EscribaLogger\env\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\strov\Documents\github\EscribaLogger
configfile: pytest.ini
plugins: anyio-3.7.1, mock-3.11.1
collected 5 items

tests/unit/test_builtin_drivers.py::test_driver_stdout... PASSED                     [ 20%]
tests/unit/test_builtin_drivers.py::test_driver_stdout... PASSED                     [ 40%]
tests/unit/test_builtin_drivers.py::test_driver_file_s... PASSED                     [ 60%]
tests/unit/test_builtin_drivers.py::test_driver_file_s... PASSED                     [ 80%]
tests/unit/test_extra_content.py::test_extra_context_p... PASSED                     [100%]

===================================== 5 passed in 0.21s ===================================

Continue below...
```

the command above will generate the `.coverage` file in root path. Now you can generate the coverage report

```console
(escriba-logger-pyenv) [~/EscribaLogger] -> coverage report -m

OR

(escriba-logger-pyenv) [~/EscribaLogger] -> python -m coverage report -m
```

Or you can create a entire webpage to see the results:

```console
(escriba-logger-pyenv) [~/EscribaLogger] -> coverage html
```
