FROM python:3.11-slim

COPY ./ /code/
RUN pip install --upgrade pip
RUN pip install --upgrade -r /code/requirements.txt

WORKDIR /code/

CMD ["python3.11", "-u", "main.py" ]