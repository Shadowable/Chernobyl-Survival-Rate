# Chernobyl Scenario Lab

This project contains a Flask API and Streamlit interface for an explicitly
fictional interface demonstration. It is **not** a survival predictor: the
displayed demo index is invented, has no scientific or historical validation,
and must not be interpreted as a survival probability, radiation-risk
assessment, medical assessment, or safety guidance.

## What the demo does

The interface collects age, distance from the reactor, an arbitrary physical
ability slider (1 = Low, 10 = High), and an ambient dose-rate entry in
microsieverts per hour (`µSv/h`). The API returns a made-up 0-100 demo index
calculated as the arithmetic average of the four inputs after scaling each to
an arbitrary range. Higher and lower values have no meaningful interpretation.
The previous California Housing artifact, if present in `model/`, is not
loaded by this app and is excluded from Docker builds.

Distance and an ambient dose-rate reading alone cannot determine a person's
exposure or safety. This demonstration does not model radiation, health, or
survival. In a real radiation emergency, follow official emergency-management
and public-health instructions.

## Run locally on Windows

In PowerShell, from the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the Flask API in one terminal:

```powershell
python app.py
```

If an older version of the API is already running, stop it with **Ctrl+C** and
restart it so it loads the new demo endpoint and input format.

In a second terminal, activate the environment and start Streamlit:

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run streamlit_app.py
```

Open `http://localhost:8501`. The API listens at `http://127.0.0.1:5002` by
default because port 5000 may be used by other local applications. Set `PORT`
to change the local API port; update `API_BASE_URL` to match if you do.

## API

`GET /health` returns `{"status": "ok"}`.

`POST /predict` accepts:

```json
{
  "age": 35,
  "distance_km": 10,
  "physical_ability": 5,
  "dose_rate_usv_h": 0
}
```

The response contains a `demo_index` and a notice that it is not a survival
probability. The API validates age (0-120), distance (0-1000 km), physical
ability (integer from 1-10), and dose rate (0-1,000,000 µSv/h). These bounds
are interface constraints, not safety thresholds.

## Run with Docker

Start Docker Desktop, then run in PowerShell from the project directory:

```powershell
docker compose up --build
```

Open the UI at `http://localhost:8501`; the API is available at
`http://localhost:5002`. Compose maps host port 5002 to the API's container
port 5000 and configures the UI to use the internal API URL `http://api:5000`.

Stop with **Ctrl+C**. Optionally remove containers with:

```powershell
docker compose down
```

## Tests

```powershell
python -m unittest discover -s tests -v
```
