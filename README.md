# Deployment Tracker API

I built this project using Python, FastAPI, and SQLite to understand how REST APIs work and how a backend application communicates with a database.

The application keeps track of deployment information such as the application name, version, environment, and deployment status. It supports basic CRUD operations (Create, Read, Update, and Delete) through REST API endpoints.

## Technologies Used

- **Python** – Backend development
- **FastAPI** – Building REST API endpoints
- **SQLite** – Storing deployment records
- **Pydantic** – Validating incoming request data
- **Uvicorn** – Running the API server
- **Swagger UI** – Testing API requests and responses

## Features

- Create new deployment records.
- Retrieve all deployments or find a specific deployment using its ID.
- Update existing deployment information.
- Delete deployment records.
- Store deployment information in SQLite so records remain available after restarting the application.
- Validate incoming request data and return appropriate HTTP status codes.

## Project Structure

```text
fastapi-deployment-tracker/
├── main.py
├── database.py
├── requirements.txt
├── .gitignore
└── README.md
```

`main.py` contains the API endpoints and application logic. `database.py` handles database initialization and SQLite connections.

## How to Run

**1. Create a Python virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**2. Install the required packages**

```bash
python -m pip install -r requirements.txt
```

**3. Initialize the SQLite database**

```bash
python database.py
```

This creates the database file and the table used to store deployment records.

**4. Start the FastAPI application**

```bash
fastapi dev main.py
```

The application runs locally at:

http://127.0.0.1:8000

The API documentation can be accessed at:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/hello` | Returns a simple demo message |
| GET | `/deployments` | Retrieves all deployment records |
| GET | `/deployments/{deployment_id}` | Retrieves a deployment by ID |
| POST | `/deployments` | Creates a new deployment record |
| PUT | `/deployments/{deployment_id}` | Updates an existing deployment |
| DELETE | `/deployments/{deployment_id}` | Deletes a deployment record |

## Example

To create a deployment, send a POST request to `/deployments` with the following JSON:

```json
{
  "application": "vehicle-api",
  "version": "1.0.0",
  "environment": "testing",
  "status": "success"
}
```

The API saves the information in SQLite and automatically generates an ID for the new record.

An example response with HTTP status **201 Created**:

```json
{
  "application": "vehicle-api",
  "version": "1.0.0",
  "environment": "testing",
  "status": "success",
  "id": 1
}
```

The created deployment can then be retrieved using `GET /deployments/1`.

If the requested deployment does not exist, the API returns **404 Not Found**.

## Database

I used SQLite to store deployment records locally instead of keeping them in a Python list. This allows the data to remain available even after the FastAPI server restarts.

The API uses parameterized SQL queries to keep input values separate from SQL statements.

The database file is excluded from Git and can be created locally using `python database.py`.

## Project Scope

This project focuses on REST API development, database integration, and basic error handling. 