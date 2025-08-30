# SmellInspector Companion Software

This software allows controlling one (or multiple) SmellInspector devices from SmartNanoTubes.

## Driver Setup

The software **must be ran on the PC that the SmellInspector devices are connected to**. To allow the devices
to be connected, the CP210x USB-to-UART Bridge driver must be installed, which allows communicating with the SmellInspector
using a serial connection. 

### Windows

The driver can be found under `backend/resources/CP210x_Universal_Windows_Driver.zip`. Newer drivers can be installed from Silicon Labs, see below.

### MacOS / Linux

The driver can be installed from [Silicon Labs](https://www.silabs.com/software-and-tools/usb-to-uart-bridge-vcp-drivers).

## Installation

![Microservices Architecture Diagram](_html/microservice_architecture.svg)

The app is split into three parts:

- A `Python3 (v12+) WSGI (Flask/Waitress)` backend.
- A `ReactJS + TailwindCSS` frontend, bundled with an `NginX Reverse-Proxy`.
- A `Python3 (v12+) WSGI (Flask/Waitress)` Machine-Learning backend.

The frontend and machine-learning backend are bundled as a docker-compose config, while the backend is a standalone python application.

> This is intentional and due to limitations in communication between the docker container and the connected serial devices (the app has a polling-/enumeration-mechanism to find
connected SmellInspector devices which doesnt work when containerized). 

To run the app, create a venv and then start the backend first:

```bash
cd backend/
python -m venv venv

# Windows
./venv/Scripts/activate.ps1
# MacOS / Linux
source ./venv/bin/activate

pip install -r requirements.txt --no-cache
python app.py
```

and then launch the frontend + machine learning containers:

```bash
docker compose up --build -d
```

> The frontend will be hosted on `http://localhost/`. To change the host address (for remote connections), change the variable `defaultIP` in the file `frontend/src/authentication/global-vars.ts` to the respective address.

### Machine-Learning - Note

> The microservice will receive data from running tests and re-train the enabled models. For more information, see the [machine-learning `README.md`](https://github.com/leolion3/SmartNanoTubes-SmellInspector-Companion/blob/main/machine_learning/README.md).


