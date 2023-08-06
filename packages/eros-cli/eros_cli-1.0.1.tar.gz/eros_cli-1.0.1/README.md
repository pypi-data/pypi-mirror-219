# Eros CLI Interface

This is a terminal based interface to interact with eros. Its built ontop eros-core-python.


## Recommended installation


### Step 1: Install the Package with PIP

Install the package using pip. Run the command:

```
pip install git+https://github.com/Florioo/eros-cli-python
```

This method of installation and the function of the installation in the following action:

[![Python test package installation](https://github.com/Florioo/eros-python-logger-app/actions/workflows/test_installation.yml/badge.svg?branch=master)](https://github.com/Florioo/eros-python-logger-app/actions/workflows/test_installation.yml)

### Step 2: Verify Installation

After installation, you can verify if Eros was installed correctly. Run the command:
```
eros --help
```
If the installation was successful, this command should show the help menu


If the above failed, ther might be something wrong with your python path (or with the package installation), try the following as a workaround:
```
python -m eros_cli.entrypoint --help
```

## Installation from source

Follow the steps below to install Eros-View:

### Step 1: Clone the Repository

Clone the repository to your local machine. Use the command below:
```
git clone git@github.com:Florioo/eros-cli-python.git
```

### Step 2: Navigate to the Directory

Navigate to the cloned repository's directory using the command:
```
cd eros-cli-python
```

### Step 3: Install the Package

Install the package using pip. Run the command:

```
pip install .
```

### Step 4: Verify Installation

After installation, you can verify if Eros-View was installed correctly. Run the command:
```
eros --help
```
If the installation was successful, this command should show the help menu of Eros-View.


# Usage
To start an application we need to use the following commands
```
eros [OPTIONS] <transport [OPTIONS]> <application1 [OPTIONS]> <application2 [OPTIONS]...>
```

## EROS arguments
Optional Arguments:
- `--debug`: Is flag set, eros cli will be launced in debug mode

## Transport
Here the transport is configured

### UART

To select UART, use the `uart` option, the following arguments can be provided

```
uart --port [PORT] --baud [BAUD_RATE] --vid [VENDOR_ID]
```
Optional Arguments:
- `[PORT]`: Port for UART communication (default is "auto", this will auto select uart based on vendor id)
- `[BAUD_RATE]`: Baud rate for UART communication (default is 2000000)
- `[VENDOR_ID]`: Vendor ID for automatic serial port detection (default is 4292)

### TCP/UDP

To select TCP or UDP, use the `tcp` or `udp` option, the following arguments can be provided
```
tcp --ip [IP_ADDRESS] --port [PORT]
udp --ip [IP_ADDRESS] --port [PORT]
```


Optional Arguments:
- `[IP_ADDRESS]`: IP address (default is "192.168.0.1")
- `[PORT]`: Port (default is 6767)

## Application

The final argument are the applications, these specify what to do with the output. Multiple applications can also be specified in the command by chaining them.

To get the arguments fot a specifc application, type help after it

For example:
```
eros uart log --help

Usage: eros uart log [OPTIONS]

  Log the data of a specific channel

Options:
  --channel INTEGER  Channel to monitor
  -f, --log_failed   also log failed packets (which could not be decoded)
  --help             Show this message and exit.
```


### log
This is one of the basic applications which provides textual logs

### dump
This will dump all the data received from eros

### cli
This provides a interactive CLI to the device.

Note: the device needs repl-CLI enabled for this to work

### m-cli
This provides a semi-interactive CLI to the device.

This can be used to test the machine cli

Note: the device needs machine-CLI enabled for this to work

### perf
This is an utility to monitor the troughput eros
is a great combination with `zmq`:

For example:
```
eros uart zmq perf
```


### zmq
This exposes eros over zmq, making it accesible for multiple programs