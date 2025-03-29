# Airflow ETL Pipeline with Postgres and API Integration

This project involves creating an ETL (Extract, Transform, Load) pipeline using Apache Airflow. The pipeline extracts data from an external API (in this case, NASA's Astronomy Picture of the Day (APOD) API), transforms the data, and loads it into a PostgreSQL Database. The entire workflow is orchestrated by Airflow, a platform that allows scheduling, monitoring, and managing workflows.

The project leverages Docker to run airflow and postgres as services, ensuring an isolated and reproducible environment. We also utilize Airflow hooks and operators to handle the ETL process efficiently.

## Key components of the Project:
### Airflow for Orchestration

Airflow is used to define, schedule, and monitor the ETL pipeline. It manages task dependencies, ensuring the process runs sequentially and reliably. The Airflow DAG (Directed Acyclic Graph) defines the workflow, which includes tasks like data extraction, transformation, and loading.

### Postgres Database:

A PostgreSQL databases is used to store the extracted and transformed data. Postgres is hosted in a docker container, making it easy to manage and ensuring data persistence through Docker volumes. We interact with Postgres using Airflow's PostgresHook and PostgresOperator.

### NASA API:

The external API used in this project is NASA's APOD API, which provides data about the astronomy picture of the day. This includes metadata such as the title, explanation, and the URL of the image. We use Airflow's SimpleHttpOperator to extract data from the API.

### Objectives
#### Extract Data:

The pipeline extracts astronomy-related data from the NASA's APOD API on a scheduled basis (daily, in this case).

#### Transform Data:

Transformations such as filtering or processing the API response are performed to ensure that the data is in a suitable format before being inserted into the database.

#### Load Data:

The transformed data is loaded into the PostgreSQL database. The data can be used for further analysis, reporting, or visualization.

Architecture and workflow:

The ETL pipeline is orchestrated in Airflow using a DAG (Directed Acyclic Graph). The pipeline consists of the following stages:

1. **Extract**: The **SimpleHttpOperator** is used to make HTTP GET requests to NASA's APOD API. The response is in JSON format, containing fields like the title of the picture, the explanation, and the URL to the image.
2. **Transform**: The extracted JSON data is processed in the transform task using Airflow's Taskflow API (with the **@task** decorator). This stage involves extracting relevant fields like title, explanation, url, and date and ensuring they are in the correct format for the database.
3. **Load**: The transformed data is loaded into a Postgres table using **PostgresHook**. If the target table doesn't exist, it is created automatically as part of the DAG create table task.