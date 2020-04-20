FROM node:10.15.1-alpine
LABEL maintainer="jason.gass@sewan.es"

RUN mkdir -p /var/app
WORKDIR /var/app

COPY ebiblio-front /var/app/

RUN cd /var/app 
RUN npm install
CMD [ "npm", "start"]