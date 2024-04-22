# Usage

1. Clone the Git repository:

```shell
  git clone https://github.com/starzkeeper/TestProject.git

```
2. Create Virtual Environment
```shell
  cd project_directory
  python3 -m venv venv 
  pip3 install -r requirements.txt
```

 make sure you a postgres database configured for connection

3. Run Application
> python manage.py runserver 

## Using Docker and Docker Compose 

Run:
> docker compose up

# API Documentation 

The project provides API documentation using Swagger. To access the API documentation, follow these steps:

Ensure that the project is running by executing the command mentioned in the "Usage" section.

Open a web browser and navigate to the following endpoint:

```bash
/swagger
```
