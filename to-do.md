# GitHub Actions Docker Workflow

## Workflow steps

- [x] Run automatically on pushes, pull requests, or manual dispatch.
- [x] Check out the repository with read-only repository permissions.
- [x] Set up Python 3.14 and install project dependencies.
- [x] Run the unit test suite.
- [x] Build the Docker image with Docker Compose.
- [x] Start the API and Streamlit services and wait for them to be ready.
- [x] Add health checks for both the API and Streamlit services.
- [x] Check the API health endpoint.
- [x] Send a sample request and confirm the API returns a numeric demo index
      with the non-predictive notice.
- [x] Check that the Streamlit page responds over HTTP.
- [x] Print Compose logs on failure and stop/remove services after the run.
- [ ] Push the readiness fix and confirm the GitHub Actions run passes.

Workflow definition: [`.github/workflows/docker-validation.yml`](./.github/workflows/docker-validation.yml)
