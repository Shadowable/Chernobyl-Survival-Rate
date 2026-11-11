# Chernobyl Scenario Lab

A small Flask API and Streamlit interface for an interactive, fictional
historical scenario demo.

> **Important:** This project does not predict survival, radiation exposure,
> health outcomes, or safety. Its demo index is invented and has no scientific
> or historical validity. Do not use it to assess an actual radiation
> emergency; follow official emergency-management and public-health guidance.

## What it includes

- A Streamlit form for age, distance from the reactor, physical ability, and
  ambient dose rate.
- A Flask API that validates those inputs and returns a fictional demo index.
- Docker Compose configuration for running the UI and API together.

Physical ability is represented by an arbitrary slider from **1 (Low)** to
**10 (High)**. Dose rate is entered in microsieverts per hour (`µSv/h`). The
input limits are form constraints, not safety thresholds.

## Run locally on Windows

From the project directory, create and install the virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Open two PowerShell terminals in the project directory. Start the API in the
first:

```powershell
.\.venv\Scripts\Activate.ps1
python app.py
```

Start Streamlit in the second:

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run streamlit_app.py
```

Open **http://localhost:8501**. The API listens at **http://127.0.0.1:5002**
by default to avoid conflicts with services using port 5000. To change the
API port, set `PORT` and set Streamlit's `API_BASE_URL` to match.

## Run with Docker

Start Docker Desktop, then from the project directory run:

```powershell
docker compose up --build
```

Open **http://localhost:8501**. The API is exposed at
**http://localhost:5002**. Compose connects the UI to the API internally at
`http://api:5000`.

Stop with **Ctrl+C**. To stop and remove the containers:

```powershell
docker compose down
```

## Automated validation

GitHub Actions runs on pushes, pull requests, and manual dispatch. The workflow
runs the unit tests, builds the Docker image, starts both Compose services,
checks the API health and prediction endpoints, and verifies that the Streamlit
page responds. If a check fails, it prints the Compose logs and tears down the
services. See [`.github/workflows/docker-validation.yml`](.github/workflows/docker-validation.yml).

## API usage

Check the API:

```text
GET http://localhost:5002/health
```

Send a demo request:

```http
POST http://localhost:5002/predict
Content-Type: application/json
```

```json
{
  "age": 35,
  "distance_km": 10,
  "physical_ability": 5,
  "dose_rate_usv_h": 0
}
```

The response contains a `demo_index` and a notice that it is not a survival
probability. The calculation is only an arbitrary example of an API workflow.

## Tests

With the virtual environment activated:

```powershell
python -m unittest discover -s tests -v
```

## Project layout

```text
.
├── app.py                 # Flask API and demo-index calculation
├── streamlit_app.py       # Interactive Streamlit UI
├── compose.yaml           # API and UI services
├── Dockerfile
├── requirements.txt
├── tests/
└── overview.md            # Expanded setup and API notes
```
