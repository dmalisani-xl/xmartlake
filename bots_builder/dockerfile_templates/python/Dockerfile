FROM python:3.11-slim

COPY ./ /code/

WORKDIR /code/
RUN pip install --upgrade -r requirements.txt
RUN pip list > installed.txt

CMD ["python3.11", "-u", "main.py" ]