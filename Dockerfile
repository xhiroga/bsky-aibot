FROM python:3.11.0-slim-bullseye AS builder

WORKDIR /app

COPY ./requirements.lock /app
COPY ./pyproject.toml /app
COPY ./src/ /app/src

RUN python -m pip install --no-cache-dir --upgrade pip

RUN sed '/-e/d' requirements.lock > requirements.txt
RUN sed -i 's/requires = \["hatchling"\]/requires = \["setuptools", "setuptools-scm"\]/; s/build-backend = "hatchling.build"/build-backend = "setuptools.build_meta"/' pyproject.toml
RUN sed -i '/\[tool\.hatch\.metadata\]/d; /allow-direct-references = true/d' pyproject.toml

RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt

RUN pip install .

CMD ["python3", "./src/aibot_bsky/app.py"]
