FROM python:3.10.12-alpine3.18

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

WORKDIR /code/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
