FROM python:3.11

COPY ./ /code/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

WORKDIR /code/

CMD ["python3.11", "-u", "main.py" ]