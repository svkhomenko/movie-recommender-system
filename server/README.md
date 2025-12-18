<head>
    <div align="center">
        <h1 align="center">Movie RS (Server)</h1>
    </div>
</head>

<div align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff" />
  <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white" />
  <img alt="MySQL" src="https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=fff" />
  <img alt="Pandas" src="https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=fff" />
  <img alt="Scikit-learn" src="https://img.shields.io/badge/-scikit--learn-%23F7931E?logo=scikit-learn&logoColor=white" />
</div>

</br>

## Requirements & Dependencies

- Python
- MySQL

## Setup & Run

Prior to setup, create an `.env` file based on the `.env.example` file, and fill in the required vars.
Then proceed:

- Install all the required dependencies, listed above.
- Run `pipenv install` in the `server/` directory.
- Run `pipenv run python -m spacy download en_core_web_sm` to install a language model.
- Run `pipenv run alembic upgrade head`.
- Run `pipenv run python -m test_data.fill_db` to fill the database with the test data set. It will take some time.
- Run `pipenv run python -m recommender.prepare_models.prepare_models` to prepare models for the recommender system. It will take some time.
- Run `pipenv run uvicorn main:app`.

You can now access the API, using the host and port, provided in the `.env` file.
Documentation provided by Swagger UI is available at /docs.
