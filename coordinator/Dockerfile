FROM python:3.11

COPY ./app /code/app
RUN pip install --no-cache-dir --upgrade -r /code/app/requirements.txt


WORKDIR /code/
RUN ls -l
RUN pwd

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7000"]
