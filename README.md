# IS601 Module 12 — User and Calculation Routes + Integration Testing

This project extends my Module 11 FastAPI calculator with user registration/login,
calculation BREAD endpoints, integration tests, PostgreSQL, and Docker Hub CI/CD.

## What the API does

- **POST `/users/register`**: create a user using Pydantic validation and Argon2 password hashing
- **POST `/users/login`**: verify username/password without returning password hashes (does not issue a session or token)
- **GET `/users/{user_id}`**: view public user details
- **GET `/calculations`**: browse calculations
- **GET `/calculations/{id}`**: read one calculation
- **POST `/calculations`**: add a calculation
- **PUT `/calculations/{id}`**: edit and recalculate
- **DELETE `/calculations/{id}`**: delete a calculation

Supported operations are `Add`, `Sub`, `Multiply`, and `Divide`, matching Module 11 schemas.
Division by zero and invalid input receive HTTP 422. Missing records return 404;
duplicate accounts return 409 and incorrect login returns 401.

## Start the application (Windows / Docker Desktop)

1. Create a separate folder for Module 12 and open it in VS Code.
2. Copy `.env.example` to `.env`. **Change both passwords.** Never commit `.env`.
3. Make sure Docker Desktop is running.
4. From the folder containing `docker-compose.yml`, run:

   ```powershell
   docker compose up -d --build
   ```

5. Open http://localhost:8001/docs to exercise the user and calculation endpoints.
   Example POST `/calculations` JSON: `{"a": 10, "b": 5, "type": "Add"}`.
   The SQLAlchemy models create their tables automatically on the first database request.

Compose uses the following **Module 12-only** ports so Module 11 can remain separate:
PostgreSQL 5435, FastAPI 8001, pgAdmin 5051. Database storage is separate from Module 11.

## Run integration tests

The automated tests include user registration, duplicate users, login, hashing,
validation, calculation BREAD, invalid operations, missing records, and original
Module 11 tests. Tests interact with a configured database; new route tests roll
back their test changes.

With the Docker app running:

```powershell
docker compose exec app python -m pytest -v
```

The GitHub Actions workflow starts a **PostgreSQL 16 service** and runs
`python -m pytest -v` on each push and pull request to `main`.

## GitHub Actions and Docker Hub

- Workflow: `.github/workflows/module12-tests.yml`
- Docker Hub repository to create/use: https://hub.docker.com/r/hkasunmu/is601-module12
- In the Module 12 GitHub repository, configure the repository variable
  `DOCKERHUB_USERNAME` and the secret `DOCKERHUB_TOKEN`.
- On a successful push to `main`, the workflow builds, scans, and pushes
  `hkasunmu/is601-module12:latest` and a commit-SHA tag.
- To pull the image after the first successful deploy:

  ```powershell
  docker pull hkasunmu/is601-module12:latest
  ```

**Note:** The Docker Hub URL and the commands above describe the intended
deployment setup. Confirm actual image availability from Docker Hub after CI/CD succeeds.

## Manual OpenAPI / Swagger checks

Go to http://localhost:8001/docs. Expand an endpoint, click **Try it out**,
enter JSON, then **Execute**. Capture screenshots showing:
1. Successful POST `/users/register` and POST `/users/login`.
2. POST `/calculations`, GET `/calculations`, PUT, and DELETE responses.
3. A successful GitHub Actions workflow.
4. The Docker Hub image/repository after the push.

## Submission

Submit the Module 12 **GitHub repository URL**. Include the screenshots,
this README, and a genuine reflection about your development and troubleshooting.
Do not reuse Module 11 screenshots as evidence of Module 12 success.
