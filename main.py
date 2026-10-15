
# FastAPI is used to build API endpoints. HTTPException allows us to return HTTP errors such as 404 Not Found.
from fastapi import FastAPI, HTTPException

# BaseModel defines and validates incoming request data.
from pydantic import BaseModel

# Import the reusable SQLite connection function from database.py.
from database import get_connection


# Create the FastAPI application and configure its API documentation.
app = FastAPI(
    title="Deployment Tracker API",
    description="REST API for managing application deployment records.",
    version="1.0.0"
)


# GET endpoint: Return a simple welcome message.
@app.get("/hello")
def say_hello():
    return {"message": "My API demo"}


# GET endpoint: Retrieve all deployments from SQLite.
@app.get("/deployments")
def get_deployments():

    # Open a connection to the SQLite database.
    connection = get_connection()

    try:
        # Retrieve all deployment records, sorted by their ID.
        rows = connection.execute(
            "SELECT * FROM deployments ORDER BY id"
        ).fetchall()

        # Convert SQLite rows into dictionaries for the JSON response.
        return [dict(row) for row in rows]

    finally:
        # Close the connection even if an error occurs.
        connection.close()


# GET endpoint: Retrieve a specific deployment using its ID. Example: GET /deployments/1
@app.get("/deployments/{deployment_id}")
def get_deployment(deployment_id: int):

    # Open a connection to the SQLite database.
    connection = get_connection()

    try:
        # Search for the deployment with the requested ID. The ? placeholder keeps input values separate from SQL.
        row = connection.execute(
            "SELECT * FROM deployments WHERE id = ?",
            (deployment_id,)
        ).fetchone()

        # Return HTTP 404 if the requested deployment does not exist.
        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Deployment not found"
            )

        # Return the matching deployment as JSON.
        return dict(row)

    finally:
        # Close the connection even if an error occurs.
        connection.close()


# Define the data required to create or update a deployment. Pydantic validates that all required fields contain strings.
class DeploymentCreate(BaseModel):
    application: str   # Name of the application
    version: str       # Application version
    environment: str   # Example: testing or production
    status: str        # Example: success or failed


# POST endpoint: Create a new deployment in SQLite. Example: POST /deployments
@app.post("/deployments", status_code=201)
def create_deployment(deployment: DeploymentCreate):

    # Open a connection to the SQLite database.
    connection = get_connection()

    try:
        # Insert a new deployment record. Parameterized queries keep input values separate from SQL. SQLite automatically generates a unique deployment ID.
        cursor = connection.execute(
            """
            INSERT INTO deployments
            (application, version, environment, status)
            VALUES (?, ?, ?, ?)
            """,
            (
                deployment.application,
                deployment.version,
                deployment.environment,
                deployment.status
            )
        )

        # Commit the transaction so the record survives server restarts.
        connection.commit()

        # Retrieve the primary key generated for the inserted record.
        new_id = cursor.lastrowid

        # Convert the validated Pydantic object into a dictionary.
        new_deployment = deployment.model_dump()

        # Include the database-generated ID in the response.
        new_deployment["id"] = new_id

        # Return the created deployment with HTTP 201 Created.
        return new_deployment

    finally:
        # Close the connection even if an error occurs.
        connection.close()


# DELETE endpoint: Remove an existing deployment from SQLite. Example: DELETE /deployments/3
@app.delete("/deployments/{deployment_id}")
def delete_deployment(deployment_id: int):

    # Open a connection to the SQLite database.
    connection = get_connection()

    try:
        # Delete the deployment matching the requested ID. WHERE ensures that other deployment records are not deleted.
        cursor = connection.execute(
            "DELETE FROM deployments WHERE id = ?",
            (deployment_id,)
        )

        # Use rowcount to check whether a matching record was deleted. Return HTTP 404 if no deployment matched the requested ID.
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Deployment not found"
            )

        # Commit the transaction to persist the deletion.
        connection.commit()

        # Return a confirmation with HTTP 200 OK.
        return {
            "message": "Deployment deleted successfully",
            "deleted_id": deployment_id
        }

    finally:
        # Close the connection even if an error occurs.
        connection.close()


# PUT endpoint: Update an existing deployment in SQLite. Example: PUT /deployments/1
@app.put("/deployments/{deployment_id}")
def update_deployment(
    deployment_id: int,
    updated_data: DeploymentCreate
):

    # Open a connection to the SQLite database.
    connection = get_connection()

    try:
        # Update the deployment with the provided information. SET specifies which columns receive new values. WHERE ensures only the matching deployment is updated. Parameterized queries keep input values separate from SQL.
        cursor = connection.execute(
            """
            UPDATE deployments
            SET application = ?,
                version = ?,
                environment = ?,
                status = ?
            WHERE id = ?
            """,
            (
                updated_data.application,
                updated_data.version,
                updated_data.environment,
                updated_data.status,
                deployment_id
            )
        )

        # Check whether a deployment matched the requested ID. Return HTTP 404 if no matching deployment was found.
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Deployment not found"
            )

        # Commit the transaction to persist the updated information.
        connection.commit()

        # Retrieve the updated deployment from SQLite.
        row = connection.execute(
            "SELECT * FROM deployments WHERE id = ?",
            (deployment_id,)
        ).fetchone()

        # Return the updated record with HTTP 200 OK.
        return dict(row)

    finally:
        # Close the connection even if an error occurs.
        connection.close()
