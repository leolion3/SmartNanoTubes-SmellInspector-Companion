# SmellInspector Companion Software

This software allows controlling one (or multiple) SmellInspector devices from SmartNanoTubes.

**Note:** The app is currently **WINDOWS-ONLY**. Later versions will address this.

## Driver Setup

The software **must be ran on the PC that the SmellInspector devices are connected to**. To allow the devices
to be connected, the `CP210x_Universal_Windows_Driver` must be installed, which will allow Windows to operate the devices
over their serial interface. The driver can be found under `backend/resources/CP210x_Universal_Windows_Driver.zip` or installed through
the Web-App's GUI.

## Installation

The app is split into two parts:

- A `ReactJS + TailwindCSS` frontend.
- A `Python3 (v12+) WSGI (Flask/Waitress)` backend.

To run the app, launch `Windows PowerShell` and then start the backend first:

```bash
cd backend/
python -m venv venv
./venv/Scripts/activate.ps1
pip install -r requirements.txt --no-cache
python app.py
```

and then (in a second shell) launch the frontend:

```bash
cd frontend/
npm install
npm start
```

**Note:** The application does not yet support a production environment. Later versions will offer simple installation using Docker.
