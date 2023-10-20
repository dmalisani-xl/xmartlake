FROM node:20-alpine3.17

COPY ./ /code/

WORKDIR /code/
RUN npm install

EXPOSE 50000

CMD [ "node", "main.js" ]
