FROM docker:23.0.1-dind

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY ./ /code/
WORKDIR /code/

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

CMD ["python3", "-u", "main.py" ]

