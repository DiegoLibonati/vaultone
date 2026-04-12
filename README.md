# Vaultone

## Educational Purpose

This project was created primarily for **educational and learning purposes**.  
While it is well-structured and could technically be used in production, it is **not intended for commercialization**.  
The main goal is to explore and demonstrate best practices, patterns, and technologies in software development.

## Getting Started

1. Clone the repository
2. Go to the repository folder and execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute in Linux/Mac: `source venv/bin/activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.dev.txt`
7. Execute: `pip install -r requirements.test.txt`
8. Use `python app.py` or `python -m src` to execute the program

### Pre-Commit for Development

1. Once you're inside the virtual environment, let's install the hooks specified in the pre-commit. Execute: `pre-commit install`
2. Now every time you try to commit, the pre-commit lint will run. If you want to do it manually, you can run the command: `pre-commit run --all-files`

## Description

**Vaultone** is a lightweight desktop voice recorder built with Python and Tkinter. It lets you capture audio directly from your microphone and save it as a WAV file with a name you choose — no configuration, no accounts, no cloud.

The workflow is intentionally minimal: type a filename, hit **Start Record**, speak, then hit **Stop Record**. The moment you stop, Vaultone writes the file to disk and displays the total recording duration. That's the entire surface area of the app.

Under the hood, recording runs on a dedicated background thread using PyAudio, so the UI stays responsive the whole time. A second timer thread drives the live elapsed-time counter shown in the interface while you record. Both threads are cleanly joined when you stop, ensuring no audio data is lost and no resources are leaked.

The app follows an MVC-like structure: `AudioModel` owns the PyAudio stream and all threading logic; `InterfaceApp` wires user actions to model calls; `MainView` and `RecordControls` handle everything the user sees and interacts with. Configuration is environment-aware — switching between `development`, `production`, and `testing` modes via an `ENVIRONMENT` env variable adjusts debug flags and logging behavior without touching code.

The project can be packaged into a fully standalone executable for Windows, Linux, or Mac using PyInstaller, making it distributable without requiring Python to be installed on the target machine.

## Technologies used

1. Python >= 3.11
2. Tkinter

## Libraries used

#### Requirements.txt

```
PyAudio==0.2.12
python-dotenv==1.0.1
```

#### Requirements.dev.txt
```
pre-commit==4.3.0
pip-audit==2.7.3
ruff==0.11.12
```

#### Requirements.test.txt

```
pytest==8.4.2
pytest-env==1.1.5
pytest-cov==4.1.0
pytest-timeout==2.3.1
pytest-xdist==3.5.0
```

#### Requirements.build.txt

```
pyinstaller==6.16.0
```

## Portfolio Link

[`https://www.diegolibonati.com.ar/#/project/vaultone`](https://www.diegolibonati.com.ar/#/project/vaultone)

## Testing

1. Go to the repository folder
2. Execute: `python -m venv venv`
3. Execute in Windows: `venv\Scripts\activate`
4. Execute in Linux/Mac: `source venv/bin/activate`
5. Execute: `pip install -r requirements.txt`
6. Execute: `pip install -r requirements.test.txt`
7. Execute: `pytest --log-cli-level=INFO`

## Build

You can generate a standalone executable (`.exe` on Windows, or binary on Linux/Mac) using **PyInstaller**.

### Windows

1. Go to the repository folder
2. Activate your virtual environment: `venv\Scripts\activate`
3. Install build dependencies: `pip install -r requirements.build.txt`
4. Create the executable: `pyinstaller app.spec`

Alternatively, you can run the helper script: `build.bat`

### Linux / Mac

1. Go to the repository folder
2. Activate your virtual environment: `source venv/bin/activate`
3. Install build dependencies: `pip install -r requirements.build.txt`
4. Create the executable: `pyinstaller app.spec`

Alternatively, you can run the helper script: `./build.sh`

## Security Audit

You can check your dependencies for known vulnerabilities using **pip-audit**.

1. Go to the repository folder
2. Activate your virtual environment
3. Execute: `pip install -r requirements.dev.txt`
4. Execute: `pip-audit -r requirements.txt`

## Env Keys

1. `ENVIRONMENT`: Defines the application environment. Accepts `development`, `production`, or `testing`.

```
ENVIRONMENT=development
```

## Known Issues

None at the moment.