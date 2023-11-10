FROM python:3.11
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt
COPY ./ /code/
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0"]